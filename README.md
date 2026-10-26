# Onchain Asset Reports

Public-data research on asset backing, credit exposure, leverage and circular funding. Findings distinguish verified transactions from inferences and unverified ownership claims.

## 3Jane

- [USD3 / sUSD3 investigation, October 23, 2026](3Jane/3jane-usd3-investigation-2026-10-23.md)
- [Supporting evidence snapshot](3Jane/3jane-evidence-2026-10-23.json)

## Reservoir

- [Curvance circular-funding report](Reservoir/reservoir-recursive-curvance.md)
- [Dolomite borrow-and-remint report](Reservoir/reservoir-recursive.md)

These are historical September 2026 reports, not refreshed October findings.

## Cap

Research requested October 26, 2026: https://cap.app/vault/reserves/cUSD

- [cUSD / stcUSD investigation, October 26, 2026](Cap/2026-10-26/cap-cusd-investigation-2026-10-26.md)
- [Evidence guide and transaction ledger](Cap/2026-10-26/evidence/README.md)
- [Research status and limitations](Cap/2026-10-26/STATUS.md)

## Privacy and Verification

Reports are dated snapshots, not live monitoring or full solvency audits. Operational logs, machine details and personal download metadata are excluded. Some evidence has been privacy-redacted; see [PRIVACY.md](PRIVACY.md) before treating files as byte-for-byte original API responses.

Run `node scripts/privacy-check.mjs` before sharing. The local pre-commit hook checks staged content. Enable it in another clone with `git config core.hooksPath .githooks`. Review your Git author identity and hosting-account visibility separately before publishing.
