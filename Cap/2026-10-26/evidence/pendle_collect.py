from common import *
import concurrent.futures
first=json.loads((P/'pendle-all-100.json').read_text())['body'];allm=first['results']
def go(skip):return fetch('pendle-all-'+str(skip),'https://api-v2.pendle.finance/core/v1/1/markets?limit=100&skip='+str(skip))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
 for b in ex.map(go,range(100,first['total'],100)):allm+=b['results']
cap=[x for x in allm if 'cusd' in str(x).lower() and 'cusdo' not in str(x).lower()];save('pendle-cap-filter',cap)
print('Total',len(allm),'Cap',len(cap));print(json.dumps(cap,indent=2))
