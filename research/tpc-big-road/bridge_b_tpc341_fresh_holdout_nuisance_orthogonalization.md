# Bridge B - TPC-341 fresh holdout nuisance orthogonalization

## Scope

TPC-341 tests whether a nuisance projection learned from the nine-control
class means transfers to a control that was omitted from training.  It uses
three fresh, non-overlapping, cutoff-safe windows and retains the same source,
operator, masks, and control orbit as TPC-340.

## Certified finite facts

```text
TPC341_PROJECTION_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC341_FRESH_HOLDOUT_REPLAY = NUMERICALLY_CERTIFIED_FINITE_108_RAW_RECORDS
TPC341_IN_SAMPLE_PROJECTION = NUMERICALLY_CERTIFIED_FINITE_3_ROWS
TPC341_HOLDOUT_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_27_RECORDS
TPC341_IN_SAMPLE_RETENTION = NUMERICAL_OBSERVATION_0.201_TO_0.256
TPC341_HOLDOUT_RETENTION = NUMERICAL_OBSERVATION_0.444_TO_0.890
TPC341_CONTROL_STABILITY = REFUTED_SCOPED
TPC341_ARITHMETIC_ADVANCE = NO
TPC341_FIXED_POWER_CREDIT = 0
TPC341_SOURCE_UNIFORM_L2 = OPEN
TPC341_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC341_FULL_GATE_B = OPEN
TPC341_TWIN_PRIME_RESULT = NONE
TPC341_STATUS = NUMERICALLY_CERTIFIED_FINITE_FRESH_HOLDOUT_NUISANCE_ORTHOGONALIZATION
TPC341_ROUND2_CLUE = INDEPENDENT_REPRODUCTION_OR_FREEZE_NUISANCE_PROJECTION
```

The finite positive result is aggregate mean removal; the finite obstruction
is its failure on all 27 held-out control tests.  Neither statement is an
arithmetic cancellation estimate.

## Local fail-closed commands

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-341-fresh-holdout-nuisance-orthogonalization/code/tpc341_fresh_holdout_nuisance_orthogonalization.py --check
python -O -B papers/tpc-341-fresh-holdout-nuisance-orthogonalization/code/tpc341_fresh_holdout_nuisance_orthogonalization.py --check
python -B papers/tpc-341-fresh-holdout-nuisance-orthogonalization/experiments/tpc341_independent_checker.py --check
python -O -B papers/tpc-341-fresh-holdout-nuisance-orthogonalization/experiments/tpc341_independent_checker.py --check
python -B papers/tpc-341-fresh-holdout-nuisance-orthogonalization/experiments/tpc341_holdout_stress.py --check
python -O -B papers/tpc-341-fresh-holdout-nuisance-orthogonalization/experiments/tpc341_holdout_stress.py --check
```

The official Session evaluator files are absent.  This local wrapper is
fail-closed and does not claim an official Route-A or Route-B pass.
