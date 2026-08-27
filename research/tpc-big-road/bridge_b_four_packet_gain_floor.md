# Bridge B: TPC-277 four-packet gain floor and source-level attack

TPC-277 is the direct continuation of TPC-276's request for a source-level
signed-gain lower bound.  It freezes the TPC-268 literal source and the actual
four packet decomposition of TPC-275.  For four packets

```text
D=sum_j ||V_j||^2,  G=||sum_j V_j||^2,  r=D/G,
E=sum_{j<k} Re<V_j,V_k>.
```

The exact geometric identities are `G=D+2E`, `G<=4D`, and, when `E<=0`,
`G<=D`.  Thus `r>=1/4` universally and `r>=1` under the signed condition.
Writing `kappa=(D-G)/D`, one has the exact inverse coordinate
`r=(1-kappa)^(-1)`.  A positive power gain would therefore require a
near-cancellation estimate `G/D<=b^(-1)x^(-gamma)`; a sign inequality alone
cannot pay it.

The exact matrix-free source replay audits eight rows at `s=2`, including
five scales beyond the TPC-275 registry.  All eight have negative net cross
term and `r>1`; one row is below `r=101/100`.  This is a finite source
diagnostic and a scoped obstruction to a one-percent floor, not an asymptotic
counterexample.

```text
TPC277_MAXIMUM_CLAIM = PROVED_EXACT_UNIVERSAL_FOUR_PACKET_GAIN_FLOOR_PLUS_NUMERICALLY_CERTIFIED_SOURCE_SCAN
TPC277_ROUTE_ADVANCE = YES_SCOPED_SOURCE_GAIN_FLOOR_AND_FINITE_ATTACK
TPC277_UNIVERSAL_FOUR_PACKET_FLOOR = PROVED_EXACT_R>=1_OVER_4
TPC277_NONPOSITIVE_CROSS_FLOOR = PROVED_CONDITIONAL_R>=1
TPC277_CANCELLATION_COORDINATE = PROVED_EXACT_r=(1-kappa)^(-1)
TPC277_GEOMETRIC_POWER_PROMOTION = REFUTED_EXACT_BY_ORTHOGONAL_ADVERSARY
TPC277_SOURCE_SCAN = NUMERICALLY_CERTIFIED_FINITE_ALL_8_ROWS
TPC277_NATURAL_GAIN_SIGN = NUMERICALLY_CERTIFIED_FINITE_ALL_8_ROWS
TPC277_ONE_PERCENT_FLOOR = REFUTED_SCOPED_FINITE
TPC277_SOURCE_LEVEL_POWER_GAIN = OPEN_ASYMPTOTIC
TPC277_FIXED_POWER_CREDIT = 0
TPC277_ARITHMETIC_ADVANCE = NO
TPC277_L2 = NONE
TPC277_FULL_GATE_B = OPEN
TPC277_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC277_TWIN_PRIME_RESULT = NONE
TPC277_STATUS = PROVED_EXACT_UNIVERSAL_FOUR_PACKET_GAIN_FLOOR_PLUS_NUMERICALLY_CERTIFIED_SOURCE_SCAN
TPC277_ROUND2_CLUE = TEST_CROSS_SCALE_SIGNED_GAIN_STABILITY_AND_SHELL_SENSITIVITY
```

The strongest positive result is the sharp reusable geometric floor together
with an exact eight-row source replay.  The strongest obstruction is that
geometry alone has no positive power gain and the finite one-percent floor
already fails.  The next question is cross-scale stability under declared
shell and clock perturbations.  Arithmetic `L2`, full Gate B, and the
twin-prime conclusion remain open/none.  The Session-named evaluator files
are absent; the local proof/checker package is the fail-closed fallback.
