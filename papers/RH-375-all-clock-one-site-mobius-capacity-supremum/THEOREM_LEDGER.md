# RH-375 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| Fixed-clock correlation formula | PROVED INPUT / APPLIED | Every fixed finite `q`; one-site phase/current-input factors only |
| Universal-safety reduction | PROVED | Active phases are exactly a distance-two independent set; self-loops at `q=1,2` are retained |
| Fixed-clock optimum | PROVED | `F(q)` is the squarefree-density weighted phase MWIS; both orientations attain it |
| Local density coefficients | PROVED / CERTIFIED | Exact `pi^2*delta_(q,r)` Fractions for arbitrary finite `q`, including exponent-one local factors |
| Divisibility monotonicity | PROVED | `q|Q` lifts a possibly non-minimal-period factor and gives `F(q)<=F(Q)` |
| Same-support square-clock saturation | PROVED | Only for `q_y|Q` with identical prime support; uses the special `4`-zero and `9`-zero splitting structure |
| All-clock one-site supremum | PROVED | `sup_(q finite) F(q)=B_infinity` |
| Finite-clock nonattainment | PROVED | Every fixed finite `q` satisfies `F(q)<B_infinity` |
| Bounded scan `q<=256` | CERTIFIED DIAGNOSTIC | Exact reproduction only; maximum `pi^2 F(q)=97/24` at `q=180` in that finite range |
| General cyclic-cover MWIS scaling | FALSE / NOT CLAIMED | Only the square-clock support replication is proved |
| Memory-dependent or growing-clock class | OPEN / EXCLUDED | No higher-order Möbius theorem, `q(N)`, infinite selector, or uniform-in-`q` Davenport bound |
| Adaptive RH-366 capacity limit | OPEN | The all-clock one-site supremum is not identified with an ordinary capacity limit |
| Gates A--E | FALSE / OPEN | No intrinsic determinant, operator, prime-power trace, zero identification, or RH implication |

Every finite table is a source-lock or exact reproduction check.  The
all-clock conclusion follows from the proved cofinal lift and the frozen
RH-374 Euler-product theorem, not from finite numerical behavior.
