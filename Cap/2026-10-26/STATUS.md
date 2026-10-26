# Cap cUSD investigation — complete with stated limitations

Completed and verified: 2026-10-26 17:48:35 UTC / 2026-10-26 20:48:35 Europe/Istanbul.

The bounded public-data investigation is complete. [Report](cap-cusd-investigation-2026-10-26.md), [evidence guide](evidence/README.md), [verification](evidence/validation.json), and [arithmetic checks](evidence/calculation-checks.json) are saved. No onchain transactions, publication, service changes or external messages were performed.

Findings:

- Ethereum reserve book: 76,880,199.368483 USDC; booked native borrowing 56,025,760.412345; available-balance accounting 20,854,438.956138, principally Aave Ethereum plus 100,232.258645 OndoHolder. Available balance includes invested claims.
- Accrued native debt: 56,094,592.219555 USDC across 18 agents. Largest share 51.59%; top three 76.27%. One 521.38-USDC test loan has health below one.
- External Yearn Pawn debt: 6,056,474.165347 USDC against 6,392,939.735739 stcUSD. LTV 87.15%, LLTV 91.5%; lender USDC-1 yVault exposure is 32.63% of its book assets.
- Aave MegaETH stc-backed debt: 5,967,577.030991 USDm. Largest borrower owes 99.51% of all pool USDm debt; largest supplier holds 91.96% of supply. Current available USDm cash 483,220.973775. Cap's Ethereum reserve investment is a separate pool.
- Leveraged cUSD minting is proven in Yearn transactions. Aave borrowing/Morpho refinancing, native loan repayments, the M11/Safe funding and shared-signer relationship, and representative Pendle purchases/paired minting are documented. No issuer-funded external collateral lending loop was established.
- Four canonical Ethereum Pendle markets are expired. Current Morpho Cap exposure is small; restricted legacy Euler/Dolomite positions are distinguished from material venues.

Verification: 36 successful receipts checked for status and ordered decoded logs; key actual borrower/onBehalf/receiver fields asserted. Native debt totals, Aave holder balances and three complete Morpho position lists reconcile to preserved snapshots. Local report links and receipt citations checked; SHA256SUMS records final artifacts.

Limits: Cap reserve frontend/API HTTP403; no loading-zero balances used. Underlying proprietary/operator credit, FalconX credit, Ondo backing, optional legal guarantees and ultimate beneficial ownership were not independently verified. Largest Aave borrower's Ethereum USDC history is bounded to 1,000 transfers; historical fund tracing is selective, not exhaustive. Dolomite residual debt against cross-collateral was not fully reconstructed. RPC failures are retained and explicitly excluded from balance conclusions. These limits qualify the conclusions; this is not a full solvency audit or proof that no undiscovered reserve loop exists.

Observation blocks: Ethereum 26,278,245 (17:05:59 UTC / 20:05:59 Istanbul); MegaETH 30,237,747 (17:12:38 / 20:12:38). Full network and source times are in the report and evidence guide. Public snapshots were retrieved October 26, 17:06:10–17:46:25 UTC / 20:06:10–20:46:25 Istanbul. The request-date filename is not a substitute for these timestamps.

No research work remains running. Further source-of-funds or off-chain verification would be a separate expanded investigation.
