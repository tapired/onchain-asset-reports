from aave_mega import *
from concurrent.futures import ThreadPoolExecutor
TRANS='0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
wallets=['0x64471d103a7f77262529383d53bdd28b260b1ae8','0x8a4aa69f694da05c042c2e59bb9a86f198361799']
def run(x):
 n,a,d=x;topics=[TRANS,None,None];topics[d]='0x'+a[2:].rjust(64,'0')
 b=fetch(n,RPCMEGA,{'jsonrpc':'2.0','id':1,'method':'eth_getLogs','params':[{'fromBlock':'0x0','toBlock':BN,'address':ADDR['USDm_UNDERLYING'],'topics':topics}]})
 print(n,len(b.get('result',[])),b.get('error'),flush=True)
 for l in b.get('result',[]):
  val=int(l['data'],16)/1e18
  if val>50000:print(int(l['blockNumber'],16),l['transactionHash'],'from','0x'+l['topics'][1][-40:],'to','0x'+l['topics'][2][-40:],val,flush=True)
with ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(run,[(('mega-borrower' if i==0 else 'mega-supplier')+'-'+('in' if d==2 else 'out'),a,d) for i,a in enumerate(wallets) for d in [1,2]]))
