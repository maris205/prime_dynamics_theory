# RH-346: Complete lower-sideband boundary-orbit decomposition

RH-346 completes the physical boundary-orbit extraction at the mandatory
lower sideband

    n_-=2k-2=2m,  m=k-1.

The noise sequence and frozen RH-334 cells remain indexed by `(sigma,k)`.
The symbol `m` is only the period parameter of the lower boundary orbit; it
is not a replacement noise clock.

Let

    Gamma_m = {|f^j(p_(2m))| : 0<=j<2m},
    G_m = r_H^(-2m)/(1+|M_m|).

All `2m` folded marked points are distinct and share multiplier `M_m`.  A
finite set has zero localized noisy trace, so the complete signed raw atom is

    -F_m^orb,  F_m^orb=2m G_m.

The point omitted by RH-339 is

    xi_m=h(p_(2m))<b.

With the same physical windows and

    epsilon_m=1_(xi_m in J^-)=1_(q_(b,m)<=A),

the eventual orbit counts in `(J^-,J^+,F)` are

    (epsilon_m,0,2m-epsilon_m).

Along a fixed physical phase `eta_sigma->eta`, the last-point coordinate has
the shifted limit

    q_(b,m) -> sqrt(C_b) lambda^(1-eta)/(2u_c).

The factor `lambda` is forced by `m=k-1` on the same sigma clock.

Removing the complete orbit from the raw partition gives

    q_(sigma,k,2m)
      = T_(k,m)^rest + P_(sigma,2m)
        - A_(k,2m) - F_m^orb,

and

    p_(sigma,k,2m)
      = T_(k,m)^rest + P_(sigma,2m) - d_(sigma,k,2m)
        - A_(k,2m) - F_m^orb.

Thus direct lower-sideband closure requires

    T_(k,m)^rest + P_(sigma,2m) - d_(sigma,k,2m)
      = A_(k,2m) + F_m^orb + o(H_m).

The RH-339 partial atom is `D_m^orb=(2m-1)G_m`.  Exactly

    F_m^orb/D_m^orb=2m/(2m-1),
    F_m^orb-D_m^orb=G_m,

and the missing point is again super-target:

    G_m/H_m
      = (beta R)^(2m)/(C_M m)(1+o(1)) -> infinity.

The current period-`2k` counterloop contributes the exact radial sideband

    A_(k,2m)=2(beta^(2m)-beta_k^(2m)).

Its sign is not source-locked.  Nevertheless its relative scale is exact:

    A_(k,2m)/F_m^orb
      = (C_M-1)/m + o(1/m) -> 0.

Therefore `F_m^orb+A_(k,2m)` is eventually positive and asymptotic to the
complete orbit atom, but the radial term is not proved target-negligible.

The actual lower parity packet satisfies the shifted leading ratio

    P_(sigma,2m)/F_m^orb
      -> C_* C_M lambda^(eta-1),

which is the RH-347 scalar interface.  RH-346 does not estimate the
orbit-free rest, prove lower compensation or noncompensation, close the rest
of `E_off`, activate determinant gluing, or change Gates A--E.  No
Hilbert--Polya, zero-identification, von Mangoldt, completed-zeta, or RH claim
is made.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf complete-lower-sideband-boundary-orbit-decomposition.pdf
