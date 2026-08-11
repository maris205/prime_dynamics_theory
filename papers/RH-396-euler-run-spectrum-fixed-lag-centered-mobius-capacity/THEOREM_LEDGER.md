# RH-396 theorem ledger

## Objects and quantifiers

| ID | Frozen statement | Status |
|---|---|---|
| Q1 | `h>=1`, `q`, and every table `F_r:T^3->{-1,+1}` are fixed before `X->infinity` | proved |
| Q2 | `mu_0(k)=mu(k)` for `k>=1` and `mu_0(k)=0` for `k<=0` | definition |
| Q3 | the centered window is `(mu_0(n-h),mu(n),mu(n+h))` and the score is `mu(n)F_r(...)` | definition |
| Q4 | `d=2h`; universal safety forbids simultaneous positive outputs at phases `r,r+d` on every shared ternary coordinate | definition |
| Q5 | every admissible terminal clock has `1<=omega(X)<=X` and `omega(X)->infinity` | proved through RH-394 |
| Q6 | fixed-table limit precedes the finite safe maximum `C_h(q)`, which precedes the scalar supremum over finite `q` | proved and firewalled |

## Analytic bridge and tropical optimizer

| ID | Claim | Evidence |
|---|---|---|
| A1 | RH-394 gives the complete fixed three-shift terminal-log table law at `(+h,0,-h)` | manuscript Theorem 1 and Section 2; RH-394 Theorems 1.1--1.2 and Corollary 1.3 |
| A2 | `Theta_(h,q,r)(S)` uses collision-deduplicated prime-square residues; its phase sum is `kappa_h(S)` | equations `theta`, `kappa`, `phase-sum`; certificate group `theta_pi_lambda` |
| A3 | `Pi` is the nonnegative exact-support density, has phase mass `1/q`, and defines `lambda` and `mathcal K` | equations `Pi`, `lambda`, `transition` |
| A4 | positive projection deletes positive outputs with center not `+1`, preserves safety, and weakly increases score | Lemma `projection` |
| A5 | relation safety is `Target(A_r) intersect Source(A_(r+d))=empty` and saturation is `A_r=(T\Y_(r-d)) x Y_r` | Lemma `saturation` |
| A6 | reflection preserves safety and reverses the terminal sign | Lemma `reflection` |
| A7 | `C_h(q)` is the exact full eight-state tropical trace on every `r -> r+d` cycle | Theorem `fixed-clock`, Proposition `tropical` |
| A8 | four-state compression is proved when `q` does not divide `2h` | Theorem and Proposition `compression` |
| A9 | if `q | 2h`, every cycle is a self-loop and all eight states remain | Theorem `compression` |
| A10 | `h=2,q=4` strictly separates full eight-state and four-state-restricted values | equation `self-loop-obstruction`; certificate group `selfloop_compression_small_clock` |

RH-394 is the sole analytic terminal-log input.  RH-395 and RH-375 have
finite combinatorial precedent roles only.

## Square-support theorem

| ID | Claim | Evidence |
|---|---|---|
| S1 | on square-supported `Q`, `alpha_h(Q)` is raw MWIS and `M_h(Q)=K1 alpha_h(Q)/N_h(Q)` is weighted | equations `NQ`, `alphaQ`, `MQ` |
| S2 | `q|Q` implies `C_h(q)<=C_h(Q)` by literal phase-table repetition | Lemma `clock-divisibility` |
| S3 | one-site independent sets embed and give `M_h(Q)<=C_h(Q)` | Lemma `clock-divisibility` |
| S4 | adjacent positive phases have equal collision-aware marginals separately for `t=0,+1,-1` | Lemma `marginal`; equations `marginal-zero`--`marginal-total` |
| S5 | each adjacent transition pair costs at most `delta_Q`; a run of length `L` costs at most `ceil(L/2)delta_Q` | Lemma `path-charge` |
| S6 | if the support contains `p0(h)`, `C_h(Q)=M_h(Q)` | Proposition `square-saturation` |
| S7 | same-support covers scale `N` and `alpha` by `R=Q/q_P`, with no `gcd(R,2h)` condition | Proposition `same-support` |
| S8 | `h=6`, `36->72` is a strict pre-`p0` counterexample; `900->1800` is the qualified fixture | Remark `p0-counterexample` |

The equality `C_h(Q)=M_h(Q)` is load-bearing.  It is asserted only on the
qualified square-support domain, never for an arbitrary clock having a prime
to exponent one.

