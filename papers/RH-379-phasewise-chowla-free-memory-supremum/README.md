# RH-379: Phasewise Chowla-free lag-two memory supremum

RH-379 exactly optimizes universally distance-two-safe phasewise lag-two
tables

```text
epsilon_n = f_(n mod q)(mu(n-2),mu(n))
```

at each fixed finite clock `q`, under the phasewise condition
`c11(r)=0`.  The clock is fixed before `N -> infinity`.  This is the
phasewise Chowla-free class, not unrestricted memory.

The exact local census is:

- all `512` lag-two truth tables are exhausted;
- exactly `192` have `c11=0`;
- their nine `(c02,c22)` cells reduce by canonical subset dominance to
  `0,J,K,I`, with counts `120,40,24,8`;
- subset replacement is performed before `K -> I`; only after
  canonicalization do `K` and `I` have identical full incoming/outgoing
  compatibility;
- the exact optimizer therefore has the three states `{0,J,I}`.

For every finite `q`, `G(q)` is an exact cyclic max-plus value with weights
in `Q/pi^2 + Q*kappa2`.  The standard-library artifact stores those two
rational coefficients and uses a fail-closed certified interval for
`pi^2*kappa2` when a comparison is necessary.  It independently checks the
equivalent all-`J` baseline plus cycle-MWIS reduction.

The exact square-clock refinement is

```text
q_y = 4 P_y,
A_y = product_(i<=y)(p_i^2-1),
D_y = product_(i<=y)(p_i^2-2),
G(q_y) = B_y + Delta_y,
Delta_y = mathcal_E_y * (4/(A_y*pi^2)-kappa2/D_y) > 0,
```

where `mathcal_E_y=R2+R4+R6+R8` is the number of even-length positive
runs.  It is not RH-374's Euler-product notation and not its count of sites
inside even runs.  The run recurrence proves `Delta_y -> 0`, but no
monotonicity of `Delta_y` is claimed.

At `q=36`,

```text
G(36) = 9/(2*pi^2)-kappa2/7
      > F(36) = 4/pi^2.
```

This is called an exact square-clock strict gain, not the first same-clock
gain: `G(1)=6/pi^2-kappa2>F(1)=0` already.

For arbitrary fixed `q`, the upper proof lifts to
`Q_y=lcm(q,q_y)` after `y` contains every odd prime divisor of `q`.
Retained phases form a one-site independent set and contribute at most
`F(Q_y)=B_y`; every discarded `J` is charged to a square divisor
`p^2 | n-2` with `p>p_y`, at total cost at most
`sum_(p>p_y)1/p^2`.  Only after the fixed-clock `N`-limit is taken is
`y -> infinity` sent.  The reverse inequality is the RH-375 one-site
embedding `f_r(x,z)=g_r(z)`.  Hence

```text
sup_(q finite) G(q) = B_infinity.
```

The paper makes no finite-clock attainment or nonattainment claim, no
same-support memory-saturation claim, and no `q=q(N)` passage.  The first
blocker beyond its class is phase-weighted shift-two `D2` cancellation.
It proves no adaptive-capacity limit, intrinsic operator, prime-power trace,
zero model, Hilbert--Polya construction, Gate A--E result, or RH.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 make result
PYTHONDONTWRITEBYTECODE=1 make test
make pdf
PYTHONDONTWRITEBYTECODE=1 make archive
```

All finite decimals and finite clock rows are reproduction only.  The
all-clock identity follows from the fixed-clock lift, retained-phase bound,
explicit prime-square tail, and one-site embedding.
