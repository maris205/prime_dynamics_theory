# RH-358 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Physical multiplier and Hardy normalization | FROZEN | RH-17/RH-342 lock (y_k=x\exp[-\log C_M/k+o(k^{-1})]), with (x>1). |
| Complete strict upper budget | PROVED UPSTREAM | (C_k=B_k(k-1)), from RH-355/RH-357. |
| Terminal-lag partial budget | DEFINED EXACTLY | (P_k(q)=B_k(k-1-q)), (0\le q\le k-2). |
| Terminal-lag probability | DEFINED EXACTLY | (pi_k(r)=y_k^{2k-1-r}/[(2k-1-r)C_k]), (0\le r\le k-2). |
| Exact tail identity | PROVED | (P_k(q)/C_k=\sum_{r=q}^{k-2}\pi_k(r)). |
| Uniform finite-radius tail profile | PROVED | (P_k(q)/C_k=y_k^{-q}(2k-1)(1-y_k^{-(k-1-q)})/[(2k-1-q)(1-y_k^{-(k-1)})](1+O(k^{-1}))), uniformly in (q). |
| Uniform source-locked tail profile | PROVED | Replace (y_k^{-q}) by (x^{-q}C_M^{q/k}) and both finite-tail factors by their (x)-forms, with uniform relative (o(1)). |
| Sublinear lag law | PROVED | If (q=o(k)), then (P_k(q)/C_k=x^{-q}(1+o(1))). |
| Linear lag law | PROVED | If (q/k\to\theta\in[0,1)), then (P_k(q)/C_k\sim[2C_M^\theta/(2-\theta)]x^{-q}). |
| Fixed residual-depth endpoint | PROVED | If (q=k-1-\ell), fixed (ell\ge1), then (P_k(q)/C_k\sim2C_Mx^{-q}(1-x^{-\ell})). |
| Geometric localization | PROVED | Extended by zero off its finite support, (pi_k\to(1-x^{-1})x^{-r}) in (ell^1), hence in total variation. |
| Lag moments | PROVED | (mathbb E_k r\to1/(x-1)), (operatorname{Var}_k(r)\to x/(x-1)^2). |
| Fixed terminal window | PROVED | Its retained mass tends to (1-x^{-q}); fixed width never captures all mass. |
| Vanishing truncation criterion | PROVED | For arbitrary admissible (q_k), (P_k(q_k)/C_k\to0) iff (q_k\to\infty). |
| Actual-head inheritance | CONDITIONAL ONLY | Even-weight tail ratios, uniform coordinatewise lag weights, total variation, and the first two moments inherit only under the original same-clock unnormalized (D_{4k}(R)\to0). |
| Same-clock transport leaf | OPEN | RH-358 does not prove (D_{4k}(R)\to0). |
| Actual root/rank identification | OPEN | No actual-head root, rank, or spectral theorem is supplied. |
| Determinant and direct/full-trace closure | OPEN | The terminal integer (q) is not the open (q/E_{\rm off}) budget; no (p,q,E_{\rm off}) closure follows. |
| RH-241, RH-288, Gates A--E | OPEN | No moving-envelope or determinant-gluing promotion follows. |

All finite rows are formula-reproduction checks.  They are not asymptotic
evidence replacing the proofs, physical interval certificates, or actual
noisy-head observations.
