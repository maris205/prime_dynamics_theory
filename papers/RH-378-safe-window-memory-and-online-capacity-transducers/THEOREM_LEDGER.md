# RH-378 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Compatible-block safety | PROVED | Fixed finite `q`, causal contiguous `ell`-window tables; exactly `q*3^(ell+2)` compatible checks |
| Current-zero monomial basis | PROVED | Formal function space on the ternary cube; dimension `2*q*3^(ell-1)`, not arithmetic minimality |
| Lag-two safe-table census | PROVED / CERTIFIED | All 512 tables; exactly 13 safe: empty, six off-diagonal singletons, six two-edge stars |
| Six-term score ledger | PROVED | Exact at every finite endpoint with zero padding and the common `m<=N-2` convention |
| Safe coefficient rank | PROVED / CERTIFIED | Rational rank five; unique relation `c22=-c02-c11`; 13-table multiplicities frozen |
| Seven easy lag-table limits | PROVED | Unconditional; class-optimal absolute limit `rho-kappa2`, only within the seven tables |
| Six hard lag-table limits | CONDITIONAL IFF | Each exists iff ordinary shift-two Chowla `D2=o(N)`; no such cancellation is proved |
| Hard subclass optimum | CONDITIONAL | `rho-kappa2/2` only under `D2=o(N)` and only within the six hard tables |
| Comparison with `B_infinity` | PROVED CONDITIONAL COMPARISON | Hard subclass constant exceeds the one-site supremum by at least `e8/4`, but is not an unconditional bound |
| Two orientation transducers | PROVED | Fixed four-state machines output `Smax` and `Smin` exactly for every finite ternary word |
| Four-state minimality | PROVED / NARROW | Exact output realization of one frozen orientation map; not all capacity algorithms or encodings |
| Single-policy obstruction | PROVED / NARROW | No one deterministic causal universally safe policy is absolute-capacity optimal on every branch at every prefix; offline endpoint optimization excluded |
| Length-15 table safety | PROVED | Universal for every ternary input |
| Length-15 agreement | PROVED / SCOPED | Equals the greedy orientation stream when every step-two sigma-run has length at most eight; Möbius satisfies the hypothesis |
| Length-15 minimality | PROVED / NARROW | Only `q=1` causal contiguous stateless exact-stream realization on the run-at-most-eight class |
| Unrestricted recursion equivalence | FALSE | Nine same-parity sigma sites spanning a 17-site prefix give the first divergence |
| Finite endpoint rows | CERTIFIED REPRODUCTION | Exact identities through `N=2^20`; not asymptotic evidence |
| Adaptive capacity convergence | OPEN | Neither the two-machine formula nor finite memory proves a limit |
| Gates A--E | FALSE / OPEN | No determinant, operator, prime-power trace, zero identification, or RH implication |
