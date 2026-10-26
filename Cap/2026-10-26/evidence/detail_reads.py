from chain import *
FRV='0x3ed6aa32c930253fc990de58ff882b9186cd0072';PAWN='0xe63a2abc24cd9538398d825a4bfe5778d25687df'
agents=json.loads((P/'second-reads.json').read_text())['results'][0]['decoded'][0]
items=[]
for a in agents:
 for s,t in [('collateral','address'),('networks','address'),('ltv','uint256'),('liquidationThreshold','uint256')]:items.append((a+' '+s,DELEG,s+'(address)',[a],[t]))
 items += [(a+' debt',LENDER,'debt(address,address)',[a,USDC],['uint256']),(a+' liquidationStart',LENDER,'liquidationStart(address)',[a],['uint256'])]
r=calls('all-agent-configuration',items)
for a in agents:
 z=[x for x in r if x['label'].startswith(a)];d=next(x['decoded'][0] for x in z if x['label'].endswith(' debt'))
 if d:print(a,d/1e6,[(x['label'].split()[-1],x['decoded']) for x in z if not x['label'].endswith(' debt')])
items=[]
for a in ['0x7d7f72d393f242da6e22d3b970491c06742984ff','0x9939009295ead3c67259af3b93c284079ffe931e','0xbaed9839573d349e42dfbf23a8916e5ab9caf2e3','0x8092c20351cf4048b464df2144dc8a4dd49ce71d']:
 items += [(a+' strategy book',FRV,'strategies(address)',[a],['uint256']*4),(a+' name',a,'name()',[],['string']),(a+' totalAssets',a,'totalAssets()',[],['uint256']),(a+' asset',a,'asset()',[],['address'])]
for s,t in [('BORROWER','address'),('COLLATERAL_ASSET','address'),('ORACLE','address'),('LLTV','uint256'),('totalCollateral','uint256'),('rate','uint256'),('open','bool'),('paused','bool'),('CALL_DURATION','uint256'),('callDeadline','uint256'),('calledDebt','uint256')]:items.append(('Pawn '+s,PAWN,s+'()',[],[t]))
items += [('yvUSDC name','0xbe53a109b494e5c9f97b9cd39fe969be68bf6204','name()',[],['string']),('yvUSDC assets','0xbe53a109b494e5c9f97b9cd39fe969be68bf6204','totalAssets()',[],['uint256']),('yvUSDC pawn strategy','0xbe53a109b494e5c9f97b9cd39fe969be68bf6204','strategies(address)',[PAWN],['uint256']*4)]
r=calls('reserve-strategies-and-pawn',items)
for x in r:print(x['label'],x['decoded'])
