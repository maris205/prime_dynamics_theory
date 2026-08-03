# RH-355: Upper-alias counterloop burden and head-transfer precision

RH-355 sums every strict upper-alias coordinate of the source-locked graded
counterloop.  With

    beta_k = |M_k|^(-1/(2k))/r_H,
    beta   = (r_H sqrt(lambda))^(-1),
    x      = (beta R)^2 > 1,
    y_k    = (beta_k R)^2,

the RH-17 multiplier law gives

    y_k = x exp[-log(C_M)/k + o(1/k)].

For the exact RH-342 moment ledger, odd strict-upper moments vanish and

    |s_(k,2m)| R^(2m)/(2m) = y_k^m/m,
    k+1 <= m <= 2k-1.

Therefore

    C_k^up = sum_(2k<n<4k) |s_(k,n)|R^n/n
           = sum_(m=k+1)^(2k-1) y_k^m/m
           ~ x^(2k)/(2 C_M^2 k (x-1)),

and

    x^(-k) C_k^up ~ x^k/(2 C_M^2 k (x-1)),
    (x^(-k) C_k^up)^(1/k) -> x > 1.

The terminal coordinate satisfies

    x^(-k) |s_(k,4k-2)|R^(4k-2)/(4k-2)
      ~ x^(k-1)/(2 C_M^2 k),

and contributes the asymptotic fraction `(x-1)/x` of the whole upper band.

## Conditional actual-head obligation

Let `h_(sigma,n)` be the actual modulus-complete Hardy-head moment and
`d=h-s`.  Only under the original unnormalized same-clock hypothesis

    D_(4k)(R) = sum_(2<=n<4k) |d_(sigma,k,n)|R^n/n -> 0

does RH-355 conclude:

    H_k^up ~ C_k^up,
    H_(k,odd)^up -> 0,
    max_(k+1<=m<=2k-1) |h_(sigma,2m)-s_(k,2m)|/|s_(k,2m)|
      = o(k x^(-k)),
    |h_(sigma,4k-2)-s_(k,4k-2)|/|s_(k,4k-2)|
      = o(k x^(-2k)).

The paper does **not** prove `D_(4k)(R)->0`.

## Sharp normalized obstruction

The weaker condition

    Delta_k^up = x^(-k) sum_(2k<n<4k)|h-s|R^n/n -> 0

transfers the aggregate normalized budget and forces only the weaker terminal
precision `o(k x^(-k))`.  It does not imply uniform bandwise matching.

For `N=2k+2`, add the complete `N`th-root shell at

    a_k = beta_k (2/N)^(1/N).

Its defect is supported only at `n=N` in the strict upper band, where its
relative error is exactly one, while

    Delta_k^up ~ x/(C_M k) -> 0,
    D_(4k)(R)  ~ x^(k+1)/(C_M k) -> infinity.

This is a finite conjugation-closed normal information-class counterexample,
not an actual noisy operator.

RH-354 controls `p=tau-a=q-d`; it does not supply head-defect transport or a
full `q/E_off` theorem.  RH-288 and RH-241 remain inactive/open.  Gates A--E
remain false/open.  No Hilbert--Polya operator, Riemann-zero identification,
von Mangoldt trace, completed-zeta divisor equality, or proof of RH is
claimed.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf upper-alias-counterloop-burden-and-head-transfer-precision.pdf
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
