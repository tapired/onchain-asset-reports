"""Generate the evidence guide from checked snapshots and an explicit interpretation ledger."""
import csv,json,datetime
from pathlib import Path
from decimal import Decimal as D
P=Path(__file__).resolve().parent
read=lambda n:json.loads((P/(n+'.json')).read_text())
csvread=lambda n:list(csv.DictReader((P/(n+'.csv')).open()))
notes={
'cdb8aa45':'yvUSD parent 0x696d02db93291651ed510704c9b286841d506987 supplies 37,000 USDC equity to looper 0xd362efc75ef1879f37a900823495f402cfdb0986, following its own Sky/sUSDS exit.',
'8b157242':'Ordered logs: 213,000 USDC Morpho flash advance; looper 250,000 USDC to exchange 0xa1be7034b2aa8e72d81e17420b6c6c4f0035fdd4; exchange 250,000 USDC to cUSD; 250,002.332675417191372791 cUSD minted; 233,139.461481560505648366 stcUSD minted and posted to Pawn; Pawn Borrowed caller/receiver is looper for 213,000 USDC; flash loan repaid. Net new permanent debt 213,000, not 426,000.',
'1936a474':'Earlier leveraged mint: 250,000 USDC flash advance funds cUSD mint/stake; 233,234.962828 stcUSD (rounded) posted to Pawn; 250,000 permanent Pawn debt repays the flash advance.',
'80b6a827':'MegaETH Pool Borrow: user and onBehalfOf both 0x64471d103a7f77262529383d53bdd28b260b1ae8; 14,700,000 USDm received.',
'4244a35d':'Same borrower burns/bridges 10,000,000 MegaETH USDm to Ethereum. LayerZero message links the destination receipt a2d01324.',
'd203465b':'Same borrower repays 4,700,000 USDm to Aave. The debt-token burn differs slightly because interest accrues; repayment amount is the underlying-token transfer and Repay event.',
'a2d01324':'Ethereum receives the linked bridge message and mints 10,000,000 USDm to 0x6447…1ae8. Ethereum USDm is 0xec2af1c8b110a61fd9c3fa6a554a031ca9943926.',
'985fae36':'0x6447…1ae8 sends 10,000,000 Ethereum USDm to 0xe6d0ca9844f4c079e6e732f396ef3b9f98a2dac8.',
'a376ffeb':'0xe6d0ca9844f4c079e6e732f396ef3b9f98a2dac8 sends 9,999,999.290816 canonical USDC to 0x6447…1ae8. Paired transfers support a conversion relationship; its off-chain terms and counterparty ownership are unknown.',
'53698c67':'0x6447… repays 2,900,000 USDC to Morpho stcUSD market eb17955e…30062e, onBehalf itself, and withdraws 3,200,000 stcUSD. No cUSD mint. Bundler 0x4a6c…0ae0 is not the borrower.',
'1dcdfdc3':'0x6447… subsequently sends 7,099,999.290816 USDC to 0x3b4d794a66304f130a4db8f2551b0070dfcf5ca7; downstream use not established.',
'ef869705':'0x1af263eaf51c6a2dc24d929716d5e63e3602d995 funds Aave supplier Safe 0x8a4aa69f694da05c042c2e59bb9a86f198361799 with 3,000,000 USDC. Ultimate source/owner unknown.',
'dc883ecf':'Safe 0xdc74c3359c6412f6e9e208ed8dce609ece619b5e funds supplier Safe 0x8a4a… with 2,000,000.000770 USDC. Ultimate source/owner unknown.',
'17dbafee':'Supplier Safe pays 5,000,000 USDC to 0x343c18b0f1710b65ce33a7ce720b5d540215d343 and receives 4,999,999.130000 USDm minted on Ethereum. No Cap cUSD mint.',
'50303f8f':'Supplier Safe bridges 4,999,999.130000 USDm from Ethereum to itself on MegaETH; linked destination is 96ef39f0.',
'96ef39f0':'Matched MegaETH delivery mints 4,999,999.130000 USDm to the supplier Safe.',
'36a769cc':'Supplier Safe supplies 5,000,000 USDm to Aave, onBehalf itself. The 0.87 USDm difference from the immediately traced bridge is pre-existing wallet balance, not an invented bridge amount.',
'a8dfb113':'Safe 0x97f478562cfc6e4c88b125bac83f2ad83a203d8e redeems cUSD and receives 4,500,012.467555 USDC. Reserve unwind: Morpho cbBTC/USDC market 64d65c9a…fcc64 → adapter dd0f28…490d → bcc917…4760 → Gauntlet parent 8c106…a3d0 → compounder 8092…e71d → Cap reserve vault → cUSD → Safe.',
'c3afbb05':'That Safe pays 4,500,000 USDC to Lender, forwarded to cUSD. Lender Repay agent is 0x3fa0d4ce8c396b03beb3d8411e10b0126a1b913d (M11-labelled), not the Safe. Repay tuple and debt-token burn validate the recipient of debt relief.',
'8ab7c24a':'M11-labelled native agent borrows 1,250,000 USDC from Cap.',
'1f7a5623':'M11-labelled agent sends 4,499,990 USDC to Safe 0x97f4…d8e. This exceeds that day’s traced 1.25M borrowing and uses other wallet funds too; no contemporaneous remint is established.',
'c84a543a':'M11-labelled agent borrows 9,999,900 USDC. An earlier 100-USDC test borrowing appears in explorer history but is not added without a separately cited receipt.',
'cf61e8fb':'M11-labelled agent transfers 10,000,000.246666 USDC to 0x433d5b175148da32ffe1e1a37a939e1b7e79be4d, officially listed by Pareto as FalconX Credit Vault. A token subscription is visible; the underlying off-chain credit is not independently verified.',
'8982726e':'Flow-labelled agent borrows 3,000,000 USDC. Reserve unwind includes 2,997,681.179759 USDC withdrawn from Morpho market 64d65c9a…fcc64 (cbBTC/USDC) via adapter 2b968…8290 → Steakhouse parent beef088…0f51 → Cap compounder baed…f2e3 → reserve vault → cUSD → agent.',
'7eaa1140':'Flow-labelled agent sends 3,000,000 USDC to 0x938226e8c9a1c3a270d89a273b4ecbaf9d040740; downstream ownership/purpose unknown. Consult decoded receipt for authoritative full recipient.',
'f0ab4763':'0xee7ae85… sends 999,994 USDC to Flow-labelled agent. This is funding, not proof of who controls the sender.',
'1ee289c3':'Flow-labelled agent repays 999,999 USDC through Lender back to cUSD. A prior 5-USDC transfer is visible in history; the repayment is not assumed to be funded solely by the 999,994 receipt.',
'ea645d03':'Katana borrower 0x6655459bab7a5e99f2d61279316f6d0a465be784 posts 18,799.014622 stcUSD and borrows 17,000 vbUSDC; 6,500 repays another market, and 10,500.693456 enters Yearn Degen then a different Morpho market cd2dc… (not the stc collateral market). No Cap mint.',
'efa2d63f':'Same Katana borrower posts 70,834.213506 stcUSD and borrows 65,000 vbUSDC. Transaction also bridges/burns 89,245.770783 vbUSDC using other funds and deposits 10,018.618820 via Clearstar into the different cd2dc… market. No Cap mint; do not attribute all outputs to this one borrowing.',
'217f20c4':'July PT borrower 0xa1d9769c9aa6e76651a9514e6e998767009e930e posts PT-cUSD and borrows 17,269.257650 USDT onBehalf itself. Ordinary collateral use; no fresh Cap mint in this transaction.',
'66f3719d':'January PT borrower 0x4dfeb30021a5bb94afe33a149050a264fabf4c58 posts 2,067.739008953590589798 PT-stcUSD and borrows 1,800 USDC onBehalf itself. Receipt is dated 2025, not 2026.',
'bd5979a8':'PT buyer 0x444cc947a57f8fc6576abd19837b7df14c4c8e89 rolls 34,562.8478206292 matured January PT-cUSD through SY, purchasing 35,285.470554389843990896 July PT-cUSD. No YT received.',
'd5756eb0':'YT buyer 0xbeb69e7ac7f59bdb79b89fc94ed862c6b39f3c00 spends 2,000 USDS routed through USDC/cUSD/SY and receives 83,475.275943015426212443 July YT-cUSD. Equal newly minted PT goes to the pool, not the buyer: economically a YT purchase despite the mint-from-zero event.',
'ffa215a6':'Wallet 0x743d7b30661d65b41960bf6b5d1bb93cf7972a73 deposits 84,508.685787192144205899 cUSD via SY and receives equal PT and YT. Mint receiverPT equals receiverYT: actual paired mint.',
'5010d82c':'CoW settlement: 0x6447… pays 1,000,000 USDC and receives 1,000,686.345026 USDT. 0x8f10b468… appears as a settlement counterparty also seen in Odyssey/Safe history. Shared routing counterparties alone do not establish ownership.',
}
# Check recipient shorthand against actual receipt instead of relying on copied address text.
for prefix in ['7eaa1140','f0ab4763']:
 p=next(P.glob('decoded-0x'+prefix+'*.json'));d=json.loads(p.read_text())
 transfers=[l for l in d['logs'] if l.get('event')=='Transfer' and l['address']=='0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48']
 if prefix=='7eaa1140':notes[prefix]='Flow-labelled agent sends 3,000,000 USDC to '+transfers[0]['params']['to']+'; downstream ownership/purpose unknown.'
 if prefix=='f0ab4763':notes[prefix]=transfers[0]['params']['from']+' sends 999,994 USDC to Flow-labelled agent. Funding is proven; ownership is not.'
