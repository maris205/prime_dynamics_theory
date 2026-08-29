# Bridge-B TPC-306 - two-way operator/target interaction

    TPC306_MAXIMUM_CLAIM = PROVED_EXACT_TWO_WAY_LOG_BUDGET_DECOMPOSITION_AND_DOMINANCE_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_OPERATOR_TARGET_INTERACTION_ATLAS
    TPC306_ROUTE_ADVANCE = YES_SCOPED_TWO_WAY_INTERACTION_DECOMPOSITION
    TPC306_LOG_DECOMPOSITION = PROVED_EXACT_FINITE
    TPC306_SQUARED_DOMINANCE_IDENTITY = PROVED_EXACT_FINITE
    TPC306_ROW_SCALING_INVARIANCE = PROVED_EXACT_FINITE
    TPC306_DECOMPOSITION_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_CASES_54_ROWS
    TPC306_TARGET_MAIN_DOMINANCE = NUMERICALLY_CERTIFIED_FINITE_12_OF_18
    TPC306_INTERACTION_DOMINANCE = NUMERICALLY_CERTIFIED_FINITE_6_OF_18
    TPC306_MIDDLE_TARGET_MAIN = NUMERICALLY_CERTIFIED_FINITE_5_OF_6
    TPC306_MIDDLE_SAME_PREFIX_TARGET_MAIN = NUMERICALLY_CERTIFIED_FINITE_3_OF_3
    TPC306_RATIO_GAP = NUMERICALLY_CERTIFIED_FINITE_MAIN_LT_0_88_INTERACTION_GT_1_2
    TPC306_CAUSAL_IDENTIFICATION = OPEN_COMMON_AMBIENT_HOLDOUT
    TPC306_UNIFORM_ASYMPTOTIC_BUDGET = OPEN
    TPC306_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
    TPC306_FIXED_POWER_CREDIT = 0
    TPC306_FULL_GATE_B = OPEN
    TPC306_TWIN_PRIME_RESULT = NONE
    TPC306_STATUS = PROVED_EXACT_TWO_WAY_LOG_BUDGET_DECOMPOSITION_AND_DOMINANCE_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_OPERATOR_TARGET_INTERACTION_ATLAS
    TPC306_ROUND2_CLUE = TEST_COMMON_AMBIENT_UNION_SHELL_COMPLETIONS_AND_INTERACTION_STABILITY_BEFORE_ANY_GROWING_TARGET_PREFERENCE_CLAIM

TPC-306 takes the four positive budget cells from the TPC-305 fixed-operator
target-swap protocol and puts operator identity in the first index and target
identity in the second.  With

```text
B_LL, B_LR
B_RL, B_RR
```

the two target-switch effects are
`d_L=log(B_LR/B_LL)` and `d_R=log(B_RR/B_RL)`.  Their mean and half-difference
are `m=(d_L+d_R)/2` and `i=(d_L-d_R)/2`, with the exact identity
`m^2-i^2=d_L*d_R`.  Therefore same-sign row effects are target-main dominant,
whereas opposite-sign effects are operator-interaction dominant.

The locked finite replay contains 18 parent cases and 54 normalizer-level
decomposition rows.  It certifies target-main dominance in 12/18 cases and
interaction dominance in 6/18, with no unresolved case.  At the central
`Q=60->70` transition the split is 5/6 versus 1/6; all 3/3 inherited
same-prefix cases are target-main dominant.  The finite ratio margins are
`|i|/|m|<0.88` in every main-dominant row and `|i|/|m|>1.2` in every
interaction-dominant row.

This is a scoped structural and numerical advance.  It does not identify a
causal target effect, because the rows still use different physical operators
and shell-specific off-overlap completions.  It proves no arithmetic `L2`
estimate, fixed-power saving, full Gate-B theorem, or twin-prime result.  The
Session-named `propose.md` and Route-A/Route-B evaluator files are absent from
this checkout; the project proof package, parent-locked certificate,
independent replay, stress suite, PDF audit, and this checker are the local
fail-closed validation path.
