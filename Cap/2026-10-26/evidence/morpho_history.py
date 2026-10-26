from common import *
import concurrent.futures
ms=json.loads((P/'morpho-verified-cap-markets.json').read_text())
queries={
 'katana-largest-history':'chainId_in:[747474],userAddress_in:["0x6655459bab7a5e99f2d61279316f6d0a465be784"]',
 'pt-july-largest-history':'chainId_in:[1],userAddress_in:["0xa1d9769c9aa6e76651a9514e6e998767009e930e"]',
 'pt-jan-largest-history':'chainId_in:[1],userAddress_in:["0x4dfeb30021a5bb94afe33a149050a264fabf4c58"]',
 'cap-known-reserve-cap-market-history':'chainId_in:[1],userAddress_in:'+json.dumps(['0xcccc62962d17b8914c62d74ffb843d73b2a3cccc','0x3ed6aa32c930253fc990de58ff882b9186cd0072','0xbaed9839573d349e42dfbf23a8916e5ab9caf2e3','0x8092c20351cf4048b464df2144dc8a4dd49ce71d','0xbeef088055857739c12cd3765f20b7679def0f51','0x8c106eedad96553e64287a5a6839c3cc78afa3d0','0x2b9681015a1fa2225d1fc8ae40538d3d64c58290'])+',marketUniqueKey_in:'+json.dumps([m['marketId'] for m in ms if m['chain']['id']==1])
}
def run(x):
 name,w=x
 q='{marketTransactions(first:1000,where:{'+w+'}){items{txHash timestamp blockNumber logIndex type user{address} market{marketId collateralAsset{symbol address} loanAsset{symbol address}} data{__typename ... on MarketTransactionTransferData{assets shares} ... on MarketTransactionCollateralTransferData{assets}}} pageInfo{count countTotal}}}'
 b=gql(name,q);print(name, b.get('errors') or b['data']['marketTransactions']['pageInfo'],flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(run,queries.items()))
