# RH-396 updated roadmap

## Closed route

RH-396 closes the fixed-lag centered three-window route at every fixed
positive integer lag:

1. RH-394 supplies the complete fixed three-shift terminal-log table law at
   the distinct shifts `(+h,0,-h)`.
2. Positive projection and relation saturation reduce each fixed table to an
   exact subset-state transition problem.
3. The full eight-state tropical trace is valid for every finite clock.
4. Four-state compression is proved precisely off the self-loop regime
   `q | 2h`; the strict `h=2,q=4` obstruction protects this boundary.
5. Collision-aware per-state marginal equality proves centered capacity
   equals normalized one-site MWIS on square supports containing `p0(h)`.
6. Same-support cover scaling needs no coprimality between the cover degree
   and `2h`; the `h=6` examples delimit its base-support hypothesis.
7. Exact finite run densities yield a finite Euler-run expression for each
   square-clock endpoint and a termwise cofinal limit.
8. Fresh-prime recurrence explains both plateau steps and strict steps; CRT
   supplies eventual strictness.
9. A same-support bridge handles every arbitrary finite `q`, proving the
   endpoint supremum and strict finite nonattainment.
10. Isolated-run positivity and the outside-prime boundary bound identify the
    unattained infimum across fixed lags.

## New theorem edge

The reusable edge is an exact Euler-run spectrum for fixed-lag capacity:

```text
collision-aware fixed-shift densities
                 |
                 v
full-eight tropical relation optimizer
                 |
                 v
qualified square-support marginal charge
                 |
                 v
finite Euler-run endpoint + fresh-prime recurrence
                 |
                 v
strict finite-clock nonattainment for every fixed h
                 |
                 v
unattained lag infimum 3/pi^2.
```

The recurrence separates nondecreasing prime-square refinement from strict
refinement.  Even runs are exactly the local resource that pays a strict
gain; CRT proves this resource can be created after a finite extension.

## Admissible next work

These are research questions, not conclusions of RH-396:

- classify other fixed local relations whose square-support marginals admit
  an exact run-spectrum formula;
- determine whether any even four-shift or larger window has a source theorem
  strong enough to replace RH-394's three-shift law;
- quantify Euler-run endpoints only after deriving rigorous error bounds that
  are uniform in the relevant fixed parameter;
- study causal rules under their own information constraint, without using
  the centered future value `mu(n+h)`;
- test other finite graph covers for a recurrence analogous to the even-run
  excess formula.

No next paper number follows from this list.  A new route needs a fresh
repository-backed theorem edge and independent source and proof locks.

## Permanent stops

Do not infer from RH-396:

- a result with `h=h(X)`, `q=q(X)`, or an `X`-dependent table family;
- an effective or uniform convergence rate;
- ordinary Cesaro convergence or a prelimit maximum;
- a causal or online implementation;
- an even four-shift, larger-window, or generic graph theorem;
- strict gain at every prime-square step;
- a supremum, maximum, or monotonicity theorem across lags;
- an analytic trace formula, Hilbert--Polya operator, zeta-zero
  identification, completed-zeta divisor equality, or RH.

Program Gates A--E remain false.
