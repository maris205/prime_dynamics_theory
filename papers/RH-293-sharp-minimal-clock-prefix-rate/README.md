# RH-293: Sharp minimal-clock prefix rate

Let h_sigma be the shortened RH-292 bridge clock and suppose only that

    max_(2<=n<h_sigma) |tau_(sigma,n)-a_n| <= epsilon_sigma.

For R>1 the worst weighted prefix is exactly

    epsilon_sigma sum_(2<=n<h_sigma) R^n/n
      ~ epsilon_sigma R^h_sigma / (h_sigma (R-1)).

Thus, for h_sigma=ceil(a log(1/sigma)) and a power rate
epsilon_sigma=O(sigma^beta), the sharp uniform threshold is

    beta_* = a log R.

Equality still gives logarithmic decay; below the threshold a constant-error
saturation family diverges.  At the RH-292 minimal clock,

    beta_* = log(7/5)/log(10/7)
           = 0.9433582098747317...

This is a sharp information-class law.  The repository has no uniform
moving-order noisy coefficient estimate with this rate, so the bridge
remains open.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf sharp-minimal-clock-prefix-rate.pdf
