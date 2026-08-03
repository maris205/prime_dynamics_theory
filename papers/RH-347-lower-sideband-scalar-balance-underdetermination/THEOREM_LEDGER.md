# RH-347 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Physical clock | FROZEN | `k=log(1/sigma)/(2log(lambda))+O(1)` remains the noise clock; `m=k-1` is only the lower-orbit period parameter. |
| Exact lower coefficient | INHERITED EXACTLY | RH-346 gives `p=Y_m^-+P_(sigma,2m)-S_m^-`, with `Y_m^-=T_rest-d` and `S_m^-=F_m^orb+A_(k,2m)`. |
| Complete lower demand | INHERITED / PROVED | `S_m^-/F_m^orb->1`, `S_m^->0` eventually, and `F_m^orb/H_m=(2/C_M)(beta R)^(2m)(1+o(1))->infinity`. |
| Shifted actual parity law | INHERITED / PROVED | At fixed physical phase, `P_(sigma,2m)/S_m^- -> C_*C_M lambda^(eta-1)`. |
| Unique lower scalar balance | INHERITED INTERFACE | `eta_-=1-log(C_*C_M)/log(lambda)` is the unique symbolic phase with leading ratio one. |
| Conditional physical off-balance obstruction | PROVED | If the actual `Y_m^-=o(H_m)` and `eta!=eta_-`, then `|p|/(2H_m)` diverges with coefficient `|C_*C_M lambda^(eta-1)-1|/C_M`. |
| Aggregate lower nonclosure | NOT CLAIMED | The required actual theorem `Y_m^-=o(H_m)` is absent. |
| Balance target precision | PROVED NECESSARY | Under `Y_m^-=o(H_m)`, scalar closure requires `P=S_m^-+o(H_m)`, equivalently relative `o((beta R)^(-2m))`. |
| Source precision at balance | INSUFFICIENT | The available parity phase law has relative `o(1)` only. |
| Exact order-`2m` inverse parity map | PROVED EXACTLY | Every `0<X<r_H^(-2m)` has `delta_m(X)=1-(1-r_H^(2m)X)^(1/(2m))` and exact packet `X`. |
| Legal domain for both completions | PROVED EVENTUALLY | `r_H^(2m)P_m^close` and `r_H^(2m)P_m^far` lie in `(0,1)` for all large `m`, with `k=m+1`. |
| Close scalar completion | PROVED | `P_m^close=S_m^-` gives zero residual when `Y_m^-=0`. |
| Far scalar completion | PROVED | `P_m^far=S_m^-+F_m^orb/m` gives residual `F_m^orb/m=2G_m`. |
| Common square-root law | PROVED | Both scalar sequences satisfy `delta_m=C_*sqrt(sigma_m)(1+o(1))` on the same balance clock. |
| Far weighted divergence | PROVED | The far weighted term equals `G_m/H_m=(beta R)^(2m)/(C_Mm)(1+o(1))->infinity`. |
| Actual parity eigenvalue realization | NOT CLAIMED | The scalar sequences are not identified with the actual noisy operator's parity eigenvalue. |
| Decimal phase location | DIAGNOSTIC ONLY | `eta_-≈4.0609149137` is not an interval certificate and does not rigorously exclude the canonical phase window. |
| Scalar-only route verdict | STOP_SCOPED | Off balance it fails conditionally; at balance the proved scalar information is underdetermined. |
| Actual lower compensation | NOT_TESTABLE / OPEN | No moving-order theorem estimates the signed physical `Y_m^-`. |
| Punctured off-alias aggregate | NEXT ROUTE | RH-348 must control the remaining strict-prefix orders jointly or isolate another physical sideband atom. |
| RH-288 and Gates A--E | OPEN | No determinant-gluing or Gate hypothesis is activated. |
