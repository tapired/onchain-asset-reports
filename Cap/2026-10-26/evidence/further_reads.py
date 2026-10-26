from chain import *
MW='0x09a3976d8d63728d20dcdfee1e531c206ba91225';FRV='0x3ed6aa32c930253fc990de58ff882b9186cd0072'
config=json.loads((P/'all-agent-configuration.json').read_text())['results'];active=[r['label'].split()[0] for r in config if r['label'].endswith(' debt') and r['decoded'][0]>0];items=[]
for a in active:items.append((a+' underwriting vault',MW,'vaults(address)',[a],['address']))
for s,t in [('aToken','address'),('lendingPool','address'),('balanceOfAsset','uint256')]:items.append(('aave '+s,'0x7d7f72d393f242da6e22d3b970491c06742984ff',s+'()',[],[t]))
for s in ['rusdy','exchange']:items.append(('ondo '+s,'0x9939009295ead3c67259af3b93c284079ffe931e',s+'()',[],['address']))
items += [('frv actual share value',FRV,'convertToAssets(uint256)',[19904649188422],['uint256']),('frv max withdraw',FRV,'maxWithdraw(address)',[CUSD],['uint256'])]
b=json.loads((P/'euler-eth-metadata.json').read_text())['body'];pts=[m['pt']['address'].lower() for m in json.loads((P/'pendle-cap-filter.json').read_text())];valid=pts+[CUSD,STC]
for a,v in b.items():
 if isinstance(v,dict) and (v.get('asset') or {}).get('address','').lower() in valid:
  for s,t in [('asset','address'),('totalAssets','uint256'),('totalBorrows','uint256'),('cash','uint256')]:items.append(('Euler '+a+' '+s,a,s+'()',[],[t]))
for s,t in [('BASE_VAULT','address'),('QUOTE_VAULT','address'),('BASE_FEED_1','address'),('BASE_FEED_2','address'),('QUOTE_FEED_1','address'),('QUOTE_FEED_2','address'),('price','uint256')]:items.append(('PawnOracle '+s,'0x8e3386b2f6084eb1b0988070c3d826995bd175c0',s+'()',[],[t]))
r=calls('further-reads',items)
for x in r:print(x['label'],x['decoded'])
