# Bridge B — TPC-335 twin-isolated source norm

## Scope

TPC-335 applies the four TPC-334 coordinate masks to the full residual source
on origins `42001,44001` and scales `2048,4096,8192`.  The masked vectors form
an exact finite norm partition.

## Certified finite facts

```text
TPC335_MASK_NORM_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC335_SIX_WINDOW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_WINDOWS
TPC335_TWIN_RESIDUAL_SHARE = NUMERICALLY_CERTIFIED_FINITE_9.6_TO_12.3_PERCENT
TPC335_BACKGROUND_RESIDUAL_SHARE = NUMERICALLY_CERTIFIED_FINITE_67.1_TO_69.1_PERCENT
TPC335_TWIN_AMPLIFICATION = NUMERICALLY_CERTIFIED_FINITE_1.70_TO_1.78
TPC335_ARITHMETIC_ADVANCE = NO
TPC335_FIXED_POWER_CREDIT = 0
TPC335_SOURCE_UNIFORM_L2 = OPEN
TPC335_FULL_GATE_B = OPEN
TPC335_TWIN_PRIME_RESULT = NONE
TPC335_STATUS = NUMERICALLY_CERTIFIED_FINITE_TWIN_ISOLATED_SOURCE_NORM
TPC335_ROUND2_CLUE = TEST_TWIN_ISOLATED_AND_BACKGROUND_SIGNED_GRAM_RESPONSES
```

The twin residual share is larger than its raw cross-term share, but the
non-twin background remains the largest residual component on every row.

## Local fallback commands

```bash
python -B papers/tpc-335-twin-isolated-source-norm/code/tpc335_twin_isolated_source_norm.py --check
python -O -B papers/tpc-335-twin-isolated-source-norm/code/tpc335_twin_isolated_source_norm.py --check
python -B papers/tpc-335-twin-isolated-source-norm/experiments/tpc335_independent_checker.py --check
python -B papers/tpc-335-twin-isolated-source-norm/experiments/tpc335_norm_stress.py --check
```

The official Session evaluator files are absent; this is a local fail-closed
fallback only.
