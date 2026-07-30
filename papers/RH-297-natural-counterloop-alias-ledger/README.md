# RH-297: Natural counterloop alias ledger

Tie the counterloop period to the intrinsic RH-16 endpoint-resolution clock

    k_sigma = log(1/sigma)/(2 log(lambda)) + O(1).

Then the alias orders have logarithmic slopes

    2k : 1/log(lambda) = 1.930709419...,
    4k : 2/log(lambda) = 3.861418838...,
    6k : 3/log(lambda) = 5.792128258....

Consequently, for all sufficiently small noise,

    2k_sigma < h_sigma < 4k_sigma < m_sigma < 6k_sigma,

where h_sigma is the RH-292 minimal bridge clock and
m_sigma=ceil(4 log(1/sigma)).  The shortened bridge crosses exactly one
counterloop alias; the original slope-four bridge crosses exactly two.

At alias n=2 ell k, the exact shell moment contributes

    (1-1/k)/ell * (beta_k R)^(2 ell k)

to the absolute weighted ledger.  Since beta R=1.2712733045...>1, the first
and second limiting-radius impulses grow respectively like
sigma^(-0.4634069445+o(1)) and
sigma^(-0.9268138890+o(1)).

These impulses may be cancelled by an actual noisy aggregate; RH-297 does
not prove failure of E or D.  It proves that a natural-rank theorem must be
alias-inclusive rather than reusing only the pre-alias formula.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf natural-counterloop-alias-ledger.pdf
