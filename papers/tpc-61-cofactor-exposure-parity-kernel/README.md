# TPC-61: Cofactor exposure and the missing-high parity kernel

This directory contains the source and final PDF for:

> *Cofactor Exposure and the Missing--High Parity Kernel at the Critical
> Cutoff: Exact Matching Profiles, Restricted Native Grams, and a
> Determinant Reformulation*

## Why this paper is needed

TPC-60 split the complete very-high Walsh face into represented and missing
atoms and reduced their reassembly to two quantitative inputs:

- the raw mass of the missing atoms; and
- the size of their native grouping on the actual physical coefficient
  image.

The ambient native fiber degree is too expensive at the endpoint. TPC-61
therefore identifies the two physical quantities exactly instead of paying
that ambient bound.

All results use one fixed nonzero shift `h0`, the literal inherited
coefficients, raw counting-measure atomic norms, canonical largest-prime
factorization, and a carrier fixed before the row coefficient vector is
chosen.

## Exact cofactor exposure

Under the explicitly declared identical-support specialization, define the
realized cofactor measure on a source row `m` by

    nu_m(r) = sum_(w: m(w)=m, r(w)=r) |beta_w|^2.

If `I_m` is the retained cofactor set on that row, then

    W_represented(m) = nu_m(I_m),
    W_missing(m)     = nu_m(I_m^c).

Consequently the sharp coefficient-uniform missing fraction is

    max_(m: W_high(m)>0) W_missing(m) / W_high(m).

An active row containing only missing mass kills uniform represented-mass
transfer. The inherited opaque finite-relation interface does not rule out
such a row, so it implies no positive uniform exposure by itself. This is a
hypothesis-insufficiency theorem, not a counterexample to a more specific
upstream carrier.

## The fixed-row cofactor ladder

For every actually realized largest-prime cofactor, `(m,r)=1`. Fixing `m`
and `r` in

    r p - m j = h0

gives the exact ladder

    j = j0 + r t,
    p = p0 + m t,

with `p` in a reduced residue class modulo `m`. Hence

    N_m(r) << (m/phi(m)) (1 + (J/r)/log(2+J/r)).

This produces a sieve-harmonic defect certificate. It also explains why one
omitted small cofactor can be more dangerous than many omitted cofactors near
the critical ceiling: global cofactor density alone does not control the
physical exposure measure.

## Optimal restricted native Gram

Let

    D_M = diag(W_missing(m))

and let `M_X` be the literal missing native map. Its optimal physical upper
degree is

    kappa_M = lambda_max(
        D_M^(dagger/2) M_X^* M_X D_M^(dagger/2)
        restricted to Ran D_M).

Equivalently, `kappa_M` is the least constant such that

    ||M_X z||^2 <= kappa_M <D_M z,z>.

It is never larger than the ambient missing fiber degree, but it may be much
smaller. On a nonempty missing carrier, prime blocks are exact isometries
relative to their raw diagonals, so

    kappa_M = 1 + lambda_max(Xi_unequal-prime).

All excess above one is caused by unequal terminal primes aliasing at a
common native output. The paper gives exact stable-rank, weighted Schur,
codegree, Schur-complement, and block certificates for this eigenvalue.

## Literal parity kernel

After a fixed diagonal row gauge, each off-diagonal Gram entry is a weighted
two-affine-form Moebius correlation

    sum_j mu(m j + h0) mu(m' j + h0) Omega_(m,m')(j)

on the simultaneous missing carrier. With

    m j + h0  = p r,
    m' j + h0 = p' r',

the same entry is an exact signed sum on

    m' p r - m p' r' = h0 (m' - m).

This is a reformulation of the remaining parity-bearing operator, not a
cancellation estimate. Pairwise cancellation would still have to be
upgraded to a bound for the full growing-row operator norm.

## Endpoint audit

At the critical cofactor scale `theta = 133/400`, the residual-degree and
balanced cofactor-saving exponents leave the conditional window

    2 theta - 99979/210000 = 39671/210000.

Thus a residual-level mass--degree proof can have zero fixed-power
reassembly cost if its missing-cardinality, restricted erasure, and
represented-reference exponents satisfy the strict common-scope test

    e + mu_erasure + lambda_represented < 39671/210000.

By contrast, paying the full direct native degree leaves the fixed positive
gap

    267/400 - 133/400 = 67/200.

That closes only the direct phase-blind ambient-degree architecture. It is
not a lower bound for `kappa_M` and is not an additive endpoint loss.

In one-stage notation, if

    D_missing <= X^(-sigma_M+o(1)) D_ref,
    kappa_M    <= X^(nu_M+o(1)),
    ||A_X z||^2 >= X^(-lambda_rep+o(1)) D_ref,

then the strict condition

    sigma_M > nu_M + lambda_rep

gives zero fixed-power reassembly loss in the same uniform or distinguished
scope. The final physical ledger still requires total proved loss strictly
below `1/400`.

## Claim boundary

The exact disintegrations and finite-dimensional Gram theorems are L0. Their
specialization to the literal fixed-shift carrier and the cofactor-ladder
upper bound are L1. The paper does not prove:

- a positive exposure match for the actual retained relation;
- a fixed-power missing-mass saving;
- `kappa_M = X^(o(1))` or any new Moebius cancellation estimate;
- a positive physical shorted-Gram lower bound;
- a fixed-shift parity improvement, prime-pair lower bound or asymptotic, or
  twin-prime consequence.

## Build

Run `pdflatex`, `bibtex`, and two more `pdflatex` passes in this directory.
The archived PDF is `cofactor-exposure-missing-high-parity-kernel.pdf`.
