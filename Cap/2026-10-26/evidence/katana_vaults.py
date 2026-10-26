from common import *
for a in ['0x6a31358E58B8692cE5317181ff3379A5766A7ABA','0xA2d38c8A3D810EBcF4C2075821c5eC8F976bb692']:
 q='{vaultV2ByAddress(address:"'+a+'",chainId:747474){address name totalAssets adapters{items{address type assets vault{address name} ... on MorphoMarketV1Adapter{positions{items{market{marketId} state{supplyAssets}}}}}}}}'
 b=gql('katana-vault-'+a,q);print(b)
