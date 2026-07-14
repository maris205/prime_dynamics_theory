# TPC-15: Fixed-shift local models

**Paper:** *Fixed-Shift Local Models within the Square-Root Distribution Range:
Quarter-Scale Row Masks, Ramanujan Spectral Calibration, and a
Vaughan Type-II Reduction*

TPC-14 isolated the fixed-shift Type-II gate but did not subtract a
complete local model at a prescribed shift. This paper closes the full
quotient-independent Type-I row ball needed in the present Vaughan
decomposition and reduces the remaining endpoint error to one explicit
hard packet.

## Main results

- On the primitive `k=1` shell, the correct row density is

  ```text
  rho_h(a) = 1_(a,h)=1 * a/phi(a).
  ```

  Every bounded source-factor row mask with
  `a <= X^(1/4-epsilon)` has arbitrary logarithmic cancellation after
  this centering. The complete row-centered residual nevertheless has main term

  ```text
  (phi(|h|)/|h| - beta_h) X I0(W) log X.
  ```

  For `h=2` the coefficient is exactly `1/6`. When `I0(W) != 0`, this
  residual logarithmic main term is forced beyond the quarter-scale Type-I
  region; no individual `b`-orientation is isolated.

- The finite Heath--Brown model

  ```text
  Lambda_Q(n) = sum_(q<=Q) mu(q)c_q(n)/phi(q)
  ```

  is realized as a finite rational translation spectrum. Its
  autocorrelation is the truncated prime-pair singular series. For fixed
  `0<delta<1/2` and `Q=X^(1/2-delta)`, its model-model and prime-model correlations have the
  same singular-series main term with arbitrary logarithmic saving.

- The residual `r_Q=Lambda-Lambda_Q` is calibrated on every progression
  modulus `m<=Q`. Uniformly over all bounded row masks, its fixed-shift
  Type-I contribution is `O_A(X log^(-A) X)`.

- With `U=V=sqrt(Q)`, Vaughan's identity gives

  ```text
  sum Lambda(n)Lambda(n+h)W(n/X)
    = singular_series(h) X I0(W)
      + B_(h,delta)(X) + O_A(X log^(-A) X),
  ```

  where `B_(h,delta)` is one explicitly defined bilinear hard packet.
  For an admissible even `h` with `I0(W) != 0`, the weighted
  Hardy--Littlewood asymptotic is equivalent to `B_(h,delta)(X)=o(X)`.
  The paper does not prove this estimate.

The paper proves no fixed-shift prime-pair asymptotic, twin-prime lower
bound, new level of distribution, or breach of sieve parity.

## Reproduction

From this directory:

    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    python experiments/ramanujan_typeii_certificate.py
    python -m unittest experiments.test_ramanujan_typeii_certificate -v

The finite certificate checks exact Ramanujan expansions, progression
calibration, periodic correlations, local coefficients, Vaughan's
identity, and the finite-selector inequality. It does not test the
imported analytic estimates or any open prime-pair assertion.
