# Bridge B — TPC-334 cross-term support ledger

## Scope

TPC-334 is the source-support continuation of TPC-333.  It retains the two
origins `42001,44001`, three scales `2048,4096,8192`, and the finite cutoff
`50000`, and partitions the nonnegative cross term
`sum_t Lambda(t+2)b(t)`.

## Certified finite facts

```text
TPC334_SUPPORT_PARTITION = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC334_SIX_WINDOW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_WINDOWS
TPC334_TWIN_SUPPORT_SHARE = NUMERICALLY_CERTIFIED_FINITE_5.4_TO_7.2_PERCENT
TPC334_NON_TWIN_BACKGROUND = NUMERICALLY_CERTIFIED_FINITE_92.8_TO_94.5_PERCENT
TPC334_PRIME_POWER_SHARE = NUMERICALLY_CERTIFIED_FINITE_0_TO_0.286_PERCENT
TPC334_TWIN_CENSUS = BELOW_0.10_IN_6_OF_6_WINDOWS
TPC334_BACKGROUND_CENSUS = ABOVE_0.90_IN_6_OF_6_WINDOWS
TPC334_ARITHMETIC_ADVANCE = NO
TPC334_FIXED_POWER_CREDIT = 0
TPC334_SOURCE_UNIFORM_L2 = OPEN
TPC334_TWIN_PRIME_RESULT = NONE
TPC334_FULL_GATE_B = OPEN
TPC334_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_TERM_SUPPORT_LEDGER
TPC334_ROUND2_CLUE = ISOLATE_TWIN_MASK_OR_COMPENSATED_SOURCE_BEFORE_OPERATOR_REASSEMBLY
```

The support classes are twin prime, non-twin prime shift, higher prime power,
and zero support.  Their finite mass partition is independently replayed;
the dominant class is the odd composite predecessor of a prime `t+2`.

## Local fallback commands

```bash
python -B papers/tpc-334-cross-term-support-ledger/code/tpc334_cross_term_support_ledger.py --check
python -O -B papers/tpc-334-cross-term-support-ledger/code/tpc334_cross_term_support_ledger.py --check
python -B papers/tpc-334-cross-term-support-ledger/experiments/tpc334_independent_checker.py --check
python -B papers/tpc-334-cross-term-support-ledger/experiments/tpc334_support_stress.py --check
```

The official Session evaluator files are absent; this is a local fail-closed
fallback and not an official Route-A/Route-B pass.
