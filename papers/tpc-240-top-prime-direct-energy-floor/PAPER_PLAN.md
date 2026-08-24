# Paper Plan

## One-sentence contribution

For every fixed literal V59 common profile, the top-prime q-split unsigned
direct residue-row energy has the exact asymptotic constant
`1197*kappa_psi*log(2)/800` and therefore an unavoidable `x^(1/96)` floor.

## Claim-evidence matrix

| Claim | Status | Evidence |
|---|---|---|
| `1/2<=kappa_psi<=1` | `PROVED` | Cauchy--Schwarz and `psi^2<=psi` |
| Fixed-`q` primitive row identity | `PROVED`, not new alone | `4Q<H`, `U<Q`, signed-interval injectivity |
| Row asymptotic `kappa_psi pq/H+O_psi(1)` | `PROVED` | Endpoint-safe lattice Riemann estimate |
| Relative aggregation error `O_psi(H/(UQ))` | `PROVED` | Prime-count comparison and top-shell bounds |
| Exact constant `1197/800` | `PROVED` | Two weighted PNT asymptotics and `log U/log Q=399/400` |
| Fixed-power floor `x^(1/96+o(1))` | `PROVED` | `2/3-21/32=1/96` |
| Finite-window lower corollary | `PROVED_STRUCTURAL_L1` | Nonnegativity plus TPC-238 lower frame |
| `x^(1/48)` sharpness | `OPEN`, explicitly excluded | Requires q-collision saturation |
| Signed four-packet Gate B | `OPEN`, explicitly excluded | No signed projection in the object |

## Section plan

1. Abstract: state the object, exact constant, exponent, and firewall.
2. Introduction: isolate the unresolved direct factor and distinguish the new
   aggregate theorem from TPC-215 and TPC-216.
3. Frozen setup: lock scales, profile, rows, coefficient, and quantifiers.
4. Exact row and Riemann proof: prove primitive injectivity and the uniform
   fixed-profile row asymptotic.
5. Weighted-PNT aggregation: sum the rows, control the error, and compute the
   constant and exponent.
6. Certificate: document exact ledgers, independent reconstruction, mutations,
   and smooth-profile finite stress tests.
7. Route boundary: state the direct-factor obstruction and the firewalled
   finite-window corollary.
8. Conclusion: extract the reusable structure and next collision theorem.
9. Status ledger: classify every claim and declaration explicitly.

## Novelty boundary

TPC-215 already proves `C_p=c_p=-log(p)/p` in the top shell.  TPC-216 already
proves fixed-`q` injectivity and its exact row norm.  TPC-240 does not relabel
either fact as new.  Its new edge is the literal-profile aggregate: uniformly
large row depth, a profile-dependent Riemann asymptotic, two weighted-prime
averages, the exact leading constant, and a matching `x^(1/96)` lower floor.

## Stop conditions

The paper must stop below arithmetic `L2`, strict `1/400`, full Gate B, and any
twin-prime conclusion.  A plateau equal to one on all of `[-1,1]` is forbidden
because it is not a literal smooth compactly supported V59 profile.
