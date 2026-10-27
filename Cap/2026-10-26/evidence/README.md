# Evidence guide and detailed findings

This appendix supports [the concise report](../cap-cusd-investigation-2026-10-26.md). JSON files preserve requests, public endpoints, retrieval timestamps and responses; decoded files are derived interpretations. The canonical derived arithmetic is in [calculation-checks.json](calculation-checks.json). No keys, wallet secrets, private configurations or chain writes were used.

**Observation times and source dates**

| State | Block | UTC |
|---|---:|---|
| Ethereum reserve, native loans, Pawn, holders | 26,278,245 | 2026-10-26 17:05:59 |
| MegaETH Aave, remote tokens | 30,237,747 | 2026-10-26 17:12:38 |
| Katana token/adapter RPC reads | 46,291,948 | 2026-10-26 17:12:39 |
| Tempo token RPC reads | 46,008,317 | 2026-10-26 17:12:38 |
| Morpho Katana market state | 46,291,545 | 2026-10-26 17:05:56 |
| Morpho July PT-cUSD Ethereum | 26,278,244 | 2026-10-26 17:05:47 |
| Morpho January PT-stcUSD Ethereum | 26,278,240 | 2026-10-26 17:04:59 |

Morpho positions carry timestamp 17:09:59 UTC; their summed balances match the earlier market states to rounding. They are indexed accounting balances, not a fresh transaction applying interest to every market. Source observation times must not be confused with historical transaction times. The request-date filename does not override these dates.

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

| Aave USDm role | Wallet | Units | Share of relevant pool total |
|---|---|---:|---:|
| Borrower | `0x64471d103a7f77262529383d53bdd28b260b1ae8` | 5,967,570.916532 | 99.5077% |
| Borrower | `0xf8d9bee2c37474fbe77ada27b901eba42bfa4521` | 11,869.564251 | 0.1979% |
| Borrower | `0x6c423f52fc9003e50e5b51667dacd0799bf1f2f8` | 5,787.812768 | 0.0965% |
| Supplier | `0x8a4aa69f694da05c042c2e59bb9a86f198361799` | 5,959,189.937667 | 91.9603% |
| Supplier | `0x7e195b3fc91fdd51a9cd5070cc044602212ac983` | 216,754.783236 | 3.3449% |
| Supplier | `0xf20a6d74ae894712b261d2df85282287ac975c6e` | 32,156.486842 | 0.4962% |

Morpho position tables below are complete for each of the three markets above $100 debt. Full market registry, including inactive/zero markets, is [morpho-markets.csv](morpho-markets.csv). Morpho being permissionless/listed does not imply current material activity.

**Ethereum: PT-cUSD-23JUL2026 / USDT**

Market `0xfd039edc69eac5eaab4a10463fdbcaca75d6eddb1f0e00248d73fc977fb2554b`; collateral `0x928FB6ED39100a92B2480f5cbB93453f98D9F4cE`; oracle `0x25b30502467639E8FA118451105269e9B9813DD2`; LLTV 91.5%.

| Role | Wallet | Debt or supply | Collateral units (borrowers) | Market share |
|---|---|---:|---:|---:|
| Borrower | `0xa1D9769c9Aa6E76651A9514e6E998767009E930e` | 18,281.023544 | 20,489.328454 | 99.9350% |
| Borrower | `0x83DeF68f12Acc40b9157015c2dffe5028D9e7A93` | 5.904352 | 6.898604 | 0.0323% |
| Borrower | `0x7D94f632DB0F075d16e99942Ca45EAbF5f95ab30` | 4.453372 | 6.265076 | 0.0243% |
| Supplier | `0x12345678920266cd9d2b9A5A079d4a1E05d8B5df` | 5,144.502146 | 0.000000 | 24.7517% |
| Supplier | `0x022f8876029fD6E0c1B1bb85C98463cD71c0A54E` | 4,174.934926 | 0.000000 | 20.0868% |
| Supplier | `0x8D1b878509562Fe8C097536e6E8DA5Bdeed05D1b` | 3,575.923795 | 0.000000 | 17.2048% |
**Katana: stcUSD / vbUSDC**

