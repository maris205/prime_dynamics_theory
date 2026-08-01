# RH-344 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Complete folded boundary orbit | PROVED / SOURCE LOCKED | `Gamma_k={|f^j(p_k)|:0<=j<2k}` has exactly `2k` distinct marked points with common multiplier `M_k<0` eventually. |
| Per-point Hardy weight | PROVED EXACTLY | Every marked point has weight `G_k=r_H^(-2k)/(1+|M_k|)`. |
| Noisy finite-set localization | PROVED EXACTLY | Multiplication by `1_Gamma_k` is zero on `L^2`, so its localized noisy trace is zero. |
| Complete signed raw atom | PROVED EXACTLY | `F_k^orb=2k G_k` enters the raw ledger as `-F_k^orb`. |
| Critical-point allocation | PROVED EXACTLY | With `xi_k=h(p_k)<b`, `epsilon_k=1_(xi_k in J^-)=1_(q_b<=A)`. |
| Cell counts | PROVED EVENTUALLY | The complete orbit counts in `(J^-,J^+,F)` are `(epsilon_k,0,2k-epsilon_k)`. |
| Fixed-phase allocation | PROVED OFF THRESHOLD | If `eta_sigma->eta`, then `q_b->sqrt(C_b)lambda^(-eta)/(2u_c)`; allocation stabilizes when this limit differs from `A`. |
| Threshold equality | NOT DETERMINED | At limiting equality with `A`, the available `o(1)` expansion does not decide eventual allocation. |
| Orbit-free slot decomposition | PROVED EXACTLY | `B=B_rest-epsilon G`, `S=S_rest`, and `R=R_rest-(2k-epsilon)G`. |
| Raw aggregate decomposition | PROVED EXACTLY | `T_(sigma,2k)=T_k^rest-F_k^orb`. |
| Hardy full-trace identity | PROVED EXACTLY | `q=T_k^rest+P_parity-A_alias-F_k^orb`. |
| Direct coefficient identity | PROVED EXACTLY | `p=T_k^rest+P_parity-d_head-A_alias-F_k^orb`. |
| Critical compensation demand | PROVED NECESSARY | `p_(sigma,k,2k)=o(H_k)` iff `T_k^rest+P-d=A+F_k^orb+o(H_k)`; direct prefix closure implies it. |
| Relation to RH-340 | PROVED EXACTLY | `C_k^0=q+D_k^orb=T_k^rest+P-A-G_k`, so RH-340's law is the same identity after complete physical expansion. |
| RH-338 far atom relation | PROVED EXACTLY | `D_k^orb=(2k-1)G_k`, `F_k^orb/D_k^orb=2k/(2k-1)`, and `F_k^orb-D_k^orb=G_k`. |
| Missing-point scale | PROVED | `G_k/H_k=(beta R)^(2k)/(C_M k)(1+o(1))->infinity`. |
| Complete atom scale | PROVED | `F_k^orb=(2k/C_M)beta^(2k)(1+o(1))`, `F_k^orb/A_(k,2k)->1`, and `F_k^orb/H_k->infinity`. |
| Double-alias scale | PROVED | `A_(k,2k)+F_k^orb=(4k/C_M)beta^(2k)(1+o(1))` and its ratio to `A_(k,2k)` tends to `2`. |
| Exact finite-`k` sign of `A-F` | NOT CLAIMED | The exact identity is recorded, but the repository does not lock its sign. |
| Orbit-free rest estimate | NOT_TESTABLE / OPEN | No moving-order theorem controls `T_k^rest-d_(sigma,k,2k)` at target precision. |
| Actual critical closure or nonclosure | NOT CLAIMED | The signed rest may compensate; neither aggregate alternative follows. |
| Head transport and full strict prefix | OPEN | No `D_(4k)->0` or `p/q` prefix equivalence is proved. |
| RH-288 and Gates A--E | OPEN | No determinant-gluing hypothesis or Gate condition is activated. |
