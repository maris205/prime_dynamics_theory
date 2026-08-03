# RH-347: Lower-sideband scalar balance underdetermination

RH-346 gives the exact direct coefficient at the mandatory lower sideband

    m=k-1,  n_-=2m=2k-2,

in the form

    p_(sigma,k,2m)=Y_m^-+P_(sigma,2m)-S_m^-,

where

    Y_m^-=T_(k,m)^rest-d_(sigma,k,2m),
    S_m^-=F_m^orb+A_(k,2m),
    F_m^orb=2m G_m,
    G_m=r_H^(-2m)/(1+|M_m|).

The combined deterministic demand is eventually positive and satisfies

    S_m^-/F_m^orb -> 1,
    F_m^orb/H_m=(2/C_M)(beta R)^(2m)(1+o(1)),
    H_m=mR^(-2m).

The actual parity packet has the shifted phase law

    P_(sigma,2m)/S_m^-
      -> C_* C_M lambda^(eta-1)

on the same physical `(sigma,k)` clock.  Hence the unique symbolic scalar
balance is

    eta_- = 1-log(C_* C_M)/log(lambda).

This interface is inherited from RH-346.  The new conditional physical
theorem is: if the actual orbit-free remainder and head defect satisfy

    Y_m^-=o(H_m),

then every fixed phase `eta != eta_-` has

    |p_(sigma,k,2m)|/(2H_m)
      = |C_* C_M lambda^(eta-1)-1|/C_M
        * (beta R)^(2m) (1+o(1))
      -> infinity.

This is not an aggregate lower-sideband nonclosure theorem because no source
proves the hypothesis on the actual `Y_m^-`.

At the balance phase, define the exact scalar parity inverse map at order
`2m` by

    delta_m(X)=1-(1-r_H^(2m)X)^(1/(2m)),

for `0<X<r_H^(-2m)`.  On the same clock, with `k=m+1`, take

    P_m^close=S_m^-,
    P_m^far=S_m^-+F_m^orb/m.

Both packets lie in the legal inverse-map domain eventually, and both scalar
eigenvalue sequences satisfy

    delta_m=C_*sqrt(sigma_m)(1+o(1)).

In the scalar information class with `Y_m^-=0`, the close completion has
zero residual, whereas the far completion has

    p_(sigma,k,2m)=F_m^orb/m=2G_m,
    |p_(sigma,k,2m)|/(2H_m)=G_m/H_m -> infinity.

These are scalar completions, not noisy transfer operators.  They prove that
the exact parity-packet form and leading square-root law do not decide
target-scale lower compensation at balance.  The ordinary decimal diagnostic
`eta_- = 4.0609149137...` is not an interval certificate and cannot be used
to rigorously exclude the usual canonical phase window.

Actual lower compensation/noncompensation, the punctured `E_off` aggregate,
head transport, determinant gluing, and Gates A--E remain open.  No
Hilbert--Polya, Riemann-zero, von Mangoldt, completed-zeta, or RH conclusion
is made.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf lower-sideband-scalar-balance-underdetermination.pdf