text='''# Evidence guide and detailed findings

This appendix supports [the concise report](../cap-cusd-investigation-2026-10-26.md). JSON files preserve requests, public endpoints, retrieval timestamps and responses; decoded files are derived interpretations. The canonical derived arithmetic is in [calculation-checks.json](calculation-checks.json). No keys, wallet secrets, private configurations or chain writes were used.

**Observation times and source dates**

| State | Block | UTC | Europe/Istanbul |
|---|---:|---|---|
| Ethereum reserve, native loans, Pawn, holders | 26,278,245 | 2026-10-26 17:05:59 | 2026-10-26 20:05:59 |
| MegaETH Aave, remote tokens | 30,237,747 | 2026-10-26 17:12:38 | 2026-10-26 20:12:38 |
| Katana token/adapter RPC reads | 46,291,948 | 2026-10-26 17:12:39 | 2026-10-26 20:12:39 |
| Tempo token RPC reads | 46,008,317 | 2026-10-26 17:12:38 | 2026-10-26 20:12:38 |
| Morpho Katana market state | 46,291,545 | 2026-10-26 17:05:56 | 2026-10-26 20:05:56 |
| Morpho July PT-cUSD Ethereum | 26,278,244 | 2026-10-26 17:05:47 | 2026-10-26 20:05:47 |
| Morpho January PT-stcUSD Ethereum | 26,278,240 | 2026-10-26 17:04:59 | 2026-10-26 20:04:59 |

Morpho positions carry timestamp 17:09:59 UTC / 20:09:59 Istanbul; their summed balances match the earlier market states to rounding. They are indexed accounting balances, not a fresh transaction applying interest to every market. Source observation times must not be confused with historical transaction times. The request-date filename does not override these dates.

Cap documentation was fetched October 26 beginning 17:06 UTC; pages do not supply a reliable revision date. [Yearn's own Cap assessment](https://github.com/yearn/risk-score/blob/master/reports/report/cap-stcusd.md) says updated October 13, 2026; its earlier numbers were leads, not substituted for current calls. Symbiotic metadata was pinned to commit `ab506ae68f7e165d460df21244ec3bbe0646e458`. Aave's address book was fetched October 26 and checked against live deployed state. All primary URL/retrieval metadata are indexed in [source-index.csv](source-index.csv).

**Contract/network registry and reserve accounting**

| Network | cUSD | stcUSD | Decimals |
|---|---|---|---:|
| Ethereum (1) | `0xcccc62962d17b8914c62d74ffb843d73b2a3cccc` | `0x88887be419578051ff9f4eb6c858a951921d8888` | 18 |
| MegaETH (4326) | same address, remote contract | same address, remote contract | 18 |
| Katana (747474) | same address, remote contract | same address, remote contract | 18 |
| Tempo (4217) | `0x20c0000000000000000000000520792dcccccccc` | `0x20c0000000000000000000008ee4fcff88888888` | 6 |

Source: [Cap's current addresses](https://docs.cap.app/developers/addresses), verified Ethereum implementations and chain-specific `symbol/decimals/totalSupply` reads. These are not interchangeable contracts merely because an address matches. The remote tokens do not each create a separate reserve book. LayerZero message delivery and its configured verification networks are additional cross-chain dependencies; selected bridge receipts and message configurations are preserved. Unichain has two residual bridged PT representations: `0xb6168f597cd37a232cb7cb94cd1786be20ead156` (January cUSD PT) and `0x9d9874e867b877dd0a3f1eafb8bb1bc54eecc682` (July cUSD PT). Their Ethereum peers return the canonical PT addresses and reciprocal Unichain peers match exactly (`unichain-pt-canonical-mapping.json`); this is stronger than a symbol match. Reads use Unichain block 62,285,997 and the Ethereum observation block.

Ethereum Lender: `0x15622c3dbbc5614e6dfa9446603c1779647f01fc`; Delegation: `0xf3e3eae671000612ce3fd15e1019154c1a4d693f`; USDC debt token: `0xfa8c6d0b95d9191b5a1d51c868da2bdfd6c04ff9`. Canonical USDC is `0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` (6 decimals).

The Cap USDC reserve vault is `0x3ed6aa32c930253fc990de58ff882b9186cd0072`. Its Aave strategy `0x7d7f72d393f242da6e22d3b970491c06742984ff` books 20,754,202.929992 USDC and holds 20,754,561.748779 accrued aUSDC units (`0x98c23e9d8f34fefb1b7bd6a91b7ff122f4e16f5c`). Its Ethereum Core pool is `0x87870bca3f3fd6335c3f4ce8392d69350b4fa4e2`; that pool does not list cUSD/stcUSD at the snapshot. The 171,140,937.683839 USDC pool cash belongs to all suppliers, not just Cap.

OndoHolder `0x9939009295ead3c67259af3b93c284079ffe931e` books 100,232.258645 USDC; it references rUSDY `0xaf37c1167910ebc994e266949387d2c7c326b879` and exchange `0xa42613c243b67bf6194ac327795b926b4b491f15`. A visible token balance is not an independent audit of off-chain backing or redeemability.

Former Cap compounders `0xbaed9839573d349e42dfbf23a8916e5ab9caf2e3` and `0x8092c20351cf4048b464df2144dc8a4dd49ce71d` map to **parent vaults** Steakhouse Prime `0xbeef088055857739c12cd3765f20b7679def0f51` and Gauntlet USDC Prime `0x8c106eedad96553e64287a5a6839c3cc78afa3d0`. Current asset values are zero, although dust shares remain. Market adapters in historical receipts are a further layer; never assign the parent vault's entire assets to Cap. Old wWGTXX reserve vault `0xb1c1c80fdbbde5b40264e1410550f3c864113bf8` has zero assets and is not in current `assets()`.

Accounting caveats: 56,025,760.412345 booked borrowing + 20,854,438.956138 available = 76,880,199.368483 USDC supplied. The invested claim (`loaned`) is 20,854,435.188636; the reserve vault's totalAssets differs by one micro-USDC. Literal cUSD cash 4.000000 plus loaned exceeds available by 0.232498 USDC. The reserve vault also has 0.153213 loose USDC while reported totalIdle is zero. These small differences were not fully reconciled and were not added as new backing. cUSD token units exceed nominal USDC supplied by 391.664779; this is not a market-value solvency test.

Ethereum stcUSD supply is 69,250,490.083695375989298821, accounting assets 75,287,714.143851798007031687 cUSD, exchange rate 1.087179513861344516. Ethereum stc lockbox `0x983aeaaa0d0426839158435c43725ea7f45d4137` holds 6,763,265.741261 stcUSD. Remote stc supplies: MegaETH 6,672,059.455637; Katana 90,917.176288; Tempo 286.109336. Different snapshot times and bridge rounding apply; do not add these to the lockbox or Ethereum supply.

**Native loans and underwriters**

[All 18 nonzero loans](native-loans.csv) include full addresses, current accrued debt, delegated/slashable USD values, health, configuration and underlying collateral token. Delegation value is an oracle-valued security claim, not operator cash. The table labels are public metadata, not verified legal ownership. The $521.38 unhealthy loan maps to a vault whose metadata explicitly describes a Cap test vault; no material agent had health below one. Some agents exceed current borrow-opening LTV limits while remaining below liquidation thresholds; that alone does not establish a breach or default. Five smaller OETH-backed agents use another middleware; this investigation did not independently verify their legal counterparties or off-chain guarantees.

**External market wallets, collateral and oracles**

Pawn `0xe63a2abc24cd9538398d825a4bfe5778d25687df` has one authorized borrower, looper `0xd362efc75ef1879f37a900823495f402cfdb0986`, whose equity parent is yvUSD `0x696d02db93291651ed510704c9b286841d506987`. Pawn share holder USDC-1 yVault `0xbe53a109b494e5c9f97b9cd39fe969be68bf6204` holds 5,970,754.359366 shares. Complete Pawn event history identifies the same deposit/borrow roles. Pawn totalDebt 6,056,474.165347 and last-report totalAssets 6,045,024.433624 differ in accrual/report timing; this difference alone is not bad debt. Annual rate is 4.5%; `open=false`, `paused=false`, seven-day callable debt, no active call. These are operational permissions, not guaranteed liquidity.

Pawn oracle `0x8e3386b2f6084eb1b0988070c3d826995bd175c0` combines Ojo exchange-rate feed `0x797fa8167c35b19a30a5e7973561588bfec0a086`, RedStone cUSD_FUNDAMENTAL `0x9a5a3c3ed0361505cc1d4e824b3854de5724434a`, and USDC/USD `0x8fffffd4afb6115b954bd326cbe7b4ba576818f6`. Price: 1.087070841914488375440683 USDC/stcUSD. Fundamental cUSD observation was 0.99972314 at 2026-10-26 10:56:35 UTC. Oracle branding does not make Pawn a Morpho market.

Aave MegaETH Pool `0x7e324abc5de01d112afc03a584966ff199741c28`; stc aToken `0xb1b4b54780fdf4ffa82c9c1e83bec12c63bc8ebb`; USDm token `0xfafddbb3fc7688494971a79cc65dca3ef82079e7` (18 decimals), aToken `0x5df82810cb4b8f3e0da3c031ccc9208ee9cf9500`, variable debt `0x6b408d6c479c304794abc60a4693a3ad2d3c2d0d`. E-mode 8 gives 88% opening LTV, 90% liquidation threshold, 4% bonus; standard stc LTV is zero. All stc holders' USDm debts sum to 5,967,577.030991413395750882. USDT0 is also borrowable in that category, but current stc holders have zero USDT0 debt. USDm total pool debt includes other collateral and must not all be attributed to Cap.

Aave stc price is 1.08678324 USD, from oracle `0xbbc579ee0a3fd6e9240965c5f57b7e5b3e3809a8`: ratio provider `0x7055a15452b19d193fba6ec2ff6bf7b515cf577d` (description STCAPUSD/CAPUSD Exchange Rate), base aggregator `0x9182acce3c6456955877c0bbe56107bc7239fe07` (Capped USDC/USD). This has no direct cUSD spot-price leg. `isCapped=false` at the snapshot. Largest borrower's collateral value 7,247,182.82258962 USD and debt 5,967,570.91653156 yield health 1.092984839486685201. Its separate 5,595,907.866621 stcUSD on Ethereum is not added to MegaETH pledged collateral.

Aave largest supplier Safe `0x8a4aa69f694da05c042c2e59bb9a86f198361799` is 3-of-5. Its current owners do not overlap Cap's published developer Safe owners; that is limited negative evidence, not an ownership audit. All historical aToken/debt Transfer participants were enumerated, then fixed-block balances read through Multicall3. Positive-holder sums reconcile to totals within a few wei. [All positive balances](aave-mega-positions.csv).

'''
# top Aave balances
text+='| Aave USDm role | Wallet | Units | Share of relevant pool total |\n|---|---|---:|---:|\n'
aps=csvread('aave-mega-positions')
for token,total,role in [('USDm_V_TOKEN',D('5997096.356696706907849542'),'Borrower'),('USDm_A_TOKEN',D('6480174.975852717843805137'),'Supplier')]:
 for r in sorted([r for r in aps if r['token']==token],key=lambda r:D(r['balance']),reverse=True)[:3]:text+=f"| {role} | `{r['wallet']}` | {D(r['balance']):,.6f} | {D(r['balance'])/total*100:.4f}% |\n"
