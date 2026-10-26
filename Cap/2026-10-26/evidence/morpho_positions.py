from common import *
import concurrent.futures
allm=json.loads((P/'morpho-cap-markets.json').read_text())['body']['data']['markets']['items']
pts=[m['pt']['address'].lower() for m in json.loads((P/'pendle-cap-filter.json').read_text())]
valid=pts+['0xcccc62962d17b8914c62d74ffb843d73b2a3cccc','0x88887be419578051ff9f4eb6c858a951921d8888','0x20c0000000000000000000000520792dcccccccc','0x20c0000000000000000000008ee4fcff88888888','0x9d9874e867b877dd0a3f1eafb8bb1bc54eecc682','0xb6168f597cd37a232cb7cb94cd1786be20ead156']
ms=[m for m in allm if m['collateralAsset'] and m['collateralAsset']['address'].lower() in valid];save('morpho-verified-cap-markets',ms)
def go(m):
 key=m['marketId'];chain=m['chain']['id'];q='{marketPositions(first:1000,where:{marketUniqueKey_in:["'+key+'"],chainId_in:['+str(chain)+']}){items{user{address} healthFactor state{timestamp collateral supplyAssets borrowAssets borrowShares supplyShares}} pageInfo{count countTotal}}}'
 b=gql('morpho-positions-'+key,q)
 if 'errors' in b:print(key,b,flush=True);return
 pos=b['data']['marketPositions'];print(chain,key,m['collateralAsset']['symbol'],'count',pos['pageInfo'],'top borrows',sorted(pos['items'],key=lambda x:int(x['state']['borrowAssets'] or 0),reverse=True)[:3],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(go,[m for m in ms if (m['state']['borrowAssetsUsd'] or 0)>100]))
print('Verified Cap markets',len(ms))
