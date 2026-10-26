from common import *
import concurrent.futures
jobs=[('cap-implementation','0xbDaa34082F1a1a3c32190a672bC9dd1b69791b97'),('stcusd','0x88887bE419578051FF9F4eb6C858A951921D8888'),('cap-delegation','0xF3E3Eae671000612CE3Fd15e1019154C1a4d693F'),('yearn-looper','0xd362efC75Ef1879f37A900823495f402CfdB0986')]
lender=json.loads((P/'cap-lender-code.json').read_text())['body']['implementations'];jobs += [('lender-implementation',lender[0]['address_hash'])]
def go(j):
 try:
  n,a=j;b=fetch(n+'-code','https://eth.blockscout.com/api/v2/smart-contracts/'+a)
  print(n,a,b.get('name'),b.get('implementations'),flush=True)
  if b.get('implementations'):
   i=b['implementations'][0]['address_hash'];b=fetch(n+'-implementation-code','https://eth.blockscout.com/api/v2/smart-contracts/'+i);print(n+' impl',i,b.get('name'),flush=True)
  if b.get('abi'):
   save(n+'-abi',b['abi']);print(n,'views',[(i['name'],[v['type'] for v in i['inputs']],[v['type'] for v in i['outputs']]) for i in b['abi'] if i['type']=='function' and i['stateMutability']=='view'],flush=True)
 except Exception as e:print(j,str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as e:list(e.map(go,jobs))
