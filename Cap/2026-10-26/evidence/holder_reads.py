from chain import *
ms=json.loads((P/'pendle-cap-filter.json').read_text());items=[]
for m in ms:
 for typ in ['pt','yt']:
  t=m[typ];a=t['address'];name=t['symbol'];items.append((name+' totalSupply',a,'totalSupply()',[],['uint256']))
  if typ=='pt':items.append((name+' expiry',a,'expiry()',[],['uint256']))
  b=json.loads((P/(name+'-holders.json')).read_text())['body']['items']
  for h in b[:5]:items.append((name+' '+h['address']['hash'],a,'balanceOf(address)',[h['address']['hash']],['uint256']))
r=calls('pendle-holders-fixed-block',items)
for x in r:print(x['label'],x['decoded'])
