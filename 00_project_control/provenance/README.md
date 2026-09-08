# Provenance Registry

Every UCD object receives a stable canonical object ID, source path(s), SHA-256 where bytes are available, version lineage, branch ownership, and status (`CANON`, `ACTIVE_RESEARCH`, `HISTORICAL_BRANCH`, `FAILED_REPAIRED`).

Aliases do not create duplicate objects. Superseded objects are not deleted. Current canon links backward to the exact historical source object.