# RH-356 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Physical counterloop clock | FROZEN | Same RH-342/RH-355 first-alias clock and finite-radius graded shell. |
| Exact alias budget | PROVED | `A_k=(1-1/k)y_k^k`. |
| Exact post-alias budget | PROVED | `B_k(L)=sum_(j=1)^L y_k^(k+j)/(k+j)` for `1<=L<=k-1`. |
| Exact finite ratio | PROVED | `B/A=[k/(k-1)]sum_(j=1)^L y_k^j/(k+j)`. |
| Uniform mesoscopic law | PROVED | Uniformly for `1<=L<=ell_k`, `ell_k=o(k)`, `B/A=x(x^L-1)/(k(x-1))(1+o(1))`. |
| Multiplier constant at mesoscopic depth | PROVED TO CANCEL | `C_M` disappears because `sup_(j<=ell_k)|y_k^j/x^j-1|->0`. |
| Fixed-depth law | PROVED | For fixed `L`, `kB/A->x(x^L-1)/(x-1)`; the subtraction cannot be dropped. |
| Growing-depth simplification | PROVED WITH BOTH QUANTIFIERS | Only for `L->infinity` and `L=o(k)` may `1-y_k^(-L)` be deleted, giving `B/A=[x/(x-1)]x^(L-log_x k)(1+o(1))`. |
| Mesoscopic crossover | PROVED | The sign/limit of `L-log_x k` gives subcritical, finite, and supercritical regimes. |
| Continuous balance offset | PROVED | `log_x((x-1)/x)`. |
| Integer floor phase | PROVED | For `L=floor(log_x k+c)`, retain `{log_x k+c}` in the leading law. |
| Phase limit set | PROVED | Closed limit set `[0,1]`; liminf `x^c/(x-1)`, limsup `x^(c+1)/(x-1)`, no single limit. |
| Physical order displacement | PROVED | `n-2k=(2/log x)log log(1/sigma)+O(1)`. |
| Actual-head crossover | CONDITIONAL ONLY | Inherited only under the original same-clock unnormalized `D_(4k)(R)->0`. |
| Actual odd post-alias budget | CONDITIONAL ONLY | Tends to zero under the same open hypothesis. |
| Original head-transport leaf | OPEN | RH-356 does not prove `D_(4k)(R)->0`. |
| Linear-depth extension | NOT CLAIMED | Denominator uniformity fails and `C_M` can survive when `L` is proportional to `k`. |
| Direct/full-trace transfer | OPEN | Counterloop/head budgets are not RH-354's `p=tau-a=q-d` budget. |
| RH-241, RH-288, Gates A--E | OPEN | No determinant gluing or Gate promotion follows. |

Finite rational and high-precision rows reproduce formulas only.  A finite
ratio is not certified to lie inside its limiting phase cluster at any
prescribed `k`; the checker tests convergence to the phase law instead.
