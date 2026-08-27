# Bridge B: TPC-272 correlation-margin budget

TPC-272 is the direct analytic continuation of the finite phase--radius
decoupling audit in TPC-271.  It does not alter the literal V59 operator.  It
extracts the missing quantitative coordinate

```text
m = |C_perp|/R,
m^6 = Xi_C/Xi,
Xi/Xi_C = m^(-6).
```

## New theorem edge

For `E0=5/3` and `E*=1997/1200`, assume source-level hypotheses

```text
|C_perp(x)| <= A x^(E0-sigma+epsilon),
m(x) >= b x^(-eta-epsilon), eta>=0.
```

Then `R=|C_perp|/m` and

```text
|C_perp|+R <= A(1+b^(-1)) x^(E0-sigma+eta+2 epsilon).
```

Thus the strict endpoint payment is `sigma-eta>1/400`.  The exact
two-dimensional witness

```text
w=(sqrt(W),0),
g=sqrt(G)*(-m,sqrt(1-m^2))
```

has negative phase for every `0<m<=1`, proving that sign alone cannot imply a
positive margin lower bound.

## Finite audit

The producer reads the frozen TPC-271 certificate and performs positive
rational interval division.  Nine rows and four dyadic records are retained.
At `96->192`, the margin sixth-power ratio is below `(1/32)^6` while the phase
sign remains `NEGATIVE_REAL_AXIS`; at `192->384` it is above `4^6`.  These are
finite diagnostics and do not pay fixed-power credit.

```text
TPC272_MAXIMUM_CLAIM = PROVED_CONDITIONAL_CORRELATION_MARGIN_TO_RADIUS_BUDGET_COMPILER
TPC272_ROUTE_ADVANCE = YES_SCOPED_CONDITIONAL_MARGIN_BUDGET_AND_FINITE_AUDIT
TPC272_CONDITIONAL_BUDGET_COMPILER = PROVED_CONDITIONAL
TPC272_MARGIN_IDENTITY = PROVED_EXACT_FINITE
TPC272_SHARP_CONVERSE = PROVED_EXACT
TPC272_FINITE_MARGIN_AUDIT = NUMERICALLY_CERTIFIED
TPC272_SOURCE_LEVEL_MARGIN = OPEN_ASYMPTOTIC
TPC272_SOURCE_LEVEL_SIGNED_SCALAR = OPEN_ASYMPTOTIC
TPC272_FIXED_POWER_CREDIT = 0
TPC272_ARITHMETIC_ADVANCE = NO
TPC272_L2 = NONE
TPC272_FULL_GATE_B = OPEN
TPC272_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC272_TWIN_PRIME_RESULT = NONE
TPC272_STATUS = PROVED_CONDITIONAL_CORRELATION_MARGIN_TO_RADIUS_BUDGET_COMPILER
TPC272_ROUND2_CLUE = AUDIT_SOURCE_LEVEL_MARGIN_LOWER_BOUND_BEFORE_ANY_PHASE_PROMOTION
```

The Session-named `propose.md` and evaluator files are absent in this
checkout.  The project proof package, theorem ledger, certificate, independent
checker, stress audit, and `AGENTS.md` provide the fail-closed local fallback.
