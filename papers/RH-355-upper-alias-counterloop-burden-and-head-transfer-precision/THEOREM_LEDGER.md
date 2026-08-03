# RH-355 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Physical clock and Hardy normalization | FROZEN | The RH-342 first-alias clock, actual modulus-complete head, and graded counterloop are used without substitution. |
| Multiplier/radius law | SOURCE LOCKED | RH-17 gives `|M_k|=C_M lambda^k(1+o(1))`, hence `y_k=x exp[-log(C_M)/k+o(1/k)]`. |
| Exact strict upper-band ledger | PROVED | `C_k^up=sum_(m=k+1)^(2k-1)y_k^m/m`; all odd terms vanish. |
| Raw counterloop asymptotic | PROVED | `C_k^up~x^(2k)/(2 C_M^2 k(x-1))`. |
| Normalized counterloop burden | PROVED | `x^(-k)C_k^up~x^k/(2 C_M^2 k(x-1))` and its `k`th root tends to `x>1`. |
| Terminal coordinate | PROVED | Its normalized size is `~x^(k-1)/(2C_M^2k)` and its share tends to `(x-1)/x`. |
| Actual upper-head asymptotic | CONDITIONAL ONLY | Follows if the original unnormalized same-clock `D_(4k)(R)->0`. |
| Odd actual upper budget | CONDITIONAL ONLY | Under `D_(4k)(R)->0`, it tends to zero. |
| Uniform even relative precision | CONDITIONAL ONLY | Under `D_(4k)(R)->0`, the maximum error is `o(kx^(-k))`. |
| Terminal relative precision | CONDITIONAL ONLY | Under `D_(4k)(R)->0`, it is `o(kx^(-2k))`. |
| Original head-transport leaf | OPEN | This paper does not prove `D_(4k)(R)->0`. |
| Weak normalized aggregate transfer | PROVED CONDITIONALLY | `Delta_k^up->0` transfers the aggregate normalized budget and gives terminal error `o(kx^(-k))`. |
| Weak normalized bandwise matching | FALSE IN FINITE NORMAL INFORMATION CLASS | A complete `(2k+2)`th-root shell has normalized defect `~x/(C_Mk)->0` but relative error one at `2k+2`; its unnormalized defect diverges. |
| Actual noisy counterexample | NOT CLAIMED | The shell construction is not an actual noisy operator or actual-head nonmatching theorem. |
| Direct/full-trace transfer | OPEN | RH-354 controls `p=tau-a=q-d`, not `q`, `d`, or `E_off`. |
| RH-241, RH-288, Gates A--E | OPEN | No gate or determinant gluing theorem is activated. |

Finite exact and high-precision rows reproduce formulas under explicit
synthetic multiplier laws.  They are not actual noisy-head observations,
interval certificates, or asymptotic evidence.
