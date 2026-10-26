# Cap cUSD / stcUSD: reserves, borrowing and funding links

**Public observations: October 26, 2026, 17:06:10–17:46:25 UTC / 20:06:10–20:46:25 Europe/Istanbul.** State timestamps: Ethereum: block **26,278,245**, **17:05:59 UTC / 20:05:59 Europe/Istanbul**. MegaETH: block **30,237,747**, **17:12:38 UTC / 20:12:38 Istanbul**. Morpho source states span 17:04:59–17:05:56 UTC; 17:09:59 position queries reconcile within rounding. Retrieval times, other blocks and transaction dates are in the [evidence guide](evidence/README.md).

**Executive findings.** Leveraged cUSD minting is proven, but **no closed path from Cap reserves into the external loans financing that minting was established**. The main concerns are concentration, liquidity and valuation dependencies:

- **72.87%** of Cap’s **76.880M USDC reserve book** is native operator borrowing. Accrued native debt is **56.095M**; the largest agent owes **51.59%**, the largest three **76.27%**.
- Yearn Pawn Broker and Aave MegaETH have **12.024M combined stcUSD-backed debt** (6.056M USDC plus 5.968M USDm), separate from native loans. Yearn’s position has **87.15% LTV versus 91.5% LLTV**, approximately **4.76% oracle-price headroom** with debt unchanged.
- Aave’s largest borrower has health **1.093**; one Safe supplies **91.96%** of the USDm pool.
- A Safe that repaid M11’s native loan shares one signer with Cap’s published multisigs. This establishes a relationship, **not common ownership or reserve recycling**.

