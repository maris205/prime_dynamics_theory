# Bridge B — TPC-324 source-location profile holdout

TPC-324 keeps the TPC-323 literal deleted-diagonal centered prime-shell
operator and changes only source location.  It freezes two disjoint panels:
the natural continuation and a gap-separated offset panel.  The two panels
contain 48 rows in total, with source counts 320, 640, and 1280, the same
height, shell anchors, exponents, and four declared sign laws as TPC-323.

```text
TPC324_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SOURCE_LOCATION_HOLDOUT_REPLICATION
TPC324_ROUTE_ADVANCE = YES_SCOPED_SOURCE_LOCATION_HOLDOUT_REPLICATION
TPC324_SOURCE_LOCATION_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_48_ROWS_2_PANELS
TPC324_ALL_PLUS_PROFILE_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_48_OF_48
TPC324_PER_PANEL_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_24_OF_24_EACH
TPC324_ALTERNATIVE_PROFILE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_48_ROWS
TPC324_TRANSLATION_COVARIANCE = PROVED_EXACT_FINITE_CONDITIONAL
TPC324_ARITHMETIC_ADVANCE = NO
TPC324_FIXED_POWER_CREDIT = 0
TPC324_FULL_GATE_B = OPEN
TPC324_TWIN_PRIME_RESULT = NONE
TPC324_STATUS = NUMERICALLY_CERTIFIED_FINITE_SOURCE_LOCATION_HOLDOUT_REPLICATION
TPC324_ROUND2_CLUE = TEST_HOLDOUT_SCALE_LADDER_OR_SOURCE_NATIVE_ARITHMETIC_L2
```

## Evidence

The exact covariance lemma says that a shift divisible by every prime in a
fixed shell preserves the literal block up to coordinate relabeling.  The
selected gap offset changes at least one active residue mask, so the finite
replication is not merely that covariance identity.  The producer uses three
accumulation/spectral paths; the independent checker rebuilds both panels in
reverse `einsum` order and checks metrics and outward intervals.  The stress
suite checks disjointness, covariance, nontrivial residue change, profile
geometry, and metric symmetry.

The finite census is all-plus `48/48` (and `24/24` on each panel); the
alternative majorizing/mixed counts are `34/14`, `42/6`, and `36/12`.
The minimum all-plus interior-prefix lower endpoint is
`1.647473532339078e-05`.

This is a local fail-closed record.  The Session-named `propose.md` and
official Route-A/Route-B evaluator files are absent from the checkout, so no
official evaluator pass is claimed.  No source-native arithmetic (L^2),
canonical arithmetic sign, asymptotic power saving, or twin-prime result is
asserted.
