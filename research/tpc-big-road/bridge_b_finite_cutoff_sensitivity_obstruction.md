# Bridge B V121 / TPC-268: finite cutoff-sensitivity obstruction

Date: 2026-08-26

Status: `NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_CUTOFF_SENSITIVITY_OBSTRUCTION`

TPC-267 found a finite quarter contraction for a literal V59 residual at a
coarse local comparison cutoff. TPC-268 keeps the physical prime shell,
outer q weight, both unit masks, deleted diagonal, beta source, kernel
operator, and rank-three projection fixed, then varies only declared finite
interface parameters. The resulting matched control/perturbation pairs give
a strict finite obstruction to a universal quarter-sector statement.

## Frozen finite object and perturbation family

For each listed row,

```text
I_N = {N/2+1,...,N}
Q < q <= 2Q, q prime
K_(H,s)(h) = (1+(h/H)^2)^(-s)
beta_N(t) = Lambda(t)/log(t) - sum_(d|t,d^400<=N^133) mu(d)
A(u,t) = 1_(u!=t) sum_q q K_(H,s)(u-t) 1_(q does not divide ut)
       * (1_(u=t mod q)-1/(q-1))
```

The shifted-prime comparison is

```text
b_N^(z)(u) = C_2^(z) 1_(2 does not divide u)
             product_(p<=z) p/(p-1)
             product_(p|u,p>z) (p-1)/(p-2),
```

with value zero when `u+2` has a prime factor at most `z`. The Euler tail
is enclosed through `P=50000`; all subsequent interval decisions use
`rho^2`, with threshold `1/16`.

## Certified result

The certificate contains 16 rows: 10 contractions and 6 obstructions.
The central matched pair is

```text
(N,H,Q,s,z)=(64,15,4,1,2): rho^2 in [0.0538214595269, 0.0538298814898]
(N,H,Q,s,z)=(64,15,4,1,3): rho^2 in [0.0748091943191, 0.0748218869170]
```

Thus changing only `z` flips the strict quarter classification. The `z=3`
obstruction persists for `H=13,15,17`; a `z=5` stress row has stored
square-root upper endpoint `0.3851247936`. The independent replay and
adversarial stress audit reproduce the classifications without importing
the interval producer.

```text
TPC268_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_CUTOFF_SENSITIVITY_OBSTRUCTION
TPC268_ROUTE_ADVANCE = YES_SCOPED_FINITE_CUTOFF_SENSITIVITY_OBSTRUCTION
TPC268_FINITE_CUTOFF_OBSTRUCTION = NUMERICALLY_CERTIFIED
TPC268_MATCHED_Z2_CONTROLS = NUMERICALLY_CERTIFIED
TPC268_CLOCK_STABILITY = REFUTED_SCOPED
TPC268_KERNEL_STABILITY = REFUTED_SCOPED
TPC268_ACTUAL_V59_RADIUS = OPEN_ASYMPTOTIC
TPC268_ACTUAL_V59_PHASE = OPEN_ASYMPTOTIC
TPC268_FIXED_POWER_CREDIT = 0
TPC268_ARITHMETIC_ADVANCE = NO
TPC268_L2 = NONE
TPC268_FULL_GATE_B = OPEN
TPC268_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC268_TWIN_PRIME_RESULT = NONE
TPC268_STATUS = NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_CUTOFF_SENSITIVITY_OBSTRUCTION
TPC268_ROUND2_CLUE = TEST_GROWING_CUTOFF_UNIFORMITY_BEFORE_ANY_PHASE_PROMOTION
```

Strongest positive result: ten finite rows, including six matched `z=2`
controls, are independently reproduced as contractions.

Strongest obstruction: the same central finite clock crosses the quarter
threshold when only the local comparison cutoff changes from `z=2` to `z=3`.

Open theorem: a growing-cutoff, source-compatible smooth-profile uniformity
theorem for the literal V59 residual.

Reusable structure: matched control -> declared perturbation -> outward
threshold separation -> fail-closed classification.

The Session-named `propose.md` and route evaluator files are absent from this
checkout. The project proof package, theorem ledger, certificate, bridge
checker, and `AGENTS.md` provide the fail-closed fallback evaluation. This
finite obstruction is not promoted to an arithmetic Route-B closure.
