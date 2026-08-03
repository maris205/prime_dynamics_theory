# RH-349 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Physical clock | FROZEN | `k=log(1/sigma)/(2log(lambda))+O(1)` and `eta_sigma->eta`. |
| Two sideband indices | PROVED / FIXED | `m_j=k-j` for exactly `j=2,3`; both lie in the punctured lower-even ladder. |
| Exact direct identities | PROVED EXACTLY | `p_j=Y_j+P_j-S_j`, preserving the noisy-head/counterloop defect inside `Y_j`. |
| Fixed-sideband demand scale | PROVED | `S_j=(2m_j/C_M)beta^(2m_j)(1+o(1))` for each fixed `j`. |
| Target scale | FROZEN | `H_(m_j)=m_jR^(-2m_j)` and `x=(beta R)^2>1`. |
| Fixed-phase parity ratios | PROVED | `P_j/S_j->gamma_j=C_*C_M lambda^(eta-j)`. |
| Phase separation | PROVED EXACTLY | `gamma_3=gamma_2/lambda`; one positive scalar cannot equal one at both coordinates. |
| Actual remainder hypotheses | UNPROVED / EXPLICIT | The theorem assumes both `Y_2=o(H_(m_2))` and `Y_3=o(H_(m_3))`. |
| Coordinate target law | PROVED CONDITIONALLY | Under the corresponding actual hypothesis, `W_j/x^(m_j)->|gamma_j-1|/C_M`. |
| Relative minimax | PROVED EXACTLY | The infimum is `(lambda-1)/(lambda+1)` at `a=2lambda/(lambda+1)`. |
| Physical weighted minimax | PROVED EXACTLY | The infimum is `1-1/lambda` at `a=1`, using `x>1`. |
| Two-order divergence | PROVED CONDITIONALLY | Under both actual hypotheses, `(W_2+W_3)/x^(k-3)` tends to a strictly positive explicit constant. |
| Bounded-phase lower law | PROVED CONDITIONALLY | Without phase convergence, bounded `eta_sigma` and the same two hypotheses give liminf at least `(1-1/lambda)/C_M`. |
| Unconditional physical nonclosure | NOT CLAIMED | Neither actual remainder hypothesis is available in the repository. |
| Full `E_off` | OPEN | No unconditional aggregate verdict, odd-order control, or upper-alias control is supplied. |
| Growing-depth ladder | OPEN | All statements here use only the two fixed indices `j=2,3`. |
| Finite diagnostics | REPRODUCTION ONLY | `Y_2=Y_3=0` is a fixture, not an actual-remainder observation. |
| RH-288 and Gates A--E | OPEN | No determinant-gluing or Gate condition is activated. |
