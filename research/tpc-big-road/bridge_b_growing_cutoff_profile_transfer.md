# Bridge B V122 / TPC-269: growing-cutoff and convex-profile transfer

Date: 2026-08-26

Status: `NUMERICALLY_CERTIFIED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER`

TPC-268 showed that a declared finite comparison cutoff can move the literal
V59 residual across the quarter threshold. TPC-269 makes the next controlled
change while retaining the same physical object: the comparison cutoff follows
the registered finite rule `z_N=floor(log N)`, and the kernel follows a convex
path between two normalized nonnegative finite profiles. The prime shell,
outer q weight, unit masks, deleted diagonal, beta source, and rank-three
projection are unchanged.

## Frozen object and finite perturbation

For each registered row,

```text
I_N = {N/2+1,...,N}
Q < q <= 2Q, q prime
K_(H,s)(h) = (1+(h/H)^2)^(-s), s in {1,2}
z_N = floor(log N)
beta_N(t) = Lambda(t)/log(t) - sum_(d|t,d^400<=N^133) mu(d)
w_N(u) = Lambda(u+2)-b_N^(z_N)(u)
```

The finite operator is

```text
A_s(u,t) = 1_(u!=t) sum_q q K_(H,s)(u-t) 1_(q does not divide ut)
           * (1_(u=t mod q)-1/(q-1))
A_theta = (1-theta) A_1 + theta A_2
g_theta = A_theta beta_N
```

The three exact block contrasts are retained. Every non-logarithmic quantity
is rational on a finite row; Euler-product and logarithm inputs use the
upstream outward interval protocol with `P=50000`.

## Certified finite transfer

The certificate has twelve threshold-separated rows: eight contractions and
four obstructions. Six rows use the growing-cutoff base `theta=0` at
`N=64,96,128,192,256,384`. The remaining rows test the convex profile path
and matched controls. At the fixed central row `(N,H,Q)=(64,15,4)`,

```text
theta=9/10: rho^2 in [0.0634078324659, 0.0634208686352]  obstruction
theta=24/25: rho^2 in [0.0622500850692, 0.0622630874560] contraction
theta=1:     rho^2 in [0.0614513775060, 0.0614643508731] contraction
```

The affine profile identity is exact on the finite interface, but the
denominator of `rho^2` is quadratic in the profile parameter. Thus a favorable
endpoint is not a profile-uniform bound. The growing rule is a finite proxy
registry, not a source-level asymptotic uniformity theorem.

```text
TPC269_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER
TPC269_ROUTE_ADVANCE = YES_SCOPED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER
TPC269_GROWING_CUTOFF_PROXY = NUMERICALLY_CERTIFIED_FINITE
TPC269_PROFILE_MIXTURE_IDENTITY = PROVED_EXACT_FINITE
TPC269_PROFILE_PATH_FLIP = NUMERICALLY_CERTIFIED_FINITE
TPC269_GROWING_UNIFORMITY = OPEN_ASYMPTOTIC
TPC269_ACTUAL_V59_RADIUS = OPEN_ASYMPTOTIC
TPC269_ACTUAL_V59_PHASE = OPEN_ASYMPTOTIC
TPC269_FIXED_POWER_CREDIT = 0
TPC269_ARITHMETIC_ADVANCE = NO
TPC269_L2 = NONE
TPC269_FULL_GATE_B = OPEN
TPC269_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC269_TWIN_PRIME_RESULT = NONE
TPC269_STATUS = NUMERICALLY_CERTIFIED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER
TPC269_ROUND2_CLUE = TEST_CROSS_SCALE_RADIUS_NORMALIZATION_AFTER_SOURCE_COMPATIBLE_PROFILE
```

Strongest positive result: the exact affine profile transfer and eight
independently audited finite contractions.

Strongest obstruction: at the same cutoff, clock, shell, and projection, the
`9/10` to `24/25` profile path crosses the quarter threshold.

Open theorem: a source-compatible growing-cutoff/profile uniformity estimate,
including a radius or signed-phase bound at growing scale.

Reusable structure: frozen physical operator -> finite growing proxy -> exact
convex profile path -> outward `rho^2` decision -> independent replay.

The Session-named `propose.md` and route evaluator files are absent from this
checkout. The project proof package, theorem ledger, certificate, bridge
checker, and `AGENTS.md` provide the fail-closed fallback evaluation. Nothing
in this finite transfer is promoted to an arithmetic Route-B closure.
