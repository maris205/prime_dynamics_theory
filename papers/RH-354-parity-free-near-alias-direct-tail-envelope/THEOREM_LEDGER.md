# RH-354 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Physical clock | FROZEN | One bounded-phase sequence with `sigma_k^(-1)=lambda^(2(k-eta_k))`. |
| Direct coefficient type | SOURCE LOCKED | `p_(sigma,k,n)=tau_(sigma,n)-a_n=q_(sigma,k,n)-d_(sigma,k,n)` at every finite order. |
| Noisy all-order cap | SOURCE LOCKED | `|tau_(sigma,n)|<=sigma^(-1) q^(n-2)` for every `n>=2`. |
| Deterministic all-order cap | SOURCE LOCKED | `|a_n|<48 q_*^n` for every `n>=2`, odd and even. |
| Bottom-normalized full direct tail | PROVED | For `N_k=2k-L_k`, the complete tail from `N_k` has the explicit two-rate majorant. |
| Sublinear-depth root law | PROVED | If `L_k=o(k)`, the full direct tail has root ceiling `rho_N<1419857/1600000<1`. |
| Complete near-alias logarithmic band | PROVED | `x^(-k) sum_(N_k<=n<4k) |p_n|R^n/n` decays with the same root ceiling. |
| Full logarithmic direct tail | PROVED | The same alias-clock conclusion holds with `n>=N_k`. |
| Odd/even and upper-alias coverage | PROVED AT DIRECT TYPE | No parity or alias decomposition is used; every order above the moving cut is included only as `p=tau-a`. |
| Linear-depth thresholds | PROVED | Exact noisy frontiers `alpha_nat` and `alpha_alias`; the target rate is not the active frontier. |
| Critical alias-threshold convergence | PROVED | `L_k=alpha_alias k+O(1)` gives an `O(k^(-1))` source upper bound, not exponential decay. |
| Unnormalized modulus-cap route | STOP_SCOPED | Its separate noisy majorant has superunit root `lambda^2(qR)^2>9604/7225`. |
| Full `E_off` transfer | OPEN | `E_off` uses `q`; the head defect `d` is not controlled. |
| Low-order direct prefix | OPEN | Orders `2<=n<N_k` are absent. |
| RH-241, RH-288, Gates A--E | OPEN | No gate or determinant quotient is activated. |

Finite rows reproduce exact rational formulas at `lambda=5/3` and evaluate
diagnostic root functions.  They are not observations of the noisy operator,
the actual coefficient sequence, or asymptotic evidence.
