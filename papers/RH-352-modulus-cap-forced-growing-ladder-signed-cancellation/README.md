# RH-352: Modulus-cap-forced growing-ladder signed cancellation

RH-352 supplies an actual moving-order theorem on the RH-350 triangular
lower-even window.  Let

    m_(k,j)=k-j,  2<=j<=J_k,
    J_k->infinity,  J_k=o(k),

and retain the direct physical coefficient identities

    p_(k,j)=tau_(sigma,2m)-a_(2m)
           =Y_(k,j)+P_(k,j)-S_(k,j).

With

    H_m=m R^(-2m),  R=7/5,
    beta=(r_H sqrt(lambda))^(-1),
    x=(beta R)^2,

define the local natural-scale cap and the selected normalized budget

    U_k=max_j |p_(k,j)|/(2 H_m x^m),
    L_k^act=x^(-(k-2)) sum_j |p_(k,j)|/(2 H_m).

The source-backed bounds

    |tau_(sigma,n)| <= sigma^(-1) q^(n-2),  q=1/2,
    |a_n| < 48 q_*^n,  q_*=(r_H lambda)^(-1),

give

    limsup U_k^(1/k) <= max(rho_N,rho_T) < 1,
    rho_N=r_H^2 lambda^3/4 < 1419857/1600000,
    rho_T=1/lambda < 1.

Consequently the same root ceiling holds for L_k^act, so the actual direct
budget tends to zero exponentially at the normalized selected scale.  Since

    Y=S-P+p,

RH-350's uniform S/P laws now force

    max_j | C_M Y_(k,j)/(2 H_m x^m)
            -(1-a_k lambda^(2-j)) | -> 0.

The actual Y budget therefore satisfies

    Yagg_k^act=F_(J_k-2)(a_k)/C_M+o(1),

and has liminf at least

    A_infinity/C_M
      =[1/(x-1)-1/(x lambda-1)]/C_M > 0.

Thus the actual branch asymptotically selects the close signed completion at
this local/natural normalization, and RH-350's aggregate small-Y hypothesis
is unconditionally false.

This does not prove that the unnormalized selected prefix tends to zero.
Indeed, the noisy separate-modulus cap on that scale has root

    lambda^2(qR)^2 > (28/17)^2(7/10)^2
                   =9604/7225 > 1.

It also does not control the critical or first-lower orders, odd orders,
upper aliases, the full E_off aggregate, or the RH-241 moving noisy all-order
envelope.  RH-288 and Gates A--E remain inactive.  No Hilbert--Polya
operator, Riemann-zero identification, von Mangoldt trace, completed-zeta
divisor equality, or proof of RH is claimed.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf modulus-cap-forced-growing-ladder-signed-cancellation.pdf
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
