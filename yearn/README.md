# Yearn JOC access-control investigations

- [Vault and strategy permissions](./access-control-investigation-strategies.md): roles, keepers, EOA holders, and direct and indirect loss paths across the JOC snapshot.
- [Strategy auctions](./access-control-investigation-auctions.md): configured auctions, enabled assets, governors, keepers, custody, and auction-specific loss paths.

These are fixed-block assessments from November 1, 2026, not live monitoring. The auction report builds on the broader strategy report. Read their TODO sections before using a finding as a current-state claim.

## Evidence handling

Linked CSV, JSON, and HTML files are publication copies of the audit outputs. Absolute audit-server paths were normalized to `unpublished-capture/` to avoid exposing operational file locations. Raw JOC detail-page captures and verified-source downloads are not bundled; `evidence.json` retains their hashes and onchain getter provenance. Progress logs are excluded. Onchain addresses, values, and claims were not intentionally changed during publication preparation.
