from chain import *
import re
RPCMEGA='https://mainnet.megaeth.com/rpc'
BN=json.loads((P/'megaeth-block.json').read_text())['body']['result']['number']
BOOK=json.loads((P/'aave-mega-addressbook.json').read_text())['body']
ADDR={k:v.lower() for k,v in re.findall(r'address internal constant (\w+)\s*=\s*(0x[a-fA-F0-9]{40})',BOOK)}
POOL='0x7e324abc5de01d112afc03a584966ff199741c28'
ORACLE='0x421117d7319e96d831972b3f7e970bbfe29c4f21'
PROVIDER='0x9588b453a4ee24a420830cb3302195ca7aa3b403'
if __name__=='__main__':
 items=[('eMode8 collateral config',POOL,'getEModeCategoryCollateralConfig(uint8)',[8],['uint16','uint16','uint16']),('emode8 collateral',POOL,'getEModeCategoryCollateralBitmap(uint8)',[8],['uint128']),('emode8 borrowable',POOL,'getEModeCategoryBorrowableBitmap(uint8)',[8],['uint128'])]
 for sym in ['stcUSD','USDm','USDT0']:
  a=ADDR[sym+'_UNDERLYING']
  items += [(sym+' '+s,a,s+'()',[],[typ]) for s,typ in [('symbol','string'),('decimals','uint8')]]
  items += [(sym+' '+typ,ADDR[sym+'_'+typ],'totalSupply()',[],['uint256']) for typ in ['A_TOKEN','V_TOKEN']]
  items += [(sym+' cash',a,'balanceOf(address)',[ADDR[sym+'_A_TOKEN']],['uint256']),(sym+' configuration',POOL,'getConfiguration(address)',[a],['uint256']),(sym+' oracle',ORACLE,'getSourceOfAsset(address)',[a],['address']),(sym+' price',ORACLE,'getAssetPrice(address)',[a],['uint256'])]
 for r in calls('aave-mega-core',items,BN,RPCMEGA):print(r['label'],r['decoded'],flush=True)
 b=fetch('aave-mega-stc-transfer-logs',RPCMEGA,{'jsonrpc':'2.0','id':1,'method':'eth_getLogs','params':[{'fromBlock':'0x0','toBlock':BN,'address':ADDR['stcUSD_A_TOKEN'],'topics':['0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef']}]});print('logs',len(b.get('result',[])),b.get('error'),flush=True)
