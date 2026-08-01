# Theorem ledger

| Claim | Status |
|---|---|
| RH-17 orbit order, component period `k>=2`, physical period `2k` | Imported analytic source; `k>=2` is required by the preclosing prefix |
| Finite physical/affine comparison domain | `k>=2` and `sigma>0` |
| Canonical two-step tangent coarsening in the scaled cycle coordinates | Derived: signed slope `S'(x_(k,j))`, variance `1+f'(f(x_(k,j)))^2` |
| Signed raw forward affine row `N(a_(k,j) q,beta_(k,j)^2)` | Defined for `j=0,...,k-2` |
| Exact expansion of the preclosing coordinate | Proved |
| First-innovation identity `s_k=beta_0 prod_(1)^(k-2)m_j=beta_0|M_k|/(m_0m_(k-1))` | Proved |
| Forward variance recurrence `v_(j+1)=a_j^2 v_j+beta_j^2` | Proved |
| RH-18 Riccati widths as forward moment bounds | False data-type identification; they are peak-normalized backward observables |
| Symbolic law `s_k=C_s lambda^(2k)(1+o(1))` | Proved from imported analytic asymptotics |
| Uniform Gaussian maximum-interval-mass lemma | Proved |
| Physical preclosing support interval has length `1/sigma` | Exact |
| Finite unhalved `L1` lower bound with factor `4` | Proved |
| Lower bound for retained prefixes and extensions retaining the preclosing coordinate | Proved by marginal contraction |
| Fixed-phase strictly positive path `L1` liminf | Proved |
| Compact-phase uniform strictly positive lower bound | Proved |
| Raw full-line affine retained-path `O(k*sigma)` and `o(H_k)` accuracy on fixed or compact first-alias phase families | False |
| Final endpoint marginal failure after the tiny closing row | Not proved |
| Cyclic bridge, Doob transform, truncated/folded affine, adapted, or nonlinear closing reference | Not refuted; presently `NOT_TESTABLE` |
| Probability retained path identified with cyclic trace | False/open |
| Trace observation, signed parity/shell cancellation, full-trace replacement, determinant gluing | Open |

The theorem keeps `C_b,C_M` symbolic.  Ordinary decimal constants and finite
rows are non-certified reproduction checks only.  Gates A--E remain
false/open.
