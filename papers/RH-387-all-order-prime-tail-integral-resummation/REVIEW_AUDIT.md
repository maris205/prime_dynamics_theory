# RH-387 peer-review audit

## Review question

Does the manuscript rigorously replace the complete RH-383 strict
prime-tail endpoint vector by integral vectors, with uniform constants and
without importing a finite-order hypothesis into an infinite-order sum?

## Major-claim review

1. Source transfer: the proof begins with the strict Stieltjes identity
   and obtains the absolute bound epsilon_x(2xh_r+J_r).
2. Infinite resummation: nonnegative Tonelli summation converts every
   order at once to the P and J logarithmic coordinates. The boundary and
   integral contributions give exactly 3c/[1-(1+c)/x^2], then 4c.
3. Power kernel: the exact logarithmic quotient is
   log(1+c/[t^2(t^2-1-c)]), producing c/(3x^3L) with the same denominator
   margin, then 2c/3.
4. Cube: L>=512 implies x>256. The telescoping integer tail places P, J,
   I, and all joining segments in [0,1/2]^7.
5. Endpoint: summable Euler-product deficits establish u_m>0. The exact
   alpha/beta arrays give 7 and 49/8.
6. Gradient: the three derivative contributions are 2,4,4. The
   l_infinity/l_1 mean-value estimate gives 63exp(1/2)<126.
7. Master constants: 126*28=3528 and 126*(14/3)=588, with pi^2 retained.
8. Novelty: the argument sums an absolute source bound before resummation;
   it does not sum RH-386's relative finite-order logarithmic theorem.

## Adversarial review

The field-level verifier rejects 24 targeted mathematical mutations:
source constants and log-log sign; domain and channel range; inclusive
endpoint; missing divisor, product sign, or boundary; false source
constants; interchanged kernels and wrong J/I direction; endpoint sign or
prefactor; deleted loss derivative; wrong norm pair; and an illicit P_2
claim. Strict type, duplicate-key, nonfinite, full-object, source
rebinding, optimized, and scalar-leaf attacks are separate fail-closed
tests.

## Scope review

The paper restricts c to the real integers 1 through 7. It claims no
complex channel, active c11, growing clock, joint prefix/prime limit,
adaptive selector, second-order coefficient, operator, trace, zero
identification, or RH. Gates A--E are false.

## Decision

Accept. Independent theorem review reports zero blockers and zero minors.
The source/citation/PDF review independently reports zero blockers and
zero minors. The final executable replay and archive status are recorded
in REPLAY_AUDIT.md.
