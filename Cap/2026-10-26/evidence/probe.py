import requests,json,pathlib,datetime,concurrent.futures
P=pathlib.Path(__file__).parent
jobs=[('cap-apis-doc','https://docs.cap.app/apis-and-sdks.md',None),('cap-risks','https://docs.cap.app/overview/risks.md',None),('cap-vault-doc','https://docs.cap.app/concepts/vault.md',None),('cap-lender-reference','https://docs.cap.app/developers/contracts/lender.md',None),('cap-guarantees','https://docs.cap.app/overview/protocol-overview/shared-security-networks.md',None),('cap-web','https://cap.app/vault/reserves/cUSD?research=1',None),('cap-app','https://app.cap.app',None),('cap-api','https://api.cap.app',None),('morpho-introspection','https://api.morpho.org/graphql',{'query':'{__schema {types {name kind fields {name type {name kind ofType {name kind ofType {name kind}}} args{name type{name kind ofType{name kind}}}} inputFields{name type{name kind ofType{name kind}}}}}}'}),('eth-block','https://ethereum-rpc.publicnode.com',{'jsonrpc':'2.0','id':1,'method':'eth_getBlockByNumber','params':['latest',False]})]
def go(j):
 name,url,data=j
 try:
  r=requests.post(url,json=data,timeout=40) if data else requests.get(url,timeout=40,headers={'User-Agent':'Mozilla/5.0'})
  try: body=r.json()
  except:body=r.text
  out={'url':url,'request':data,'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':r.status_code,'body':body};(P/(name+'.json')).write_text(json.dumps(out,indent=2));print(name,r.status_code,len(r.content),str(body)[:700],flush=True)
 except Exception as e: print(name,str(e),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:list(ex.map(go,jobs))
