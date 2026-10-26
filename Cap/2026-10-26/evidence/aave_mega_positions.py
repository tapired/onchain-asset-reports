from aave_mega import *
from multicall import multi
from concurrent.futures import ThreadPoolExecutor
TRANSFER='0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
def logs(k):
 f=P/('aave-mega-'+k+'-logs.json')
 b=json.loads(f.read_text())['body'] if f.exists() else fetch('aave-mega-'+k+'-logs',RPCMEGA,{'jsonrpc':'2.0','id':1,'method':'eth_getLogs','params':[{'fromBlock':'0x0','toBlock':BN,'address':ADDR[k],'topics':[TRANSFER]}]})
 print(k,len(b.get('result',[])),b.get('error'),flush=True);return k,b
with ThreadPoolExecutor(max_workers=3) as ex:rs=list(ex.map(logs,['USDm_A_TOKEN','USDm_V_TOKEN','USDT0_A_TOKEN']))
stc=json.loads((P/'aave-mega-stc-transfer-logs.json').read_text())['body']
rs.append(('stcUSD_A_TOKEN',stc))
users={k:sorted(set('0x'+t[-40:] for l in b.get('result',[]) for t in l['topics'][1:]) - {'0x'+'0'*40}) for k,b in rs}
save('aave-mega-ever-addresses',users)
items=[]
for k,aa in users.items():
 for a in aa:items.append((k+' holder '+a,ADDR[k],'balanceOf(address)',[a],['uint256']))
for a in users['stcUSD_A_TOKEN']:
 items += [(a+' account',POOL,'getUserAccountData(address)',[a],['uint256']*6),(a+' eMode',POOL,'getUserEMode(address)',[a],['uint256'])]
 for k in ['USDm_V_TOKEN','USDT0_V_TOKEN']:items.append((a+' debt '+k,ADDR[k],'balanceOf(address)',[a],['uint256']))
items += [('emode8 collateral config',POOL,'getEModeCategoryCollateralConfig(uint8)',[8],['uint16','uint16','uint16'])]
for r in multi('aave-mega-positions',items,BN,RPCMEGA):
 if r['decoded'] and any(r['decoded']):print(r['label'],r['decoded'],flush=True)
