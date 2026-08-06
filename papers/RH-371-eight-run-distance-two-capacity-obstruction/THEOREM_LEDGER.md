# RH-371 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| RH-366 distance-two constraint | LOCKED | Positive positions are independent sets on the odd and even step-two paths. |
| Even-path isolation | PROVED | Every nonzero even Mobius value is at `n=2 mod 4`; multiples of four are zero. |
| Odd-run length bound | PROVED | Nine odd positions at step two hit a multiple of nine, so nonzero same-sign runs have length at most eight. |
| Eight-run identity | PROVED | `W_sigma=E_sigma+sum_{k=1}^8(-1)^(k+1) C_sigma,k` for every `N`. |
| Capacity identity | PROVED | `K_N=max(abs(-M_N+2W_+),abs(-M_N-2W_-))` for every `N`. |
| Density reduction | PROVED / OPEN | `K_N/N` converges iff the maximum of the two finite run combinations divided by `N` converges; the needed Mobius convergence is open. |
| Periodic pair obstruction | PROVED / SCOPED | Two period-18 ternary words have identical cyclic ordered pair ledgers but capacities `10q` and `12q`. |
| Open-prefix pair equality | FALSE | The words already differ at lag two in their length-18 open ledgers. |
| Mobius interpretation of witness | FALSE | The periodic words are synthetic and do not form a Mobius counterexample. |
| Gates A--E | FALSE / OPEN | No canonical determinant, operator, prime trace, zero identification, or RH implication is claimed. |

All finite rows are exact reproduction checks.  No finite endpoint is used as
evidence for an asymptotic capacity constant.
