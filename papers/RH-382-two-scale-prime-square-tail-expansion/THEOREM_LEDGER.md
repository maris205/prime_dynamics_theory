# RH-382 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Frozen factor class | PROVED INPUT / RETAINED | Fixed finite `q` before `N->infinity`; universally safe phasewise lag-two tables with `c11(r)=0` at every phase |
| Exact infinite increment sum | PROVED INPUT / APPLIED | RH-381 telescope after fixed-clock limits; no `q(N)` exchange |
| Run Euler formula | PROVED INPUT / APPLIED | Second differences for `1<=ell<=7`; terminal `R8=P_y E8` separately |
| Terminal indices | PROVED / CERTIFIED | `E9=0` exactly from the `p=3` factor; no `E10` is constructed or used |
| Euler ratio product | PROVED / CERTIFIED | `u_m/U_m^(j)=product_(k>=j)(1-(m-1)a_(k+1))` |
| Bonferroni bounds | PROVED / CERTIFIED | `T-T^2/2 <= 1-product(1-a) <= T`, valid all-order by finite products and passage to the limit |
| Inverse-product bound | PROVED / CERTIFIED | `0<=U-u-(m-1)uT<=U(m-1)^2T^2`, with `U<=(9-m)/8` |
| Numerator first variation | PROVED / CERTIFIED | `abs(X_j-X_infinity-Y_infinity*T_j)<=931*T_j^2/4` |
| Memory Euler form | PROVED / CERTIFIED | `M_j/A_j=2U3-4U4+6U5-8U6+10U7-12U8` |
| Memory convergence | PROVED / CERTIFIED | `abs(M_j/A_j-m_infinity)<=63T_j`; also `0<=M_j/A_j,m_infinity<=1` |
| Exact `H` product | PROVED INPUT / APPLIED | Normalized `H_(j+1)` is `product_(k>=j+1)(1-a_(k+1))` |
| `H` quadratic loss | PROVED / CERTIFIED | Normalized loss is `T_(j+1)+eta`, `-T_(j+1)^2/2<=eta<=0` |
| Current-tail identity | PROVED / CERTIFIED | `sum a_(j+1)T_j=(T_y^2+S_y)/2` |
| Next-tail identity | PROVED / CERTIFIED | `sum a_(j+1)T_(j+1)=(T_y^2-S_y)/2` |
| Cube telescopes | PROVED / CERTIFIED | Mixed sum equals `(T_y^3-sum a^3)/3`; right-square sum at most `T_y^3/3` |
| Numerator cubic budget | PROVED / CERTIFIED | At most `931*T_y^3/(2*pi^2)` |
| Memory cubic budget | PROVED / CERTIFIED | At most `254*T_y^3/(3*pi^2)` |
| Two-scale expansion | PROVED | Coefficients of `T_y^2,S_y` are `Y_infinity+2m_infinity,Y_infinity-2m_infinity` |
| Strong cubic remainder | PROVED / CERTIFIED | `abs(R_y)<=3301*T_y^3/(6*pi^2)` for every `y>=1` |
| Published cubic remainder | PROVED | `3301/6<551`, hence `abs(R_y)<=551*T_y^3/pi^2` |
| `p=71` memory-sign mutation | CERTIFIED / REPRODUCTION ONLY | Correct ratio `0.042746686479386`; changing only `-2mS` to `+2mS` gives `7.335622869337969` and fails; difference exactly `4mS` |
| Source locks | CERTIFIED | 33 immutable files; live hashes, release blobs, group digests, and aggregate digest all agree |
| Prime number theorem / `p_y` scale | NOT USED / EXCLUDED | Intrinsic `T_y,S_y` scales retained |
| Active phasewise `c11(r)!=0` | OPEN / EXCLUDED | Requires phase-weighted shift-two correlation theorem |
| Growing clock / adaptive capacity | OPEN / EXCLUDED | No `q(N)` or capacity-limit exchange |
| Gates A--E | FALSE / OPEN | No determinant, scattering completion, generator, von Mangoldt trace, or completed-zeta divisor equality |
| Hilbert--Polya / zeros / RH | NOT CLAIMED | No operator, zero identification, or RH implication |

The executable finite rows are exact reproduction and adversarial layers.
The all-`y` conclusion comes from the manuscript's all-order product
inequalities and telescopes, never from a finite fit.
