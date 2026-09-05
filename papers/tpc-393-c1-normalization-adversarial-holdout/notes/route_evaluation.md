# TPC-393 route evaluation

The official Session evaluator files `propose.md`,
`skills/route-a-evaluator.md`, and `skills/route-b-evaluator.md` are not
present in this checkout.  The available local evidence is the proof package,
canonical certificate, independent descending-shell replay, 25-case mutation
stress, PDF diagnostics, and Bridge-B locks.

```text
ROUTE_A = NOT_EVALUATED_OFFICIALLY
ROUTE_B = OPEN
FINITE_RESULT = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ADVERSARIAL_HOLDOUT
FORECAST_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
ORIGIN_UNIFORMITY = OPEN
SPECTRAL_ENVELOPE = REFUTED_ON_DECLARED_FINITE_PANEL
SCHUR_ENVELOPE = NUMERICALLY_CERTIFIED_FINITE_SCOPED_ONLY
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
TWIN_PRIME_RESULT = NONE
```

`SPECTRAL_ENVELOPE` is deliberately qualified: 32/32 finite rows exceed the
declared $0.64$ cap, but this does not prove a growing-family theorem.  The
all-plus/alternating origin-spread split is an observation on the selected
five-origin family, not a source-uniform claim.
