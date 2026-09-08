# 03 — Shared Law Ledger and Provenance

The Algorithms-of-Reality branch requires one shared law ledger so every engine works against the same canonical mathematical identities.

## Canonical law object

Each law/result object should contain at least:

- canonical object ID;
- name and historical aliases;
- exact statement or executable predicate;
- domain and assumptions;
- status;
- source file/package provenance;
- proof/verifier pointer;
- result certificate pointer where computational;
- supersedes/superseded-by links;
- dependency parents and children;
- checksum/version/commit information.

## Status vocabulary

The ledger separates at least:

- `EXACT_THEOREM`
- `EXACT_IDENTITY`
- `EXACT_CONSTRUCTION`
- `EXACT_COUNTERMODEL`
- `CONDITIONAL_THEOREM`
- `PHYSICAL_PROMOTION_OPEN`
- `WORK`
- `BLOCKED`
- `FAILED_TESTED_FAMILY`
- `HISTORICAL`
- `SUPERSEDED`
- `HARNESS_ONLY`

A status update never deletes the object.

## Duplicate identity rule

Byte-identical evidence is counted once while all historical paths remain recorded. Mathematical duplicates are merged only after identity is established at the level of statement/domain/assumptions, not merely because their titles are similar.

The target invariant is

$$
\boxed{
\text{one mathematical identity}
\leftrightarrow
\text{one canonical object ID}
}
$$

with any number of source aliases and proof lenses.

## Dependency graph

For canonical objects `A` and `B`, an edge

$$
A\rightarrow B
$$

means `B` explicitly depends on `A` as a premise or construction input. This graph is used to prevent a later manuscript from importing a superseded or conditional premise as though it were current canon.

## Reuse rule

Once an object has been proved under an exact content identity, later engines should reuse the certified object rather than recompute or recount it unless a new independent verification is being deliberately added.