text+='\nMorpho position tables below are complete for each of the three markets above $100 debt. Full market registry, including inactive/zero markets, is [morpho-markets.csv](morpho-markets.csv). Morpho being permissionless/listed does not imply current material activity.\n\n'
markets=read('morpho-verified-cap-markets');positions=csvread('morpho-positions')
for m in markets:
 ps=[r for r in positions if r['market_id']==m['marketId']]
 if not ps:continue
 text+=f"**{m['chain']['network']}: {m['collateralAsset']['symbol']} / {m['loanAsset']['symbol']}**\n\nMarket `{m['marketId']}`; collateral `{m['collateralAsset']['address']}`; oracle `{m['oracle']['address']}`; LLTV {D(m['lltv'])/D(10)**16}%.\n\n| Role | Wallet | Debt or supply | Collateral units (borrowers) | Market share |\n|---|---|---:|---:|---:|\n"
 for k,role,share in [('borrowed','Borrower','borrow_share_pct'),('supplied','Supplier','supply_share_pct')]:
  for r in sorted(ps,key=lambda r:D(r[k]),reverse=True)[:3]:text+=f"| {role} | `{r['wallet']}` | {D(r[k]):,.6f} | {D(r['collateral']):,.6f} | {D(r[share]):.4f}% |\n"
