# Roadmap after RH-356

RH-356 locates the sharp crossover inside the strict upper-alias burden of
RH-355.  The first `L` post-alias coordinates remain negligible relative to
the first alias while `L-log_x(k)->-infinity`; they become comparable in the
window `L=log_x(k)+O(1)` and dominate beyond it.  On the physical noise clock
this window is only logarithmic in `log(1/sigma)` above the first alias.

The integer floor phase is now part of the locked theorem.  A fixed integer
offset does not produce a single constant: the ratio has the complete cluster
interval from `x^c/(x-1)` to `x^(c+1)/(x-1)`.  Any future scalar balance that
selects an integer post-alias depth must either retain this phase or prove a
subsequence/selection law.

The theorem also closes two tempting shortcuts:

1. at fixed depth, `x^L-1` cannot be replaced by `x^L`;
2. the mesoscopic law cannot be extended to `L` proportional to `k`, where
   denominator variation and finite-radius drift are no longer negligible.

There is also an immediate source-backed scoped continuation on the graded
counterloop itself.  The next investigation should take

    L/k -> alpha,   0 < alpha <= 1,

and derive the linear/full-depth upper-counterloop profile.  Endpoint
geometric domination predicts the new factors

    C_M^(-alpha),   (1+alpha)^(-1).

At `alpha=1` the profile must recover the complete RH-355 upper burden; as
`alpha` decreases to zero it must join the growing-depth RH-356 law.  This is
the immediate scoped mathematical route for RH-357, not an actual-head
theorem and not an extension already proved by RH-356.

For physical transfer, the first blocker remains an actual same-clock
theorem.  The narrow options are:

1. prove the original unnormalized `D_(4k)(R)->0` leaf for the actual
   modulus-complete Hardy head, which would conditionally transfer the new
   crossover;
2. prove a direct theorem for the full-trace `q/E_off` budget that bypasses
   head transport without conflating it with RH-354's direct `p` theorem;
3. obtain an actual rank/root transport theorem strong enough to imply the
   required weighted head budget on the physical clock.

No such actual theorem is supplied here.  RH-241 remains open, RH-288 remains
inactive, Gates A--E remain false/open, and no conclusion about the Riemann
Hypothesis follows.
