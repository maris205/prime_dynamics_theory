# Bridge B - TPC-343 cross-panel shared-nuisance meta-certificate

## Scope

TPC-343 combines the TPC-341 parent panel and the TPC-342 independent fresh
panel under their locked protocol.  It compares two finite stacking models:

1. a row-block nuisance span, with one nuisance coefficient vector per row;
2. a shared nuisance span, with one coefficient vector across all six rows.

The second model is a deliberately explicit finite model comparison.  It is
not a claim that the nuisance coordinates are canonical or arithmetic noise.

## Certified finite facts

```text
TPC343_STACKED_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC343_ROW_BLOCK_META = NUMERICALLY_CERTIFIED_FINITE_6_ROW_POOLED_PROJECTION
TPC343_SHARED_COEFFICIENT_RAW = NUMERICAL_OBSERVATION_0.319_TO_0.320
TPC343_SHARED_COEFFICIENT_EQUAL_ROW = NUMERICAL_OBSERVATION_0.354_TO_0.355
TPC343_SHARED_COEFFICIENT_STABILITY = REFUTED_SCOPED
TPC343_HOLDOUT_META = NUMERICALLY_CERTIFIED_FINITE_54_RECORDS
TPC343_ARITHMETIC_ADVANCE = NO
TPC343_FIXED_POWER_CREDIT = 0
TPC343_SOURCE_UNIFORM_L2 = OPEN
TPC343_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC343_FULL_GATE_B = OPEN
TPC343_TWIN_PRIME_RESULT = NONE
TPC343_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_PANEL_META_CERTIFICATE
TPC343_ROUND2_CLUE = ALTERNATIVE_NUISANCE_BASIS_OR_PRINCIPAL_ANGLE_AUDIT
```

The row-block pooled in-sample residual retention is `0.2325429101`, below
the inherited `0.30` guard.  A single shared coefficient vector instead has
retention `0.3198013104` under raw energy weighting and `0.3549335801` after
equal-row normalization; both exceed the same guard.  The nine shared
leave-one-control-out cross-panel tests retain `0.6408306196--0.9090948298`.
These are finite model-comparison observations: they show that the strong
row-local fit does not supply a single cross-panel nuisance law.

The official Session evaluator files are absent in this checkout.  The local
Bridge-B wrapper is fail-closed and does not claim an official Route-A or
Route-B pass.

## Local commands

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-343-cross-panel-meta-certificate/code/tpc343_cross_panel_meta_certificate.py --check
python -O -B papers/tpc-343-cross-panel-meta-certificate/code/tpc343_cross_panel_meta_certificate.py --check
python -B papers/tpc-343-cross-panel-meta-certificate/experiments/tpc343_independent_checker.py --check
python -O -B papers/tpc-343-cross-panel-meta-certificate/experiments/tpc343_independent_checker.py --check
python -B papers/tpc-343-cross-panel-meta-certificate/experiments/tpc343_meta_stress.py --check
python -O -B papers/tpc-343-cross-panel-meta-certificate/experiments/tpc343_meta_stress.py --check
```

The canonical certificate is
`papers/tpc-343-cross-panel-meta-certificate/results/tpc343_certificate.json`,
and the audited manuscript is
`papers/tpc-343-cross-panel-meta-certificate/paper/paper.pdf`.
