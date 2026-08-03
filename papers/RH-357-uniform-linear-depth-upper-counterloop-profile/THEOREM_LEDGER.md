# RH-357 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Physical multiplier and Hardy normalization | FROZEN | RH-17/RH-342 locks (y_k=x\exp[-\log C_M/k+o(k^{-1})]), (x>1). |
| Exact first-alias budget | PROVED | (A_k=(1-1/k)y_k^k). |
| Exact post-first-alias budget | PROVED | (B_k(L)=\sum_{j=1}^L y_k^{k+j}/(k+j)), (1\le L\le k-1). |
| Uniform endpoint geometric localization | PROVED | (B_k(L)=y_k^{k+L+1}(1-y_k^{-L})/((k+L)(y_k-1))(1+O(k^{-1}))), uniformly over the complete band. |
| Source-locked (x,C_M) profile | PROVED | (B_k(L)=x^{k+L+1}(1-x^{-L})/[C_M^{1+L/k}(k+L)(x-1)](1+o(1))), uniformly. |
| Uniform ratio profile | PROVED | (B_k(L)/A_k=x^{L+1}(1-x^{-L})/[C_M^{L/k}(k+L)(x-1)](1+o(1))), uniformly. |
| Linear-depth constants | PROVED | If (L/k\to\alpha\in(0,1]), factors are (C_M^{-(1+\alpha)}(1+\alpha)^{-1}) and (C_M^{-\alpha}(1+\alpha)^{-1}). |
| Deterministic root rates | PROVED | (B_k(L)^{1/k}\to x^{1+\alpha}), ((B_k(L)/A_k)^{1/k}\to x^\alpha). |
| Physical-clock logarithmic rates | PROVED | Per \(\log(1/\sigma)): ((1+\alpha)\log x/(2\log\lambda)) and \(\alpha\log x/(2\log\lambda)). |
| Floor-phase normalization | PROVED | For (L=\lfloor\alpha k+c\rfloor), retain (\theta_k=\{\alpha k+c\}) in both normalized laws. |
| Rational phase behavior | PROVED | Rational \(\alpha=a/b\) has a finite periodic phase orbit of period (b) (possibly reduced by coincidences). |
| Irrational phase behavior | PROVED | Fractional parts are dense; normalized cluster values form the closed phase image interval. |
| Bounded-depth boundary | PROVED | (1-x^{-L}) is leading at bounded (L); it cannot be deleted. |
| α=0 boundary | PROVED WITH QUANTIFIERS | Terminal simplification requires (L\to\infty) and (L=o(k)), RH-356; no bounded-depth upgrade. |
| α=1 endpoint | PROVED | (L=k-1) is exactly the RH-355 complete strict upper band. |
| Actual-head transfer | CONDITIONAL ONLY | Uniform inheritance and odd-budget decay follow only under original same-clock unnormalized (D_{4k}(R)\to0). |
| Same-clock transport leaf | OPEN | RH-357 does not prove (D_{4k}(R)\to0). |
| Root/rank identification | OPEN | No actual-head root or rank theorem is supplied. |
| Direct/full-trace closure | OPEN | This profile is not RH-354's direct (p) theorem and does not close (q/E_{\rm off}). |
| RH-241, RH-288, Gates A--E | OPEN | No determinant gluing or Gate promotion follows. |

All finite rows are reproduction checks.  They are not asymptotic evidence,
physical interval certificates, or actual noisy-head observations.
