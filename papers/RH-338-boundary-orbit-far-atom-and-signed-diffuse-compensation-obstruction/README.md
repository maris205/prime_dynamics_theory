# RH-338: Boundary-orbit far atom and signed diffuse compensation obstruction

RH-338 works in the corrected physical basepoint data type of RH-334.  For
fixed A>0, its windows are

    J_minus = [0,1] intersect [b-A*sqrt(sigma), b),
    J_plus  = [0,1] intersect [b, b+A*sqrt(sigma)],
    F       = [0,1] minus (J_minus union J_plus).

Let p_(2k) be the primitive RH-17 boundary orbit and delete only the folded
marked point at time 2k-2, namely h(p_(2k)).  The remaining set Omega_k has
2k-1 points.  Three fixed physical gaps prove that Omega_k is contained in F
for every fixed A and all sufficiently small noise:

- p_(2k) is at least p_1>b;
- every other retained even component point is at most h(b)<b;
- every odd folded point is at most r<b.

Absolute-value folding preserves the multiplier and marked-point
multiplicity.  Since a finite set has zero multiplication operator on L2,
the noisy localized trace on Omega_k is exactly zero.  The deterministic
orbit mass is

    D_orb,k = r_H^(-2k) (2k-1)/(1+abs(M_k)),

so the signed far subledger is exactly

    R_orb,k = -D_orb,k.

Omega_k is an analytic subpartition of the already-frozen far set, not a new
canonical physical window or a fitted observation coefficient.

The physical multiplier law gives

    D_orb,k = (2k/C_M) beta^(2k) (1+o(1)),
    D_orb,k / A_(k,2k) -> 1,
    D_orb,k / H_k -> +infinity.

This is a physical alias-sized negative atom, not an aggregate far verdict.
Writing

    R_k = R_orb,k + R_rest,k,

aggregate closure would require

    R_rest,k = D_orb,k + o(H_k)

at relative precision o((beta R)^(-2k)).  No moving-order estimate for the
diffuse rest is available.  Consequently aggregate R_k=o(H_k) and aggregate
nonvanishing are both NOT_TESTABLE.  The atom/rest route cannot close by
separate absolute summation, but signed cancellation remains possible.

The Decimal rows at k=2,4,8,16,32 and A=1/4 reproduce orbit counts and scale
ratios only.  They are not interval certificates or asymptotic evidence.

No actual/model Delta_R is activated, and no result closes parity--alias,
off-alias, head/counterloop, determinant, or Gate A--E obligations.  The
paper constructs no Hilbert--Polya operator, identifies no Riemann zero,
proves no von Mangoldt trace formula or completed-zeta divisor equality, and
does not prove RH.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf boundary-orbit-far-atom-and-signed-diffuse-compensation-obstruction.pdf
