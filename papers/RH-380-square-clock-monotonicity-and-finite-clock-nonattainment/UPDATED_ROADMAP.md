# RH-380 updated roadmap

RH-380 closes the finite-clock attainment question inside the exact
phasewise `c11=0` memory class of RH-379. The closed chain is:

```text
per-run prime-square deletion
  -> exact even-run recurrence
  -> exact square-clock increment
  -> strict G(q_y) monotonicity
  -> separator-specific same-support saturation
  -> lcm lift for arbitrary fixed q
  -> finite-clock nonattainment plus explicit gap.
```

Computing more square clocks does not create another theorem edge. There is,
however, an immediate analytic rate trigger inside the same `c11=0` class.
Define

```text
T_y = sum_(p>p_y) 1/(p^2-1),
e_m = product_(p odd) (1-m/p^2),
X_infinity = (2e_4-4e_5+6e_6-8e_7+10e_8)/e_1 > 0.
```

The exact reopen target is

```text
B_infinity-G(q_y)
  = (2X_infinity/pi^2) T_y + O(T_y^2),
```

with the successor required to prove that the `M_y` contribution is only
second order. RH-380 does not prove this normalized-tail theorem. A
successor must supply the all-order Euler-product expansion and remainder
bound; finite regression or fitted decay is not sufficient.

The first edge that enlarges the factor class is a natural-average theorem for

```text
sum_(n<=N) w_(n mod q) mu(n-2)mu(n)
```

for every fixed periodic weight required by the phasewise interpolation.
Without such an input, nonzero phasewise `c11(r)` remains `STOP_SCOPED`.

Admissible reopen routes are:

1. prove the normalized tail expansion above and the quadratic `M_y` bound;
2. prove the needed fixed-period phase-weighted shift-two cancellation, or
   a theorem that genuinely implies it with the required normalization;
3. produce a different universally safe memory class whose full moment
   interface avoids all currently unproved correlations;
4. reopen a dynamical-zeta route only after its named strong-space,
   projector, resolvent, or trace hypothesis is proved rather than fitted;
5. return to the adaptive two-envelope problem only with a theorem that
   justifies a growing-clock or capacity-limit exchange.

Computing more finite values, fitting `Delta_y`, or testing unrelated
multipliers does not reopen the branch. The same-support theorem is
separator-specific and cannot be promoted to a general cover statement.

No current route supplies Gate A, B, C, D, or E. In particular, RH-380
constructs no Hilbert--Polya operator, identifies no Riemann zero, and does
not imply RH.
