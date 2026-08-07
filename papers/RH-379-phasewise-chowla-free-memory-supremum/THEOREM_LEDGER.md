# RH-379 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Fixed-phase cancellation | PROVED | Each finite `q` fixed before `N->infinity`; `c11(r)=0` separately at every phase |
| Squarefree AP weights | PROVED INPUT / CERTIFIED | Exact `delta=A/pi^2` and `theta=B*kappa2`, including exponent-one local factors |
| Full local census | PROVED / CERTIFIED | All 512 tables; 192 phasewise Chowla-free tables and nine exact `(c02,c22)` cells |
| Canonical subset dominance | PROVED / CERTIFIED | Every one of the 192 maps to a subset among `0,J,K,I` with no smaller limiting payoff |
| `K -> I` replacement | PROVED / ORDERED | Only after canonical reduction; canonical `K,I` have identical full in/out compatibility and `I=J+K>=K` |
| Fixed-clock optimum `G(q)` | PROVED / CERTIFIED | Exact three-state cyclic max-plus DP on `{0,J,I}`, with self-loops for `q=1,2` retained |
| Independent-set reduction | PROVED / CERTIFIED | All-`J` baseline plus `+2`-cycle MWIS gains `K_r-J_(r-2)` |
| Input reflection | PROVED | Preserves safety and reverses the main payoff, so positive optimization equals maximum absolute score |
| `q=36` strict gain | PROVED / CERTIFIED | `G(36)=9/(2*pi^2)-kappa2/7 > F(36)=4/pi^2`; exact square-clock strict gain, not first same-clock gain |
| Exact square-clock formula | PROVED / CERTIFIED | `G(q_y)=B_y+Delta_y`, `Delta_y=mathcal_E_y(4/(A_y*pi^2)-kappa2/D_y)>0` |
| Square-clock convergence | PROVED | `mathcal_E_y/A_y<=1/2` and `H_y=kappa2*A_y/D_y -> 4/pi^2` give `Delta_y->0` |
| Arbitrary-clock cofinal upper bound | PROVED | Lift fixed `q` to `Q_y=lcm(q,q_y)`; retained one-site bound plus discarded tail `sum_(p>p_y)p^-2` |
| Reverse supremum inequality | PROVED INPUT / APPLIED | RH-375 one-site embedding `f_r(x,z)=g_r(z)` gives `G(q)>=F(q)` |
| All-clock phasewise-memory supremum | PROVED | `sup_(q finite)G(q)=B_infinity` |
| Same-support memory saturation | NOT CLAIMED | Only the retained one-site set invokes RH-375 saturation |
| `Delta_y` monotonicity | NOT CLAIMED | Positivity and convergence to zero only |
| Finite-clock attainment / nonattainment | OPEN / NOT CLAIMED | The scalar supremum identity alone decides neither |
| Phasewise `c11(r)!=0` | OPEN / EXCLUDED | First blocker is phase-weighted ordinary shift-two `D2` cancellation |
| Growing clock / adaptive capacity | OPEN / EXCLUDED | No `q(N)`, uniform Davenport theorem, or adaptive-capacity convergence |
| Gates A--E | FALSE / OPEN | No intrinsic determinant, operator, prime-power trace, zero identification, or RH implication |

Finite clock values and decimal intervals are exact or certified
reproduction fixtures.  They are not used as asymptotic evidence.
