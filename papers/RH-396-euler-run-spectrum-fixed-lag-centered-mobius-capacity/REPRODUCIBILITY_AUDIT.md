# RH-396 reproducibility audit

## Deterministic release objects

The release regenerates four objects without network access:

1. `results/result.json`;
2. `results/result.schema.json`;
3. `results/dependency_manifest.json`;
4. `results/archive_verification.json`.

Stored and fresh values must match by recursive exact type/value equality and
by sorted pretty UTF-8 bytes.  The same four SHA-256 values are required under
ordinary Python and `python -OO -B`.  This is deterministic artifact replay;
it does not claim byte replay of the language-model activity that assisted
manuscript production.

## Certificate replay

- 96 rows partitioned `12+16+16+12+12+12+8+8`;
- 83,309 canonical bytes, SHA-256
  `7cc0da78ee7e47a22b357d7e8d907bc9d9879caeb82ede30709e8cb1023032ba`;
- fresh and false verification pass;
- 32/32 core, 65/65 result, and 28/28 schema mutations rejected;
- 262,144 ordered relation pairs scanned and 3,375 safe;
- only exact integers, fractions, and outward rational intervals used by the
  formal oracle.

## Source replay

- 160 Git inputs are read at the frozen RH-395 release identity.
- Group sizes `148+8+4`, all three group digests, and the all-Git digest are
  exact.
- Four local remote-lock objects are checked in canonical and pretty form.
- All remote invocations report `NETWORK_DISABLED` and make zero requests.
- Rights remain `false,false,true,false`; every external PDF remains
  nonvendored.

## Schema replay

`experiments/build_schema.py` regenerates an exact, recursively closed Draft
2020-12 schema.  The independent official `jsonschema` implementation runs
`Draft202012Validator.check_schema` and validates the stored result with zero
errors.  The custom exact-instance validator and official validator are both
required.

## Archive replay

The inner manifest builder and outer verifier independently check:

- exact publication membership and all SHA-256 values;
- safe relative regular paths and complete 160-object external membership;
- source commits, group sizes/digests, all-Git digest, remote order, rights,
  logical count/digest, and four zero-request rows;
- frozen Stage-1 and manuscript identities;
- result/schema fresh equality and official schema validation;
- semantic-PDF byte equality and six-payload exclusion;
- symlink, cache, bytecode, path/content sentinel, special-file, carriage
  return, EOF, and unlisted-file counters;
- exact fresh manifest/report equality and failure count zero.

`make archive` is run after targeted normal/optimized release checks and the
single cache-free full suite.  Any nonzero test, builder, verifier, PDF, log,
or hygiene gate blocks release.

## Environment boundary

The executable package requires Python 3.10 or later,
`pytest==8.4.2`, and `jsonschema==4.26.0`.  Tests set
`PYTHONDONTWRITEBYTECODE=1`, use `-B`, and disable the pytest cache provider.
No remote service, external dataset, or source PDF is required to reproduce
the finite artifacts.  Verdict: deterministic release replay is specified
and executable.
