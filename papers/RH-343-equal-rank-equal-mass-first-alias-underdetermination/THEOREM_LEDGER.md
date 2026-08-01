# RH-343 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Complete-shell moment identity | PROVED EXACTLY | `p_n(U_L(r))=L r^n 1_(L|n)` for every `L>=2`, `r>0`, and `n>=1`. |
| Model candidate construction | PROVED EXACTLY | `X_k^inv=Y_k disjoint_union U_(4k)(c)` and `X_k^vis=Y_k disjoint_union U_(2k)(a) disjoint_union U_(2k)(b)`. |
| Equal rank | PROVED EXACTLY | Both candidates have rank `6k-2`. |
| Equal squared spectral mass | PROVED EXACTLY | Both have `(2k-2)beta_k^2+481k/200`. |
| Conjugation and normal realizability | PROVED EXACTLY | Both are conjugation closed and are spectra of finite normal diagonal matrices. |
| Eventual simplicity and annular location | PROVED | RH-272 gives `beta_k->beta=0.908052...`; hence eventually `q<a<c<b<beta_k<1/r_H`, with common maximum modulus `beta_k`. |
| Coarse physical-clock compatibility | PROVED | Rank and squared mass are `O(k)=O(log(1/sigma))=o(1/sigma)`, so the RH-282 coarse ceilings do not exclude the models. |
| Physical noisy-operator realization | NOT CLAIMED | Coarse compatibility supplies no actual `K_sigma` spectrum. |
| Pre-alias moment equality | PROVED EXACTLY | Both candidates equal `Y_k` for every `2<=n<2k`. |
| Eventual fixed-order equality | PROVED EXACTLY | For every fixed `n`, both shell contributions vanish once `2k>n`. |
| Whole strict-prefix equality of both candidates | FALSE | They split at `n=2k`; only the invisible candidate remains equal to `Y_k` throughout `n<4k`. |
| Invisible strict-prefix budget | PROVED EXACTLY | `D_(4k)(X_k^inv,Y_k)=0`. |
| Visible strict-prefix budget | PROVED EXACTLY | `D_(4k)(X_k^vis,Y_k)=(21/20)^(2k)+(28/25)^(2k)->infinity`. |
| Exact `1/n` cancellation | PROVED EXACTLY | At `n=2k`, shell multiplicity `2k` cancels the budget denominator `2k`. |
| Strict endpoint | ESSENTIAL | The excluded order `4k` is the first visible moment of `U_(4k)(c)`. |
| Genus-one quotient factors | PROVED EXACTLY | `1-(cz)^(4k)` and `[1-(az)^(2k)][1-(bz)^(2k)]`. |
| Equal-invariant underdetermination | PROVED | Equal rank, mass, cap/max modulus, normal simplicity, and pre-alias/fixed-order data do not determine moving `D_(4k)`. |
| Future actual rank cap | EXCLUSION TRIGGER | A proved actual cap `r_sigma<=2k-2` would exclude both rank-`6k-2` examples. |
| Actual head transport | NOT_TESTABLE / OPEN | No candidate is identified with the actual noisy head. |
| Actual `D_(4k)` behavior | NOT CLAIMED | Neither physical divergence nor physical vanishing follows. |
| RH-288 determinant gluing | OPEN | No physical prefix equivalence or determinant identification is proved. |
| Gates A--E | OPEN | No status changes. |
