# UCD source recovery — first durable checkpoint

This checkpoint preserves the original sources listed in `source_manifest.json`, with exact SHA-256 checksums. Source upload and the full UCD Google Drive consolidation are continuing on this review branch.

Verify the currently preserved sources from the repository root with `python tools/verify_recovered_sources.py`. Later checkpoints extend the manifest without changing these original bytes. Compiler repairs and the consolidated mathematical exposition are maintained separately from immutable originals.
