# RH-341 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| RH-241 deterministic numerator anchor | CLOSED LATER | RH-263 proves the all-order deterministic anchor. |
| RH-241 deterministic all-order envelope | CLOSED LATER | RH-267 proves `abs(a_n)<48 q_*^n`; RH-268 proves the sharp root rate. |
| Moving noisy all-order coefficient bridge | OPEN | No source identifies the moving noisy coefficients with the deterministic anchor at all orders. |
| Common physical clock and cut | FROZEN | `k=log(1/sigma)/(2log(lambda))+O(1)`, `u=4k`. |
| Corrected all-order five-slot identity | PROVED | `q_n=B+S+R+P-A` for every `n>=2`, explicitly stated in RH-339. |
| Direct/full-trace identity | PROVED EXACTLY | `p_n=q_n-d_n`. |
| Prefix synchronization | PROVED EXACTLY | `abs(P_u-E_u)<=D_u`. |
| Same-clock three-budget reduction | PROVED CONDITIONALLY | Requires `D_(4k)->0`, `E_off->0`, and `q_(2k)=o(H_k)`. |
| Critical orbit compensation | NECESSARY | `C_k^0-d_(2k)=D_k^orb+o(H_k)`. |
| Lower-sideband orbit compensation | NECESSARY | `C_k^--d_(2k-2)=D_(k-1)^orb+o(H_(k-1))`. |
| Separate-absolute orbit/diffuse/head route | STOP_SCOPED | Its two-atom weighted submajorant diverges. |
| Abstract cancelling completion | PROVED TO EXIST ALGEBRAICALLY | Combined signed complements equal the two atoms. |
| Abstract noncancelling completion | PROVED TO EXIST ALGEBRAICALLY | Combined signed complements vanish, leaving both atoms. |
| Two physical noisy operators constructed | FALSE | The completions are information-class ledgers only. |
| Aggregate physical prefix or `E_off` verdict | NOT_TESTABLE | No moving signed complement/head estimate exists. |
| RH-288 determinant gluing | OPEN | Tails close; prefix, off-alias, critical, and head leaves do not. |
| Individual archives | VERIFIED | Ten paper manifests, zero failures. |
| Batch archive | VERIFIED | 154 publication files, zero failures. |
| Gates A--E | OPEN | All 50 batch Gate values remain false. |

Finite witness rows check exact algebra only.  They are not physical data or
asymptotic evidence.
