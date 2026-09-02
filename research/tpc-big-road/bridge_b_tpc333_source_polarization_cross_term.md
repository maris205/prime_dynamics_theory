# Bridge B — TPC-333 source polarization cross-term ledger

## Scope

TPC-333 is a source-only continuation of TPC-332.  It uses the parent-locked
finite source model on origins `42001,44001` and scales `2048,4096,8192`.
There are six source windows and four adjacent nested-scale comparisons.

## Certified finite facts

```text
TPC333_POLARIZATION_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC333_SIX_WINDOW_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_WINDOWS
TPC333_CANCELLATION_COEFFICIENT = NUMERICALLY_CERTIFIED_FINITE_0.35_TO_0.37
TPC333_KAPPA_RANGE = [0.35486589921455675, 0.36250235375855522]
TPC333_RESIDUAL_FRACTION_RANGE = [0.63749764624144467, 0.64513410078544309]
TPC333_NORMALIZED_CORRELATION_RANGE = [0.46455337638475735, 0.48443427505641973]
TPC333_NEAR_ORTHOGONALITY = REFUTED_SCOPED_FINITE_PANEL
TPC333_NEAR_TOTAL_CANCELLATION = REFUTED_SCOPED_FINITE_PANEL
TPC333_ARITHMETIC_ADVANCE = NO
TPC333_FIXED_POWER_CREDIT = 0
TPC333_SOURCE_UNIFORM_L2 = OPEN
TPC333_FULL_GATE_B = OPEN
TPC333_TWIN_PRIME_RESULT = NONE
TPC333_STATUS = NUMERICALLY_CERTIFIED_FINITE_SOURCE_POLARIZATION_LEDGER
TPC333_ROUND2_CLUE = CLASSIFY_CROSS_TERM_SUPPORT_BY_PRIME_POWER_AND_TWIN_MASK
```

The exact rational anchor is `(Lambda,b) = ((3,-2,5,1),(1,1,-1,2))`, with
norms `39`, `7`, cross term `-2`, and residual norm `50`.  The source replay's
largest identity error is `1.4551915228366852e-11`.

## Local fallback commands

```bash
python -B papers/tpc-333-source-polarization-cross-term/code/tpc333_source_polarization_cross_term.py --check
python -O -B papers/tpc-333-source-polarization-cross-term/code/tpc333_source_polarization_cross_term.py --check
python -B papers/tpc-333-source-polarization-cross-term/experiments/tpc333_independent_checker.py --check
python -B papers/tpc-333-source-polarization-cross-term/experiments/tpc333_polarization_stress.py --check
```

The Session-named official evaluator files are absent from this checkout;
this document records a local fail-closed fallback only.
