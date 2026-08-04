# RH-360 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Terminal-lag distribution | PROVED UPSTREAM | Exact `pi_k(r)` from RH-358, supported on `0<=r<=k-2`. |
| Generating function identity | PROVED | `G_k(z)=A_k(z/y_k)/A_k(1/y_k)` with exact finite sum `A_k`. |
| Subcritical transform | PROVED | For fixed `0<=z<x`, `G_k(z)->(1-x^(-1))/(1-z/x)`, locally uniformly below `x`. |
| Critical-window transform | PROVED | For `z_k=x exp(tau/k)`, `G_k(z_k)/k` tends to the stated Riemann integral with drift `tau+log C_M`. |
| Critical value | PROVED | At `z=x`, the leading constant retains `C_M` through `log C_M`; it is not the naive geometric pole. |
| Supercritical transform | PROVED | For fixed `z>x`, `G_k(z)~2 C_M(1-x^(-1))(z/x)^(k-2)/(1-x/z)`. |
| Free-energy law | PROVED | `k^(-1) log G_k(z)->max(0,log(z/x))` for fixed `z>=0`. |
| Subcritical tilted law | PROVED | `pi_(k,z)` converges in total variation to geometric ratio `z/x`. |
| Critical tilted law | PROVED | Under `z_k=x exp(tau/k)`, `r/k` converges weakly to density proportional to `exp[(tau+log C_M)s]/(2-s)`. |
| Supercritical tilted law | PROVED | For `z>x`, `ell=k-2-r` converges in total variation to geometric ratio `x/z`. |
| Conditional actual transform | CONDITIONAL ONLY | Uniform generating-function and tilted-law inheritance requires original same-clock unnormalized `D_(4k)(R)->0`. |
| Same-clock transport leaf | OPEN | RH-360 does not prove `D_(4k)(R)->0`. |
| Spectral interpretation | OPEN/FORBIDDEN | Tilted budget laws are not eigenvalue, root-counting, or noisy stochastic distributions. |
| Direct/full-trace closure | OPEN | No `p,q,E_off` closure or determinant gluing follows. |
| RH-241, RH-288, Gates A--E | OPEN | No moving-envelope, gluing, Hilbert--Polya, zero-identification, or RH promotion follows. |

Finite rows are reproduction checks only.
