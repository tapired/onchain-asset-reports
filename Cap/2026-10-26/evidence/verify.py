"""Verify final report links, saved receipt status and the central transaction claims."""
import datetime,json,re
from pathlib import Path
P=Path(__file__).resolve().parent
R=P.parent

def load(prefix):return json.loads(next(P.glob('decoded-0x'+prefix+'*.json')).read_text())
def ev(d,name,address=None):return [l for l in d['logs'] if l.get('event')==name and (address is None or l['address']==address)]
d=load('8b157242');c=ev(d,'Mint','0xcccc62962d17b8914c62d74ffb843d73b2a3cccc')[0];s=ev(d,'Deposit','0x88887be419578051ff9f4eb6c858a951921d8888')[0];b=ev(d,'Borrowed')[0]
assert c['params']['amountIn']==250000000000 and c['params']['amountOut']==250002332675417191372791
assert s['params']['shares']==233139461481560505648366
assert b['params']['amount']==213000000000 and b['params']['caller']==b['params']['receiver']=='0xd362efc75ef1879f37a900823495f402cfdb0986'
assert c['logIndex']<s['logIndex']<b['logIndex']
d=load('80b6a827');b=ev(d,'Borrow')[0]['params'];assert b['amount']==14700000*10**18 and b['user']==b['onBehalfOf']=='0x64471d103a7f77262529383d53bdd28b260b1ae8'
d=load('c3afbb05');b=ev(d,'Repay','0x15622c3dbbc5614e6dfa9446603c1779647f01fc')[0]['params'];assert b['agent']=='0x3fa0d4ce8c396b03beb3d8411e10b0126a1b913d' and b['details']['repaid']==4500000*10**6
for prefix,a in [('217f20c4','0xa1d9769c9aa6e76651a9514e6e998767009e930e'),('66f3719d','0x4dfeb30021a5bb94afe33a149050a264fabf4c58')]:
 assert all(l['params']['onBehalf']==a for l in ev(load(prefix),'Borrow'))
d=load('ffa215a6');m=[l for l in ev(d,'Mint') if 'receiverPT' in l['params']][0]['params'];assert m['receiverPT']==m['receiverYT']=='0x743d7b30661d65b41960bf6b5d1bb93cf7972a73' and m['amountPYOut']==84508685787192144205899
receipts=list(P.glob('decoded-*.json'))
for dfile in receipts:
 d=json.loads(dfile.read_text());assert d['status']=='0x1';assert not [l for l in d['logs'] if 'error' in l]
 assert [l['logIndex'] for l in d['logs']]==sorted(l['logIndex'] for l in d['logs'])
checks=[]
for path in [R/'cap-cusd-investigation-2026-10-26.md',P/'README.md']:
 text=path.read_text()
 for label,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',text):
  if target.startswith(('https://','http://','#')):continue
  assert (path.parent/target.split('#')[0]).exists(),(path,target)
 hashes=set(re.findall(r'https://[^)\s]+/tx/(0x[0-9a-fA-F]{64})',text))
 for h in hashes:assert json.loads((P/('decoded-'+h+'.json')).read_text())['status']=='0x1'
 checks.append(dict(file=path.name,words=len(text.split()),successful_receipt_citations=len(hashes)))
now=datetime.datetime.now(datetime.timezone.utc)
result=dict(verified_utc=now.isoformat(),status='passed',receipt_count=len(receipts),key_sequences='mint/stake/permanent borrowing; actual Aave onBehalf; native repayment agent; PT borrower and paired-mint receiver',documents=checks,arithmetic_file='calculation-checks.json',limitations='Checks validate these public snapshots and selected sequences, not underlying off-chain solvency or exhaustive fund provenance.')
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