text+='''
Katana market-facing supplier `0xafa6ce7b33dbea40189f195f4642287ae191e1f0` returns parentVault `0x6a31358e58b8692ce5317181ff3379a5766a7aba` (Clearstar Core USDC). Yearn Degen parent `0xa2d38c8a3d810ebcf4c2075821c5ec8f976bb692` is listed by the API but its current allocation to this market is zero. Katana oracle feeds were separately read in `katana-adapter-oracle.json`; no assumption that its feed set equals Ethereum's.

Euler's current metadata marks AlphaGrowth Cap deprecated: cUSD vault has 26.914886 cUSD and no debt; stc vault zero; its USDC vault has 13,346.941381 assets and 0.792795 USDC borrowing. This residual is not a material active Cap borrowing venue. [Dolomite's markets documentation](https://docs.dolomite.io/markets) describes cUSD supply paused and stc withdrawal-only. Ethereum market 14 cUSD has 25.638794687148954340 supplied, 12.633107572894820791 cUSD borrowed; market 15 stc has 10,616.043432813892296182 supplied and no stc borrowing. Both supply caps are one wei; stc isClosing=true. These are restricted legacy positions. Debt in other Dolomite assets secured by residual stc was not fully reconstructed; zero stc borrowing does not prove zero collateral-backed debt.

**Pendle and token holders**

All 504 returned Ethereum Pendle markets were paginated; four matched canonical Cap assets, all matured. This is not an all-chain proof that no undiscovered derivative exists. [Market/PT/YT registry](pendle-cap-filter.json); fixed-block top-holder reads replace explorer balances where the latter were stale. Top holders below are not an all-time buyer-volume ranking or beneficial-owner map.

| Token | Holder | Fixed-block units |
|---|---|---:|
'''
hs=csvread('largest-token-holders')
for token in dict.fromkeys(r['token'] for r in hs):
 for r in sorted([r for r in hs if r['token']==token],key=lambda r:D(r['balance']),reverse=True)[:3]:text+=f"| {token} | `{r['holder']}` | {D(r['balance']):,.6f} |\n"
