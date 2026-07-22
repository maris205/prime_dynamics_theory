# TPC-60: Shorted-Gram reassembly of the missing high face

This directory contains the source and final PDF for:

> *Shorted-Gram Reassembly of an Incomplete High-Prime Image at a Fixed
> Shift: Missing Walsh Coordinates, Exact Kernel Tests, and Endpoint
> Certificates*

## Why this paper is needed

TPC-59 proved that the complete declared Walsh diagonal splits as

    D0 = Dbase + Drepresented + Dmissing.

The terminal census reaches only the represented high coordinates. Restoring
the missing coordinates is not norm-monotone after native grouping: their
output can cancel the represented affine vector.

TPC-60 puts all objects on the same fixed row-coefficient space:

    A = base + represented high,
    M = missing high,
    B = A + M = full output.

All maps use one fixed nonzero physical shift, literal coefficients, the
same declared carrier, and raw counting-measure norms.

## Exact shorted-Gram constant

The optimal uniform reassembly constant is

    delta_reasm = inf_(Az != 0) ||(A+M)z||^2 / ||Az||^2.

Let

    N = ker A,
    S = N^perp,
    W = (A+M)(N) = M(N),
    P = projection onto W^perp.

Then

    delta_reasm
      = inf_(s in S, s != 0) ||P(A+M)s||^2 / ||As||^2.

The projection is essential. Directions in ker A do not change the
denominator but can cancel the full output. If G=(A+M)^*(A+M) is written
on S direct-sum N, the correct numerator is the shorted Gram

    Q = G_SS - G_SN G_NN^dagger G_NS,

not the ordinary compression G_SS. Therefore

    delta_reasm
      = lambda_min((A_S^* A_S)^(-1/2) Q (A_S^* A_S)^(-1/2)).

At every finite scale,

    delta_reasm > 0
      iff ker(A+M) is contained in ker A.

This is an exact qualitative test. It does not by itself give a
scale-uniform or polynomial lower bound.

## Physical alias structure

For every fixed native output and high prime, at most one high Walsh atom is
active. Hence represented and missing vectors belonging to the same high
prime have disjoint output support. Reassembly cancellation can therefore
come only from:

- base versus missing interaction; or
- unequal high primes aliasing at the same native output.

Same-prime represented/missing cancellation is impossible, but the two
remaining mechanisms can still cancel completely.

## Raw missing mass times native degree

Let Dmissing(z) be the raw missing atomic mass and let dmissing be the
maximum number of missing atoms entering one native output. Then

    ||Mz||^2 <= dmissing Dmissing(z),

and

    ||(A+M)z||^2 / ||Az||^2
      >= (1 - sqrt(dmissing Dmissing(z) / ||Az||^2))_+^2.

If

    dmissing = X^(mu_missing+o(1)),
    Dmissing(z)/||Az||^2 <= X^(-sigma_missing+o(1)),

then sigma_missing > mu_missing is sufficient for zero fixed-power
reassembly loss in the same scope: pointwise for a distinguished vector,
or uniformly when both hypotheses are uniform on the declared class. The
two scopes use separate loss exponents. The product threshold is sharp: n missing atoms of
amplitude -1/n in one output have raw mass 1/n but cancel a unit
represented output exactly.

## Missing-carrier localization

The missing carrier has a definitional exact ordered first-failure
partition. On the
common literal Walsh/terminal support, the shaped-weight and
squarefree/coprimality pseudo-failure layers are empty. If the two
constructions have identical row, orbit, prime, mask, and profile supports
and no additional terminal-only pruning,
then the only missing mechanism is

    (m,r) not in the retained-pair carrier I_X.

This is a support identity, not a proof that missing mass is small.

The paper also proves:

- a sharp rowwise minimax for represented raw mass;
- an X^o(1)(1+L/R) determinant-ladder bound in one residual block;
- zero fixed-power cost for diagnostic first-failure/dyadic localization;
- a no-go for any route that pays the residual-ladder coefficient-blind
  capacity, whose exponent is at least 15077/105000, far above the endpoint
  allowance 1/400. This is not a lower bound for the actual native degree;
  the direct crude native certificate has exponent 267/400.

## Claim boundary

The abstract shorted-Gram and mass-degree results are L0. Their exact
specialization to the literal fixed-shift Walsh carrier is L1. The paper
does not prove:

- Dmissing = o(Drepresented);
- a polynomial lower bound for the physical reassembly constant;
- lambda_reasm = 0 for the arithmetic family;
- a fixed-shift parity improvement, prime-pair lower bound, or twin-prime
  consequence.

## Build

Run pdflatex, bibtex, and two more pdflatex passes in this directory.
The archived PDF is shorted-gram-missing-high-reassembly.pdf.
