# UCD Public Corpus Baseline

This repository tracks the owner-approved public UCD corpus only.

Earlier internal forensic work was broader than the public repository scope. It included material that the owner may choose to keep private or outside this repository. Those broader internal counts are not used as the public completion target and are not reproduced here.

The public reconciliation baseline is rebuilt from only material approved for publication. Every included object receives a canonical object identity, source/provenance record, version/alias relationships, and a checksum where applicable.

## Public completion gate

The public monorepo is complete only when:

- `orphan_public_items = 0`
- `unmapped_public_source_files = 0`
- `unresolved_public_duplicate_identities = 0`
- `public_historical_names_without_provenance_pointer = 0`
- `public_computational_claims_without_code_or_verifier_pointer = 0`

Owner-designated private or nonpublic work is excluded from these counters and is not represented by filenames, branch names, summaries, archive entries, or source inventories in this repository.