text+='''
The stcUSD holders `0xf0bb20865277abd641a307ece5ee04e79073416c`, `0x5f46d540b6ed704c3c8789105f30e075aa900726`, and `0x08c6f91e2b681faf5e17227f2a44c307b3c1364c` are publicly labelled Ether.fi vaults; `0xac21b22b5aeb11bc32de4ecf59e4538fca48b694` is Cap Farm. `0x31b7d5a2b1ce1871dd642f6aecc0ef68d126b95a` holds 6.457M but its ultimate ownership was not established. A wrapper holder is not itself an identified beneficial investor. Expired YT supply can remain large after PT redemption; do not attach a dollar value or future yield to the token count.

**Verified transaction ledger**

Every row has receipt status `0x1`, an exact block/time and ordered logs. Explorer links contain the complete hash; [verified-transactions.csv](verified-transactions.csv) provides unabridged hashes and UTC/Istanbul dates. `decoded-<hash>.json` identifies actual event caller, borrower/onBehalf/receiver and canonical token emitter. `tx-`, `tx-body-`, and `tx-block-` files retain raw evidence. No zero-value spam is used as a funding link.

'''
txs=csvread('verified-transactions')
for r in txs:
 prefix=r['hash'][2:10]
 if prefix not in notes:continue
 text+=f"- **{r['utc']} UTC; {r['istanbul']} Istanbul; {r['chain']} block {int(r['block']):,}.** [{r['hash']}]({r['explorer']}) — {notes[prefix]}\n\n"
