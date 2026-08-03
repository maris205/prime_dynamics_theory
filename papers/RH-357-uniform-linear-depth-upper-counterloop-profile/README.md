# RH-357: Uniform linear-depth upper-counterloop profile

RH-357 extends the strict upper-alias ledger from mesoscopic depth to every
integer depth below the second alias.  It is an unconditional theorem for the
deterministic graded counterloop, with a separately marked conditional statement
for an actual modulus-complete Hardy head.

Let

    x       = (beta R)^2 > 1,
    y_k     = (beta_k R)^2
            = x exp[-log(C_M)/k + o(1/k)],
    A_k     = (1-1/k)y_k^k,
    B_k(L)  = sum_(j=1)^L y_k^(k+j)/(k+j),

for `1 <= L <= k-1`.  The main uniform theorem is

    B_k(L)
      = y_k^(k+L+1)(1-y_k^(-L))
        / ((k+L)(y_k-1)) * (1+O(1/k)),

uniformly over the complete strict upper band.  Using the multiplier law,

    B_k(L)
      = x^(k+L+1)(1-x^(-L))
        / (C_M^(1+L/k)(k+L)(x-1)) * (1+o(1)),

and

    B_k(L)/A_k
      = x^(L+1)(1-x^(-L))
        / (C_M^(L/k)(k+L)(x-1)) * (1+o(1)),

with relative errors uniform in `1 <= L <= k-1`.

## Linear depth

If `L/k -> alpha` with `0 < alpha <= 1`, then

    B_k(L) ~ x^(k+L+1)
      / (C_M^(1+alpha) k (1+alpha)(x-1)),

    B_k(L)/A_k ~ x^(L+1)
      / (C_M^alpha k (1+alpha)(x-1)).

Consequently the deterministic `k`th-root rates are `x^(1+alpha)` and
`x^alpha`.  With the RH-355 physical clock
`k = log(1/sigma)/(2 log(lambda)) + O(1)`, the corresponding logarithmic
rates per `log(1/sigma)` are `(1+alpha)log(x)/(2log(lambda))` and
`alpha log(x)/(2log(lambda))`.

For `L=floor(alpha k+c)`, write `theta_k={alpha k+c}`.  The phase-safe laws are

    k x^(-(1+alpha)k) B_k(L)
      = x^(c+1-theta_k)
        / (C_M^(1+alpha)(1+alpha)(x-1)) * (1+o(1)),

    k x^(-alpha k) B_k(L)/A_k
      = x^(c+1-theta_k)
        / (C_M^alpha(1+alpha)(x-1)) * (1+o(1)).

Rational `alpha` gives a finite periodic phase orbit; irrational `alpha` gives
the closed phase limit set `[0,1]` and an interval of normalized cluster
values.  These phases are not collapsed into one constant.  At `alpha=1`,
`L=k-1` recovers the complete RH-355 strict upper band.

The boundary `alpha=0` is deliberately separate: bounded `L` retains
`1-x^(-L)`, while the terminal simplification is allowed only when
`L -> infinity` and `L=o(k)`, as proved in RH-356.

## Conditional actual-head scope

If, on one common physical clock, the original unnormalized transport leaf

    D_(4k)(R) = sum_(2<=n<4k) |h_(sigma,n)-s_(k,n)| R^n/n -> 0

is assumed, then the actual first-alias and even post-alias budgets inherit the
uniform relative profile and the odd upper-band budget tends to zero.  RH-357
does not prove this leaf, identify actual roots or ranks, close a direct/full
trace budget, activate RH-288, or establish any of Gates A--E.  It does not
construct a Hilbert--Polya operator, identify Riemann zeros, or prove RH.

## Reproduction

From this directory:

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf uniform-linear-depth-upper-counterloop-profile.pdf
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py

The Python rows are exact rational or high-precision synthetic reproductions;
they are not interval certificates for the physical multiplier and are not
actual noisy-head observations.
