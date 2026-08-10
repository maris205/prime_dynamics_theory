# RH-392 deterministic replay audit

## Four-object replay

The release regenerates four finite objects without network access:

1. `results/result.json` from `experiments/build_result.py`;
2. `results/result.schema.json` from `experiments/build_schema.py`;
3. `results/dependency_manifest.json` from `experiments/build_archive.py`;
4. `results/archive_verification.json` from `experiments/verify_archive.py`.

Stored objects must equal fresh objects by exact recursive type/value equality,
and their sorted pretty serialization must be byte-identical. The same four
SHA-256 values are required under ordinary Python and `python -OO -B`.

## Analytic-artifact replay

- The certificate is rebuilt at 220,832 canonical bytes with SHA-256
  `614297795d4d4dfeadfb5667d3e0d405d04fbe8e07e9d87a743faed9cb267a96`.
- Both false-mode and fresh-mode verification pass for the baseline.
- All 24 named semantic mutations are rejected.
- Every declared builder is forbidden in false-mode verification.
- The result and schema exact SHA-256 values are frozen in the archive.

## Source replay

- All 106 Git inputs are re-read from the RH-389 release commit and compared
  with the live workspace copies.
- The `95+8+3` group digests, all-Git digest, and logical-109 digest are exact.
- The three local remote-lock objects are rebuilt semantically and compared
  byte-for-byte with their inherited pretty copies.
- Three offline invocations make `0+0+0` requests.

## Archive replay

The outer verifier independently checks exact manifest membership, regular
non-symlink files, SHA syntax and values, closure counts, ordered remote
digests, source commit, zero-request rows, official Draft 2020-12 validation,
rights/nonvendoring, five-payload member/tree exclusion, semantic-PDF equality,
frozen hashes, and hygiene counters. A fresh manifest must equal the stored
manifest exactly; otherwise the report fails closed.

Use `make archive` only after `make test`, `make test-optimized`, and
`make remote` pass with cache creation disabled.
