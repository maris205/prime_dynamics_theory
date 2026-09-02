# Bridge B - TPC-342 independent fresh-panel reproduction

## Scope

TPC-342 is a true protocol reproduction of TPC-341 on a disjoint panel.  It
tests whether a nuisance projection learned from the nine-control class means
transfers to a control that was omitted from training.  The source, operator,
masks, controls, rank rule, and guards are locked to TPC-341; only the three
cutoff-safe windows change.

## Certified finite facts

```text
TPC342_PROJECTION_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC342_INDEPENDENT_FRESH_REPLAY = NUMERICALLY_CERTIFIED_FINITE_108_RAW_RECORDS
TPC342_IN_SAMPLE_PROJECTION = NUMERICALLY_CERTIFIED_FINITE_3_ROWS
TPC342_HOLDOUT_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_27_RECORDS
TPC342_IN_SAMPLE_RETENTION = NUMERICAL_OBSERVATION_0.270_TO_0.296
TPC342_HOLDOUT_RETENTION = NUMERICAL_OBSERVATION_0.589_TO_0.943
TPC342_CONTROL_STABILITY = REFUTED_SCOPED
TPC342_ARITHMETIC_ADVANCE = NO
TPC342_FIXED_POWER_CREDIT = 0
TPC342_SOURCE_UNIFORM_L2 = OPEN
TPC342_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC342_FULL_GATE_B = OPEN
TPC342_TWIN_PRIME_RESULT = NONE
TPC342_STATUS = NUMERICALLY_CERTIFIED_FINITE_INDEPENDENT_FRESH_HOLDOUT_REPRODUCTION
TPC342_ROUND2_CLUE = CROSS_PANEL_META_CERTIFICATE_OR_ALTERNATIVE_NUISANCE_BASIS
```

The finite positive result is that the TPC-341 protocol reproduces its
aggregate-versus-holdout split on a disjoint panel.  The finite obstruction is
again failure on all 27 held-out control tests.  Neither statement is an
arithmetic cancellation estimate.

## Local fail-closed commands

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-342-independent-fresh-holdout-reproduction/code/tpc342_independent_fresh_holdout_reproduction.py --check
python -O -B papers/tpc-342-independent-fresh-holdout-reproduction/code/tpc342_independent_fresh_holdout_reproduction.py --check
python -B papers/tpc-342-independent-fresh-holdout-reproduction/experiments/tpc342_independent_checker.py --check
python -O -B papers/tpc-342-independent-fresh-holdout-reproduction/experiments/tpc342_independent_checker.py --check
python -B papers/tpc-342-independent-fresh-holdout-reproduction/experiments/tpc342_holdout_stress.py --check
python -O -B papers/tpc-342-independent-fresh-holdout-reproduction/experiments/tpc342_holdout_stress.py --check
```

The official Session evaluator files are absent.  This local wrapper is
fail-closed and does not claim an official Route-A or Route-B pass.
