# RH-358: Terminal-lag geometric localization

RH-358 reindexes the complete deterministic strict upper-counterloop band by
distance from its terminal coordinate.  It proves a uniform finite-tail law,
an exact probability identity, and total-variation localization to a geometric
law.  The result is unconditional for the deterministic graded counterloop and
has only a separately marked conditional actual-head inheritance statement.

Let

    x       = (beta R)^2 > 1,
    y_k     = (beta_k R)^2
            = x exp[-log(C_M)/k + o(1/k)],
    B_k(L)  = sum_(j=1)^L y_k^(k+j)/(k+j),
    C_k     = B_k(k-1),
    P_k(q)  = B_k(k-1-q),       0 <= q <= k-2.

For the terminal coordinate `r=0,...,k-2`, put

    pi_k(r) = [y_k^(2k-1-r)/(2k-1-r)] / C_k.

Then exactly

    P_k(q)/C_k = sum_(r=q)^(k-2) pi_k(r).

The main uniform theorem is

    P_k(q)/C_k
      = y_k^(-q) (2k-1)/(2k-1-q)
        (1-y_k^(-(k-1-q)))/(1-y_k^(-(k-1)))
        (1+O(1/k)),

uniformly over `0 <= q <= k-2`.  The source-locked form is

    P_k(q)/C_k
      = x^(-q) C_M^(q/k) (2k-1)/(2k-1-q)
        (1-x^(-(k-1-q)))/(1-x^(-(k-1)))
        (1+o(1)),

again with uniform relative error.  In particular:

- if `q=o(k)`, then `P_k(q)/C_k=x^(-q)(1+o(1))`;
- if `q/k -> theta < 1`, then the leading prefactor is
  `2 C_M^theta/(2-theta)`;
- if `q=k-1-ell` with fixed `ell>=1`, the surviving lower block has
  relative mass asymptotic to
  `2 C_M x^(-q)(1-x^(-ell))`.

The normalized terminal-lag distribution satisfies

    ||pi_k - (1-x^(-1))x^(-r)||_1 -> 0,

so its total variation distance tends to zero and

    E_k[r]   -> 1/(x-1),
    Var_k[r] -> x/(x-1)^2.

For fixed `q`, the lower tail has mass `x^(-q)` and the retained top `q`
coordinates have mass `1-x^(-q)`.  A terminal window has vanishing relative
truncation error if and only if its width tends to infinity.  Here `q` is only
the terminal-lag integer; it is not the open direct/full-trace budget sometimes
also denoted by `q` elsewhere in the project.

## Conditional actual-head scope

If, on one common physical clock, the original unnormalized transport leaf

    D_(4k)(R) = sum_(2<=n<4k) |h_(sigma,n)-s_(k,n)| R^n/n -> 0

is assumed, then the actual even upper-band weights inherit the uniform tail
profile, the geometric total-variation limit, and the first two lag moments.
The moment transfer uses uniform coordinatewise relative control, not total
variation alone.  RH-358 does not prove this leaf, identify actual roots or
ranks, close a determinant or a direct/full trace budget, activate RH-241 or
RH-288, or establish any of Gates A--E.  It does not construct a
Hilbert--Polya operator, identify Riemann zeros, or prove RH.

## Reproduction

From this directory:

    make result
    make test
    make pdf
    make archive

Equivalently, the underlying commands are recorded in the `Makefile`.  The
Python rows are exact rational or high-precision synthetic reproductions; they
are not interval certificates for the physical multiplier and are not actual
noisy-head observations.
