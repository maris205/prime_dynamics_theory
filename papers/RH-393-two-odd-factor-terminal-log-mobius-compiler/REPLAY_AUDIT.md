# RH-393 deterministic replay audit

## Four-object replay

The release regenerates, without network access:

1. `results/result.json`;
2. `results/result.schema.json`;
3. `results/dependency_manifest.json`;
4. `results/archive_verification.json`.

Stored and fresh objects must match by recursive exact type/value equality and
sorted pretty UTF-8 bytes. The same four SHA-256 values are required under
ordinary Python and `python -OO -B`.

## Certificate replay

- 576 rows, partitioned `512+27+8+12+9+8`;
- 117,096 canonical bytes, SHA-256
  `f109da241722796418f39708b16fa162cce0b85a6e448998d3ede593b7bd697b`;
- false and fresh verification pass;
- all 32 semantic mutations are rejected;
- result and schema exact digests are frozen by the archive.

## Source replay

- 117 Git inputs are read at the RH-392 release identity.
- The `106+8+3` group digests, all-Git digest, and logical-120 digest are
  exact.
- Three local remote-lock objects are checked in canonical and pretty form.
- Offline invocations make `0+0+0` requests.

## Archive replay

The outer verifier independently checks exact membership, safe regular paths,
SHA syntax/values, closure counts, ordered remote digests, source commit,
rights, zero-request rows, official schema validation, payload exclusion,
semantic-PDF equality, frozen hashes, and hygiene counters. Any fresh/stored
manifest difference fails closed.

Run `make archive` only after cache-free normal and optimized tests and the
three offline verifiers pass.
