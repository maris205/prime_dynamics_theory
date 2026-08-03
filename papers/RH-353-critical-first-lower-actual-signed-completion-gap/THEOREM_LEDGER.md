# RH-353 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Physical clock | FROZEN | One bounded-phase sequence; `m=k-1` is a period parameter, not a second noise clock. |
| Direct coefficient type | SOURCE LOCKED | `p=tau-a=q-d` at both `2k` and `2k-2`. |
| Critical decomposition | SOURCE LOCKED | `p_k^0=Y_k^0+P_k^0-S_k^0`. |
| First-lower decomposition | SOURCE LOCKED | `p_k^-=Y_k^-+P_k^--S_k^-`. |
| Two-order direct natural-scale cap | PROVED | Root ceiling `max(r_H^2 lambda^3/4,1/lambda)<1`. |
| Critical actual completion | PROVED | `C_M Y_k^0/(2H_k x^k)=2-gamma_k+o(1)`. |
| First-lower actual completion | PROVED | `C_M Y_k^-/(2H_m x^m)=1-gamma_k/lambda+o(1)`. |
| Phase-free affine gap | PROVED | `Z_k^0-lambda Z_k^- -> 2-lambda > 3/10`. |
| Uniform two-coordinate minimax | PROVED | `liminf max(|Z_k^0|,|Z_k^-|)>1/9`. |
| Actual boundary signed supply | PROVED | The maximum of the two unnormalized `Y` contributions diverges on the `x^(k-1)` scale; the maximizing order may vary with `k`. |
| Direct critical closure | OPEN | Natural-scale smallness is weaker than `p_k^0=o(H_k)`. |
| Direct first-lower closure | OPEN | Natural-scale smallness is weaker than `p_k^-=o(H_m)`. |
| Full direct prefix and `E_off` | OPEN | Odd, upper-alias, head, and remaining orders are absent. |
| RH-241 moving noisy envelope | OPEN | Two boundary orders are not an all-order envelope or coefficient bridge. |
| RH-288 and Gates A--E | OPEN | No gate is activated. |

Finite rational rows check the affine gap and exact minimax formulas only.
They are not noisy trace observations or asymptotic evidence.
