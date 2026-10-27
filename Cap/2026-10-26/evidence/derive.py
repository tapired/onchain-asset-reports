"""Rebuild human-readable tables from preserved public snapshots; no network calls."""
import csv, json, datetime
from pathlib import Path
from decimal import Decimal as D
P=Path(__file__).resolve().parent
def read(n): return json.loads((P/(n+'.json')).read_text())
def rows(n): return read(n)['results']
def write(n,rs,lineterminator=None):
    with (P/(n+'.csv')).open('w') as f:
        options={} if lineterminator is None else {'lineterminator':lineterminator}
        w=csv.DictWriter(f,fieldnames=list(rs[0]),**options);w.writeheader();w.writerows(rs)
def val(n,label): return next(r['decoded'][0] for r in rows(n) if r['label']==label)
def amount(v,dec=18):return str(D(v)/D(10)**dec)
cfg={}; agents={}; vaults={}
for r in rows('all-agent-configuration'):
    a,k=r['label'].split(' ',1);cfg.setdefault(a,{})[k]=r['decoded'][0] if r['decoded'] else None
for r in rows('native-agents'):
    a,k=r['label'].split(' ',1);agents.setdefault(a.lower(),{})[k]=r['decoded']
for r in rows('further-reads'):
    if ' underwriting vault' in r['label']:vaults[r['label'].split()[0]]=r['decoded'][0]
metadata={}
for p in P.glob('symbiotic-0x*.json'):
    d=json.loads(p.read_text());metadata[p.stem[10:].lower()]=d['body'].get('name','unidentified')
native=[]
for a,v in cfg.items():
    if not v.get('debt'):continue
    ag=agents[a]['agent'];uv=vaults.get(a,'')
    native.append(dict(agent=a,usdc_debt=amount(v['debt'],6),delegation_usd=amount(ag[0],8),slashable_usd=amount(ag[1],8),health_factor=amount(ag[5],27),ltv=amount(ag[3],27),configured_ltv=amount(v['ltv'],27),liquidation_threshold=amount(v['liquidationThreshold'],27),collateral_token=v['collateral'],underwriter_vault=uv,public_metadata=metadata.get(uv,'unidentified / other middleware'),liquidation_start=v['liquidationStart']))
native.sort(key=lambda x:D(x['usdc_debt']),reverse=True);write('native-loans',native)
total=sum(D(r['usdc_debt']) for r in native)
assert total==D('56094592.219555') and len(native)==18 and len(cfg)==44
markets=read('morpho-verified-cap-markets');out=[];posrows=[]
for m in markets:
    s=m['state'];dec=m['loanAsset']['decimals'];out.append(dict(chain=m['chain']['network'],market_id=m['marketId'],collateral=m['collateralAsset']['symbol'],collateral_token=m['collateralAsset']['address'],loan_token=m['loanAsset']['address'],loan_symbol=m['loanAsset']['symbol'],supplied=amount(s['supplyAssets'],dec),borrowed=amount(s['borrowAssets'],dec),liquidity=amount(s['liquidityAssets'],dec),lltv=amount(m['lltv']),oracle=m['oracle']['address'],block=s['blockNumber'],source_utc=datetime.datetime.fromtimestamp(s['timestamp'],datetime.timezone.utc).isoformat()))
    p=P/('morpho-positions-'+m['marketId']+'.json')
    if not p.exists():continue
    d=json.loads(p.read_text())['body']['data']['marketPositions'];assert d['pageInfo']['count']==d['pageInfo']['countTotal']
    ps=d['items'];assert abs(sum(int(p['state']['borrowAssets'] or 0) for p in ps)-int(s['borrowAssets']))<=len(ps)
    assert abs(sum(int(p['state']['supplyAssets'] or 0) for p in ps)-int(s['supplyAssets']))<=len(ps)
    for p in ps:
        x=p['state'];posrows.append(dict(chain=m['chain']['network'],market_id=m['marketId'],wallet=p['user']['address'],collateral=amount(x['collateral'],m['collateralAsset']['decimals']),borrowed=amount(x['borrowAssets'],dec),supplied=amount(x['supplyAssets'],dec),health_factor=p['healthFactor'],borrow_share_pct=str(D(x['borrowAssets'])/D(s['borrowAssets'])*100),supply_share_pct=str(D(x['supplyAssets'])/D(s['supplyAssets'])*100),position_timestamp=x['timestamp']))
