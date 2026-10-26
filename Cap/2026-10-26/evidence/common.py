import requests,json,pathlib,datetime,time
P=pathlib.Path(__file__).parent
RPC='https://ethereum-rpc.publicnode.com'
def save(name,data):
 (P/(name+'.json')).write_text(json.dumps(data,indent=2));return data
def fetch(name,url,data=None):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 r=requests.post(url,json=data,timeout=45) if data is not None else requests.get(url,timeout=45)
 try:b=r.json()
 except:b=r.text
 save(name,{'url':url,'request':data,'observed_utc':t,'http_status':r.status_code,'body':b});return b
def gql(name,q): return fetch(name,'https://api.morpho.org/graphql',{'query':q})
def rpc(name,method,params):return fetch(name,RPC,{'jsonrpc':'2.0','id':1,'method':method,'params':params})
