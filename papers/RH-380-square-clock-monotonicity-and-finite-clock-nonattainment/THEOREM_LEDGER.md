# RH-380 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Frozen factor class | PROVED INPUT / RETAINED | Fixed finite `q` before `N->infinity`; universally safe phasewise lag-two tables with `c11(r)=0` at every phase |
| RH-379 fixed-clock optimum | PROVED INPUT / APPLIED | Positive three-state `{0,J,I}` optimum equals absolute `G(q)` by input reflection |
| Square run formula and odd-run recurrence | PROVED INPUT / APPLIED | RH-374 cyclic word; runs have length at most eight; `O_(y+1)=(s-1)O_y+L_y` |
| Per-run deletion ledger | PROVED | Even old run has `s-2` even descendants; odd old run of length `l` has `l-1` |
| Even-run recurrence | PROVED / CERTIFIED | `mathcal_E_(y+1)=(s-2)mathcal_E_y+M_y` for every `y>=1` |
| Exact square-clock increment | PROVED / CERTIFIED | Two-term formula in `Q/pi^2+Q*kappa2`, derived from four exact recurrences |
| Persistent strict term | PROVED INPUT / APPLIED | `L_y-2mathcal_E_y=2R4+4R6+6R8>=6` because RH-374 proves `R8>=1` |
| Square-clock monotonicity | PROVED | `G(q_(y+1))-G(q_y)>=12/(pi^2 A_y(s-1))>0` |
| Density scaling at same support | PROVED / CERTIFIED | For `Q=R q_y` with identical prime support, every fine `delta` and `theta` coefficient is `1/R` times its projection |
| Cause-specific separators | PROVED / CERTIFIED | Mod-4 zero phase on the even cycle and mod-9 zero phase on the odd cycle; zero-weight action may be set to `0` |
| Same-support saturation | PROVED / CERTIFIED | `G(Q)=G(q_y)` only for the square-clock same-prime-support setting |
| New-prime negative control | CERTIFIED / SCOPED NEGATIVE | `Q=180=5*36` is outside same support and `G(180)>G(36)` by the locked H bound |
| Clock divisibility | PROVED | If `q|Q`, lift the periodic phase tables to obtain `G(q)<=G(Q)` |
| Arbitrary exponent scope | PROVED | The lcm argument allows arbitrary 2-adic exponent and arbitrary exponents of supported odd primes |
| Finite-clock nonattainment | PROVED | Every fixed finite `q` satisfies `G(q)<B_infinity` |
| Explicit finite-clock gap | PROVED | If `y` contains all odd prime divisors of `q`, gap is at least `12/(pi^2 A_y(p_(y+1)^2-1))` |
| `Delta_y` monotonicity | NOT CLAIMED | Only `G(q_y)` is proved increasing |
| General cyclic-cover saturation | NOT CLAIMED / EXCLUDED | Proof needs square-clock local weights and mod-4/mod-9 separators |
| First-order gap asymptotic | REOPEN TRIGGER / NOT PROVED HERE | Candidate `B_infinity-G(q_y)=(2X_infinity/pi^2)T_y+O(T_y^2)` requires an all-order Euler-product expansion |
| Phasewise `c11(r)!=0` | OPEN / EXCLUDED | First blocker is phase-weighted shift-two Möbius correlation |
| Growing clock / adaptive capacity | OPEN / EXCLUDED | No `q(N)` and no adaptive-capacity convergence |
| Gates A--E | FALSE / OPEN | No intrinsic determinant, scattering completion, self-adjoint generator, von Mangoldt trace, or completed-zeta divisor equality |
| Hilbert--Polya / zeros / RH | NOT CLAIMED | No operator, zero identification, or RH implication |

The finite certificate is a reproduction and adversarial-check layer. The
all-order results are proved symbolically in the manuscript, not inferred
from the finite rows.
