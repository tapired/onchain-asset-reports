# Privacy and Evidence Handling

This repository contains reports and supporting public-chain evidence, not the research environment or account configuration.

- Operational prompts, session logs, launch scripts, server connection notes and personal archive metadata were removed from the publishable folder. An unmodified private backup is retained outside the repository.
- HTTP error bodies containing requester network metadata were replaced with explicit redaction notices. HTTP status, request URL and observation time were retained where available.
- Absolute home-directory prefixes in saved metadata were normalized. Some originated in third-party contract compilation metadata, not the report author's machine.
- Transaction hashes, contract addresses, balances and research findings were not intentionally changed.
- The Cap evidence checksum manifest was regenerated after redaction. It verifies the sanitized files, not the original server bytes. The original manifest is retained only in the private backup.

## Checks

`node scripts/privacy-check.mjs` checks Git-visible files, including untracked non-ignored files. `--staged` reads the exact staged blobs used by a commit. The check rejects common private paths, credentials, operational filenames and identifiers from an optional private local denylist. Personal denylist entries are not stored in this repository.

The repository-local Git identity uses the maintainer's chosen public pseudonym. Author and committer names and emails are visible in published commits; the file-content checker does not anonymize Git metadata. Signing remains disabled locally to avoid unintentionally attaching a personal signing identity.

These measures remove detected identifiers, but cannot guarantee anonymity. Publishing through a personal hosting account, reusing an already-public report, screenshots, external links, future commits, or forcibly adding ignored files can still reveal identity. A Git hook is an additional check, not a security boundary.
