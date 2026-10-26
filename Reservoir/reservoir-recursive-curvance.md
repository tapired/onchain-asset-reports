# Reservoir / Curvance: Confirmed Circular Loop

**Confirmed round: 1,571,000 USDC borrowed and reminted into Reservoir.** Reservoir then returned **1,570,842.90 USDC** to the same Curvance lending market, after a **157.10 USDC bridge fee**. The borrower posted wsrUSD collateral and borrowed again.

**Date:** September 8, 2026; all times UTC. Verified September 26.  
**Borrower:** `0xaB0d6DB22FB533E2195d137E114DD22a5a52c0AE`  
**Reservoir reserve wallet:** `0x289C204B35859bFb924B9C0759A4FE80f610671c`  
**Curvance USDC market:** `0x7f779f7F5316F6164dC5a25422A5ee51504B284A` on Monad.

## Transactions in Order

| UTC | Chain | Action | Transaction |
|---|---|---|---|
| 18:17:11 | Monad | Borrower borrows **1,571,000 USDC** from Curvance. | [Borrow](https://monadscan.com/tx/0xb4030f793c5007561702f1b77814155ff527107dab47c8097770f80b5e5b60bb) |
| 18:26:09 | Monad | Borrower bridges **1,571,000 USDC** to Ethereum through Circle CCTP. | [Bridge out](https://monadscan.com/tx/0xbd586f16bd5cc73e32d56cb122bbd0e3fe087044bdabaf3b58fb477a002ae6cc) |
| 18:26:47 | Ethereum | Borrower receives **1,571,000 USDC**. | [Bridge receipt](https://eth.blockscout.com/tx/0x975a68315ae77a576e67b650b05851e4b26454731b85478a77e863018f6b7a51) |
| 18:28:59 | Ethereum | Borrower deposits **1,571,000 USDC** into Reservoir's PSM, mints rUSD, converts it into approximately **1,432,473.6755 wsrUSD**, and bridges the wsrUSD to Monad. | [Mint and bridge](https://eth.blockscout.com/tx/0xac00229c46b66223b0378321cc9c0a1c89643b85c10dcba45c8f608067034274) |
| 18:31:47 | Ethereum | Reservoir's Safe withdraws **1,571,000 USDC from that PSM** and transfers it to the reserve wallet. | [Reserve withdrawal](https://eth.blockscout.com/tx/0x06868018bfa0d6eae193179e6354448676b7e206062004a887be45eb9f70a49b) |
| 18:32:59 | Ethereum | Reserve wallet bridges **1,571,000 USDC** to Monad. | [Reserve bridge out](https://eth.blockscout.com/tx/0x965779c4a6840fee04b4d995912fcd1d73d34cafed26aa57000019c5492c4e06) |
| 18:33:17 | Monad | Borrower receives approximately **1,432,473.6755 wsrUSD** from the mint-and-bridge transaction. | [wsrUSD receipt](https://monadscan.com/tx/0xabd89eab8e75e6af031488afd57fbb2d46632d9ab0c83ad661046dccd1d28c97) |
| 18:33:23 | Monad | Reserve wallet receives **1,570,842.90 USDC**, net of the **157.10 USDC** CCTP fee. | [Reserve bridge receipt](https://monadscan.com/tx/0x3dcf2a1320f9f3f9c314e9234d78bde7ddf550df71ce2c75ec430972a8e3a7f7) |
| 18:34:00 | Monad | Reserve wallet supplies **1,570,842.90 USDC back into the same Curvance USDC market**. | [Reserve resupply](https://monadscan.com/tx/0xeffdca7a026229edfd3ddbe8dfc0630eb2eb9fda24ffb898ad746f6b566f4d92) |
| 18:35:52 | Monad | Borrower deposits **1,370,000 wsrUSD** as Curvance collateral. | [Collateral deposit](https://monadscan.com/tx/0x428f0db709b92f18ffa41eda676c8c13183128c9c6724516550e0026a06bf22e) |
| 18:36:21 | Monad | Borrower takes another **1,420,644.4554 USDC** loan from that market. | [Borrow again](https://monadscan.com/tx/0xfa694cdd68d22b53683a931916892040c4d8b2dd05180a14ec776226defedc21) |

**Loop:** Curvance USDC -> borrower -> Reservoir mint -> wsrUSD collateral -> more borrowing. In parallel, Reservoir PSM -> reserve wallet -> the same Curvance USDC market.

The **1.571M USDC** is the verified reminted amount for this round, not fresh investor capital or the total size of all Curvance loops. The subsequent **1.4206M USDC** borrowing is not added to that total without tracing its next mint. The borrower deposited 1.37M wsrUSD, not the entire newly minted amount.

## Broader Circular Exposure

Separate from the transaction trace, the saved **September 23, 2026, 18:50 UTC** [Feather snapshot](https://app.feather.zone/research/wsrusd/) attributes the following reserve exposure to Curvance markets accepting wsrUSD collateral:

| Curvance market | Reservoir allocation | Reservoir-attributed outstanding loans |
|---|---:|---:|
| USDC against wsrUSD | $31.36M | $28.14M |
| AUSD against wsrUSD | $19.20M | $17.27M |
| **Total** | **$50.56M** | **$45.41M** |

The **$45.41M** is approximately **41.5% of the snapshot's $109.43M reserves**. It measures circular collateral exposure, not proven remint volume or expected losses. These are dated snapshot figures, not live balances; the AUSD market's exposure is not proof of an AUSD borrow-and-remint loop in this report.

Bridge legs were matched using Circle's attested message and LayerZero's source/destination record, not just similar amounts. This evidence does not establish that the borrower is owned by Reservoir or Agua.
