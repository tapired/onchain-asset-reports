from common import *
q='''{markets(first:100,where:{search:"cUSD"}){items{marketId chain{id network} lltv listed creationBlockNumber collateralAsset{address symbol decimals} loanAsset{address symbol decimals} oracle{address type} irmAddress state{blockNumber timestamp supplyAssets borrowAssets liquidityAssets collateralAssets price supplyAssetsUsd borrowAssetsUsd utilization borrowApy} supplyingVaults{address name} supplyingVaultV2s{address name}} pageInfo{count countTotal}}}'''
b=gql('morpho-cap-markets',q)
if 'errors' in b:print(b)
else:
 for x in b['data']['markets']['items']:
  s=x['state'];print(x['chain']['id'],x['marketId'],x['collateralAsset'],x['loanAsset']['symbol'],'LLTV',x['lltv'],'SUPPLY',s['supplyAssetsUsd'],'BORROW',s['borrowAssetsUsd'])
