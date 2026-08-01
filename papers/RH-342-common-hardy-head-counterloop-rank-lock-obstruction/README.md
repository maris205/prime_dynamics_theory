# RH-342: Common-Hardy head/counterloop rank lock and a hidden-shell obstruction

RH-342 locks the actual noisy head and the graded counterloop in one Hardy
normalization.  Let `A_sigma=K_sigma/r_H`, with `r_H=17/20`, remove the two
peripheral eigenvalues, and define

    H_sigma = {algebraic eigenvalues mu of A_sigma with |mu|>q}, q=1/2,
    h_(sigma,n) = sum_(mu in H_sigma) mu^n.

For the physical first-alias clock

    k = log(1/sigma)/(2 log(lambda)) + O(1),   u=4k,

the graded counterloop is

    Y_k = {beta_k exp(+- i j pi/k): 1<=j<=k-1},

has rank `2k-2`, and has moments

    s_(k,n) = beta_k^n (2k 1_(2k|n) - 1 - (-1)^n).

Thus the strict prefix `2<=n<4k` contains the first alias `2k` and excludes
`4k`.  With `d_(sigma,k,n)=h_(sigma,n)-s_(k,n)`, the quotient of the two
finite genus-one factors has local logarithmic coefficients `-d_n/n` for
every `n>=2`.  This is an exact analytic comparison germ, not a common
physical determinant decomposition.

The first new theorem is a zero-padding rank lock.  If `r_sigma=#H_sigma`
and `m_k=2k-2`, then

    d1^0(H_sigma,Y_k)
      >= q (r_sigma-m_k)_+ + beta_k (m_k-r_sigma)_+.

Since `beta_k->beta>q`, any matching cost `o(1)`---in particular any
`O(sigma^gamma)` with `gamma>0`---forces eventual exact rank equality
`r_sigma=2k-2`.  The repository supplies only `r_sigma<=4/sigma`; it does
not identify the RH-16 endpoint singular rank with this spectral-head rank.

The second new theorem recovers a nonzero finite multiset from shifted
moments.  If two multisets have ranks at most `N` and their power sums agree
for every `2<=n<=2N+1`, then the multisets are identical.  The proof uses

    F_X(z) = sum_(x in X) x^2/(1-xz).

The numerator of `F_X-F_Y` has degree at most `2N-1`, while the moment
equalities give a zero of order `2N`.  Consequently, under the rank cap
`N=2k-2`, exact strict-prefix head/counterloop moment equality would identify
the roots even though the first moment is absent.

The rank cap is essential.  Put

    Z_k = {(3/4) exp(2 pi i j/(4k)): 0<=j<4k},
    X_k = Y_k disjoint_union Z_k.

Then all power sums of `X_k` and `Y_k` agree for `2<=n<4k`, so `D_(4k)=0`
exactly, but

    d1^0(X_k,Y_k) >= 4k q = 2k.

The extra genus-one factor is exactly `1-(3z/4)^(4k)`.  This is a finite,
conjugation-closed, normal spectral information-class counterexample, not an
actual noisy operator.  It shows that aggregate strict-prefix moments can
miss an entire high-rank shell.

Specializing RH-299 to `u=4k`, the source-safe global cap `B=1/r_H` requires

    gamma > 2 log(R/r_H)/log(lambda)
          = 1.926813889034... .

This global cap is valid because the unscaled noisy operator is Markov, so
its nonperipheral eigenvalues have modulus below one, while RH-272 gives
`beta_k->beta<1/r_H` for the counterloop roots.

The smaller threshold `0.926813889034...` uses the unproved local statement
that every actual-head root has modulus at most `beta+o(1)`; for a strict
exponent above the limiting threshold this gives an eventual common cap
`B=beta+epsilon`.  Either threshold also needs eventual rank equality and an
actual root-matching theorem; no source supplies them.  Therefore activation of the
RH-299 root-l1 route without a rank law/cap/rate is `STOP_SCOPED`.
Aggregate moment/Fourier/Hardy and direct annular routes remain
`NOT_TESTABLE`/open.  No physical rank mismatch, `D_(4k)` divergence,
determinant gluing, Gate progress, Hilbert--Polya operator, Riemann-zero
identification, von Mangoldt trace, completed-zeta divisor equality, or RH
conclusion is asserted.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf common-hardy-head-counterloop-rank-lock-obstruction.pdf
