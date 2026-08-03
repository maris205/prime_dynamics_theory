# RH-354: Parity-free near-alias direct-tail envelope

RH-354 removes the parity restriction from the normalized actual direct
coefficient analysis.  On one bounded-phase physical clock define

    N_k = 2 k - L_k,
    p_(sigma,k,n) = tau_(sigma,n) - a_n,

where `0 <= L_k <= 2 k - 2`.  With

    s = q R = 7/10,
    t = q_* R = 28/(17 lambda),
    x = (beta R)^2,
    u = s/sqrt(x),
    v = t/sqrt(x) = lambda^(-1/2),

and

    rho_N = lambda^2 u^2 = r_H^2 lambda^3/4,
    rho_T = v^2 = 1/lambda,

the complete bottom-normalized direct tail

    W_k = x^(-N_k/2) sum_(n>=N_k) |p_(sigma,k,n)| R^n

satisfies the explicit source-bound

    W_k <= [q^(-2) lambda^(-2 eta_k)/(1-s)] rho_N^k u^(-L_k)
           + [48/(1-t)] rho_T^k v^(-L_k).

Consequently, for every `L_k=o(k)`,

    limsup W_k^(1/k)
      <= max(rho_N,rho_T)
      = rho_N
      < 1419857/1600000 < 1.

This is an all-order direct-coefficient theorem above the moving cut: the tail
contains both parities, the critical order, the first-lower order whenever
`L_k>=2`, the complete upper-alias band, and every later order.  It uses no parity decomposition or
order-specific orbit extraction.

The determinant-weighted near-alias band

    B_k = x^(-k) sum_(N_k<=n<4k) |p_(sigma,k,n)| R^n/n

therefore also decays exponentially with the same root ceiling.  In fact the
same conclusion holds for the full logarithmic tail from `N_k` onward.

The source bounds permit linear depths.  If

    ell = limsup L_k/k,

then the natural bottom-normalized and alias-clock root ceilings are

    max(rho_N u^(-ell), rho_T v^(-ell)),
    max(rho_N s^(-ell), rho_T t^(-ell)),

respectively.  Their noisy thresholds are

    alpha_nat   = log(1/rho_N)/log(1/u),
    alpha_alias = log(1/rho_N)/log(1/s).

The archived physical decimal gives the diagnostics `0.263953...` and
`0.441576...`; these decimals are not interval certificates.  At the exact
alias threshold, `L_k=alpha_alias k+O(1)` still gives an `O(1/k)` upper bound,
but no longer an exponential one.

The normalization is essential.  After removing `x^(-k)`, the separate noisy
majorant has root

    lambda^2 (q R)^2 > 9604/7225 > 1.

This is a strict method boundary, not a lower bound for the actual difference
`p=tau-a`.  Moreover `p=q-d`; the full-trace `E_off` budget uses `q`, so the
new theorem does not transfer to `E_off` without a same-clock head-defect
estimate.  Low orders below `N_k`, RH-241, RH-288, and Gates A--E remain open.
No Hilbert--Polya operator, Riemann-zero identification, von Mangoldt trace,
completed-zeta divisor equality, or proof of RH is claimed.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf parity-free-near-alias-direct-tail-envelope.pdf
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
