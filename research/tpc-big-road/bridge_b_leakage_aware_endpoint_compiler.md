# Bridge B: additive-leakage-aware gain and endpoint compiler

Date: 2026-08-27

TPC-280 is the minimal continuation of the exact TPC-279 deficit criterion.
It asks how a raw estimate with a multiplicative main term and an additive
leakage term can be normalized without silently assigning the leakage the
main-term exponent.

Let `X>=1`, `D>=d X^a`, and

```text
G <= B X^(-gamma) D + ell X^(a-delta),
d>0, B>=0, ell>=0, gamma>=0, delta>=0.
```

Then

```text
G/D <= B X^(-gamma) + (ell/d) X^(-delta).
```

For positive `G`, reciprocal division gives the exact two-term lower bound

```text
D/G >= [B X^(-gamma)+(ell/d)X^(-delta)]^(-1).
```

With `kappa=min(gamma,delta)` and `C=B+ell/d`, the one-exponent compiler is

```text
D/G >= C^(-1) X^kappa.
```

Combining this with the inherited exact identity `m^2=(D/G)m_D^2` gives
`eta_eff=max(0,eta_D-kappa/2)` and the strict endpoint condition
`sigma-eta_eff>1/400`.  The formal equality family
`D=dX^a`, `G=BX^(-gamma)D+ell X^(a-delta)` saturates the two-term compiler.
Thus, when `delta<gamma` and `ell>0`, the slower leakage exponent is a genuine
information-model bottleneck.

Six budget fixtures, four margin fixtures, four endpoint fixtures, and all
twelve TPC-279 parent rows are exact-rationally regenerated.  The parent
transfer preserves the 8 positive / 4 negative deficit census, but supplies no
new asymptotic or arithmetic input.

```text
TPC280_MAXIMUM_CLAIM = PROVED_CONDITIONAL_TWO_TERM_LEAKAGE_ENDPOINT_COMPILER_PLUS_NUMERICALLY_CERTIFIED_TRANSFER
TPC280_ROUTE_ADVANCE = YES_SCOPED_ADDITIVE_LEAKAGE_ENDPOINT_COMPILER
TPC280_TWO_TERM_COMPILER = PROVED_CONDITIONAL
TPC280_DOMINANT_EXPONENT = PROVED_KAPPA_EQUALS_MIN_GAMMA_DELTA
TPC280_MARGIN_COMPILER = PROVED_CONDITIONAL_ETA_EFF_EQUALS_MAX_ZERO_ETA_D_MINUS_KAPPA_OVER_2
TPC280_LEAKAGE_BOTTLENECK = PROVED_CONDITIONAL_DELTA_LT_GAMMA
TPC280_SHARPNESS = PROVED_CONDITIONAL_EQUALITY_FAMILY
TPC280_FINITE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS
TPC280_FIXED_POWER_CREDIT = 0
TPC280_ARITHMETIC_ADVANCE = NO
TPC280_L2 = NONE
TPC280_FULL_GATE_B = OPEN
TPC280_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC280_TWIN_PRIME_RESULT = NONE
TPC280_STATUS = PROVED_CONDITIONAL_TWO_TERM_LEAKAGE_ENDPOINT_COMPILER_PLUS_NUMERICALLY_CERTIFIED_TRANSFER
TPC280_ROUND2_CLUE = AUDIT_TYPED_ARITHMETIC_L2_INTERFACE_FOR_FULL_GATE_B
```

Strongest positive result: an exact two-term normalization and conditional
gain/margin endpoint compiler with a sharp equality family.  Strongest
obstruction: the slower additive leakage exponent caps the available gain
power.  Open theorem: a literal growing source decomposition with arithmetic
`L2`.  Reusable structure:
`source floor -> normalize additive term -> min-exponent compiler -> strict endpoint ledger`.

The Session-named evaluator files are absent.  The proof package, canonical
certificate, independent checker, hostile stress audit, and fail-closed checker
give the local scoped Route-B verdict.
