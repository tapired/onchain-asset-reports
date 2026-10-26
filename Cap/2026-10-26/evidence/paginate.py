from common import *
from urllib.parse import urlencode
import sys
name=sys.argv[1];url=sys.argv[2];limit=int(sys.argv[3]) if len(sys.argv)>3 else 10
allitems=[];params={};failed=False
for i in range(limit):
 u=url+('&' if '?' in url else '?')+urlencode(params)
 b=fetch(name+'-page-'+str(i),u)
 if not isinstance(b,dict) or 'items' not in b:failed=True;print('ERROR',str(b)[:300],flush=True);break
 allitems+=b['items'];params=b.get('next_page_params');print(name,i,len(b['items']),params,flush=True)
 if not params:break
save(name+'-all',{'items':allitems,'next_page_params':params,'complete':not params and not failed,'failed':failed})
