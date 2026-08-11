# RH-395 theorem ledger

## Objects and quantifiers

| ID | Frozen statement | Status |
|---|---|---|
| Q1 | `T={-1,0,+1}`; `q` and all phase tables are fixed before `X->infinity` | proved |
| Q2 | `1<=omega(X)<=X` and `omega(X)->infinity`; the theorem holds for every such terminal clock | proved through RH-394 |
| Q3 | `epsilon_n=F_(n mod q)(mu_0(n-1),mu(n),mu(n+1))` is centered and explicitly noncausal | definition |
| Q4 | universal safety forbids `F_r(a,b,c)=F_(r+2)(c,d,e)=+1` for every phase and ternary word | definition |
| Q5 | `L_q(F)` is formed before the maximum defining `C(q)` | proved and firewalled |

## Analytic reduction

| ID | Claim | Evidence |
|---|---|---|
| A1 | Every fixed three-window phase table has a terminal-log limit on every admissible clock | RH-394 Theorem 1.1, equation (8), Theorem 1.2, equations (11)--(12), and Corollary 1.3, printed/PDF pages 2--3 |
| A2 | Exact-support phase densities `Pi_(q,r)(U)` are nonnegative and have phase mass `1/q` | RH-394 Theorem 1.2 and equations (11)--(12) |
| A3 | Deleting every `+1` output whose center is not `+1` preserves safety and weakly increases the signed score | manuscript Lemma 2.1 |
| A4 | A projected table is encoded by one of 512 relations `A_r subset T^2`; each relation has `2^18` full-table preimages | manuscript Lemma 2.1 |
| A5 | The projected limit is `sum_r sum_((x,y) in A_r) lambda_r(x,y)` | manuscript equation (19) |

RH-394 is the sole terminal-log analytic input.  RH-375 has no analytic
terminal-clock role in RH-395.

## Relation algebra and tropical optimizer

| ID | Claim | Evidence |
|---|---|---|
| R1 | safety iff `Target(A_r) intersect Source(A_(r+2))` is empty | manuscript Lemma 2.2; certificate relation audit |
| R2 | nonnegative saturation gives `A_r=(T\Y_(r-2)) x Y_r` | manuscript Lemma 2.2; certificate projection audit |
| R3 | `C(q)` is the full eight-subset tropical trace along every `r -> r+2` cycle | manuscript Theorem 1.1 and Proposition 3.1; certificate subset-state rows |
| R4 | reflection `F^rho(x,z,y)=F(-x,-z,-y)` preserves safety and negates the limit | manuscript Lemma 2.3; certificate reflection audit |
| R5 | for `q>=3`, multi-affinity yields an optimizer on four antipodal subset states | manuscript Proposition 3.2; certificate transfer/compression rows |
| R6 | four-state compression is not used for `q=1,2` | manuscript and theorem firewall |
| R7 | `q=1` is a separate full-eight self-loop and `q=2` genuinely needs a singleton-sign state | manuscript Proposition 3.3; 16 q=2 self-loop rows |

The finite program enumerates all `512^2=262144` ordered relation pairs and
finds exactly 3375 safe pairs.  This enumeration reproduces the finite
relation algebra; it is not analytic evidence.

## Exact small clocks

Let `K_j=prod_p(1-j/p^2)`, so `K_1=6/pi^2`.

| Clock | Exact centered capacity |
|---:|---|
| 1 | `K2-K3` |
| 2 | `(3K2-K3)/4` |
| 3 | `3K1/8=9/(4*pi^2)` |
| 4 | `2K1/3=4/pi^2` |
| 6 | `K1/8+K2/2` |

The one-site value at clock 6 is `3K1/8`; hence the centered gain is
`(2K2-K1)/4>0`.  The strict inequality is proved by rational Euler-product
enclosures, not floating-point comparison.

## Square-support rigidity

| ID | Claim | Evidence |
|---|---|---|
| S1 | `q|Q` implies `C(q)<=C(Q)` by literal nonminimal-period lift | manuscript Lemma 4.1 |
| S2 | RH-375 supplies `q_y`, the one-site values `B_y`, and `B_infinity` | RH-375 equations (10)--(12), Proposition 4.1 equation (13), and Theorem 5.1 equations (16)--(17), printed/PDF pages 3--5 |
| S3 | on same-prime-support multiples of `q_y`, every positive center phase has one common charge `delta_Q` | manuscript Lemma 4.2 |
| S4 | adjacent positive phases satisfy a shared-coordinate marginal identity and pair charge at most `delta_Q` | manuscript Lemma 4.2 |
| S5 | forced modulo-4 and modulo-9 zero phases split the `+2` cycles into runs; a length-`L` run costs at most `ceil(L/2)delta_Q` | manuscript Proposition 4.3 |
| S6 | if `q_y|Q` and the prime supports agree, `C(Q)=B_y` | manuscript Proposition 4.3 |
| S7 | for every finite `q`, a cofinal lcm bridge gives `C(q)<B_infinity` | manuscript Section 5 |
| S8 | embedded one-site square-clock witnesses give the reverse supremum bound | manuscript Section 5 |
| S9 | `sup_(q finite) C(q)=B_infinity`, with no finite maximizer | manuscript Theorem 1.1 and Section 5 |

RH-375 is used here only for its finite squarefree density/MWIS/lift/
same-support combinatorics and endpoint data.  Its ordinary-Cesàro equation is
not promoted to a terminal-clock theorem.

## Source and artifact identities

| Object | Frozen identity |
|---|---|
| RH-394 release | `6b3d616851cd2d7cba66371d0aa9f25b8e8bf2f7` |
| RH-375 release | `071fed1b2a5d8488b9d2e35a99a753953b233584` |
| Git closure | 148 objects, groups `128+8+4+8`, digest `9b5e0c04bb3189ddcb802ccb65d5f6b3cc8aa081000acd9fa781fd9f81e50ec9` |
| logical closure | `148+4=152`, digest `5c4b81ea2f7bdd661fe4374d1174ef3a1909a8327d5982aa01510e4201340bd3` |
| certificate | 72 rows, 32,983 canonical bytes, SHA-256 `31afb062208af97fddb5192bc4d6f1f4f030ad69b5a3f9b6ed1d1d9b2b1128a9` |
| result | 148,331 pretty bytes, SHA-256 `7557bcc78811b29d7ac9f155fd8553c75d70b659748a37cf2fef427af4958f27` |
| schema | 678,979 pretty bytes, SHA-256 `2eb368a88cc7e3363a3c4f216ea7d3efd423b4faf9bcdec003d36316b2bfe643` |

## Claim ceiling

The following remain outside the theorem: a causal or online centered
controller, the RH-378 window-end model, `q=q(X)`, growing tables, an effective
rate, ordinary Cesàro convergence, a maximum before the terminal limit,
adaptive finite-prefix capacity, generic graph-coupled capacity, even
odd-support correlations of order at least four, any operator model, any
trace formula, any zero identification, the Riemann hypothesis, and Gates
A--E.
