from common import *
import concurrent.futures
m=json.loads((P/'cap-middleware-code.json').read_text())['body']['implementations'][0]['address_hash']
jobs=[('cap-middleware-impl','https://eth.blockscout.com/api/v2/smart-contracts/'+m),('pawn-logs','https://eth.blockscout.com/api/v2/addresses/0xe63a2abc24cd9538398d825a4bfe5778d25687df/logs'),('looper-transfers','https://eth.blockscout.com/api/v2/addresses/0xd362efc75ef1879f37a900823495f402cfdb0986/token-transfers?type=ERC-20'),('euler-eth-metadata','https://app.euler.finance/api/public/metadata?chainId=1'),('aave-strategy-code','https://eth.blockscout.com/api/v2/smart-contracts/0x7d7f72d393f242da6e22d3b970491c06742984ff'),('ondo-strategy-code','https://eth.blockscout.com/api/v2/smart-contracts/0x9939009295ead3c67259af3b93c284079ffe931e')]
def go(j):
 try:b=fetch(*j);print(j[0],str(b)[:250],flush=True)
 except Exception as e:print(j[0],str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as e:list(e.map(go,jobs))
