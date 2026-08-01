# RH-344: Complete critical boundary-orbit atom decomposition

RH-344 completes the physical boundary-orbit extraction at the critical order
`n=2k`.  RH-338 isolated `2k-1` folded marked points in the frozen far cell.
The remaining marked point

    xi_k = h(p_k) < b

has phase-dependent membership in `J^-` or `F`, but it cannot be discarded at
the target scale.

Let

    Gamma_k = {|f^j(p_k)| : 0<=j<2k},
    G_k = r_H^(-2k)/(1+|M_k|).

The `2k` folded points are distinct, all have multiplier `M_k`, and a finite
set has zero localized noisy trace.  Therefore the complete raw orbit atom is

    F_k^orb = 2k G_k
            = r_H^(-2k) 2k/(1+|M_k|),

with signed raw contribution `-F_k^orb`.

For the frozen RH-334 cells, put

    epsilon_k = 1_(xi_k in J^-) = 1_(q_b<=A).

Eventually the complete orbit counts in `(J^-,J^+,F)` are exactly

    (epsilon_k, 0, 2k-epsilon_k).

If the full orbit is removed before evaluating the deterministic rest, the
three physical slots satisfy

    B_k = B_k^rest - epsilon_k G_k,
    S_k = S_k^rest,
    R_k = R_k^rest - (2k-epsilon_k)G_k.

Thus, with `T_k^rest=B_k^rest+S_k^rest+R_k^rest`,

    q_(sigma,k,2k)
      = T_k^rest + P_(sigma,2k) - A_(k,2k) - F_k^orb,

and the direct coefficient is

    p_(sigma,k,2k)
      = T_k^rest + P_(sigma,2k) - d_(sigma,k,2k)
        - A_(k,2k) - F_k^orb.

Consequently critical direct closure requires the exact signed compensation

    T_k^rest + P_(sigma,2k) - d_(sigma,k,2k)
      = A_(k,2k) + F_k^orb + o(H_k).

The new scale point is strict.  If `D_k^orb=(2k-1)G_k` is the RH-338 far
atom, then

    F_k^orb/D_k^orb = 2k/(2k-1),
    F_k^orb-D_k^orb = G_k,

but

    G_k/H_k
      = (beta R)^(2k)/(C_M k) (1+o(1)) -> infinity.

Hence `F_k^orb=D_k^orb(1+o(1))` cannot be strengthened to
`F_k^orb=D_k^orb+o(H_k)`.  Moreover

    F_k^orb/A_(k,2k) -> 1,
    (A_(k,2k)+F_k^orb)/A_(k,2k) -> 2.

This is an exact physical raw-partition decomposition and a necessary
double-alias-sized compensation demand.  It does not estimate the orbit-free
rest or the head defect, and it proves neither critical closure nor
nonclosure.  The actual strict prefix, determinant gluing, Gates A--E,
Hilbert--Polya construction, Riemann-zero identification, von Mangoldt trace,
completed-zeta divisor equality, and RH all remain open.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf complete-critical-boundary-orbit-atom-decomposition.pdf
