# RH-372 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Open graph capacity | PROVED | Max-plus DP for every finite open prefix on a finite directed constraint graph. |
| Universal safe transducer test | PROVED | A finite clock/memory table is checked for every consecutive input pair. |
| One-site arithmetic factor | PROVED | If the observed label is `g(r,mu(n))`, its Cesaro correlation has the AP squarefree-density formula. |
| Bounded-resource classification | PROVED | For fixed clock `q` and memory budget `m`, the table class is finite and exhaustible. |
| RH-366 four-state instance | CERTIFIED | `q=4`, two-state universal completion recovers the `4/pi^2` lower certificate. |
| RH-368 three-cell instance | CERTIFIED | `q=2` safe transducer recovers the `4/pi^2` parity-factor certificate. |
| New q=3 safe switch | PROVED / CERTIFIED | A two-state universal completion of two equal-length loops on the RH-366 graph gives `9/(4 pi^2)` without the RH-366 q=4 rule. |
| Memory-dependent labels | OPEN | Higher-order Mobius correlations are required; no unconditional formula is claimed. |
| RH-366 capacity limit | OPEN | This paper supplies no convergence theorem for the distance-two capacity. |
| Gates A--E | FALSE / OPEN | No canonical determinant, operator, prime trace, zero identification, or RH implication is claimed. |

All finite computations are exact checks of the stated contracts.  They are
not asymptotic evidence beyond the imported squarefree and Davenport theorems.
