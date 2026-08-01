# RH-343: Equal-rank, equal-mass first-alias underdetermination

RH-343 proves an exact finite-normal spectral information-class theorem.  It
does **not** construct two noisy operators.  For the complete shell

    U_L(r) = {r exp(2 pi i j/L): 0<=j<L},

the exact power ledger is

    p_n(U_L(r)) = L r^n 1_(L|n).

Put

    a=3/4,  b=4/5,  c=sqrt(481/800),
    c^2=(a^2+b^2)/2,

and let `Y_k` be the RH-342 counterloop of rank `2k-2` and radius
`beta_k`.  Define the model spectra

    X_k^inv = Y_k disjoint_union U_(4k)(c),
    X_k^vis = Y_k disjoint_union U_(2k)(a)
                      disjoint_union U_(2k)(b).

Both candidates have rank `6k-2` and exact squared spectral mass

    (2k-2) beta_k^2 + 481k/200.

They are conjugation closed and admit finite normal diagonal realizations.
Since

    1/2 < a < c < b < beta_k < 1/r_H

eventually, both spectra are eventually simple, lie in the same Hardy
annulus, and have the same maximum modulus `beta_k`.  Their ranks and squared
spectral masses are `O(k)=O(log(1/sigma))=o(1/sigma)` on the physical clock,
so they do not violate the coarse RH-282 ceilings.  This compatibility is not
a physical realization theorem.

Both candidates agree exactly with `Y_k` for every `2<=n<2k`, and therefore
for every fixed order eventually.  They do not agree on the whole strict
prefix `2<=n<4k`: at the first alias `n=2k`, the invisible candidate still
contributes zero while the visible candidate contributes

    2k(a^(2k)+b^(2k)).

With the RH-299 normalization

    D_m(X,Y) = sum_(2<=n<m) |p_n(X)-p_n(Y)| R^n/n,
    R=7/5,

the strict endpoint gives the exact dichotomy

    D_(4k)(X_k^inv,Y_k) = 0,
    D_(4k)(X_k^vis,Y_k)
      = (21/20)^(2k) + (28/25)^(2k) -> infinity.

The factor `1/n` cancels the multiplicity `2k` exactly.  The strict endpoint
`n<4k` is essential: it keeps the first `4k`-shell moment excluded.  The
corresponding genus-one quotient factors are exactly

    1-(cz)^(4k)

and

    [1-(az)^(2k)][1-(bz)^(2k)].

Thus equal rank, equal squared spectral mass, the same cap and maximum
modulus, simple conjugation-closed normal realizability, and all pre-alias or
eventual fixed-order data do not determine the moving strict-prefix budget.
A future actual rank cap `r_sigma<=2k-2` would exclude both examples.

The actual alias-inclusive head transport remains `NOT_TESTABLE`/open.  No
actual `D_(4k)` divergence or vanishing, physical rank mismatch, determinant
gluing, prefix equivalence, RH-288 activation, Gate progress,
Hilbert--Polya operator, Riemann-zero identification, von Mangoldt trace,
completed-zeta divisor equality, or RH conclusion is asserted.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf equal-rank-equal-mass-first-alias-underdetermination.pdf