write('morpho-markets',out);write('morpho-positions',posrows)
core={r['label']:r['decoded'][0] for r in rows('aave-mega-core') if r['decoded'] and r['label']!='eMode8'}
ap=rows('aave-mega-positions');aout=[]
for r in ap:
    if ' holder ' not in r['label']:continue
    assert r['success'] and r['decoded'] is not None
    token,_,wallet=r['label'].split();v=r['decoded'][0]
    if v:aout.append(dict(token=token,wallet=wallet,balance=amount(v,6 if token.startswith('USDT0') else 18)))
write('aave-mega-positions',aout)
for k in ['USDm_A_TOKEN','USDm_V_TOKEN','stcUSD_A_TOKEN']:
    sm=sum(D(r['balance']) for r in aout if r['token']==k)
    target=D(core[k.replace('_',' ',1)])/D(10)**18
    assert abs(sm-target)<D('0.00000000001'),(k,sm,target)
stcdebt=sum(D(r['decoded'][0])/D(10)**18 for r in ap if r['label'].endswith(' debt USDm_V_TOKEN'))
holder=[]
for r in rows('holders-and-oracle-feeds'):
    if r['signature']=='balanceOf(address)':holder.append(dict(token='stcUSD',token_address=r['address'],holder=r['args'][0],balance=amount(r['decoded'][0]),block=r['block']))
for r in rows('pendle-holders-fixed-block'):
    if r['signature']=='balanceOf(address)':holder.append(dict(token=r['label'].split()[0],token_address=r['address'],holder=r['args'][0],balance=amount(r['decoded'][0]),block=r['block']))
write('largest-token-holders',holder)
txs=[]
mega={json.loads(p.read_text())['body']['result']['transactionHash'] for p in P.glob('tx-0x*.json') if json.loads(p.read_text()).get('url')=='https://mainnet.megaeth.com/rpc' and json.loads(p.read_text()).get('body',{}).get('result')}
katana={json.loads(p.read_text())['body']['result']['transactionHash'] for p in P.glob('tx-0x*.json') if 'katana' in json.loads(p.read_text()).get('url','') and json.loads(p.read_text()).get('body',{}).get('result')}
for p in P.glob('decoded-0x*.json'):
    d=json.loads(p.read_text());assert d['status']=='0x1';assert [l['logIndex'] for l in d['logs']]==sorted(l['logIndex'] for l in d['logs'])
    chain='MegaETH' if d['hash'] in mega else 'Katana' if d['hash'] in katana else 'Ethereum'
    domain='megaeth.blockscout.com' if chain=='MegaETH' else 'katanascan.com' if chain=='Katana' else 'etherscan.io'
    txs.append(dict(chain=chain,hash=d['hash'],block=d['block'],utc=d['utc'],status=d['status'],sender=d['from'],to=d['to'],explorer='https://'+domain+'/tx/'+d['hash'],evidence=p.name))
txs.sort(key=lambda x:x['utc']);write('verified-transactions',txs,lineterminator='\n')
summary=dict(native_count=len(native),native_total=str(total),native_top1_pct=str(D(native[0]['usdc_debt'])/total*100),native_top3_pct=str(sum(D(r['usdc_debt']) for r in native[:3])/total*100),aave_stc_backed_usdm_debt=str(stcdebt),aave_top_usdm_supplier_pct=str(D('5959189.937666596365153856')/D('6480174.975852717843805137')*100),aave_top_usdm_borrower_pct=str(D('5967570.916531551217216063')/D('5997096.356696706907849542')*100),external_pawn_plus_aave_stc_debt=str(stcdebt+D('6056474.165347')),pawn_parent_exposure_pct=str(D('6038311.770369')/D('18505494.346401')*100),pawn_price_drop_to_lt_pct=str((1-D('0.871488000199616865')/D('0.915'))*100),morpho_markets=len(markets),morpho_small_markets_debt_usd=sum(m['state']['borrowAssetsUsd'] or 0 for m in markets if (m['state']['borrowAssetsUsd'] or 0)<100),verified_receipts=len(txs))
(P/'calculation-checks.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
