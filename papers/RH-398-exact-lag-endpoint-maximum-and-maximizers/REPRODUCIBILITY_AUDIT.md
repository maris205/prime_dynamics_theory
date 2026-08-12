# RH-398 reproducibility audit

## Deterministic objects

The release regenerates five deterministic layers:

1. the 72-row finite certificate, 36,635 canonical bytes, SHA-256
   `d47de091a8fe5a134ba4bbf8ac4689f53b54786d45dc3bfc7061c99b46bea741`;
2. `results/result.json`, 187,434 pretty bytes and 116,612 canonical bytes;
3. `results/result.schema.json`, 961,955 pretty bytes and 325,778 canonical
   bytes;
4. the exact 41-member publication manifest;
5. the outer archive-verification report.

Normal and `python -OO` executions reproduce all stored machine objects
byte-for-byte.  Each complete test mode collects and passes 75 tests.  The
official `jsonschema` 4.26.0 Draft 2020-12 validator checks the schema and
accepts the stored result with zero errors.  Local recursive validation
remains the exact-type, exact-order, closed-topology gate.

## Finite checks and attacks

The certificate partitions 72 rows as `12+12+12+12+8+8+4+4`.  It checks the
complete four-branch deletion-loss formula, local collision-level order,
finite CRT product and telescope, strict exact-run cylinders, maximizer
partition, complement sequence, quantitative gap, joint endpoint, and claim
firewalls.

All 66 core, 44 result, and 32 schema semantic mutations are distinct and
rejected.  False validators are anchored by canonical and order-sensitive
pretty seals plus recursive exact JSON types.  Coordinated semantic,
nested-order, tuple/list, helper-rebinding, global-rebinding, wrong-producer,
and optimized-mode attacks fail closed.  Test modules contain no bare
`assert` statements.

## Source and offline replay

The source closure freezes 184 Git blobs in groups `172+8+4`, four ordered
remote logical locks, and 188 logical inputs.  Its all-Git digest is
`e7341caa25f0787a2e48a4d9c156e0d785b6c2a5516172bdfb25c2ac45377ea8`;
its logical digest is
`4cc752fb7baae977bb15a9420101c5ed37727b1f3f7eecf72afce9dec3c73b13`.
Each remote replay reports `NETWORK_DISABLED`, `network_opt_in=false`, and
exact integer `requests_made=0`.  No remote PDF or source archive is required.

## Release commands and hygiene

With `PYTHONDONTWRITEBYTECODE=1`, run `make result`, `make schema`, normal and
optimized tests with the cache provider disabled, `make remote`, `make pdf`,
and `make archive`.  The manifest hard-gates all 41 publication members, the
two release records, frozen hashes, source closure, rights, payload exclusion,
semantic-PDF equality, and zero counts for symlinks, cache directories,
bytecode, sentinels, carriage returns, EOF defects, unlisted regular files,
and special paths.

The executable artifacts and frozen publication files support byte-level
replay.  The mathematical terminal limits remain theorems, not computational
experiments.  AI-assisted prose generation is not claimed to be
byte-reproducible; the released prose is auditable through its frozen hash,
not through a deterministic model replay guarantee.
