# RH-348 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Physical clock | FROZEN | The noise sequence remains `k=log(1/sigma)/(2log(lambda))+O(1)`. |
| Punctured lower-even index set | PROVED | `m_star<=m<=k-2`, hence `n=2m` excludes `2k` and `2k-2` and lies in every one-alias strict prefix. |
| Complete folded orbit at each order | SOURCE LOCKED | `Gamma_m` has `2m` distinct folded marked points for every ladder order. |
| Exact full atom | PROVED | `F_m^orb=2mG_m`, `G_m=r_H^(-2m)/(1+|M_m|)`, enters the raw coefficient with a minus sign. |
| Simultaneous full-trace ladder | PROVED EXACTLY | `q=T_rest+P-A-F_m^orb` at every `m` in the ladder. |
| Simultaneous direct ladder | PROVED EXACTLY | `p=Y+P-S`, with `Y=T_rest-d` and `S=F_m^orb+A_(k,2m)`. |
| Orbit weighted identity | PROVED EXACTLY | `F_m^orb R^(2m)/(2m)=G_mR^(2m)`. |
| Superunit ladder ratio | INHERITED / CERTIFIED | `x=(beta R)^2>1`. |
| Orbit aggregate asymptotic | PROVED | `L_k^orb=x^(k-1)/(C_M(x-1))(1+o(1))`. |
| Radial aggregate | PROVED | Its absolute weighted mass is `O(1/k)L_k^orb`; no radial sign is used. |
| Combined deterministic demand | PROVED | Its absolute weighted mass is `L_k^orb(1+o(1))->infinity`. |
| Aggregate reverse-triangle law | PROVED EXACTLY | `supply_mass + residual_mass >= demand_mass`. |
| Necessary compensation mass | PROVED | Vanishing residual subprefix forces supply mass divided by `L_k^orb` to have liminf at least one. |
| Actual supply estimate | NOT_TESTABLE / OPEN | The repository has no moving-order signed theorem for the orbit-free rest, parity, and head supply together. |
| Punctured lower-even closure/nonclosure | NOT CLAIMED | A divergent demand can be cancelled coefficientwise; no actual supply bound is available. |
| Full `E_off` | OPEN | Odd orders and orders above the first alias are outside this theorem. |
| Finite diagnostics | REPRODUCTION ONLY | Decimal rows check formulas and are not interval certificates or asymptotic evidence. |
| RH-288 and Gates A--E | OPEN | No determinant-gluing or Gate condition is activated. |
