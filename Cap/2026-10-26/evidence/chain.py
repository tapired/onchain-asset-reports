from common import *
import concurrent.futures
CUSD='0xcccc62962d17b8914c62d74ffb843d73b2a3cccc'
STC='0x88887be419578051ff9f4eb6c858a951921d8888'
USDC='0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'
LENDER='0x15622c3dbbc5614e6dfa9446603c1779647f01fc'
DELEG='0xf3e3eae671000612ce3fd15e1019154c1a4d693f'
BLOCK=json.loads((P/'eth-block.json').read_text())['body']['result']['number']
SELECTORS=json.loads((P/'selectors.json').read_text()) if (P/'selectors.json').exists() else {}
def batch(name,items,url=RPC):
 data=[dict(jsonrpc='2.0',id=i,method=m,params=p) for i,(m,p) in enumerate(items)]
 b=fetch(name,url,data)
 if not isinstance(b,list):raise ValueError(b)
 return [next(x for x in b if x['id']==i) for i in range(len(items))]
def ensure(sigs):
 ss=list(set(sigs)-SELECTORS.keys())
 if ss:
  b=batch('selector-'+str(len(SELECTORS)),[('web3_sha3',['0x'+s.encode().hex()]) for s in ss]);SELECTORS.update({s:r['result'][:10] for s,r in zip(ss,b)});save('selectors',SELECTORS)
def encode_arg(x):
 return (x[2:].lower().rjust(64,'0') if isinstance(x,str) and x.startswith('0x') else hex(int(x))[2:].rjust(64,'0'))
def decode(raw,types):
 data=bytes.fromhex(raw[2:]); words=[int.from_bytes(data[i:i+32],'big') for i in range(0,len(data),32)]
 if not data:return None
 def dec(t,v):
  if t.startswith('int') and v>=2**255:return v-2**256
  if t=='address':return '0x'+hex(v)[2:].rjust(40,'0')
  if t=='bool':return bool(v)
  if t=='string':return data[v+32:v+32+int.from_bytes(data[v:v+32],'big')].decode(errors='replace')
  if t.endswith('[]'):
   n=int.from_bytes(data[v:v+32],'big');return [dec(t[:-2],int.from_bytes(data[v+32+i*32:v+64+i*32],'big')) for i in range(n)]
  return v
 return [dec(t,v) for t,v in zip(types,words)]
def calls(name,items,block=BLOCK,url=RPC):
 # entries label,address,signature,args,return types
 ensure([x[2] for x in items]);out=[]
 for start in range(0,len(items),35):
  part=items[start:start+35]
  raw=batch(name+'-raw-'+str(start),[('eth_call',[{'to':a,'data':SELECTORS[s]+''.join(encode_arg(x) for x in args)},block]) for _,a,s,args,_ in part],url)
  for (label,a,s,args,types),r in zip(part,raw):
   try:d=decode(r['result'],types) if 'result' in r else None
   except Exception as e:d={'decode_error':str(e)}
   out.append({'label':label,'address':a,'signature':s,'args':args,'block':block,'raw':r,'decoded':d})
 save(name,{'block':block,'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':out});return out
if __name__=='__main__':
 items=[('cusd supply',CUSD,'totalSupply()',[],['uint256']),('assets',CUSD,'assets()',[],['address[]']),('fractional vaults',CUSD,'fractionalReserveVaults()',[],['address[]']),('stcusd supply',STC,'totalSupply()',[],['uint256']),('stcusd assets',STC,'totalAssets()',[],['uint256']),('stcusd pps',STC,'convertToAssets(uint256)',[10**18],['uint256'])]
 items += [(s,LENDER,s+'()',[],['uint256']) for s in ['grace','expiry','targetHealth','bonusCap','emergencyLiquidationThreshold','reservesCount']]
 results=calls('core-initial',items)
 for r in results:print(r['label'],r['decoded'])
 assets=results[1]['decoded'][0];items=[]
 for a in assets:
  items += [(a+' '+s,CUSD,s+'(address)',[a],['address'] if s=='fractionalReserveVault' else ['uint256']) for s in ['totalSupplies','totalBorrows','availableBalance','loaned','reserve','fractionalReserveVault','claimableInterest']]
  items += [(a+' '+s,a,s+'()',[],[typ]) for s,typ in [('symbol','string'),('decimals','uint8'),('totalSupply','uint256')]]
  items += [(a+' vault cash',a,'balanceOf(address)',[CUSD],['uint256']),(a+' reserve data',LENDER,'reservesData(address)',[a],['uint256','address','address','address','uint8','bool','uint256'])]
 results=calls('reserve-accounting',items)
 for r in results:print(r['label'],r['decoded'])
 holders=json.loads((P/'cap-debt-holders.json').read_text())['body']['items'];items=[]
 for h in holders:
  a=h['address']['hash'];items += [(a+' agent',LENDER,'agent(address)',[a],['uint256']*6),(a+' debt',LENDER,'debt(address,address)',[a,USDC],['uint256'])]
 results=calls('native-agents',items)
 for r in results:print(r['label'],r['decoded'])
