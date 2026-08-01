# RH-339: First lower sideband orbit atom compensation obstruction

Every one-alias cut 2k<h<=4k contains the first lower even sideband

    n_minus = 2k-2 = 2m,  m=k-1.

For the actual Hardy full-trace constituent, the corrected RH-334 identity
holds at every n>=2:

    q_(sigma,k,n) = B + S + R + P - A.

At n_minus, the primitive physical boundary orbit of period 2m has a folded
far subset of 2m-1=2k-3 marked points.  Its exact signed subledger is

    R_orb_minus = -D_m_orb,
    D_m_orb = r_H^(-2m) (2m-1)/(1+abs(M_m)).

The multiplier law and the exact beta*R>1 certificate give

    D_m_orb / H_m -> +infinity,
    H_m = m R^(-2m).

Writing the complete signed coefficient as

    q_minus = -D_m_orb + C_minus,

off-alias vanishing necessarily requires

    C_minus = D_m_orb + o(H_m)

at relative precision o((beta R)^(-2m)).  The isolated absolute orbit
contribution to the weighted prefix is D_m_orb/(2H_m), which diverges.
Thus an orbit/complement proof cannot take separate absolute values before
the signed sum.

This is not a lower bound for abs(q_minus).  The complement C_minus includes
the remaining raw cells, parity, and the radial counterloop sideband and may
cancel the atom.  No moving-order estimate for C_minus is available, so both
E_off->0 and E_off nonvanishing remain NOT_TESTABLE.

The exact radial counterloop identity is

    A_(k,2k-2) = 2 (beta^(2k-2)-beta_k^(2k-2)).

No sign is claimed: the physical source proves C_M>0, while its printed
value above one is not an interval certificate.

Finite Decimal rows are reproduction checks only.  No critical-packet,
head/counterloop, determinant, full-trace, Gate A--E, Hilbert--Polya,
Riemann-zero, von Mangoldt, completed-zeta, or RH conclusion is obtained.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf first-lower-sideband-orbit-atom-compensation-obstruction.pdf
