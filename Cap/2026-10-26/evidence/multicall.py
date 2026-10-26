"""Read-only Multicall3 aggregate3, ABI-encoded without web3.py."""
from chain import *
MULTICALL='0xca11bde05977b3631167028862be2a173976ca11'
def word(x):return int(x).to_bytes(32,'big')
def aggregate_data(items):
 chunks=[]
 for _,a,s,args,_ in items:
  data=bytes.fromhex(SELECTORS[s][2:]+''.join(encode_arg(x) for x in args))
  chunks.append(bytes.fromhex(a[2:]).rjust(32,b'\0')+word(1)+word(96)+word(len(data))+data.ljust((len(data)+31)//32*32,b'\0'))
 cursor=len(chunks)*32;offsets=[]
 for c in chunks:offsets.append(word(cursor));cursor+=len(c)
 return '0x82ad56cb'+(word(32)+word(len(chunks))+b''.join(offsets)+b''.join(chunks)).hex()
def aggregate_decode(h):
 b=bytes.fromhex(h[2:]);u=lambda pos:int.from_bytes(b[pos:pos+32],'big');base=u(0);n=u(base);start=base+32;out=[]
 for i in range(n):
  pos=start+u(start+32*i);success=bool(u(pos));bp=pos+u(pos+32);ln=u(bp);out.append((success,'0x'+b[bp+32:bp+32+ln].hex()))
 return out

def multi(name,items,block=BLOCK,url=RPC,size=200):
 ensure([x[2] for x in items]);out=[]
 for start in range(0,len(items),size):
  part=items[start:start+size];data=aggregate_data(part)
  for attempt in range(3):
   b=fetch(name+'-raw-'+str(start),url,{'jsonrpc':'2.0','id':1,'method':'eth_call','params':[{'to':MULTICALL,'data':data},block]})
   if 'result' in b:break
   time.sleep(2)
  if 'result' not in b:raise ValueError(b)
  rs=aggregate_decode(b['result'])
  assert len(rs)==len(part)
  for (label,a,s,args,types),(ok,raw) in zip(part,rs):
   try:d=decode(raw,types) if ok else None
   except Exception as err:d={'decode_error':str(err)}
   out.append(dict(label=label,address=a,signature=s,args=args,block=block,success=ok,raw=raw,decoded=d))
 save(name,dict(block=block,observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),results=out));return out
