# Bridge B: TPC-278 cross-scale signed-gain stability obstruction

TPC-278 is the hostile continuation of TPC-277.  It retains the same literal
source, beta weights, masks, deleted diagonal, four actual source packets,
and rank-three Haar projection.  Only the finite prime-shell endpoint `Q` or
clock `H` is varied, with `s=2` and the local comparison cutoff fixed.

For `D=sum_j||V_j||^2`, `G=||sum_jV_j||^2`, and
`E=sum_{j<k}Re<V_j,V_k>`, the exact identity `G-D=2E` gives

```text
E<0 <=> D/G>1,
E>0 <=> D/G<1.
```

The exact rational twelve-row replay has eight negative and four positive
cross terms.  It certifies four fixed-scale sign flips:

```text
(128,Q=5)->(128,Q=6),
(192,Q=6)->(192,Q=7),
(256,Q=5)->(256,Q=6),
(192,H=29)->(192,H=32).
```

The `N=192,Q=6` natural row has `D/G` near `1.006248`, while the `Q=7`
perturbation has `D/G` near `0.866928`.  This closes only the finite
stability shortcut.  It does not claim an asymptotic counterexample or a
failure of the intended growing schedule.

```text
TPC278_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_GAIN_STABILITY_OBSTRUCTION
TPC278_ROUTE_ADVANCE = YES_SCOPED_SIGNED_GAIN_STABILITY_OBSTRUCTION
TPC278_LITERAL_SOURCE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC278_NATURAL_CONTROLS = NUMERICALLY_CERTIFIED_FINITE_3_ROWS
TPC278_SHELL_CLOCK_FLIPS = NUMERICALLY_CERTIFIED_FINITE_4_FLIPS
TPC278_SIGNED_GAIN_STABILITY = REFUTED_SCOPED_FINITE
TPC278_SOURCE_LEVEL_UNIFORMITY = OPEN_ASYMPTOTIC
TPC278_FIXED_POWER_CREDIT = 0
TPC278_ARITHMETIC_ADVANCE = NO
TPC278_L2 = NONE
TPC278_FULL_GATE_B = OPEN
TPC278_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC278_TWIN_PRIME_RESULT = NONE
TPC278_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_GAIN_STABILITY_OBSTRUCTION
TPC278_ROUND2_CLUE = FORMULATE_MINIMAL_SOURCE_LEVEL_COHERENCE_TO_GAIN_THEOREM
```

Strongest positive result: exact twelve-row source census and four sign
flips.  Strongest obstruction: Q/H interface changes can reverse the signed
gain.  Open theorem: a schedule-specific source-level estimate for `G/D`.
The Session-named evaluator files are absent; the local proof package,
certificate, independent replay, stress audit, and checker are the
fail-closed fallback.