Market `0xea8f588be62079a1ad874bf7c7217166b323e0fe8ea3e59b584430ed1b859ace`; collateral `0x88887bE419578051FF9F4eb6C858A951921D8888`; oracle `0x832AEC697F9031709281e29ACb4fB69b1E3A6f7a`; LLTV 86%.

| Role | Wallet | Debt or supply | Collateral units (borrowers) | Market share |
|---|---|---:|---:|---:|
| Borrower | `0x6655459bAb7a5e99f2d61279316f6d0a465Be784` | 62,840.907353 | 89,633.228128 | 99.5781% |
| Borrower | `0x1a90D8F5a0A09D11b651835bBB25BfED7a4E6478` | 265.675462 | 305.095302 | 0.4210% |
| Borrower | `0x50B75d586929Ab2F75dC15f07E1B921b7C4Ba8fA` | 0.546425 | 1.000000 | 0.0009% |
| Supplier | `0xaFA6ce7b33dBEA40189f195F4642287AE191E1F0` | 70,157.218075 | 0.000000 | 99.9991% |
| Supplier | `0x50B75d586929Ab2F75dC15f07E1B921b7C4Ba8fA` | 0.505222 | 1.000000 | 0.0007% |
| Supplier | `0x000000000000000000000000000000000000dEaD` | 0.101044 | 0.000000 | 0.0001% |
**Ethereum: PT-stcUSD-29JAN2026 / USDC**

Market `0x03f715ef1ae508ab3e1faf4dffdbf2a077d1f0ad10c5aad42cf4438d5e3328af`; collateral `0xC3c7E5E277d31CD24a3Ac4cC9af3B6770F30eA33`; oracle `0xC86CfE9dE224bf0A14Ea83949591a54467BE647D`; LLTV 91.5%.

| Role | Wallet | Debt or supply | Collateral units (borrowers) | Market share |
|---|---|---:|---:|---:|
| Borrower | `0x4Dfeb30021a5bb94aFE33a149050A264FAbf4C58` | 11,188.121169 | 15,146.482138 | 99.2996% |
| Borrower | `0xeA11b00e1BBd20b5AFBfe46D021305bf9eF89E4D` | 78.812956 | 104.188870 | 0.6995% |
| Borrower | `0x482CeaFf3f256033777B20595e833345d766e4DA` | 0.092977 | 3.037890 | 0.0008% |
| Supplier | `0xf7C04A39e47C7ea9D6888F9389eA85846e22aE1a` | 7,268.006350 | 0.000000 | 57.6460% |
| Supplier | `0x72c3943dcbadf4725FE1E079F4B4eC17163c22aF` | 2,052.662874 | 0.000000 | 16.2807% |
| Supplier | `0x9A23657EBA76190E3bD4162179BFA3a80D673aC7` | 1,846.063592 | 0.000000 | 14.6420% |

Katana market-facing supplier `0xafa6ce7b33dbea40189f195f4642287ae191e1f0` returns parentVault `0x6a31358e58b8692ce5317181ff3379a5766a7aba` (Clearstar Core USDC). Yearn Degen parent `0xa2d38c8a3d810ebcf4c2075821c5ec8f976bb692` is listed by the API but its current allocation to this market is zero. Katana oracle feeds were separately read in `katana-adapter-oracle.json`; no assumption that its feed set equals Ethereum's.

