# RH-383 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Frozen factor class | PROVED INPUT / RETAINED | Fixed finite `q` before `N->infinity`; universally safe phasewise lag-two tables with `c11(r)=0` at every phase |
| Endpoint `B_y,G(q_y)` forms | PROVED INPUT / APPLIED | RH-374/RH-379 finite run and memory identities; no finite fitting |
| Terminal indices | PROVED INPUT / CERTIFIED | Second differences only for `1<=ell<=7`; `R8=mathcal_P_y E8` for the period product separately; `E9=0`; no `E10` |
| Tail bound | PROVED | `T_y<=sum_(odd n>=5)1/(n^2-1)=1/8`, hence `rho_y=7T_y<=7/8` |
| Absolute convergence | PROVED | `c*a<=7/24`; the logarithmic double series and every homogeneous rearrangement converge absolutely |
| Euler-ratio normal form | PROVED / CERTIFIED | `U_m^(y)=u_m exp(Phi_(m-1)(y))` for `2<=m<=8` |
| Squarefree tail normal form | PROVED / CERTIFIED | `H_y=(4/pi^2)exp(-Phi_1(y))` |
| Exact endpoint gap | PROVED / CERTIFIED | `pi^2(Binf-G)=2(C(u)-C(U))-4W(U)(1-exp(-Phi_1))` |
| Partition expansion | PROVED / CERTIFIED | Absolutely convergent sum over all nonempty partitions in the independent power sums `P_r` |
| Finite gamma compiler | PROVED / CERTIFIED | Exact `z_lambda`, endpoint `alpha/beta`, and `product((m-1)^r-1)^k_r` formula |
| Partition loss sign | PROVED / CERTIFIED | Termwise sign is `(-1)^(length(lambda)+1)`; total degree is rejected as a termwise mutation |
| All-order `m=2` cancellation | PROVED / CERTIFIED | Every nonempty partition has zero `m=2` coefficient |
| Increment compiler | PROVED / CERTIFIED | Original `XI/ETA` channels expanded by current-tail `h_r` and strict-successor `e_s` |
| Direct `A/F` telescope | PROVED / CERTIFIED | Independent channel compiler and direct finite-gap oracle |
| Low-order recovery | PROVED / CERTIFIED | `gamma_1=2X`, `gamma_11=Y+2m`, `gamma_2=Y-2m`; independent `P2` retained |
| Cubic block | PROVED / CERTIFIED | Exact coefficients of `(1,1,1)`, `(2,1)`, and `(3)` displayed; no regression |
| Increment ledgers | PROVED / CERTIFIED | `sum|XI_m|u_m<=35/4`, `sum|ETA_m|u_m<=14`; not endpoint-array ledgers |
| Homogeneous bounds | PROVED | `abs(Gamma_X,n)<=5rho^n/2`, `abs(Gamma_M,n)<=4rho^n/3` |
| Arbitrary-order remainder | PROVED / CERTIFIED | For every `y>=1` and exact integer `D>=1`, `abs(R_D)<=92rho^(D+1)/(3pi^2)<31rho^(D+1)/pi^2` |
| Special-purpose constants | BOUNDARY | General `92/3` ledger does not inherit RH-381's `342` or RH-382's `3301/6` fixed-order bounds |
| Three independent oracles | CERTIFIED | Endpoint `C/W`, increment `Gamma/h/e/Phi`, and direct `A/F` telescope agree |
| Exact grids | CERTIFIED / REPRODUCTION ONLY | Counts `67,864,432,1084,144,33,67+12,1151,804,4,7`; label redundancy disclosed |
| Negative mutations | CERTIFIED | 20/20 wrong compilers or complete formulas rejected; no `actual+1` tautologies |
| Source locks | CERTIFIED | 41 immutable files, group sizes `7/8/8/8/8/2`, live/release/group/aggregate hashes agree |
| Prime number theorem / `p_y` scale | NOT USED / EXCLUDED | Intrinsic power sums retained |
| Active phasewise `c11(r)!=0` | OPEN / EXCLUDED | Requires a phase-weighted shift-two correlation theorem |
| Growing clock / adaptive capacity | OPEN / EXCLUDED | No `q(N)`, limit exchange, RH-377 envelope, or capacity convergence |
| Gates A--E | FALSE / OPEN | No intrinsic determinant, scattering completion, generator, von Mangoldt weighted trace, or completed-zeta divisor equality |
| Hilbert--Polya / zeros / RH | NOT CLAIMED | No operator, zero identification, or RH implication |

The infinite conclusions are proved by absolutely convergent products,
partition expansions, and homogeneous majorants. Finite rows reproduce and
attack those arguments; they do not establish them by interpolation.
