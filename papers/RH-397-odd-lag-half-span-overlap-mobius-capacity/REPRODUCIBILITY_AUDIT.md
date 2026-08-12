# RH-397 reproducibility audit

## Deterministic objects

The release regenerates four exact JSON objects:

1. the 72-row finite certificate, 24,297 canonical bytes, SHA-256
   `23f714236b53c2b89caa72b53f8139cfeab74cd07132082061c3ab0dfc048697`;
2. `results/result.json`, 151,768 pretty bytes and 105,495 canonical bytes;
3. `results/result.schema.json`, 670,920 pretty bytes and 257,468 canonical
   bytes;
4. the publication manifest and its outer verification report.

Normal and `python -OO` executions must reproduce the stored result and schema
byte-for-byte.  The official `jsonschema` 4.26 Draft 2020-12 validator checks
the schema itself and reports zero instance errors.  Local recursive validation
remains the primary exact-type, exact-order, closed-topology gate.

## Finite checks and attacks

The certificate partitions 72 rows as `10+10+12+12+12+12+4`.  It enumerates
512 ternary relations and all 262,144 ordered pairs, reproducing exactly
61,440 safe and 200,704 unsafe pairs, flag counts `16,48,48,400`, and rectangle
sizes `4,6,6,9`.  It checks collision branches, phase translation, edge gain,
rising-set/weighted-DP equivalence, reflection, odd-clock CRT cases, and five
formal coefficient controls.

All 60 core, 78 result, and 32 schema semantic mutations are distinct and
rejected.  False validators are independently anchored by canonical and
order-sensitive pretty seals plus recursive exact JSON types; coordinated
semantic, nested-order, tuple/list, helper-rebinding, and optimized-mode
attacks fail closed.  Test modules contain no bare `assert` statements.

## Source and offline replay

The source closure freezes 172 Git blobs in groups `160+8+4`, four ordered
remote logical locks, and 176 logical inputs.  Its all-Git digest is
`b3f5688380762a4e3c27d512311f4c0d22173c434cc40459fc77bb3eb87fb5c4`;
its logical digest is
`e9588b58f75e02e31ba5ffb279aea267074ec72f717afa84670f320d6c1030e0`.
Each remote replay reports `NETWORK_DISABLED`, `network_opt_in=false`, and
exact integer `requests_made=0`.  No remote PDF or source archive is required.

## Release commands and hygiene

With `PYTHONDONTWRITEBYTECODE=1`, run `make result`, `make schema`, normal and
optimized tests, `make remote`, `make pdf`, and `make archive`.  Cache-provider
creation is disabled for pytest.  The manifest hard-gates all 41 publication
members, the two release records, frozen hashes, source closure, rights,
payload exclusion, semantic-PDF equality, and zero counts for symlinks, cache
directories, bytecode, sentinels, carriage returns, EOF defects, unlisted
regular files, and special paths.

The executable artifacts reproduce finite identities and detect drift.  They
are not the analytic proof of the terminal limits.