**Contracts and reserves.** [Official deployments](https://docs.cap.app/developers/addresses) identify Ethereum [cUSD](https://etherscan.io/address/0xcccc62962d17b8914c62d74ffb843d73b2a3cccc), [stcUSD](https://etherscan.io/address/0x88887be419578051ff9f4eb6c858a951921d8888), [Lender](https://etherscan.io/address/0x15622c3dbbc5614e6dfa9446603c1779647f01fc) and [reserve vault](https://etherscan.io/address/0x3ed6aa32c930253fc990de58ff882b9186cd0072). Current calls confirm USDC is the only active reserve asset. Supply is **76,880,591.033262 cUSD**; **69,250,490.083695 stcUSD** represents **75,287,714.143852 cUSD**. Do not count staking or bridged wrappers again as backing.

| Reserve accounting | USDC |
|---|---:|
| Total supplied/booked claims | 76,880,199.368483 |
| Native booked borrowing | 56,025,760.412345 |
| Available-balance accounting | 20,854,438.956138 |
| Of available balance: Aave V3 USDC strategy | 20,754,202.929992 |
| Of available balance: OndoHolder USDC strategy | 100,232.258645 |
| Literal USDC in cUSD contract | 4.000000 |

“Available” includes investments, not idle cash. The reserve vault uses Yearn V3 infrastructure. Its Aave strategy has a visible aUSDC claim; OndoHolder introduces rUSDY backing, redemption and compliance dependencies. Former Steakhouse/Gauntlet Morpho strategies have **zero current book value**. The **391.664779** difference between cUSD units and nominal USDC book claims is not itself a dollar solvency calculation; smaller cash/accounting differences are disclosed in the evidence. [Reserve reads](evidence/reserve-accounting.json), [strategy reads](evidence/reserve-strategies-and-pawn.json).

Ethereum, MegaETH and Katana use the same token addresses on different networks; Tempo uses separate six-decimal addresses. The [network registry](evidence/README.md) distinguishes remote tokens from Ethereum reserves.

**Native borrowers.** Eighteen of 44 registered agents have debt. Labels come from [Symbiotic’s published metadata](https://github.com/symbioticfi/metadata-mainnet/tree/ab506ae68f7e165d460df21244ec3bbe0646e458/vaults), joined to deployed delegation mappings; they are not beneficial-owner verification.

| Agent / operator label | Accrued USDC debt | Underwriter / collateral | Health |
|---|---:|---|---:|
| [0x0d35…e21a](https://etherscan.io/address/0x0d35d950fdb0741f11c4384dad15a07edb26e21a), Flow Traders | 28,936,521.42 | Lombard / LBTC | 1.295 |
| [0x7f21…eba1](https://etherscan.io/address/0x7f2165014a477f6aba532000d8088ed64dd1eba1), Odyssey | 8,481,781.09 | Vesper / wstETH | 1.371 |
| [0x3fa0…913d](https://etherscan.io/address/0x3fa0d4ce8c396b03beb3d8411e10b0126a1b913d), M11 Credit | 5,362,281.38 | Ether.fi / weETH | 2.890 |
| [0x4cd7…72d6](https://etherscan.io/address/0x4cd7c473985ca1399810536e0482df1e4e0672d6), StakeStone | 4,829,250.29 | StakeStone / wstETH | 2.234 |
| [0xacaa…d34a](https://etherscan.io/address/0xacaaf5aac016257bf305640fc7d7239648a0d34a), Selini | 2,987,255.30 | Bedrock / uniBTC | 1.565 |

Accrued and booked debt are different accounting views, not additive. One **521.38-USDC test-vault loan** has health **0.0875**; all liquidation-window timestamps are zero. This small exception is not evidence that the material book is liquidating. [Complete loans and underwriters](evidence/native-loans.csv).

**External borrowing actually outstanding.** Values are loan-token units. Expired PT can still secure debt without an active Pendle yield market.

| Venue / collateral | Supplied | Debt | Available cash | Liquidation threshold |
|---|---:|---:|---:|---:|
| [Yearn Pawn, stcUSD/USDC](https://etherscan.io/address/0xe63a2abc24cd9538398d825a4bfe5778d25687df) | 6.045M last-report assets | **6.056M** | **0.000001** | 91.5% |
| [Aave MegaETH, USDm pool](https://megaeth.blockscout.com/address/0x7e324abc5de01d112afc03a584966ff199741c28) | 6.480M | 5.997M total; **5.968M stc-backed** | 483,220.97 | 90%, e-mode 8 |
| [Morpho Katana, stcUSD/vbUSDC](https://app.morpho.org/katana/market/0xea8f588be62079a1ad874bf7c7217166b323e0fe8ea3e59b584430ed1b859ace) | 70,157.82 | 63,107.13 | 7,050.70 | 86% |
| [Morpho Ethereum, July PT-cUSD/USDT](https://app.morpho.org/ethereum/market/0xfd039edc69eac5eaab4a10463fdbcaca75d6eddb1f0e00248d73fc977fb2554b) | 20,784.43 | 18,292.92 | 2,491.51 | 91.5% |
| [Morpho Ethereum, January PT-stcUSD/USDC](https://app.morpho.org/ethereum/market/0x03f715ef1ae508ab3e1faf4dffdbf2a077d1f0ad10c5aad42cf4438d5e3328af) | 12,607.99 | 11,267.04 | 1,340.95 | 91.5% |

Pawn’s sole borrower is [yvUSD’s looper](https://etherscan.io/address/0xd362efc75ef1879f37a900823495f402cfdb0986), pledging **6,392,939.735739 stcUSD**. Its sole shareholder is [USDC-1 yVault](https://etherscan.io/address/0xbe53a109b494e5c9f97b9cd39fe969be68bf6204): **6.038M booked exposure, 32.63% of vault assets**. Its [oracle](https://etherscan.io/address/0x8e3386b2f6084eb1b0988070c3d826995bd175c0) combines stc/cUSD exchange value, RedStone **cUSD_FUNDAMENTAL**, and USDC/USD; it is not simply a spot depeg feed.

Aave borrower [0x6447…1ae8](https://megaeth.blockscout.com/address/0x64471d103a7f77262529383d53bdd28b260b1ae8) pledges **6,668,471.279139 stcUSD**, owing **5,967,570.916532 USDm: 99.51% of USDm debt**. Supplier [Safe 0x8a4a…1799](https://megaeth.blockscout.com/address/0x8a4aa69f694da05c042c2e59bb9a86f198361799) holds **5,959,189.937667 aUSDm**. The [oracle](https://megaeth.blockscout.com/address/0xbbc579ee0a3fd6e9240965c5f57b7e5b3e3809a8) uses stc/cUSD exchange value and **capped USDC/USD**, creating a cUSD credit/market-price basis dependency. Cap’s reserve Aave investment is **Ethereum USDC**, a different pool. [Aave deployment registry](https://github.com/bgd-labs/aave-address-book/blob/main/src/AaveV3MegaEth.sol).

Morpho’s largest borrowers are respectively [0x6655…e784](https://katanascan.com/address/0x6655459bab7a5e99f2d61279316f6d0a465be784), **62,840.91 (99.58%)**; [0xa1d9…930e](https://etherscan.io/address/0xa1d9769c9aa6e76651a9514e6e998767009e930e), **18,281.02 (99.93%)**; and [0x4dfe…4c58](https://etherscan.io/address/0x4dfeb30021a5bb94afe33a149050a264fabf4c58), **11,188.12 (99.30%)**. The Katana supplier is an adapter for **Clearstar Core USDC**, holding **99.9991%** of supply; Yearn Degen’s listed adapter has **zero allocation**. The two PT markets’ largest suppliers hold **24.75% and 57.65%**. Full wallets, collateral, oracles and concentrations are in the [market appendix](evidence/README.md) and [positions CSV](evidence/morpho-positions.csv). Other identified Morpho markets total about **$70 debt**. Euler’s deprecated Cap cluster has under **1 USDC debt**. Dolomite has restricted legacy balances; residual cross-collateral debt was not fully reconstructed.

**Confirmed transactions.** Cited receipts succeeded; canonical token addresses, actual borrower fields and log order were checked.

- **Yearn leveraged mint, July 25, 21:27:35 UTC:** after [37,000 USDC equity funding](https://etherscan.io/tx/0xcdb8aa45efd51ddb89f1c46bea2067789df789df9c2d8f4a3d1c4e6a53d204a0), [the looper](https://etherscan.io/tx/0x8b157242b3484f62532f5beb85f8ff406cc6a76a9b145ff52fca194d392c746d) flash-borrows **213,000 USDC**, spends **250,000**, mints **250,002.332675417191372791 cUSD**, stakes into **233,139.461481560505648366 stcUSD**, posts Pawn collateral and borrows **213,000 USDC** permanently to repay the flash loan. Count permanent debt once. This proves leveraged minting, not issuer financing.
- **Aave refinancing, July 8:** `0x6447…` [borrows 14.7M USDm at 21:11:05](https://megaeth.blockscout.com/tx/0x80b6a8279ff4f9b02e4aa52251bc32b0b213f574860e1587ac384e6c13bc0797), bridges 10M, repays 4.7M, transfers the bridged USDm to `0xe6d0…dac8`, then receives **9,999,999.290816 USDC** from that address. At **21:38:47** it [repays 2.9M USDC on Morpho and withdraws 3.2M stcUSD](https://etherscan.io/tx/0x53698c676d60a67508965c01c2dd593070c51dd437028c5f22bd32371a5b2a53). Those transactions contain no fresh cUSD mint.
- **Native relationship:** on **May 19, 17:17:59**, [Safe 0x97f4…d8e repays 4.5M USDC for M11’s agent](https://etherscan.io/tx/0xc3afbb05b630671037a7b5f965a8700a74b4047a48e9f44038539039f8aad286), after redeeming cUSD. On **June 16**, the agent borrows **1.25M**, then [sends that Safe 4,499,990 USDC at 16:35:47](https://etherscan.io/tx/0x1f7a5623d54d60704d01c70376442196a88c255194e986da6e981c1e01aac511). The Safe shares one signer with Cap both historically and currently. The transfers do not prove reminting or identify their contractual purpose.

Historical Cap reserve withdrawals through Gauntlet/Steakhouse reached **cbBTC/USDC**, not Cap-collateral Morpho lending. The scoped known-reserve-address query found no Cap-market history. The [exact transaction ledger](evidence/README.md) also documents Flow’s borrowing/repayment, M11’s **10M-USDC allocation to Pareto’s FalconX credit vault**, and the Aave supplier’s USDC→USDm→Aave funding. Unknown intermediaries prevent an exhaustive funding conclusion.

**Pendle and holders.** The primary API returned four canonical Ethereum markets, all matured **January 29 or July 23, 2026**. July PT-cUSD’s largest wallet holds **35,285.47**; Morpho holds **29.83%** of residual supply. Morpho holds **94.61%** of January PT-stcUSD. Large stcUSD holders include Ether.fi vaults, the bridge lockbox and Cap Farm; these aggregate holders are not beneficial owners. [PT/YT and stcUSD holders](evidence/largest-token-holders.csv).

Receipts distinguish [a February 21 PT purchase/roll](https://etherscan.io/tx/0xbd5979a8f203c66c38ba24ca162e0f638dd48ded7b10db887f7b64431fcb7acc), [a 2,000-USDS YT purchase](https://etherscan.io/tx/0xd5756eb0ce5a3f824f5af059b57d8dc4f5e7f1ac360cd2e8261f8a02e23d800b), and [July 13 paired minting of 84,508.685787192144205899 PT and YT to one wallet](https://etherscan.io/tx/0xffa215a6e5b89dcea81f84b67a08cfc0acfded4075f035c6959f03c486d9cddd). YT mint events alone do not establish paired ownership; expired YT quantities are not dollar values.

**Losses and limits.** Native liquidation repays USDC and slashes delegated underwriter collateral, subject to grace/emergency rules. Reviewed reserve accounting does not automatically mark unpaid credit to realizable value; full fractional-reserve divestment can revert on a shortfall. stcUSD is not a separately funded first-loss tranche. Pawn can report collateral-value losses; Morpho assigns realized bad debt to market suppliers. Recovery requires collateral, execution and liquidity. [Deployed sources](evidence/source), [Cap risk documentation](https://docs.cap.app/overview/risks).

Onchain balances and selected credit-vault subscriptions are visible; proprietary operator positions, underlying FalconX credit, Ondo backing, optional off-chain guarantee agreements and ultimate ownership were not independently verified. Cap’s reserve API returned **HTTP 403**; loading zeros were never used. This completed bounded investigation is not a full solvency audit or proof that no undiscovered reserve loop exists.
