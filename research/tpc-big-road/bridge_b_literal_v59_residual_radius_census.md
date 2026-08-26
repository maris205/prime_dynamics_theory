# Bridge B V120 / TPC-267: finite literal V59 residual-radius census

Date: 2026-08-26

Status: `NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_RESIDUAL_PHASE_CENSUS`

TPC-266 left the actual V59 orthogonal residual radius and signed phase open.
TPC-267 makes the first finite physical replay of that object.  It keeps the
prime-only shell, outer (q) weight, both unit masks, deleted diagonal,
source β, and shifted-prime comparison.  The finite (P_3) is the same
three-dimensional consecutive-block Haar span used in TPC-257--266.

## Frozen finite interface

For the twelve rows in the certificate,

```text
I_N = {N/2+1,...,N}
Q < q <= 2Q, q prime
K_(H,s)(h) = (1+(h/H)^2)^(-s), s in {1,2}
beta_N(t) = Lambda(t)/log(t) - sum_(d|t,d^400<=N^133) mu(d)
w_N(u) = Lambda(u+2)-2 C_2 1_(2 does not divide u)
       * product_(p|u,p>2) (p-1)/(p-2)
```

The two displayed kernels come from explicit normalized nonnegative Fourier
profiles and are declared finite modeling choices.  (C_2) is enclosed by
the finite product through (P=50000) and the rational tail bound

```text
prod_(p>P)(1-(p-1)^(-2)) >= 1-1/(P-1).
```

No floating-point value is silently substituted for the tail.

## Exact finite split and certificate

Writing (g=A\beta_N), direct finite summation and the three orthogonal block
contrasts give

```text
C = <w,g> = C_3 + C_perp,
R^2 = ||(I-P_3)w||^2 ||(I-P_3)g||^2,
rho^2 = |C_perp|^2/R^2.
```

All non-logarithmic terms are rational.  Outward rational intervals enclose
the logarithms and (C_2); the certificate proves (R^2>0) and

```text
rho < 1/4
```

for all twelve rows.  The largest stored upper bound is `0.2320126753`.
The independent replay reproduces all rows without importing the producer.

This is a finite signed-phase contraction, not a radius estimate: (R) is
not shown to be (O(N^{5/3-δ})), the phase sector is not uniform in the
growing V59 parameters, and no fixed-power credit is paid.

```text
TPC267_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_RESIDUAL_PHASE_CENSUS
TPC267_ROUTE_ADVANCE = YES_SCOPED_FINITE_LITERAL_RESIDUAL_CENSUS
TPC267_LITERAL_MASK_OPERATOR = PROVED_EXACT_FINITE
TPC267_BETA_FORMULA = PROVED_EXACT_FINITE
TPC267_HYBRID_EULER_ENCLOSURE = PROVED_INTERVAL_FINITE
TPC267_PROJECTION_SPLIT = PROVED_EXACT_FINITE
TPC267_FINITE_RESIDUAL_RADIUS = NUMERICALLY_CERTIFIED
TPC267_FINITE_SIGNED_PHASE = NUMERICALLY_CERTIFIED
TPC267_QUARTER_CONTRACTION = NUMERICALLY_CERTIFIED_ALL_12_ROWS
TPC267_ACTUAL_V59_RADIUS = OPEN_ASYMPTOTIC
TPC267_ACTUAL_V59_PHASE = OPEN_ASYMPTOTIC
TPC267_FIXED_POWER_CREDIT = 0
TPC267_ARITHMETIC_ADVANCE = NO
TPC267_L2 = NONE
TPC267_FULL_GATE_B = OPEN
TPC267_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC267_TWIN_PRIME_RESULT = NONE
TPC267_LITERAL_PRIME_SHELL_COUNTEREXAMPLE = NONE
TPC267_STATUS = NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_RESIDUAL_PHASE_CENSUS
TPC267_ROUND2_CLUE = REPEAT_THE_CENSUS_WITH_GROWING_LOCAL_CUTOFF_AND_SMOOTH_PROFILE
```

Strongest positive result: a reproducible finite physical residual has a
strictly contracted signed correlation with the Schur radius on twelve
natural-clock rows.

Strongest obstruction: the finite ratio contains no information about the
asymptotic size of (R), and the profile/clock choices are not yet uniform.

Open theorem: prove a literal growing-(x) radius or signed-phase estimate
with effective saving strictly greater than (1/400).

Reusable structure: exact physical operator → rank-three projection split →
interval certificate for (R^2) → signed residual ratio.

The Session-named `propose.md` and route evaluator files are absent from this
checkout; the project proof package, theorem ledger, certificate and
`AGENTS.md` provide the fail-closed fallback evaluation.
