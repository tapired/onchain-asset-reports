from chain import *
LOOP='0xd362efc75ef1879f37a900823495f402cfdb0986';PAWN='0xe63a2abc24cd9538398d825a4bfe5778d25687df'
items=[('agents',DELEG,'agents()',[],['address[]'])]
for a in ['0x3ed6aa32c930253fc990de58ff882b9186cd0072','0xb1c1c80fdbbde5b40264e1410550f3c864113bf8',PAWN]:
 for s,t in [('name','string'),('asset','address'),('totalAssets','uint256'),('totalIdle','uint256'),('totalDebt','uint256'),('get_default_queue','address[]'),('role_manager','address')]:items.append((a+' '+s,a,s+'()',[],[t]))
 items += [(a+' cusd shares',a,'balanceOf(address)',[CUSD],['uint256']),(a+' usdc cash',USDC,'balanceOf(address)',[a],['uint256'])]
for s,t in [('balanceOfDebt','uint256'),('balanceOfCollateral','uint256'),('getCurrentLTV','uint256'),('getCurrentLeverageRatio','uint256'),('getLiquidateCollateralFactor','uint256'),('PAWN_BROKER','address'),('exchange','address'),('totalAssets','uint256')]:items.append(('looper '+s,LOOP,s+'()',[],[t]))
results=calls('second-reads',items)
for r in results:print(r['label'],r['decoded'],r['raw'].get('error',''))
