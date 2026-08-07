# RH-377 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Native run endpoint | LOCKED | For level `k`, every sum uses `1<=n<=N-2(k-1)`, `n` odd; windows overlap and are not maximal exact-length runs |
| Mixed Boolean identity | PROVED | `2^k C_(sigma,k)=H_(k,0)+A_k+sigma(H_(k,1)+B_k)` for all prefixes, signs, and `1<=k<=8` |
| Zero-sign layer | PROVED / CLASSICAL | `H_(k,0)/N -> Delta_k=e_k/2`, `e_k=prod_(p odd)(1-k/p^2)`; the outside `1/2` is exactly the odd-start factor |
| One-sign layer | PROVED | `H_(k,1)=o(N)` by bounded periodic prime-square masks, fixed-AP Davenport cancellation, and cutoff removal |
| Simultaneous signed densities | PROVED EQUIVALENCE | All 16 limits exist iff `A_k/N` for `2<=k<=8` and `B_k/N` for `3<=k<=8` all exist |
| Single-sign inference | SCOPED NEGATIVE | At `k>=3`, one signed density controls only `(A_k+sigma B_k)/N`; it does not force the two aggregate limits separately |
| Formal coordinate map | PROVED / FORMAL ONLY | 466 formal higher coordinates map to 13 disjoint block sums; rank 13, kernel 453; no arithmetic minimality claim |
| Exact finite capacity channels | PROVED | `R_sigma=P+U+sigma(Q+V)` and `max R=P+U+abs(Q+V)` |
| Exact capacity residual | PROVED | `abs(K-2(P+U+abs(V)))<=abs(M)+2abs(Q)` at every prefix |
| Two-envelope asymptotic | PROVED | `K_N/N=2r_0+2(U_N+abs(V_N))/N+o(1)` |
| Capacity convergence | OPEN / EXACT BOUNDARY | `K_N/N` converges iff `(U_N+abs(V_N))/N` converges; neither convergence nor nonconvergence is proved |
| Full mixed cancellation | CONDITIONAL / SUFFICIENT ONLY | Would give `2/pi^2+sum s_k e_k/2^k`; it is neither necessary nor proved |
| Stationary ternary witness | PROVED / SYNTHETIC | Uniform-pair second-order chain has the frozen moment identities and directional moment `8 epsilon/81`; it is not Möbius |
| Möbius implication of witness | FALSE / NOT CLAIMED | The chain does not match Möbius squarefree density and proves no arithmetic nonconvergence |
| Gates A--E | FALSE / OPEN | No determinant, operator, prime-power trace, zero identification, completed-zeta divisor equality, or RH implication |

All stored numerical rows are exact finite reproduction.  The 502 raw and
502 square-only enumerations concern block lengths at most eight; the
arbitrary-distinct-time stationary statements are proved analytically by
latest-time conditioning and sign inversion.
