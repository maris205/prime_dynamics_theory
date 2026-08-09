# RH-390 peer-review audit

## Review question

Does exact retention below a growing rank, followed by the complete
factorial Laplace window at and above that rank, approximate the endpoint
uniformly at the `P_s` scale; and is the retained-rank boundary sharp at
every fixed threshold inside the declared hierarchy?

## Major-claim review

1. The source transfer starts from the strict Stieltjes identity and sums
   its absolute bound over every rank `r>=s`.
2. The rank-tail generator `R_s` pays the separate endpoint and integral
   terms, giving the exact coefficient `4-1/s`.
3. The `J-I` comparison uses exponent `s+1` in `B_(s,c)` and the ratio
   `(2s-1)/(2s+1)`.
4. The factorial comparison uses the exact signed finite Laplace remainder
   and a geometric sum over all `r>=s`.
5. The complete `K` window follows from a symbolic recurrence with
   positive-real `D`; no factorial convergence is claimed.
6. Prime and surrogate coordinates share the real cube `[0,1/2]^7`, and
   the endpoint mean-value theorem uses the dual norm bound 126.
7. The growing-rank proof consumes `7^S`, `log S=o(V)`, denominator floors,
   the full-K induction, and uniform `P_s/K_s->1`.
8. The all-rank singleton coefficient is derived from the endpoint map;
   low ranks use exact rational intervals and high ranks use exact
   cross-product inequalities.
9. Integer-valued Maynard gaps yield infinitely many consecutive gaps at
   most 600, not merely a liminf slogan.
10. The fixed-rank scalar jump retains the exact next-prime atom and shows
    the smooth interval term vanishes.
11. The common-head endpoint lift pays the Hessian and square remainders
    with constants 224 and 112; higher ranks and the full `J-I` tail are
    negligible at the fixed scale.
12. The negative conclusion is restricted to fixed `s` and the explicit
    `P/J/I` hierarchy.

## Adversarial artifact review

The 24 named mutations attack the strict endpoint, Stieltjes boundary,
rank split, tail generator, source and power denominators, Laplace rate,
factorial sign and factorial, complete rank sum, full-K window, cube,
dual norm, normalized coefficients, growing rank budget, all-rank gamma
bridge, successor atom, smooth interval, Taylor cross terms, fixed-rank
quantifier, scale normalization, and scope firewalls.

Separate tests attack exact types, Boolean aliases, duplicate/nonfinite
JSON, builder independence, source and logical digest rebinding, closed
schema membership, manifest hashes and membership, nested nonobjects,
unsafe and overlong paths, stage count, remote order, offline requests,
optimized mode, and recursive payload exclusion.

## Novelty and scope review

RH-388 established the rank-one `P_2` prototype.  RH-390's new edge is the
simultaneous growing exact-retention frontier, the complete factorial
window at every admissible rank, and the all-rank positivity bridge proving
fixed-threshold necessity.

The paper claims no moving-rank necessity, arbitrary-surrogate obstruction,
convergent factorial series, complex channel, active `c11`, growing clock,
`K_N`, operator, trace, zero identification, or RH.  Gates A--E remain
false.

## Decision

Accept.  Independent theorem review and independent source/citation/PDF
review each report zero blockers and zero minors.  The executable archive
decision is recorded in `REPLAY_AUDIT.md`.
