# TPC-364 paper plan

## Question

Can the first high-shell failure isolated by TPC-362 and shown to persist in
TPC-363 be changed by a simple, explicitly declared prime-shell tilt, without
using a source response or an adaptive sign law?

## Frozen finite protocol

- origins: `(313030,311166,321651)`, inherited from TPC-361;
- counts: `256,512`;
- shell anchors: `Q=80,128,256,512`;
- kernel exponents: `1,2`;
- sign laws: `all_plus`, `alternating_index`, `mod4_character`, `half_split`;
- tilt menu: `beta in {-2,-1,0,1,2}`;
- block weight: `w_(p,beta)=(p/Q)^beta`;
- weighted geometry: `G_(beta,u)=sum_(p,t)(w_(p,beta)B_p(u,t))^2`;
- normalized matrix: `D_G^(-1/2) A_beta D_G^(-1/2)`.

The full Cartesian product has `960` law rows.  The inherited spectral value
`0.64` is used only as a finite working cap.  The complete menu is reported;
the best beta is not treated as an independent holdout.

## Claim discipline

The exact contribution is the finite weighted-block definition, positivity of
the weighted geometry diagonal, and the standard finite Schur/Frobenius
envelopes.  The numerical contribution is a complete all-law phase diagram.
Any beta=2 cap repair is a finite scoped observation.  It is not an
asymptotic operator estimate, an arithmetic `L2` theorem, a Route-A/Route-B
pass, a fixed-power saving, or a twin-prime result.

## Next experiment

TPC-365 must test beta=2 on a response-blind, disjoint fresh-origin holdout.
If transfer fails, the finite repair is a panel artifact or a normalization
obstruction; if it transfers, the next work must attack scale growth and
source validity rather than silently promote it to a theorem.
