# RH-346 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Same physical noise clock | FROZEN | `k=log(1/sigma)/(2log(lambda))+O(1)` remains the noise clock; `m=k-1` is only the lower-orbit period parameter. |
| Mandatory sideband order | PROVED EXACTLY | `n_-=2m=2k-2` lies in every one-alias strict prefix. |
| Complete folded lower orbit | PROVED / SOURCE LOCKED | `Gamma_m={|f^j(p_(2m))|:0<=j<2m}` has exactly `2m` distinct marked points. |
| Per-point Hardy weight | PROVED EXACTLY | `G_m=r_H^(-2m)/(1+|M_m|)`. |
| Complete signed raw atom | PROVED EXACTLY | `F_m^orb=2mG_m` enters the raw coefficient as `-F_m^orb`. |
| Cellwise allocation | PROVED EVENTUALLY | With `epsilon_m=1_(xi_m in J^-)`, counts in `(J^-,J^+,F)` are `(epsilon_m,0,2m-epsilon_m)`. |
| Shifted fixed-phase location | PROVED | `q_(b,m)->sqrt(C_b)lambda^(1-eta)/(2u_c)` on the same sigma clock. |
| Threshold equality | NOT DETERMINED | The available `o(1)` expansion does not decide stabilization when the limit equals `A`. |
| Orbit-free raw decomposition | PROVED EXACTLY | `T_(sigma,2m)=T_(k,m)^rest-F_m^orb`. |
| Full-trace sideband identity | PROVED EXACTLY | `q=T_rest+P-A_(k,2m)-F_m^orb`. |
| Direct sideband identity | PROVED EXACTLY | `p=T_rest+P-d-A_(k,2m)-F_m^orb`. |
| Direct lower compensation demand | PROVED NECESSARY | `p=o(H_m)` iff `T_rest+P-d=A_(k,2m)+F_m^orb+o(H_m)`. |
| RH-339 partial atom relation | PROVED EXACTLY | `D_m^orb=(2m-1)G_m`, `F_m^orb/D_m^orb=2m/(2m-1)`, and `F_m^orb-D_m^orb=G_m`. |
| Missing-point target scale | PROVED | `G_m/H_m=(beta R)^(2m)/(C_Mm)(1+o(1))->infinity`. |
| Complete atom target scale | PROVED | `F_m^orb/H_m=(2/C_M)(beta R)^(2m)(1+o(1))->infinity`. |
| Exact radial sideband | INHERITED EXACTLY | `A_(k,2m)=2(beta^(2m)-beta_k^(2m))`. |
| Radial sign | NOT CLAIMED | The repository proves `C_M>0` but does not certify its relation to one. |
| Radial/full relative law | PROVED | `A_(k,2m)/F_m^orb=(C_M-1)/m+o(1/m)->0`. |
| Radial target negligibility | NOT CLAIMED | Relative `o(1)` against the orbit atom does not imply `o(H_m)`. |
| Combined lower demand | PROVED | `F_m^orb+A_(k,2m)` is eventually positive and has ratio one to `F_m^orb`. |
| Shifted parity interface | PROVED | At fixed phase, `P_(sigma,2m)/F_m^orb->C_*C_M lambda^(eta-1)`. |
| Actual lower compensation | NOT_TESTABLE / OPEN | No moving-order theorem estimates the signed orbit-free rest and head defect. |
| Remaining off-alias aggregate | NOT_TESTABLE / OPEN | One selected sideband does not close `E_off,(4k)`. |
| RH-288 and Gates A--E | OPEN | No determinant-gluing or Gate condition is activated. |
