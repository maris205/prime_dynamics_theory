# RH-363 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Four-volume foundation | FROZEN / PRESERVED | RH-1--RH-361 remain the atomic sources in the disjoint ranges `1--160`, `161--241`, `242--281`, and `282--361`; the outer replay remains `4` volumes, `361` sources, `73` archive members, `1,548` dependency hashes, `8` result hashes, and `0` failures. |
| RH-362 return ranks | PROVED UPSTREAM / LOCKED | For nonperiodic integral `P`, the local ranks `r_p(P)` tend to infinity cofinally and `Z_P(s)=prod_p(1-p^(-s r_p))^-1` is holomorphic and zero-free on `Re(s)>0`. |
| Return-power family | PROVED | `B_m(P)={p^(m r_p(P))}` is infinite, pairwise coprime, and thin for every integer `m>=1`. |
| Periodic-orbit collapse | PROVED | Every `X_m(P)=A_(B_m(P))` has only `0^infinity` periodic, hence `N_n=1` for all `n` and `zeta_(X_m)(z)=(1-z)^-1`. |
| Entropy identity | PROVED | `E_m=h_top(X_m)/log 2=prod_p(1-p^(-m r_p))=Z_P(m)^-1` lies in `(0,1)`. |
| Entropy tower monotonicity | PROVED | `E_m` is strictly increasing and `E_m -> 1`. |
| Multiples-Mobius inversion | PROVED | With `Lambda_m=-log E_m` and `M_m=sum_p p^(-m r_p)`, both relevant series converge absolutely and `M_m=sum_(j>=1) mu(j)Lambda_(mj)/j`. |
| Complete rank recovery | PROVED | The moment sequence recursively recovers the strictly ordered atoms `p^(-r_p)`; unique factorization recovers every labeled `(p,r_p)`. |
| Finite gcd-stratified count | PROVED UPSTREAM / SPECIALIZED | Every finite approximant has the exact pairwise-coprime inclusion--exclusion count with reduced moduli `gcd(n,p_i^(m r_i))`. |
| Universal elimination and first defect | PROVED | For the first `k` primes, `N_n=1` iff the primorial `W_k` does not divide `n`; at `W_k` the exact first defect is the prime-wheel value `P_(p_1,...,p_k)(2)`, independent of `P`, `m`, and the ranks. |
| First zeta coefficient defect | PROVED | Coefficients equal those of `(1-z)^-1` below degree `W_k`; at degree `W_k` the excess is `[P_(p_1,...,p_k)(2)-1]/W_k`, the number of new primitive cycles. |
| Finite entropy and radii | PROVED | `E_(m,k)=prod_(i<=k)(1-p_i^(-m r_i))` and `R_(m,k)^log=R_(m,k)^zeta=2^(-E_(m,k))`, with a nonremovable positive pole at that radius. |
| Sharp exhaustion disk | PROVED | The zeta germs converge uniformly on every closed disk `|z|<=r<2^(-E_m)`; no larger centered disk admits tailwise holomorphic convergence because the positive poles approach `2^(-E_m)`. |
| Radius discontinuity | PROVED | `R_(m,k) -> 2^(-E_m)<1`, while the coefficientwise limit `(1-z)^-1` has radius `1`. |
| Engineered-functor boundary | PROVED SCOPE / NOT A GATE | Once `P` and `m` are fixed, the return-power tower is well-defined and functorial, but it is assembled by inserting the marked ranks into forbidden prime-power moduli; it is not an intrinsic canonical global Hénon dynamics or operator. |
| One-zeta spectral recovery | FALSE / SCOPED NEGATIVE | Every tower level has the same trivial Artin--Mazur zeta; the ranks are recovered only from the full entropy tower. |
| Canonical RH operator | FALSE / NOT CLAIMED | No single global operator, signed trace law, scattering completion, or physical noisy determinant is supplied. |
| Original physical triggers 1--4 | UNTOUCHED | No `D_(4k)`, typed `q/E_off`, complete unnormalised prefix, or RH-241 moving noisy bridge is supplied. |
| Gates A--E | FALSE/OPEN | No canonical physical determinant, time-oriented completion, self-adjoint generator, von Mangoldt trace, or completed-zeta divisor equality is proved. |

Finite computations are reproduction checks only.  The all-prime and
all-order assertions are proved in the manuscript.
