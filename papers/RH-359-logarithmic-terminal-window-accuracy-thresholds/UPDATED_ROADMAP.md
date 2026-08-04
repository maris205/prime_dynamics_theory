# Roadmap after RH-359

RH-359 turns RH-358's qualitative statement `q_k -> infinity` into a sharp
accuracy ledger.  A window of size `a log(k)/log(x)` is exactly the scale for
relative error `k^(-a)`.  Integer rounding is structural: the normalized
error has a full multiplicative phase interval, and the minimal admissible
integer width has correction limit set `[0,1]`.

The phase result is not a finite fit.  It follows from the monotone unbounded
clock `a log_x(k)+c`, whose successive increments tend to zero, together with
the uniform RH-358 tail theorem.  The inverse result also records the maximal
claim allowed by the source remainder: away from integer crossings the
minimal width is the ceiling, while at a crossing no universal exact integer
choice is source-locked.

The next read-only candidate is RH-360, **terminal-lag exponential-tilt phase
transition**.  It should study the generating function

    G_k(z) = sum_r z^r pi_k(r)

below, at, and above the critical value `z=x`.  The expected theorem edge is
a finite geometric transform for `z<x`, a `k`-scaled critical Riemann-integral
law in the window `z_k=x exp(tau/k)`, and exponential endpoint dominance for
`z>x`.  Any tilted-distribution statement must remain a deterministic budget
law, not an eigenvalue or noisy stochastic law.

For physical transfer, the first blocker remains the original unnormalized
same-clock leaf `D_(4k)(R)->0`, or a typed direct/full-trace theorem paying the
open `q/E_off` ledger.  RH-241 and RH-288 remain open/inactive, Gates A--E
remain false/open, and no statement about Riemann zeros or RH follows.
