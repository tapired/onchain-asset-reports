from common import *
import concurrent.futures
ms=json.loads((P/'pendle-cap-filter.json').read_text());jobs=[]
for m in ms:
 for t in ['pt','yt']:jobs.append((m[t]['symbol']+'-holders','https://eth.blockscout.com/api/v2/tokens/'+m[t]['address']+'/holders'))
jobs += [('pawn-oracle-code','https://eth.blockscout.com/api/v2/smart-contracts/0x8e3386b2f6084eb1b0988070c3d826995bd175c0'),('euler-katana','https://app.euler.finance/api/public/metadata?chainId=747474'),('euler-mega','https://app.euler.finance/api/public/metadata?chainId=4326'),('native-usdc-0d35','https://eth.blockscout.com/api/v2/addresses/0x0d35d950fdb0741f11c4384dad15a07edb26e21a/token-transfers?type=ERC-20&token=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'),('native-usdc-7f21','https://eth.blockscout.com/api/v2/addresses/0x7f2165014a477f6aba532000d8088ed64dd1eba1/token-transfers?type=ERC-20&token=0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48')]
def go(j):
 try:b=fetch(*j);print(j[0],len(str(b)),flush=True)
 except Exception as e:print(j[0],str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:list(ex.map(go,jobs))