Euler's current metadata marks AlphaGrowth Cap deprecated: cUSD vault has 26.914886 cUSD and no debt; stc vault zero; its USDC vault has 13,346.941381 assets and 0.792795 USDC borrowing. This residual is not a material active Cap borrowing venue. [Dolomite's markets documentation](https://docs.dolomite.io/markets) describes cUSD supply paused and stc withdrawal-only. Ethereum market 14 cUSD has 25.638794687148954340 supplied, 12.633107572894820791 cUSD borrowed; market 15 stc has 10,616.043432813892296182 supplied and no stc borrowing. Both supply caps are one wei; stc isClosing=true. These are restricted legacy positions. Debt in other Dolomite assets secured by residual stc was not fully reconstructed; zero stc borrowing does not prove zero collateral-backed debt.

**Pendle and token holders**

All 504 returned Ethereum Pendle markets were paginated; four matched canonical Cap assets, all matured. This is not an all-chain proof that no undiscovered derivative exists. [Market/PT/YT registry](pendle-cap-filter.json); fixed-block top-holder reads replace explorer balances where the latter were stale. Top holders below are not an all-time buyer-volume ranking or beneficial-owner map.

| Token | Holder | Fixed-block units |
|---|---|---:|
| stcUSD | `0xf0bb20865277aBd641a307eCe5Ee04E79073416C` | 14,065,880.973686 |
| stcUSD | `0x5f46d540b6eD704C3c8789105F30E075AA900726` | 8,432,091.630362 |
| stcUSD | `0x983AEAaA0d0426839158435C43725EA7F45d4137` | 6,763,265.741261 |
| PT-cUSD-23JUL2026 | `0x444CC947a57f8fC6576abD19837b7df14C4c8e89` | 35,285.470554 |
| PT-cUSD-23JUL2026 | `0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb` | 20,516.400949 |
| PT-cUSD-23JUL2026 | `0x9EaAedA23177B7168c55a3A0F937f67919733449` | 8,517.273100 |
| YT-cUSD-23JUL2026 | `0xbeb69E7ac7f59BDb79b89fc94ED862c6B39F3C00` | 839,847.432221 |
| YT-cUSD-23JUL2026 | `0xC4dA1707a7a16cf4Ac15D75d6a49A684b23EE1E4` | 606,076.755429 |
| YT-cUSD-23JUL2026 | `0x9A4dDebE4BF2dE5B0602cABcB0678EEf50d888C4` | 186,876.915274 |
| PT-cUSD-29JAN2026 | `0x307c15f808914Df5a5DbE17E5608f84953fFa023` | 7,081.933473 |
| PT-cUSD-29JAN2026 | `0x5a928A20CC48308323eC95bE838c8717F51f49e9` | 4,904.949737 |
| PT-cUSD-29JAN2026 | `0x000000000004444c5dc75cB358380D2e3dE08A90` | 740.735801 |
| YT-cUSD-29JAN2026 | `0x815f5BB257e88b67216a344C7C83a3eA4EE74748` | 11,956,328.665916 |
| YT-cUSD-29JAN2026 | `0x5a41D004A64aba3cf07D8a11598349fFcd3e07cF` | 10,077,379.571656 |
| YT-cUSD-29JAN2026 | `0x308b7f73738082EBDeFfd215bBAB0550Dc6b679C` | 10,001,000.000000 |
| PT-stcUSD-23JUL2026 | `0xfc1F6bFff376806163262D32Cf060e3783a925d4` | 48,690.234046 |
| PT-stcUSD-23JUL2026 | `0xEA829678bEC82cF0f90737Ae9c7D1C31771E0Da2` | 7,252.774607 |
| PT-stcUSD-23JUL2026 | `0x23AaAd5c1b83bE9A26757F1cF2315f84d1d70615` | 681.439521 |
| YT-stcUSD-23JUL2026 | `0x40506E9C699B7DeD298D8f76a4B674473F03eBad` | 481,584.805596 |
| YT-stcUSD-23JUL2026 | `0xC34aE1A39662415a4720d4A3e7C2Be0E202568C2` | 329,796.041318 |
| YT-stcUSD-23JUL2026 | `0xe0A86AFB73c0922A50D4A985A25507EcDA8a9B51` | 86,107.087965 |
| PT-stcUSD-29JAN2026 | `0xBBBBBbbBBb9cC5e90e3b3Af64bdAF62C37EEFFCb` | 15,519.102133 |
| PT-stcUSD-29JAN2026 | `0x719e77027952929ed3060dbFFC5D43EC50c1cf79` | 554.778275 |
| PT-stcUSD-29JAN2026 | `0x1C744202290c1eA17A92B64512762F1b0a95cC0c` | 102.998822 |
| YT-stcUSD-29JAN2026 | `0x815f5BB257e88b67216a344C7C83a3eA4EE74748` | 37,822,446.295679 |
| YT-stcUSD-29JAN2026 | `0xC34aE1A39662415a4720d4A3e7C2Be0E202568C2` | 8,482,852.395509 |
| YT-stcUSD-29JAN2026 | `0x9Db0Ee5BAc43EA008312295a95c2e287ECFf8C8d` | 4,314,978.963056 |

The stcUSD holders `0xf0bb20865277abd641a307ece5ee04e79073416c`, `0x5f46d540b6ed704c3c8789105f30e075aa900726`, and `0x08c6f91e2b681faf5e17227f2a44c307b3c1364c` are publicly labelled Ether.fi vaults; `0xac21b22b5aeb11bc32de4ecf59e4538fca48b694` is Cap Farm. `0x31b7d5a2b1ce1871dd642f6aecc0ef68d126b95a` holds 6.457M but its ultimate ownership was not established. A wrapper holder is not itself an identified beneficial investor. Expired YT supply can remain large after PT redemption; do not attach a dollar value or future yield to the token count.

**Verified transaction ledger**

Every row has receipt status `0x1`, an exact block/time and ordered logs. Explorer links contain the complete hash; [verified-transactions.csv](verified-transactions.csv) provides unabridged hashes and UTC dates. `decoded-<hash>.json` identifies actual event caller, borrower/onBehalf/receiver and canonical token emitter. `tx-`, `tx-body-`, and `tx-block-` files retain raw evidence. No zero-value spam is used as a funding link.

- **2025-10-19T23:25:35+00:00 UTC; Ethereum block 23,614,944.** [0x66f3719d2095b3a425dd6bf81dabb1a76eb1f1770b2695905d666a7ed660122a](https://etherscan.io/tx/0x66f3719d2095b3a425dd6bf81dabb1a76eb1f1770b2695905d666a7ed660122a) — January PT borrower 0x4dfeb30021a5bb94afe33a149050a264fabf4c58 posts 2,067.739008953590589798 PT-stcUSD and borrows 1,800 USDC onBehalf itself. Receipt is dated 2025, not 2026.

- **2026-02-13T17:02:11+00:00 UTC; Ethereum block 24,449,222.** [0xef869705faf4d0cd18577cb8a0ecebb50f3b3a5d150d75c49eaccdd20c516d51](https://etherscan.io/tx/0xef869705faf4d0cd18577cb8a0ecebb50f3b3a5d150d75c49eaccdd20c516d51) — 0x1af263eaf51c6a2dc24d929716d5e63e3602d995 funds Aave supplier Safe 0x8a4aa69f694da05c042c2e59bb9a86f198361799 with 3,000,000 USDC. Ultimate source/owner unknown.

- **2026-02-14T11:47:35+00:00 UTC; Ethereum block 24,454,827.** [0xdc883ecffb8afa8341cdd660888f267ef7dc34e5ba2e7b7a016281e7fbd579d7](https://etherscan.io/tx/0xdc883ecffb8afa8341cdd660888f267ef7dc34e5ba2e7b7a016281e7fbd579d7) — Safe 0xdc74c3359c6412f6e9e208ed8dce609ece619b5e funds supplier Safe 0x8a4a… with 2,000,000.000770 USDC. Ultimate source/owner unknown.

- **2026-02-14T11:54:59+00:00 UTC; Ethereum block 24,454,864.** [0x17dbafee03627263edff1e52869ef0cb499723a2322539f37598bbc27f47ce76](https://etherscan.io/tx/0x17dbafee03627263edff1e52869ef0cb499723a2322539f37598bbc27f47ce76) — Supplier Safe pays 5,000,000 USDC to 0x343c18b0f1710b65ce33a7ce720b5d540215d343 and receives 4,999,999.130000 USDm minted on Ethereum. No Cap cUSD mint.

- **2026-02-14T12:03:23+00:00 UTC; Ethereum block 24,454,906.** [0x50303f8ff60086ea9c6bb4c0f332289fc261ba27afb03ad1cdd9f2a5f6d5410c](https://etherscan.io/tx/0x50303f8ff60086ea9c6bb4c0f332289fc261ba27afb03ad1cdd9f2a5f6d5410c) — Supplier Safe bridges 4,999,999.130000 USDm from Ethereum to itself on MegaETH; linked destination is 96ef39f0.

- **2026-02-14T12:06:55+00:00 UTC; MegaETH block 8,273,804.** [0x96ef39f00b23abd25606a681525719d5aedb2ea37d77b3d4243bde9a0c9702c0](https://megaeth.blockscout.com/tx/0x96ef39f00b23abd25606a681525719d5aedb2ea37d77b3d4243bde9a0c9702c0) — Matched MegaETH delivery mints 4,999,999.130000 USDm to the supplier Safe.

- **2026-02-14T12:55:21+00:00 UTC; MegaETH block 8,276,710.** [0x36a769ccb4aceae1ec6e8174e9ed49372e79bd6861e50dcee1f7b8ea6a8e68ec](https://megaeth.blockscout.com/tx/0x36a769ccb4aceae1ec6e8174e9ed49372e79bd6861e50dcee1f7b8ea6a8e68ec) — Supplier Safe supplies 5,000,000 USDm to Aave, onBehalf itself. The 0.87 USDm difference from the immediately traced bridge is pre-existing wallet balance, not an invented bridge amount.

- **2026-02-21T16:07:11+00:00 UTC; Ethereum block 24,506,331.** [0xd5756eb0ce5a3f824f5af059b57d8dc4f5e7f1ac360cd2e8261f8a02e23d800b](https://etherscan.io/tx/0xd5756eb0ce5a3f824f5af059b57d8dc4f5e7f1ac360cd2e8261f8a02e23d800b) — YT buyer 0xbeb69e7ac7f59bdb79b89fc94ed862c6b39f3c00 spends 2,000 USDS routed through USDC/cUSD/SY and receives 83,475.275943015426212443 July YT-cUSD. Equal newly minted PT goes to the pool, not the buyer: economically a YT purchase despite the mint-from-zero event.

- **2026-02-21T22:49:11+00:00 UTC; Ethereum block 24,508,330.** [0xbd5979a8f203c66c38ba24ca162e0f638dd48ded7b10db887f7b64431fcb7acc](https://etherscan.io/tx/0xbd5979a8f203c66c38ba24ca162e0f638dd48ded7b10db887f7b64431fcb7acc) — PT buyer 0x444cc947a57f8fc6576abd19837b7df14c4c8e89 rolls 34,562.8478206292 matured January PT-cUSD through SY, purchasing 35,285.470554389843990896 July PT-cUSD. No YT received.

- **2026-03-09T09:00:35+00:00 UTC; Ethereum block 24,618,883.** [0xc84a543ad67d5142dd17eb68b93a37f3f9ffc0f1d8f628bcc00e0ddd7ccc8dd4](https://etherscan.io/tx/0xc84a543ad67d5142dd17eb68b93a37f3f9ffc0f1d8f628bcc00e0ddd7ccc8dd4) — M11-labelled agent borrows 9,999,900 USDC. An earlier 100-USDC test borrowing appears in explorer history but is not added without a separately cited receipt.

- **2026-03-09T09:18:11+00:00 UTC; Ethereum block 24,618,970.** [0xcf61e8fbec75c420a7ce580f325cb293ba6f365f7e045d12df3f070f21f80fbd](https://etherscan.io/tx/0xcf61e8fbec75c420a7ce580f325cb293ba6f365f7e045d12df3f070f21f80fbd) — M11-labelled agent transfers 10,000,000.246666 USDC to 0x433d5b175148da32ffe1e1a37a939e1b7e79be4d, officially listed by Pareto as FalconX Credit Vault. A token subscription is visible; the underlying off-chain credit is not independently verified.

- **2026-04-25T06:43:11+00:00 UTC; Ethereum block 24,955,287.** [0x217f20c438f338d9b358daaac4507795f65631ccd9f9615de22c76c4caa00dd5](https://etherscan.io/tx/0x217f20c438f338d9b358daaac4507795f65631ccd9f9615de22c76c4caa00dd5) — July PT borrower 0xa1d9769c9aa6e76651a9514e6e998767009e930e posts PT-cUSD and borrows 17,269.257650 USDT onBehalf itself. Ordinary collateral use; no fresh Cap mint in this transaction.

- **2026-05-19T17:10:35+00:00 UTC; Ethereum block 25,130,674.** [0xa8dfb11301d4c1738a266944c84d7908917c594319cabc1a710aab05ec2bda5d](https://etherscan.io/tx/0xa8dfb11301d4c1738a266944c84d7908917c594319cabc1a710aab05ec2bda5d) — Safe 0x97f478562cfc6e4c88b125bac83f2ad83a203d8e redeems cUSD and receives 4,500,012.467555 USDC. Reserve unwind: Morpho cbBTC/USDC market 64d65c9a…fcc64 → adapter dd0f28…490d → bcc917…4760 → Gauntlet parent 8c106…a3d0 → compounder 8092…e71d → Cap reserve vault → cUSD → Safe.

- **2026-05-19T17:17:59+00:00 UTC; Ethereum block 25,130,711.** [0xc3afbb05b630671037a7b5f965a8700a74b4047a48e9f44038539039f8aad286](https://etherscan.io/tx/0xc3afbb05b630671037a7b5f965a8700a74b4047a48e9f44038539039f8aad286) — That Safe pays 4,500,000 USDC to Lender, forwarded to cUSD. Lender Repay agent is 0x3fa0d4ce8c396b03beb3d8411e10b0126a1b913d (M11-labelled), not the Safe. Repay tuple and debt-token burn validate the recipient of debt relief.

- **2026-06-16T16:16:35+00:00 UTC; Ethereum block 25,331,221.** [0x8ab7c24a3bb630dd95934359d79f7103b21f5f19bd12511880e2a5b56d7c33c2](https://etherscan.io/tx/0x8ab7c24a3bb630dd95934359d79f7103b21f5f19bd12511880e2a5b56d7c33c2) — M11-labelled native agent borrows 1,250,000 USDC from Cap.

- **2026-06-16T16:35:47+00:00 UTC; Ethereum block 25,331,317.** [0x1f7a5623d54d60704d01c70376442196a88c255194e986da6e981c1e01aac511](https://etherscan.io/tx/0x1f7a5623d54d60704d01c70376442196a88c255194e986da6e981c1e01aac511) — M11-labelled agent sends 4,499,990 USDC to Safe 0x97f4…d8e. This exceeds that day’s traced 1.25M borrowing and uses other wallet funds too; no contemporaneous remint is established.

- **2026-07-08T21:11:05+00:00 UTC; MegaETH block 20,748,054.** [0x80b6a8279ff4f9b02e4aa52251bc32b0b213f574860e1587ac384e6c13bc0797](https://megaeth.blockscout.com/tx/0x80b6a8279ff4f9b02e4aa52251bc32b0b213f574860e1587ac384e6c13bc0797) — MegaETH Pool Borrow: user and onBehalfOf both 0x64471d103a7f77262529383d53bdd28b260b1ae8; 14,700,000 USDm received.

- **2026-07-08T21:14:03+00:00 UTC; MegaETH block 20,748,232.** [0x4244a35df22c3b4304317d30302647f20c7508fb77e55297fa829a8b5f55795e](https://megaeth.blockscout.com/tx/0x4244a35df22c3b4304317d30302647f20c7508fb77e55297fa829a8b5f55795e) — Same borrower burns/bridges 10,000,000 MegaETH USDm to Ethereum. LayerZero message links the destination receipt a2d01324.

- **2026-07-08T21:17:19+00:00 UTC; MegaETH block 20,748,428.** [0xd203465b11dc53437413664246d39e5a1f6f9481a826958489745cea8f1831ac](https://megaeth.blockscout.com/tx/0xd203465b11dc53437413664246d39e5a1f6f9481a826958489745cea8f1831ac) — Same borrower repays 4,700,000 USDm to Aave. The debt-token burn differs slightly because interest accrues; repayment amount is the underlying-token transfer and Repay event.

- **2026-07-08T21:19:47+00:00 UTC; Ethereum block 25,490,495.** [0xa2d0132482fd431753ae0ea0126f0b399bbc1ec97f4b35292e310a55724ce408](https://etherscan.io/tx/0xa2d0132482fd431753ae0ea0126f0b399bbc1ec97f4b35292e310a55724ce408) — Ethereum receives the linked bridge message and mints 10,000,000 USDm to 0x6447…1ae8. Ethereum USDm is 0xec2af1c8b110a61fd9c3fa6a554a031ca9943926.

- **2026-07-08T21:23:11+00:00 UTC; Ethereum block 25,490,512.** [0x985fae3664c87e4a7e2c788cc2ab1f8123a85131990cf1a7e312d8e2ce76a8e8](https://etherscan.io/tx/0x985fae3664c87e4a7e2c788cc2ab1f8123a85131990cf1a7e312d8e2ce76a8e8) — 0x6447…1ae8 sends 10,000,000 Ethereum USDm to 0xe6d0ca9844f4c079e6e732f396ef3b9f98a2dac8.

- **2026-07-08T21:36:23+00:00 UTC; Ethereum block 25,490,578.** [0xa376ffebf93e9fd966a84afe2fd8f7724430edf12ba97d1f8dd235f8d8877168](https://etherscan.io/tx/0xa376ffebf93e9fd966a84afe2fd8f7724430edf12ba97d1f8dd235f8d8877168) — 0xe6d0ca9844f4c079e6e732f396ef3b9f98a2dac8 sends 9,999,999.290816 canonical USDC to 0x6447…1ae8. Paired transfers support a conversion relationship; its off-chain terms and counterparty ownership are unknown.

- **2026-07-08T21:38:47+00:00 UTC; Ethereum block 25,490,590.** [0x53698c676d60a67508965c01c2dd593070c51dd437028c5f22bd32371a5b2a53](https://etherscan.io/tx/0x53698c676d60a67508965c01c2dd593070c51dd437028c5f22bd32371a5b2a53) — 0x6447… repays 2,900,000 USDC to Morpho stcUSD market eb17955e…30062e, onBehalf itself, and withdraws 3,200,000 stcUSD. No cUSD mint. Bundler 0x4a6c…0ae0 is not the borrower.

- **2026-07-08T21:41:11+00:00 UTC; Ethereum block 25,490,602.** [0x1dcdfdc3319b5d11ae72cfd8e4c3a037471376b30dae2b56c57078af053fa4c5](https://etherscan.io/tx/0x1dcdfdc3319b5d11ae72cfd8e4c3a037471376b30dae2b56c57078af053fa4c5) — 0x6447… subsequently sends 7,099,999.290816 USDC to 0x3b4d794a66304f130a4db8f2551b0070dfcf5ca7; downstream use not established.

- **2026-07-09T12:19:47+00:00 UTC; Ethereum block 25,494,981.** [0x5010d82c4a909ee04d5226536ae728b802298691fe396f246257962bfceafce8](https://etherscan.io/tx/0x5010d82c4a909ee04d5226536ae728b802298691fe396f246257962bfceafce8) — CoW settlement: 0x6447… pays 1,000,000 USDC and receives 1,000,686.345026 USDT. 0x8f10b468… appears as a settlement counterparty also seen in Odyssey/Safe history. Shared routing counterparties alone do not establish ownership.

- **2026-07-13T14:55:11+00:00 UTC; Ethereum block 25,524,438.** [0xffa215a6e5b89dcea81f84b67a08cfc0acfded4075f035c6959f03c486d9cddd](https://etherscan.io/tx/0xffa215a6e5b89dcea81f84b67a08cfc0acfded4075f035c6959f03c486d9cddd) — Wallet 0x743d7b30661d65b41960bf6b5d1bb93cf7972a73 deposits 84,508.685787192144205899 cUSD via SY and receives equal PT and YT. Mint receiverPT equals receiverYT: actual paired mint.

- **2026-07-17T21:27:19+00:00 UTC; Katana block 37,580,828.** [0xea645d03e0e417d981c146facedcab29a2d76b26f2ec4db3351f6fe873380243](https://katanascan.com/tx/0xea645d03e0e417d981c146facedcab29a2d76b26f2ec4db3351f6fe873380243) — Katana borrower 0x6655459bab7a5e99f2d61279316f6d0a465be784 posts 18,799.014622 stcUSD and borrows 17,000 vbUSDC; 6,500 repays another market, and 10,500.693456 enters Yearn Degen then a different Morpho market cd2dc… (not the stc collateral market). No Cap mint.

- **2026-07-23T03:13:11+00:00 UTC; Ethereum block 25,592,673.** [0x1936a4743a900b346259c42dc6f9230a0a217e4a26731aceeb7b6da985588b51](https://etherscan.io/tx/0x1936a4743a900b346259c42dc6f9230a0a217e4a26731aceeb7b6da985588b51) — Earlier leveraged mint: 250,000 USDC flash advance funds cUSD mint/stake; 233,234.962828 stcUSD (rounded) posted to Pawn; 250,000 permanent Pawn debt repays the flash advance.

- **2026-07-25T21:24:35+00:00 UTC; Ethereum block 25,612,458.** [0xcdb8aa45efd51ddb89f1c46bea2067789df789df9c2d8f4a3d1c4e6a53d204a0](https://etherscan.io/tx/0xcdb8aa45efd51ddb89f1c46bea2067789df789df9c2d8f4a3d1c4e6a53d204a0) — yvUSD parent 0x696d02db93291651ed510704c9b286841d506987 supplies 37,000 USDC equity to looper 0xd362efc75ef1879f37a900823495f402cfdb0986, following its own Sky/sUSDS exit.

- **2026-07-25T21:27:35+00:00 UTC; Ethereum block 25,612,473.** [0x8b157242b3484f62532f5beb85f8ff406cc6a76a9b145ff52fca194d392c746d](https://etherscan.io/tx/0x8b157242b3484f62532f5beb85f8ff406cc6a76a9b145ff52fca194d392c746d) — Ordered logs: 213,000 USDC Morpho flash advance; looper 250,000 USDC to exchange 0xa1be7034b2aa8e72d81e17420b6c6c4f0035fdd4; exchange 250,000 USDC to cUSD; 250,002.332675417191372791 cUSD minted; 233,139.461481560505648366 stcUSD minted and posted to Pawn; Pawn Borrowed caller/receiver is looper for 213,000 USDC; flash loan repaid. Net new permanent debt 213,000, not 426,000.

- **2026-09-07T11:43:31+00:00 UTC; Katana block 42,038,600.** [0xefa2d63fc638f624cb65b9594fdf334b3970c5d23809407fc786288b67769c88](https://katanascan.com/tx/0xefa2d63fc638f624cb65b9594fdf334b3970c5d23809407fc786288b67769c88) — Same Katana borrower posts 70,834.213506 stcUSD and borrows 65,000 vbUSDC. Transaction also bridges/burns 89,245.770783 vbUSDC using other funds and deposits 10,018.618820 via Clearstar into the different cd2dc… market. No Cap mint; do not attribute all outputs to this one borrowing.

- **2026-09-21T15:27:47+00:00 UTC; Ethereum block 26,026,776.** [0x8982726eac16d7146f1ea2822d5c9d6be00b8182e410a1ae83c2db897f63e353](https://etherscan.io/tx/0x8982726eac16d7146f1ea2822d5c9d6be00b8182e410a1ae83c2db897f63e353) — Flow-labelled agent borrows 3,000,000 USDC. Reserve unwind includes 2,997,681.179759 USDC withdrawn from Morpho market 64d65c9a…fcc64 (cbBTC/USDC) via adapter 2b968…8290 → Steakhouse parent beef088…0f51 → Cap compounder baed…f2e3 → reserve vault → cUSD → agent.

- **2026-09-21T15:43:23+00:00 UTC; Ethereum block 26,026,853.** [0x7eaa11407bfb46ae53cde5608dfe80a92981c0a31dcee53467e238a30c9cbed0](https://etherscan.io/tx/0x7eaa11407bfb46ae53cde5608dfe80a92981c0a31dcee53467e238a30c9cbed0) — Flow-labelled agent sends 3,000,000 USDC to 0x938226907b3b956ff8b15261a568340a9f550b64; downstream ownership/purpose unknown.

- **2026-10-15T14:53:11+00:00 UTC; Ethereum block 26,198,637.** [0xf0ab47631f731c63231314e2b9a5ba83b246f9ddb5bc525d4f94e1b362053ea8](https://etherscan.io/tx/0xf0ab47631f731c63231314e2b9a5ba83b246f9ddb5bc525d4f94e1b362053ea8) — 0xee7ae85f2fe2239e27d9c1e23fffe168d63b4055 sends 999,994 USDC to Flow-labelled agent. Funding is proven; ownership is not.

- **2026-10-15T15:19:59+00:00 UTC; Ethereum block 26,198,771.** [0x1ee289c3f81723f757309fc12198541a5b36c6cb620fbe04ec5d6285da78323b](https://etherscan.io/tx/0x1ee289c3f81723f757309fc12198541a5b36c6cb620fbe04ec5d6285da78323b) — Flow-labelled agent repays 999,999 USDC through Lender back to cUSD. A prior 5-USDC transfer is visible in history; the repayment is not assumed to be funded solely by the 999,994 receipt.

**Funding and ownership limits**

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
