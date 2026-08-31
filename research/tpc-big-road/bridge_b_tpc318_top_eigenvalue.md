# Bridge B — TPC-318 finite top-eigenvalue audit

This bridge carries a direct finite spectral-radius readout of the same
literal deleted-diagonal prime-shell operator used by TPC-317.  It is a scoped
diagnostic bridge, not an official Route-A or Route-B evaluator; the
Session-named evaluator files are absent from this checkout.

```text
TPC318_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_TOP_EIGENVALUE_AUDIT
TPC318_ROUTE_ADVANCE = YES_SCOPED_TOP_EIGENVALUE_READOUT
TPC318_TOP_EIGENVALUE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
TPC318_TOP_EIGENVALUE_DECREASE = NUMERICALLY_CERTIFIED_FINITE_16_OF_16
TPC318_DUAL_SOLVER_AGREEMENT = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
TPC318_RESIDUAL_AUDIT = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
TPC318_NEAR_DEGENERACY = NUMERICALLY_CERTIFIED_FINITE_CENSUS
TPC318_NORMALIZED_TREND = NUMERICAL_OBSERVATION_FINITE_ONLY
TPC318_UNNORMALIZED_POWER = OPEN
TPC318_CLUSTERED_EIGENSPACE = OPEN
TPC318_ARITHMETIC_CANCELLATION = OPEN
TPC318_ARITHMETIC_ADVANCE = NO
TPC318_FIXED_POWER_CREDIT = 0
TPC318_FULL_GATE_B = OPEN
TPC318_TWIN_PRIME_RESULT = NONE
TPC318_ROUND2_CLUE = AUDIT_THE_TOP_EIGENSPACE_CLUSTER_AND_NORMALIZATION_LAW_BEFORE_ANY_ARITHMETIC_CANCELLATION_PROMOTION
```

## Scope

The certificate covers `X=640,1280,2560`, `Q={24,36,54,80}`, and `s={1,2}`.
It uses forward/reverse shell accumulation, a symmetric top-two eigensolver,
an independent full `eigvalsh` scalar path, and a finite Weyl perturbation
guard with the safe literal-entry bound `|K|<=160`.

The positive result is a finite normalized top-eigenvalue decrease.  The
obstruction is equally important: 10/24 rows have relative top gap below
`0.01` (minimum about `0.001704`), and normalization by source count does not
pay an unnormalized power saving.  No arithmetic reassembly or endpoint
theorem is asserted.
