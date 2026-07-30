# RH-299: Zero-padded root-l1 bridge clock

Finite noisy heads and counterloop shells need not have the same cardinality.
Pad the smaller multiset with zeros and minimize the root-l1 matching cost
d_1.  If both padded multisets lie in the disk of radius B, then

    |sum x_j^n - sum y_j^n| <= n B^(n-1) d_1

and therefore

    D_m(R) <= d_1 R sum_(j=1)^(m-2) (BR)^j.

For BR>1 and m=ceil(a log(1/sigma)), the displayed Lipschitz bound
guarantees decay for a power cost d_1=O(sigma^gamma) when

    gamma > a log(BR).

A one-pair radial perturbation proves sharpness within this disk-bounded
information class: equality can stay of order one and every smaller exponent
can diverge.

At the RH-292 minimal clock and the limiting shell radius
beta=(0.85 sqrt(lambda))^(-1), the local-shell threshold is

    gamma_* = 0.6729348509145321....

Using only the global Hardy-scaled cap B=1/0.85 raises it to
1.399008185460602....  No actual root-l1 matching theorem for the
modulus-complete noisy head is present, so D_sigma remains open.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf zero-padded-root-l1-bridge-clock.pdf
