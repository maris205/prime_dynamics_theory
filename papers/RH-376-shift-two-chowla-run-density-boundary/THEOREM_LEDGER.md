# RH-376 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| RH-371 two-site count | LOCKED | Odd starts `1<=n<=N-2`; overlapping same-sign intervals, not maximal exact-length runs |
| Common-endpoint Boolean identity | PROVED | `4C_(sigma,2)=Q2+sigma U2+sigma V2+D2` for every `N` and either sign |
| Even-start removal | PROVED | For even `n`, one of `n,n+2` is divisible by four, so every summand vanishes |
| Squarefree-pair density | PROVED / CLASSICAL | `Q2/N -> kappa2=prod_p(1-2/p^2)` |
| One-mask cancellation | PROVED | `U2,V2=o(N)` by a fixed divisor cutoff, fixed-AP Davenport cancellation, then cutoff removal |
| Logarithmic affine input | PROVED INPUT / APPLIED | Teräväinen--Walker for the fixed forms `m+1,m+3`, determinant two, zero twist |
| Cesàro-limit rigidity | PROVED | If `D2/N` has a limit, Abel summation and the logarithmic input force that limit to be zero |
| Signed interval-density equivalence | PROVED | For either fixed sign, `C_(sigma,2)/N` converges iff ordinary shift-two Cesàro Chowla `D2=o(N)`; value `kappa2/4` |
| Shift-two Chowla | OPEN / NOT PROVED | The equivalence does not establish `D2=o(N)` |
| Nonconvergence | FALSE / NOT CLAIMED | No failure of a signed interval density, run envelope, or capacity limit is proved |
| Higher run lengths | OPEN | `k>=3` requires additional mixed-exponent correlations |
| RH-371 envelope and `K_N/N` | OPEN | One component density does not settle the alternating eight-run maximum |
| Gates A--E | FALSE / OPEN | No intrinsic determinant, operator, prime-power trace, zero identification, or RH implication |

The endpoint `N=2^20` and all prefix checks are exact finite reproduction.
They play no role in the asymptotic proof.
