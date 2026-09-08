# Manifests

Whole-project manifests live here: source-file inventory, object-ID registry, branch assignment, SHA-256 ledger, generated-artifact ledger, missing/unmounted-source list, and migration status.

The master reconciliation manifest should be machine-readable (CSV/JSON) and support the terminal checks `orphan_items=0`, `unmapped_source_files=0`, and `unresolved_duplicate_identities=0`.