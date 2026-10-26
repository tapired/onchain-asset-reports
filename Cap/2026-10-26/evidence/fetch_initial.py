import requests, pathlib, datetime, json, re, concurrent.futures
p=pathlib.Path(__file__).parent
urls={'cap-reserves':'https://cap.app/vault/reserves/cUSD','cap-addresses':'https://docs.cap.app/developers/addresses.md','cap-docs-llms':'https://docs.cap.app/llms.txt','cap-sitemap':'https://docs.cap.app/sitemap.xml','cap-reserves-doc':'https://docs.cap.app/concepts/vault/fractional-reserves.md','pendle-active':'https://api-v2.pendle.finance/core/v1/1/markets/active','morpho-schema':'https://api.morpho.org/graphql?query=%7B__schema%7BqueryType%7Bname%7D%7D%7D','yearn-yvusd':'https://raw.githubusercontent.com/yearn/risk-score/master/reports/report/yearn-yvusd.md'}
def get(k,u):
 try:
  r=requests.get(u,timeout=30); f=p/(k+('.json' if 'json' in r.headers.get('Content-Type','') else '.txt')); f.write_text(r.text); return {'name':k,'url':u,'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':r.status_code,'file':str(f),'bytes':len(r.content)}
 except Exception as e:return {'name':k,'url':u,'error':str(e)}
results=list(concurrent.futures.ThreadPoolExecutor(max_workers=8).map(lambda x:get(*x),urls.items()))
(p/'fetch-initial.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
html=(p/'cap-reserves.txt').read_text();print('\nSCRIPTS',re.findall(r'<script[^>]+src="([^"]+)"',html));print('\nDOCS', (p/'cap-docs-llms.txt').read_text()[:22000])
