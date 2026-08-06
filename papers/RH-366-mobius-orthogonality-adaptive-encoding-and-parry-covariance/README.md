# RH-366: Möbius orthogonality, adaptive encoding, and Parry covariance

RH-366 freezes an independent arithmetic--dynamical theorem edge on the
certified local survivor of

    H_6(x,y) = (1-6x^2-y,x).

The survivor is conjugate to a primitive four-state subshift.  Its scalar
sign code obeys one exact rule: two plus signs cannot occur at distance two.
On this single positive-entropy basic set the paper proves a sharp
typical/exceptional separation.

1. Every fixed periodic orbit is Möbius-orthogonal for every continuous
   observable.
2. For Parry-almost every point, one full-measure set works simultaneously
   for every continuous observable.
3. An explicit admissible point selected after reading the positive-time
   Möbius sequence has raw sign correlation exactly `4/pi^2`.
4. For `F=(sqrt(5) epsilon+1)/2`, odd covariances vanish and the covariance
   at lag `2k` is `(-phi^(-2))^k`; the exact finite-prefix variance obeys
   `0 <= V_N <= sqrt(5) N`.
5. The limit `V_N/N -> 6/pi^2` is conditional on ordinary Cesàro two-point
   Chowla at every fixed even shift.
6. The open finite-horizon capacity is two path maximum-weight-independent-
   set problems, is exactly computable in `O(N)`, and satisfies

       4/pi^2 <= liminf K_N/N <= limsup K_N/N <= 6/pi^2.

No limit for `K_N/N` is asserted.

## Frozen finite audit

At `N=2^20`, the locked source reports:

- exceptional raw correlation `0.405335426`;
- open absolute capacity `0.492251396`;
- 420 of 1023 conditional block surrogates at least as large as the observed
  ordering, hence rank `p=421/1024=0.4111328125`.

This is a scoped negative finite ordering test.  It is not evidence for an
asymptotic capacity constant.  The stored decimal variance density is a
tolerance-controlled floating diagnostic; only the displayed mathematical
variance formula is called exact.

## Route boundary

Route A is `GO`: the periodic/typical orthogonality theorems, the explicit
adaptive exceptional point, the exact covariance, the unconditional variance
bound, and the capacity theorem form a standalone package.

Route B is `STOP_SCOPED`: the exceptional point is chosen offline after the
Möbius sequence is known.  This proves encoding capacity, not spontaneous or
canonical arithmetic coupling.  Orbit correlations and Parry variances are
not operator traces, von-Mangoldt prime-power coefficients, a spectral
determinant, an L-function family, or a Riemann-zero model.

The survivor is local, not the full Hénon nonwandering set.  Positive entropy
also means that the exceptional point is not a counterexample to Sarnak's
zero-entropy conjecture.  Gates A--E remain false/open; no Hilbert--Pólya
operator, completed-zeta divisor equality, or proof of RH is claimed.

## Reproduction

Run:

    make result
    make test
    make pdf
    make archive

Finite tables reproduce exact arithmetic identities, exact `Q(sqrt(5))`
covariances, graph/sign equivalence, and dynamic programming against brute
force.  They do not prove the all-order analytic-number-theory inputs.
