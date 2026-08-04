# RH-359 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Terminal-tail ledger | PROVED UPSTREAM | `E_k(q)=P_k(q)/C_k`, `0<=q<=k-2`, from RH-358. |
| Log-window uniformity | PROVED | For each fixed `A>0`, `sup_(0<=q<=A log k) |x^q E_k(q)-1| -> 0`. |
| Polynomial phase law | PROVED | For `q=floor(a log(k)/log(x)+c)`, `k^a E_k(q)=x^(theta_k-c)(1+o(1))`. |
| Complete logarithmic phase set | PROVED | For every `a>0`, real `c`, `{a log_x(k)+c}` has limit set `[0,1]`. |
| Error cluster interval | PROVED | The complete limit set of `k^a E_k(q)` is `[x^(-c),x^(1-c)]`; no unique constant exists. |
| Polynomial exponent classification | PROVED | If `q=o(k)` and `q log(x)/log(k)->a`, then `log E_k(q)/log(k)->-a`. |
| Superpolynomial sublinear regime | PROVED | If `q=o(k)` and `q/log(k)->infinity`, then `E_k(q)=o(k^(-A))` for every fixed `A>0`. |
| Exact minimal accuracy width | DEFINED | `Q_k(a,c)=min{q:E_k(q)<=x^(-c)k^(-a)}` exists eventually by strict tail monotonicity. |
| Minimal-width first order | PROVED | `Q_k(a,c)=a log(k)/log(x)+c+O(1)`. |
| Minimal-width correction set | PROVED | The complete limit set of `Q_k(a,c)-[a log(k)/log(x)+c]` is `[0,1]`. |
| Generic integer selection | PROVED WITH PHASE MARGIN | If the floor phase stays in a compact subset of `(0,1)`, then `Q_k=ceil(a log_x(k)+c)` eventually. |
| Physical double-log width | PROVED | On the RH-355 clock, logarithmic-in-`k` width is logarithmic in `log(1/sigma)`, with no unique integer constant. |
| Actual-head inheritance | CONDITIONAL ONLY | Phase, exponent, and minimal-width conclusions transfer only under the original same-clock unnormalized `D_(4k)(R)->0`. |
| Same-clock transport leaf | OPEN | RH-359 does not prove `D_(4k)(R)->0`. |
| Root/rank/determinant identification | OPEN | No actual spectral or determinant theorem is supplied. |
| Direct/full-trace closure | OPEN | The window integer `q` is not the open direct/full-trace `q`; no `p,q,E_off` closure follows. |
| RH-241, RH-288, Gates A--E | OPEN | No moving-envelope, gluing, Hilbert--Polya, zero-identification, or RH promotion follows. |

Finite rows are reproduction checks only and never replace the all-order
proofs.
