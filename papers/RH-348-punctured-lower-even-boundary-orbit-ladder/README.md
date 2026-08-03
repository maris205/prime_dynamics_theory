# RH-348: Punctured lower-even boundary-orbit ladder

RH-348 returns to the punctured one-alias prefix after the selected critical
and first-lower orders have been isolated.  On the same physical noise clock,
fix an eventual multiplier threshold `m_star` and take

    I_k={m_star,...,k-2},  n=2m.

These orders lie strictly below `2k-2`; hence they exclude both selected
orders `2k` and `2k-2` and form a genuine lower-even subfamily of the
punctured prefix.

For every `m in I_k`, let

    Gamma_m={|f^j(p_(2m))|:0<=j<2m},
    G_m=r_H^(-2m)/(1+|M_m|),
    F_m^orb=2m G_m.

Removing the complete finite orbit gives simultaneously

    q_(sigma,k,2m)
      =T_(k,m)^rest+P_(sigma,2m)-A_(k,2m)-F_m^orb,

    p_(sigma,k,2m)
      =Y_(k,m)+P_(sigma,2m)-S_(k,m),

where

    Y_(k,m)=T_(k,m)^rest-d_(sigma,k,2m),
    S_(k,m)=F_m^orb+A_(k,2m),
    A_(k,2m)=2(beta^(2m)-beta_k^(2m)).

Let `x=(beta R)^2>1` and use the prefix weight `R^(2m)/(2m)`.  The exact
orbit ladder is

    L_k^orb=sum_(m_star<=m<=k-2) G_m R^(2m).

The multiplier law yields the strict aggregate asymptotic

    L_k^orb
      =x^(k-1)/(C_M(x-1)) (1+o(1)).

The whole radial ladder is lower order even without a sign theorem:

    sum |A_(k,2m)| R^(2m)/(2m)
      =O(1/k) L_k^orb.

Consequently the absolute combined deterministic demand satisfies

    sum |S_(k,m)| R^(2m)/(2m)
      =L_k^orb(1+o(1)) -> infinity.

This produces an aggregate necessary compensation theorem.  Put

    Z_(k,m)=Y_(k,m)+P_(sigma,2m),
    E_k^low=sum |Z_(k,m)-S_(k,m)| R^(2m)/(2m),
    C_k^low=sum |Z_(k,m)| R^(2m)/(2m).

The reverse triangle inequality gives exactly

    C_k^low >= sum |S_(k,m)|R^(2m)/(2m)-E_k^low.

Therefore vanishing of this direct punctured lower-even subprefix would force
the actual signed supply to carry asymptotically at least the full divergent
orbit-ladder mass.  No repository theorem estimates that supply, so RH-348
does not prove closure or nonclosure of the subprefix or of `E_off`.

Odd orders, orders above the first alias, actual signed compensation, head
transport, determinant gluing, and Gates A--E remain open.  Finite rows are
formula checks only.  No Hilbert--Polya, Riemann-zero, von Mangoldt,
completed-zeta, or RH conclusion is made.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf punctured-lower-even-boundary-orbit-ladder.pdf
