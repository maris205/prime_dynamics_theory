# RH-353: Critical--first-lower actual signed-completion gap

RH-353 resolves the actual signed remainders at the two boundary orders
excluded from the RH-352 lower-even ladder.  On the physical clock let

    m=k-1,
    p_k^0=p_(sigma,k,2k),
    p_k^-=p_(sigma,k,2m),

and retain the exact physical identities

    p_k^0=Y_k^0+P_k^0-S_k^0,
    p_k^-=Y_k^-+P_k^--S_k^-.

With `H_l=l R^(-2l)` and `x=(beta R)^2`, define

    Z_k^0=C_M Y_k^0/(2 H_k x^k),
    Z_k^-=C_M Y_k^-/(2 H_m x^m).

The same actual modulus-complement and deterministic all-order bounds used
in RH-352 give

    max(|p_k^0|/(2 H_k x^k), |p_k^-|/(2 H_m x^m)) -> 0

exponentially, with root ceiling

    max(r_H^2 lambda^3/4,1/lambda)<1.

The critical source laws give normalized demand/parity limits `2` and
`gamma_k`, while the first-lower laws give `1` and `gamma_k/lambda`, where

    gamma_k=C_* C_M lambda^(eta_k).

Consequently the actual remainders obey

    Z_k^0=2-gamma_k+o(1),
    Z_k^-=1-gamma_k/lambda+o(1),

and the phase cancels from the cross-order difference:

    Z_k^0-lambda Z_k^- -> 2-lambda > 3/10.

Hence

    liminf max(|Z_k^0|,|Z_k^-|)
      >= (2-lambda)/(1+lambda) > 1/9.

The two-coordinate maximum of the actual boundary remainders therefore
carries an exponentially large unnormalized weighted contribution, although
the maximizing order may vary with `k`.  This is the required signed
supply that cancels the deterministic/parity mismatch at the leading
natural scale.  It is not a lower bound for the direct coefficients
`p_k^0,p_k^-`: their unnormalized target-scale behavior remains open.

The result does not control odd orders, upper aliases, the full `E_off`
aggregate, the RH-241 moving noisy all-order envelope, or head transport.
RH-288 and Gates A--E remain inactive.  No Hilbert--Polya operator,
Riemann-zero identification, von Mangoldt trace, completed-zeta divisor
equality, or proof of RH is claimed.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf critical-first-lower-actual-signed-completion-gap.pdf
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
