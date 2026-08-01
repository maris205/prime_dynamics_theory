# RH-340 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Natural cut `u=4k` is one-alias admissible | PROVED | `2k<u<=4k` for integer `k>=2`. |
| Noisy tail at `u=4k` | PROVED | Direct corollary of the RH-282 mass/cap estimate; exponent is strictly positive. |
| Deterministic target tail at `u=4k` | PROVED | RH-267 all-order envelope and RH-262 `28/17<lambda`. |
| Prefix identity `p=q-d` | PROVED EXACTLY | One common Hardy normalization and clock. |
| Sharp synchronization inequality | PROVED EXACTLY | `|P_u-E_u|<=D_u`; hence `D_u->0` gives `P_u->0 iff E_u->0`. |
| One-alias three-budget equivalence | PROVED CONDITIONALLY | With the exact RH-330 critical extraction and `D_u->0`. |
| Critical orbit compensation | NECESSARY | `P_u->0` forces `C_k^0-d_{2k}=D_k^orb+o(H_k)`. |
| Lower-sideband compensation | NECESSARY | `P_u->0` forces `C_k^--d_{2k-2}=D_{k-1}^orb+o(H_{k-1})`. |
| Separate-absolute orbit/head majorant | STOP_SCOPED | Its two mandatory atom terms diverge. |
| Aggregate signed prefix or `E_off` verdict | NOT_TESTABLE | No moving-order signed complement/head estimate exists. |
| RH-288 determinant gluing | OPEN | Tail leaves close, but prefix/head/critical leaves do not. |
| Gates A--E | OPEN | No status changes. |

The equations are necessary conditions only.  They do not prove that the
fully signed complement fails, and they do not identify a physical operator
with the abstract determinant factor.
