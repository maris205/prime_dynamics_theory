# RH-294: Rate-free weighted full-trace diagonal bridge

RH-287 chose a diagonal clock that made the coefficient error uniformly
small on a growing prefix.  Choosing the level tolerances relative to the
weighted geometric sum strengthens that argument:

    E_sigma^(h)(R)
      = sum_(2<=n<=h_sigma)
        |c_(sigma,n)-s_(k_sigma,n)-a_n| R^n/n
      -> 0

for some h_sigma->infinity and k_sigma->infinity with h_sigma<2k_sigma.

The proof uses only the archived fixed-order noisy trace convergence and the
fixed-order finite-radius counterloop convergence.  It is exact, but the
clock can grow arbitrarily slowly.  In particular it gives no estimate
h_sigma >= a log(1/sigma), so it does not reach the RH-292 minimal bridge
clock and does not activate determinant gluing.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf rate-free-weighted-full-trace-diagonal-bridge.pdf
