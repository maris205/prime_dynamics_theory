# TPC-59: Critical very-high cutoffs and cofactor occupancy

This directory contains the source and final PDF for:

> *Critical Very-High Cutoffs and Cofactor Occupancy at a Fixed Shift:
> Cutoff-Band Reciprocity, Sharp Projection Minimax, and Dyadic
> Localization*

## Core route correction

TPC-58 used the convenient cutoff

    y = X^(267/400+eta),  eta > 0 fixed,

which forces every very-high terminal cofactor into

    r <= X^(133/400-eta+o(1)).

TPC-59 proves that this positive-power displacement is not forced by the
literal TPC-45 decomposition. Its exact inequalities already admit

    y = C_vh Q,  Q = X^(267/400+o(1)),

for a fixed support-dependent constant. If omega_X = y/Q, then

    R_safe = N_-/(2y) ~ J/omega_X,
    R_max  = N_+/y    ~ J/omega_X.

Thus the critical choice omega_X ~ 1 restores geometric compatibility
with the inherited exponent R ~ J = X^(133/400+o(1)). It does not create
cofactor labels or move energy between them.

## Exact occupancy and activation constants

The literal pre-terminal coefficient has no cofactor dependence:

    [G_X^L]_(m,r,j,gamma) = c_(m,j,gamma) zeta_m.

For a fixed cofactor set Rset, define N(m) as the total retained cofactor
multiplicity in row m, N_Rset(m) as its retained multiplicity inside Rset,
and

    B_m = sum_(j,gamma) |c_(m,j,gamma)|^2.

The sharp constant uniform over the bounded row-coefficient cube is

    beta_Rset
      = min_(m:B_m N(m)>0) N_Rset(m)/N(m).

The paper gives analogous exact rowwise formulas for terminal activation
tau_Rset and the combined parent-to-terminal constant chi_Rset, with

    chi_Rset >= beta_Rset tau_Rset.

All three constants may be zero under the inherited hypotheses. This
separates cutoff compatibility, actual cofactor occupancy, and terminal
prime activation.

## Largest-prime census and dyadic localization

Because y > sqrt(N_+), every very-high terminal target has a unique prime

    p = P^+(mj+h0),  r = (mj+h0)/P^+(mj+h0).

The paper gives the exact retained-pair and terminal-mask census for these
atoms. Their raw atomic energy partitions exactly into O(log X) dyadic
cofactor cells. Conditional on nonzero very-high terminal energy, one
canonical maximal cell retains an X^(-o(1)) fraction. Hence

    lambda_blk = 0

after high-face activation. This is not a parent-to-high-face theorem.

## Undeleted singleton interface

For a selected very-high root cell, let D_R be its raw terminal energy and
let I_R^full be the coefficient-weighted rooted collision incidence
computed in the complete terminal vector. Then

    min(G_H, G_full) >= max(D_R - I_R^full, 0).

Every full-fiber partner of a root with r in [R,2R) lies in [R/2,4R).
This localizes the remaining collision estimate to three adjacent dyadic
cells, but does not prove a positive singleton fraction. In particular,
factor exchange cannot transport an old R ~ J atom across the fixed-power
gap created by a fixed positive eta.

## Endpoint audit

Writing omega_X = X^(xi+o(1)), the largest compatible exponent is

    theta_c(xi) = 133/400 - xi.

On every compatible block, the inherited support-only capacity certificate
has exponent at least

    15077/105000 + xi,

which exceeds the 1/400 allowance by

    29629/210000 + xi.

The automatic-singleton threshold misses the compatible ceiling by

    55273/105000 + xi.

Therefore xi=0 is support-optimal, but the existing support-only singleton
shortcuts still cannot close the endpoint.

TPC-59 retires the older relocation entry in favor of an ordered
feasibility/energy distinction:

    cutoff feasibility prerequisite -> lambda_occ.

At the critical cutoff, the feasibility gate is open at exponent R ~ J;
this is not an additive energy exponent. TPC-59 proves lambda_blk = 0 after
high-face activation. Occupancy, terminal activation, weighted singleton
survival, the native and affine Gram constants, missing-high/off-carrier
reassembly, boundary control, and tail reconnection remain separate gates,
and their total loss must satisfy

    Lambda_tot < 1/400.

## Claim boundary

The minimax laws and finite support identities are L0. Their exact
specialization to the literal raw atoms at one fixed nonzero shift is L1.
The paper is a genuine L1 route correction: it removes an artificial
positive-power cutoff displacement and identifies the exact constants that
replace it. It proves no positive fixed-shift arithmetic lower square, no
parity improvement, and no twin-prime consequence.

## Build

Run pdflatex, bibtex, and two further pdflatex passes in this directory.
The archived PDF is
critical-very-high-cutoffs-cofactor-occupancy.pdf.
