# Bridge-B proof package: TPC-363 bulk persistence localization

## Scope

TPC-363 is a finite localization audit of the TPC-362 normalized literal
prime-shell operator.  It freezes origins `(313030,311166,321651)`, counts
`256,512`, shell anchors `80,128,256`, exponents `1,2`, and the four fixed
sign laws.  The certificate contains 144 law rows with true spectra.

For each row, `k=floor(N/20)` coordinates are selected in two deterministic
ways: largest normalized Schur row mass, and largest squared coordinate mass
of the principal eigenvector.  The spectral norm of each resulting principal
submatrix is recomputed.  The finite cap is the inherited working value
`0.64`.

## Finite result

```text
TPC363_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_BULK_PERSISTENCE_OBSTRUCTION
TPC363_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
TPC363_FINITE_ENVELOPE_INEQUALITIES = PROVED_EXACT_FINITE
TPC363_FIRST_Q128_FAILURE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC363_BULK_PERSISTENCE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC363_SINGLE_ROW_SPIKE_EXPLANATION = REFUTED_SCOPED_ON_DECLARED_TRIMS
TPC363_EIGENVECTOR_DELOCALIZATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC363_RENORMALIZED_REPAIR = OPEN
TPC363_GROWING_OPERATOR_BOUND = OPEN
TPC363_SOURCE_UNIFORM_L2 = OPEN
TPC363_ARITHMETIC_ADVANCE = NO
TPC363_FIXED_POWER_CREDIT = 0
TPC363_FULL_GATE_B = OPEN
TPC363_TWIN_PRIME_RESULT = NONE
```

The Q=80 control has zero original cap failures and maximum trimmed spectrum
`0.60313535281541197`.  There are six original failures at Q=128 and twelve
at Q=256; all are all-plus rows.  All 18 persist after both deletion rules.
The minimum retained spectrum is `1.1843597700033823` at Q=128 and
`0.86120283374232454` over the full failure set.  These are scoped finite
observations, not universal or asymptotic claims.

## Independent controls

The producer locks the TPC-355 base and TPC-362 parent certificate.  The
independent checker reconstructs the sieve, shell traversal, masks, signs,
eigenvectors, score rankings, and principal restrictions without importing the
producer.  The certificate stress script applies 16 structural and claim
mutations.  The local checker locks all claim-bearing files, checks the PDF
and compile log, and runs producer, independent checker, and stress in normal
and optimized modes with byte-identical stdout.  This is local finite
evidence only; the Session-named official evaluator files are absent, so no
official Route-A or Route-B pass is declared.

## Route decision

This paper closes the specific single-row/single-coordinate explanation on
the declared five-percent trims.  It does not test a new normalization and
does not advance arithmetic reassembly.  The next natural question is an
explicitly frozen renormalization or shell reweighting tested on a holdout.
