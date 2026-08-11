# RH-395 reproducibility audit

## Deterministic objects

The release regenerates four objects without network access:

1. `results/result.json`;
2. `results/result.schema.json`;
3. `results/dependency_manifest.json`;
4. `results/archive_verification.json`.

Stored and fresh objects must match by recursive exact type/value equality and
by sorted pretty UTF-8 bytes.  The same four SHA-256 values are required under
ordinary Python and `python -OO -B`.  This is deterministic artifact replay;
it does not claim deterministic replay of manuscript-generating language-model
activity.

## Certificate replay

- 72 rows partitioned `8+10+16+12+12+8+6`;
- 32,983 canonical bytes, SHA-256
  `31afb062208af97fddb5192bc4d6f1f4f030ad69b5a3f9b6ed1d1d9b2b1128a9`;
- fresh and false verification pass;
- 57/57 core and 45/45 result semantic mutations are rejected;
- 262,144 ordered relation pairs are scanned and 3,375 are safe;
- rigorous rational Euler-product intervals resolve every encoded comparison.

## Source replay

- 148 Git inputs are read at the frozen RH-394 and RH-375 release identities.
- Group sizes `128+8+4+8`, all four group digests, and the all-Git digest are
  exact.
- Four local remote-lock objects are checked in canonical and pretty form.
- All remote invocations report `NETWORK_DISABLED` and make zero requests.
- Rights remain `false,false,true,false`; all external PDFs remain
  nonvendored.

## Schema replay

`experiments/build_schema.py` regenerates an exact, recursively closed Draft
2020-12 schema.  The independent official `jsonschema` implementation runs
`Draft202012Validator.check_schema` and validates the stored result with zero
errors.  The custom exact-instance validator and the official validator are
both required; neither substitutes for the other.

## Archive replay

The inner manifest builder and outer verifier independently check:

- exact publication membership and all SHA-256 values;
- safe relative regular paths and complete external Git membership;
- source commits, group sizes/digests, all-Git digest, remote order, rights,
  logical count/digest, and four zero-request rows;
- frozen Stage-1 and manuscript identities;
- result and schema fresh equality plus official schema validation;
- semantic-PDF byte equality and six-payload exclusion;
- symlink, cache, bytecode, path/content sentinel, special-file, carriage
  return, EOF, and unlisted-file counters;
- exact fresh manifest/report equality and failure count zero.

Run `make archive` only after targeted normal/optimized release checks and the
single cache-free full suite.  A nonzero test, builder, verifier, PDF, log, or
hygiene gate blocks release.

## Environment boundary

The executable package requires Python 3.10 or later, `pytest==8.4.2`, and
`jsonschema==4.26.0`.  Tests set `PYTHONDONTWRITEBYTECODE=1`, use `-B`, and
disable the pytest cache provider.  No remote service, external dataset, or
source PDF is required to reproduce the finite artifacts.

Verdict: deterministic release replay is specified and executable.
