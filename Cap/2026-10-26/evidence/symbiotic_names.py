from common import *
import concurrent.futures
vals=json.loads((P/'further-reads.json').read_text())['results'];addresses=[x['decoded'][0] for x in vals if 'underwriting vault' in x['label'] and x['decoded'] and int(x['decoded'][0],16)>0];tree=json.loads((P/'symbiotic-metadata-tree.json').read_text())['body']['tree']
paths=[x['path'] for x in tree if x['path'].endswith('/info.json') and any(a in x['path'].lower() for a in addresses)]
def go(p):
 b=fetch('symbiotic-'+p.split('/')[1],'https://raw.githubusercontent.com/symbioticfi/metadata-mainnet/ab506ae68f7e165d460df21244ec3bbe0646e458/'+p);print(p,b,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:list(ex.map(go,paths))