## Euler-run endpoint and strict nonattainment

| ID | Claim | Evidence |
|---|---|---|
| E1 | `D_h(J)` is an absolutely convergent collision-aware Euler product | equation `Dh`; Lemma `infinite-density` |
| E2 | `R_(ell,h)` is the four-term exact bracketed-run density and is nonnegative | equation `Rlh`; finite/infinite run lemmas |
| E3 | every positive run has `ell<p0(h)^2` | Lemma `finite-runs` |
| E4 | raw MWIS has the exact finite odd-run identity | equation `alpha-run` |
| E5 | `C_h(q_P)=M_h(q_P)=B_(h,P)` on qualified square clocks | Proposition `finite-endpoint` |
| E6 | prime-initial square supports converge termwise to `B_infinity(h)` | Proposition `cofinal` |
| E7 | fresh-prime recurrence is `N'=(P^2-1)N`, `alpha'=(P^2-1)alpha+E` | Proposition `fresh-recurrence` |
| E8 | a fresh-prime step is strict iff the old positive graph has an even run | equation `normalized-gain` |
| E9 | `M_9(36)=M_9(900)=2K1/3` is a genuine plateau | Remark `plateau` |
| E10 | CRT creates an exact length-two run after a finite extension | Lemma `CRT-two-run` |
| E11 | every qualified finite square support is eventually followed by a strict lift | Proposition `eventual-strictness` |
| E12 | arbitrary `q` embeds into a same-support cover below the cofinal endpoint | proof of Theorem `endpoint` |
| E13 | `sup_(q finite)C_h(q)=B_infinity(h)` and every finite `q` is strict | Theorem `endpoint` |

## Landscape over fixed lags

| ID | Claim | Evidence |
|---|---|---|
| H1 | every fixed `h` has `R_(1,h)>0`, hence `B_infinity(h)>3/pi^2` | Lemma `isolated-positive` |
| H2 | for `d_Y=product_(p<=Y)p^2` and `h_Y=d_Y/2`, every run boundary comes from `p>Y` | Lemma `outside-prime-tail` |
| H3 | `B_infinity(h_Y)-3/pi^2 <= (1/2)sum_(p>Y)p^-2 -> 0` | equation `outside-tail` |
| H4 | `inf_(fixed h>=1)B_infinity(h)=3/pi^2`, unattained | Corollary `lag-infimum` |
| H5 | no supremum, maximum, or monotonicity claim over `h` is made | theorem statement and claim firewall |

## Frozen artifact identities

| Object | Frozen identity |
|---|---|
| RH-395 direct predecessor | commit `20de7202518f4488cbd9c7d63bf94aaa3dc94476` |
| RH-394 analytic source | commit `6b3d616851cd2d7cba66371d0aa9f25b8e8bf2f7` |
| RH-375 finite precedent | commit `071fed1b2a5d8488b9d2e35a99a753953b233584` |
| Git closure | 160 objects in `148+8+4`, digest `472bf5ce5e352dce0d3a44ad10b22345b98e0e8b9a0cd745be9ecd93dedf0a86` |
| logical closure | `160+4=164`, digest `72040ab3d7a5d98ce308b91d0748d52a8d4886cf245f5079f14c69ee659cc287` |
| certificate | 96 rows, 83,309 canonical bytes, SHA-256 `7cc0da78ee7e47a22b357d7e8d907bc9d9879caeb82ede30709e8cb1023032ba` |
| result | 290,629 pretty bytes, SHA-256 `a7ea39793a255a9b51f2e1b8523293bf4f4a9fdd0934263f9950417ca28371d4` |
| schema | 1,629,267 pretty bytes, SHA-256 `b78f958c60b1651446a3e0ac2af7a2e696cba2642a6414237877d997ff51691a` |
| manuscript | 48,304 bytes, SHA-256 `5d9a8c6c9a39436d07a94e082fffc003cfba91ece1d3859c11e2facbd5ffe99d` |
| PDF | 447,519 bytes, 15 A4 pages, SHA-256 `590f472a38bbe652b4f3a2e1eac11a407d9c5ed8a076abb3419334106834db1d` |

## Claim ceiling

Outside scope are growing lags, clocks, or tables; uniform or effective
rates; ordinary Cesaro convergence; maximum-before-limit or adaptive rules;
causal access; even four-shift and larger-window laws; generic graph
capacities; analytic operators or traces; zeta-zero identification; the
Riemann hypothesis; and Gates A--E.
