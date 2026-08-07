# RH-381 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Frozen factor class | PROVED INPUT / RETAINED | Fixed finite `q` before `N->infinity`; universally safe phasewise lag-two tables with `c11(r)=0` at every phase |
| Square-clock run formula | PROVED INPUT / APPLIED | RH-374 runs of lengths `1..8`, exact finite Euler products |
| All-clock square-clock limit | PROVED INPUT / APPLIED | RH-379 gives `G(q_y)->B_infinity` inside the frozen class |
| Exact square-clock increment | PROVED INPUT / APPLIED | RH-380 two-term increment, telescoped only after fixed-clock limits |
| Normalized numerator identity | PROVED / CERTIFIED | `X_j=(L_j-2E_j)/A_j=2U4-4U5+6U6-8U7+10U8` |
| Positive limit coefficient | PROVED | `X_infinity>=6e8/e1>0` by nonnegative run second differences |
| Euler-tail Lipschitz bound | PROVED / CERTIFIED | `abs(X_j-X_infinity)<=170T_j`; coefficient ledger `6+16+30+48+70=170` |
| Exact `H` product | PROVED INPUT / DERIVED | `H_(j+1)/(4/pi^2)=product_(p>p_(j+1))(1-a_p)` |
| `H` tail bound | PROVED | `0<=4/pi^2-H_(j+1)<=(4/pi^2)T_(j+1)` |
| Memory normalization | PROVED / CERTIFIED | `0<=M_j/A_j<=1` by positive-site counting |
| Current-tail identity | PROVED / CERTIFIED | `sum a_(j+1)T_j=(T_y^2+sum a_(j+1)^2)/2<=T_y^2` |
| Next-tail identity | PROVED / CERTIFIED | `sum a_(j+1)T_(j+1)=(T_y^2-sum a_(j+1)^2)/2<=T_y^2/2` |
| Infinite telescope | PROVED | Finite telescope plus `G(q_K)->B_infinity`; no `N/K` limit exchange |
| Quadratic remainder | PROVED / CERTIFIED | `abs(B_infinity-G(q_y)-(2X_infinity/pi^2)T_y)<=342T_y^2/pi^2` |
| Ratio limit | PROVED | Gap divided by `T_y` tends to `2X_infinity/pi^2>0` |
| Positivity and decay of `T_y` | PROVED | Infinitely many odd primes give `T_y>0`; integer-square comparison gives `T_y->0` |
| Prime number theorem | NOT USED | No `p_y`-scale substitution or prime-counting asymptotic |
| Exact second-order coefficient | NOT CLAIMED | `S_y=sum a^2` remains an independent quadratic scale for a successor |
| Growing clock / adaptive capacity | OPEN / EXCLUDED | No `q(N)` and no capacity-limit exchange |
| Phasewise `c11(r)!=0` | OPEN / EXCLUDED | Requires phase-weighted shift-two correlation input |
| Gates A--E | FALSE / OPEN | No determinant, scattering completion, generator, von Mangoldt trace, or completed-zeta divisor equality |
| Hilbert--Polya / zeros / RH | NOT CLAIMED | No operator, zero identification, or RH implication |

The finite rows reproduce exact identities and outward enclosures. They do
not turn finite fitting into an all-order theorem.
