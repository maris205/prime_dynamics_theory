# Bridge-B TPC-299 — native profile budget frontier

```
TPC299_MAXIMUM_CLAIM = PROVED_EXACT_FINITE_PROFILE_BUDGET_KKT_FRONTIER_PLUS_NUMERICALLY_CERTIFIED_FINITE_NATIVE_BUDGET_OBSTRUCTION_ATLAS
TPC299_ROUTE_ADVANCE = YES_SCOPED_PROFILE_ANGLE_TO_NATIVE_BUDGET_FRONTIER
TPC299_PROFILE_BUDGET_KKT_FRONTIER = PROVED_EXACT_FINITE
TPC299_NESTED_BUDGET_MONOTONICITY = PROVED_EXACT_FINITE
TPC299_WEIGHTED_HALF_RMS_BUDGET_FLOOR = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_9E_MINUS_5
TPC299_WEIGHTED_HALF_RMS_BUDGET_MID_FLOOR = NUMERICALLY_CERTIFIED_FINITE_15_OF_18_ABOVE_5E_MINUS_4
TPC299_WEIGHTED_HALF_RMS_BUDGET_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_14_OF_18_ABOVE_1E_MINUS_3
TPC299_WEIGHTED_FULL_PREFIX_BUDGET_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_11_OF_18_ABOVE_1E_MINUS_3
TPC299_PLUS_HALF_RMS_BUDGET_CEILING = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_BELOW_1E_MINUS_4
TPC299_WEIGHTED_PLUS_BUDGET_GAP = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_20
TPC299_PROFILE_BUDGET_GROWTH = OPEN
TPC299_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC299_FIXED_POWER_CREDIT = 0
TPC299_FULL_GATE_B = OPEN
TPC299_TWIN_PRIME_RESULT = NONE
TPC299_ROUND2_CLUE = TEST_BUDGET_CONSTRAINED_PROFILE_FRONTIER_ON_GROWING_SHELLS_AND_SOURCE_NORMALIZATION
```

TPC-299 is the native-source continuation of TPC-298.  For
`V_k=A^T U_k` and `M_k=U_k^T U_k`, it introduces

```
B_(k,tau)(b) = min { c^T M_k c : ||V_k c-b|| <= tau ||b|| }.
```

The exact KKT path is

```
c_lambda = (V_k^T V_k + lambda M_k)^(-1)V_k^T b.
```

At normalized RMS `tau=1/2`, the weighted target's minimum threshold budget
is above `9e-5 ||beta||^2` on all 18 rows, above `1e-3` on 14 rows, and
above `1e-3` on 11 rows even at the full available prefix.  The positive
control is below `1e-4` on all rows, with a threshold-budget gap above 20.

The source profile family, cutoff ladder, finite grid, and normalization are
declared finite modeling choices.  The Session-named Route-A/Route-B
evaluator files are absent from this checkout, so this bridge records the
local fail-closed validation path only.

## Local validation path

```
export PYTHONDONTWRITEBYTECODE=1
python -B research/tpc-big-road/tpc_bridge_b_tpc299_native_profile_budget_frontier_checker.py --check
```
