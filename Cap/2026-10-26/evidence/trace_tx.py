from chain import *
import sys,common,re
CACHED='--cached' in sys.argv
if CACHED:sys.argv.remove('--cached')
if '--rpc' in sys.argv:
 i=sys.argv.index('--rpc');common.RPC=sys.argv[i+1];del sys.argv[i:i+2]
TXS=sys.argv[1:] or ['0x8b157242b3484f62532f5beb85f8ff406cc6a76a9b145ff52fca194d392c746d','0xcdb8aa45efd51ddb89f1c46bea2067789df789df9c2d8f4a3d1c4e6a53d204a0','0x1936a4743a900b346259c42dc6f9230a0a217e4a26731aceeb7b6da985588b51','0x1ee289c3f81723f757309fc12198541a5b36c6cb620fbe04ec5d6285da78323b','0xf0ab47631f731c63231314e2b9a5ba83b246f9ddb5bc525d4f94e1b362053ea8']
abis=[];specific_events={}
file_addresses={'cap-implementation-code':CUSD,'stcusd-implementation-code':STC,'lender-implementation-code':LENDER,'pawn-code':'0xe63a2abc24cd9538398d825a4bfe5778d25687df','yearn-looper-code':'0xd362efc75ef1879f37a900823495f402cfdb0986'}
for f in ['cap-implementation-code','stcusd-implementation-code','lender-implementation-code','pawn-code','yearn-looper-code','yearn-looper-implementation-code','pendle-yt-code','pendle-pool-code','morpho-blue-code','aave-pool-events-code']:
 if not (P/(f+'.json')).exists():continue
 start=len(abis)
 b=json.loads((P/(f+'.json')).read_text())['body'];abis+=b.get('abi',[])
 # Solidity library events can be absent from a contract's published ABI.
 # Recover simple event declarations from the same verified source bundle.
 for source in [b]+b.get('additional_sources',[]):
  for name,params in re.findall(r'event\s+(\w+)\s*\(([^;]*?)\)\s*;',source.get('source_code',''),re.S):
   inputs=[]
   for param in params.split(','):
    bits=param.strip().split()
    if len(bits)<2:break
    typ='bytes32' if bits[0]=='Id' else bits[0]
    if not re.fullmatch(r'(address|bool|bytes\d*|u?int\d*)(\[\])?',typ):break
    inputs.append({'name':bits[-1],'type':typ,'indexed':'indexed' in bits})
   else:abis.append({'type':'event','name':name,'inputs':inputs})
 if f in file_addresses:specific_events[file_addresses[f]]={x['name']+'('+','.join(z['type'] for z in x['inputs'])+')':x for x in abis[start:] if x['type']=='event'}
events={x['name']+'('+','.join(z['type'] for z in x['inputs'])+')':x for x in abis if x['type']=='event'}
raw=batch('event-signatures',[('web3_sha3',['0x'+s.encode().hex()]) for s in events]);bytopic={r['result']:events[s] for s,r in zip(events,raw)}
topic_by_signature={s:r['result'] for s,r in zip(events,raw)}
specific_bytopic={a:{topic_by_signature[s]:e for s,e in es.items()} for a,es in specific_events.items()}
def parse(log):
 e=specific_bytopic.get(log['address'].lower(),{}).get(log['topics'][0]) or bytopic.get(log['topics'][0]);out={'logIndex':int(log['logIndex'],16),'address':log['address']}
 # Repay(address,address,(uint256,uint256,uint256,uint256)), from verified BorrowLogic.
 if log['address'].lower()==LENDER and log['topics'][0]=='0x8724b82b02b7703009fffcf7ee566fdb17f774e77af587630fb5b046a8cb8e8d':
  return dict(out,event='Repay',params={'asset':'0x'+log['topics'][1][-40:],'agent':'0x'+log['topics'][2][-40:],'details':dict(zip(['repaid','vaultRepaid','restakerRepaid','interestRepaid'],decode(log['data'],['uint256']*4)))})
 if not e:return dict(out,topics=log['topics'],data=log['data'])
 ins=e['inputs'];indexed=[x for x in ins if x['indexed']];plain=[x for x in ins if not x['indexed']]
 try:
  vals=decode(log['data'],[x['type'] for x in plain]) or []
  params={x['name']:v for x,v in zip(plain,vals)}
  for x,t in zip(indexed,log['topics'][1:]):params[x['name']]=t if x['type'].startswith('bytes') else decode(t,[x['type']])[0]
  return dict(out,event=e['name'],params=params)
 except Exception as err:return dict(out,event=e['name'],error=str(err),topics=log['topics'],data=log['data'])
for h in TXS:
 if CACHED and (P/('tx-'+h+'.json')).exists():
  r=json.loads((P/('tx-'+h+'.json')).read_text())['body']
 else:r={}
 for attempt in range(3):
  if r.get('result'):break
  r=rpc('tx-'+h,'eth_getTransactionReceipt',[h])
  if r.get('result'):break
 if not r.get('result'):raise RuntimeError('Receipt unavailable: '+h)
 t={};b={}
 if CACHED and (P/('tx-block-'+h+'.json')).exists():
  t=json.loads((P/('tx-body-'+h+'.json')).read_text())['body'];b=json.loads((P/('tx-block-'+h+'.json')).read_text())['body']
 if not t.get('result'):t=rpc('tx-body-'+h,'eth_getTransactionByHash',[h])
 for attempt in range(3):
  if b.get('result'):break
  b=rpc('tx-block-'+h,'eth_getBlockByNumber',[r['result']['blockNumber'],False])
  if not b.get('result'):time.sleep(1)
 if not b.get('result'):raise RuntimeError('Block timestamp unavailable: '+h)
 x=r['result']; tx=t.get('result') or x
 out={'hash':h,'status':x['status'],'block':int(x['blockNumber'],16),'utc':datetime.datetime.fromtimestamp(int(b['result']['timestamp'],16),datetime.timezone.utc).isoformat(),'from':tx['from'],'to':tx['to'],'transaction_fields_source':'eth_getTransactionByHash' if t.get('result') else 'eth_getTransactionReceipt','logs':[parse(l) for l in x['logs']]};save('decoded-'+h,out)
 print(h,out['utc'],'status',x['status'],flush=True)
 for l in out['logs']:
  if l.get('event') in ['Transfer','Borrowed','Borrow','Mint','Deposit','Repay','CollateralPosted']:print(l,flush=True)
