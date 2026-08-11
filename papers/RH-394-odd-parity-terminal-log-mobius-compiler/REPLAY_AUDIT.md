# RH-394 deterministic artifact replay audit

## Four-object replay

The release regenerates, without network access:

1. `results/result.json`;
2. `results/result.schema.json`;
3. `results/dependency_manifest.json`;
4. `results/archive_verification.json`.

Stored and fresh objects must match by recursive exact type/value equality and
sorted pretty UTF-8 bytes. The same four SHA-256 values are required under
ordinary Python and `python -OO -B`. This is deterministic artifact replay;
it does not claim deterministic replay of manuscript-generating language-model
activity.

## Certificate replay

- 658 rows, partitioned `81+17+512+8+8+8+8+8+8`;
- 108,636 canonical bytes, SHA-256
  `3c72e7fbb74a35e8b84a1e75ed56b05ea04892a522d8b4a89c51ba21cedf8998`;
- false and fresh verification pass;
- all 32 core and 32 result semantic mutations are rejected;
- result and schema exact digests are frozen by the archive.

## Source replay

- 128 Git inputs are read at the RH-393 release identity.
- The `117+8+3` group digests, all-Git digest, and logical-132 digest are exact.
- Four local remote-lock objects are checked in canonical and pretty form.
- Offline invocations make `0+0+0+0` requests.

## Archive replay

The outer verifier independently checks exact membership, safe regular paths,
SHA syntax and values, closure counts, ordered remote digests, source commit,
rights, zero-request rows, official schema validation, payload exclusion,
semantic-PDF equality, frozen hashes, and hygiene counters. Any fresh/stored
manifest difference fails closed.

Run `make archive` only after targeted checks and the one cache-free full suite.
