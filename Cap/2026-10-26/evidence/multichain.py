from chain import *
CHAINS=[('katana','https://rpc.katana.network',CUSD,STC),('megaeth','https://mainnet.megaeth.com/rpc',CUSD,STC),('tempo','https://rpc.tempo.xyz','0x20c0000000000000000000000520792dcccccccc','0x20c0000000000000000000008ee4fcff88888888')]
for n,u,c,s in CHAINS:
 try:
  b=fetch(n+'-block',u,{'jsonrpc':'2.0','id':1,'method':'eth_getBlockByNumber','params':['latest',False]})['result'];bn=b['number'];print(n,int(bn,16),datetime.datetime.fromtimestamp(int(b['timestamp'],16),datetime.timezone.utc).isoformat(),flush=True)
  items=[]
  for t,a in [('cUSD',c),('stcUSD',s)]:
   for f,typ in [('symbol','string'),('decimals','uint8'),('totalSupply','uint256')]:items.append((t+' '+f,a,f+'()',[],[typ]))
  r=calls(n+'-token-reads',items,bn,u)
  for x in r:print(n,x['label'],x['decoded'],flush=True)
 except Exception as e:print(n,str(e),flush=True)