text+='''**Funding and ownership limits**

Safe `0x97f478562cfc6e4c88b125bac83f2ad83a203d8e` is currently 2-of-3 and holds 1,971,728.253414 stcUSD. Signer `0x7c29f6a93df60bcd3b20f03b57a2f9e698fd4128` also appears in Cap developer Safe `0xb8fc49402df3ee4f8587268fb89fda4d621a8793` and token-owner Safe `0x80a216738e4e49b262deae6beb6578bdf164c2ea`, each currently 3-of-5. Owner lists were verified both at the May 19 transaction block and at the main snapshot. One signer cannot alone satisfy these thresholds. These facts establish a governance/funding connection, not common control, beneficial ownership or an issuer-financed collateral loan.

Flow, Odyssey and M11 canonical-USDC explorer histories were fully paginated, preserving even spam for auditability; meaningful positive transfers were inspected separately. The Aave largest borrower's Ethereum USDC history is bounded to 20 pages/1,000 transfers and **is not complete**. Its Ethereum USDm history and MegaETH USDm log histories were complete for the queries. Borrower transaction examples do not prove all later uses of funds. Large common routing/settlement counterparties, including the verified CoW example, do not prove wallet affiliation.

The expanded Morpho-history query covers nine known Cap reserve, compounder, parent and adapter addresses across the identified Ethereum Cap collateral markets. It returns zero matches. Both selected historical reserve unwinds instead reference market `0x64d65c9a2d91c36d56fbc42d69e979335320169b3df63bf92789e2c8883fcc64`, whose deployed parameters identify cbBTC collateral, USDC debt and 86% LLTV. This is useful scoped evidence, not proof about every historical adapter, vault depositor, undiscovered address, cross-chain transfer or off-chain account.

**Loss recognition and what is independently visible**

Reviewed deployed Lender implementation `0x68c4f03b8640c0393a832987147bae7a0b27aaa7` uses delegated collateral health. Below one, a liquidation window can be opened; current grace 12 hours, expiry three days, target health 1.25, bonus cap 10%, emergency threshold 90%. The liquidator repays the agent's USDC debt and receives slashed delegated security. Emergency conditions can bypass the ordinary grace path; a zero liquidationStart is not an unconditional statement that liquidation is impossible. Whether recovery fully covers debt depends on collateral prices, slashability and execution.

Reviewed Vault/BorrowLogic account for owed credit rather than automatically writing every unpaid loan down to realizable recovery value. FractionalReserveLogic can revert `FullDivestRequired` if full divestment returns less than the loaned accounting amount. stcUSD accounting is cUSD held with locked-profit mechanics, not an independent junior reserve. These deployed observations qualify broad [documentation statements about redemptions](https://docs.cap.app/overview/risks); no unconditional exit guarantee was established.

Pawn `_harvestAndReport` returns idle assets plus the lesser of current debt and oracle collateral value (or only idle if debt/collateral is zero). Losses therefore affect the Pawn lender's strategy value, subject to reporting and oracle assumptions. Liquidators are permissioned and debt can be called; those mechanisms are not insurance. Morpho liquidation writes off uncollectible bad debt against the affected market's suppliers. Aave's deployed LiquidationLogic burns remaining borrower debt and creates a reserve deficit when collateral is exhausted; elimination of that deficit requires an authorized coverage path, not an assumed automatic guarantee. Current `getReserveDeficit` reads for MegaETH USDm, USDT0 and stcUSD are zero.

Reserve/loan/token balances, delegation mappings, contract code and the Pareto token subscription can be inspected independently. Proprietary operator assets and trades, FalconX's off-chain credit, Ondo's underlying custody/backing and any optional guarantee agreement terms cannot be fully verified from these public reads. [Cap's underwriting documentation](https://docs.cap.app/overview/protocol-overview/shared-security-networks) describes Symbiotic/EigenLayer and optional off-chain support; it does not prove an enforceable guarantee for every current loan.

**Reproduction and failed reads**

Requires Python 3 plus `requests`; no credentials. From the research directory, run `python3 evidence/derive.py` for arithmetic/position/receipt checks and CSV regeneration, then `python3 evidence/build_appendix.py` for this guide and `python3 evidence/verify.py` for receipt/sequence/document checks. Network collectors are small separate scripts: `chain.py`, `multicall.py`, `morpho_markets.py`, `morpho_positions.py`, `pendle_collect.py`, `aave_mega_positions.py`, `paginate.py`, and `trace_tx.py`. Saved request payloads permit precise replay. Fixed-block scripts intentionally use the observation block; they are not a live dashboard. Public historical RPC availability varies.

Cap frontend/API attempts returned HTTP403. Several exploratory getter calls reverted or historical calls lacked archive access; these remain preserved and **are not zeros**. `aave-mega-core.json`'s first `eMode8` row has an initial dynamic-tuple decoding error and must not be used: the successful `emode8 collateral config` in `aave-mega-positions.json` supplies 8800/9000/10400; the collector was corrected. Earlier rate-limited Aave position raw batches are superseded by the final successful Multicall results. Dolomite's valid reads are `dolomite-cap-multicall.json`, not its failed preliminary files. Failed `latestRoundData` on a capped oracle does not invalidate its separately successful supported getters. Source revisions and protocol permissions can change after the stated blocks.

Useful derived tables: [native loans](native-loans.csv), [all Morpho markets](morpho-markets.csv), [Morpho positions](morpho-positions.csv), [Aave positions](aave-mega-positions.csv), [largest token holders](largest-token-holders.csv), [verified transactions](verified-transactions.csv), [source metadata](source-index.csv). Original JSON and verified Solidity sources remain alongside these tables; `SHA256SUMS` records the final evidence files.
'''
(P/'README.md').write_text(text)
# Keep the source inventory small: one metadata row per recorded request file, no response duplication.
sources=[]
for p in sorted(P.glob('*.json')):
 try:d=json.loads(p.read_text())
 except Exception:continue
 if isinstance(d,dict) and d.get('url'):sources.append(dict(file=p.name,url=d['url'],observed_utc=d.get('observed_utc',''),http_status=d.get('http_status','')))
with (P/'source-index.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['file','url','observed_utc','http_status']);w.writeheader();w.writerows(sources)
print('Guide words',len(text.split()),'sources',len(sources))
