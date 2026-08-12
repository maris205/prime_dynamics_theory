# RH-397 theorem ledger

## Objects and quantifiers

| ID | Frozen statement | Status |
|---|---|---|
| Q1 | `h>=1`, finite declared `q>=1`, every phase table, and the terminal clock are fixed before `X->infinity` | proved interface |
| Q2 | `mu_0(k)=mu(k)` for `k>=1` and `mu_0(k)=0` for `k<=0` | definition |
| Q3 | the window is `(mu_0(n-h),mu(n),mu(n+h))`; the score multiplies the output by `mu(n)` | definition |
| Q4 | safety forbids positive outputs at `r` and `r+h` for every `x,z,y,w`, sharing both `z,y` | definition |
| Q5 | every admissible terminal clock has `1<=omega(X)<=X` and `omega(X)->infinity` | RH-394 bridge |
| Q6 | each fixed-table limit precedes the finite safe maximum; the odd-lag maximum over finite clocks comes last | proved and firewalled |

## Analytic bridge, projection, and flags

| ID | Claim | Evidence |
|---|---|---|
| A1 | RH-394 is the sole analytic terminal-law input at the three shifts `(+h,0,-h)` | manuscript Section 2; RH-394 through RH-396 |
| A2 | `Theta`, `Pi`, `lambda`, `kappa2(h)`, and `kappa3(h)` deduplicate prime-square collisions | equations `phase-density`--`score-table`; certificate groups A--B |
| A3 | the fourth letter `w` occurs only in finite safety and invokes no four-shift law or `c1111` | Lemma `three-shift-firewall` |
| A4 | positive projection is score-monotone and safety-preserving | Lemma `positive-projection` |
| A5 | input reflection preserves safety and negates the terminal limit | Lemma `input-reflection` |
| A6 | source/target flags satisfy safety exactly when `t_r s_(r+h)=0` | Lemma `flag-obstruction` |
| A7 | flag-class counts are `16,48,48,400`; exact saturating rectangles have sizes `4,6,6,9` | Lemma `flag-rectangle-saturation`; exhaustive oracle |

## Weights, edge filling, and capacity

| ID | Claim | Evidence |
|---|---|---|
| W1 | `M=Theta(C)`, `U=Theta(L,C)/2`, `V=Theta(C,R)/2`, `W=Theta(L,C,R)/4` | equation `MUVW` |
| W2 | the rectangle value is `M-(1-s)U-(1-t)V+(1-s)(1-t)W` | equation `rectangle-value` |
| W3 | `W<=U/2`, `W<=V/2`, including collision branches | equation `weight-bounds` |
| W4 | `V_r=U_(r+h)` holds in every `p not divides q`, `p parallel q`, and `p^2 divides q` branch | Lemma `phase-translation` |
| W5 | nonnegative edge filling saturates every edge to `t_r=1-s_(r+h)` | equations `edge-gain`--`edge-saturation` |
| W6 | the rising set `J={r:s_r=0,s_(r+h)=1}` is step-`h` independent | equation `rising-set` |
| W7 | every such independent set is realized, including the empty self-loop case | Lemma `rising-set-realization` |
| W8 | `C_h^hs(q)=K1-kappa2(h)/2+(1/4)max_J sum_(r in J)Theta_r(LCR)` for every fixed `h,q` | Theorem `fixed-clock-half-span` |
| W9 | both signs of every nonzero optimum are attained by reflection | Theorem 1.1 and Lemma `input-reflection` |

## Odd-lag maximum and attainment

| ID | Claim | Evidence |
|---|---|---|
| O1 | every independent-set bonus is at most the total `kappa3(h)` mass | equation `odd-upper-bound` |
| O2 | for odd `h`, the two-phase clock puts all triple mass on one parity and attains the upper bound | Lemma `q-two-attainment` |
| O3 | literal repetition makes every even declared clock attain; no minimal-period condition is imposed | proof of Theorem 1.2 |
| O4 | for every odd declared clock, CRT finds adjacent phases of positive triple weight, forcing strict loss | Lemma `odd-clock-strictness` |
| O5 | `max_q C_h^hs(q)=C_h^hs(2)=K1-kappa2(h)/2+kappa3(h)/4` for fixed odd `h` | Theorem `odd-lag-clock-maximum` |
| O6 | equality holds if and only if the declared finite clock is even | equation `attainment-parity` |
| O7 | `(h,q)=(4,4)` is an even-lag finite control, not an even-lag classification | Section 8 and certificate group F |

## Frozen identities

| Object | Frozen identity |
|---|---|
| RH-396 direct predecessor | commit `cd57086fa90939d56656c3f952a08ffad9aabefe` |
| RH-394 analytic source | commit `6b3d616851cd2d7cba66371d0aa9f25b8e8bf2f7` |
| RH-392 comparison | commit `9768c1cb5f56d959406c19119315afd542b6c30f` |
| RH-395 comparison | commit `20de7202518f4488cbd9c7d63bf94aaa3dc94476` |
| RH-375 comparison | commit `071fed1b2a5d8488b9d2e35a99a753953b233584` |
| Git closure | 172 objects in `160+8+4`, digest `b3f5688380762a4e3c27d512311f4c0d22173c434cc40459fc77bb3eb87fb5c4` |
| logical closure | `172+4=176`, digest `e9588b58f75e02e31ba5ffb279aea267074ec72f717afa84670f320d6c1030e0` |
| certificate | 72 rows, 24297 canonical bytes, SHA-256 `23f714236b53c2b89caa72b53f8139cfeab74cd07132082061c3ab0dfc048697` |
| result | 151768 pretty bytes, SHA-256 `d21f3ab160c7cb5cfca1ff04ac7d2104ea8a7802b36eb3e2f07e32cbe1d27e4f` |
| schema | 670920 pretty bytes, SHA-256 `4f16580a613e3e0c3930fd53e3a418023fac96e2cfa15f74ed447a60bea38f83` |
| manuscript | 27620 bytes, SHA-256 `a0ded93cfcd46f48b602e3f276a39e01e99ba8c37d3961316540f3925064ec11` |
| PDF | 387054 bytes, 9 A4 pages, SHA-256 `be06c3bcd37acb7f2144cd390423ae207f9b412ffd833a8156a317c59dd44ea6` |

## Claim ceiling

Outside scope are growing or adaptive data; uniform rates; ordinary Cesaro
limits; causal rules; a safety step of `2h`; unweighted optimizers; odd-clock
attainment for odd `h`; even-lag all-clock classification; four-shift or
larger-window analytic laws; generic graph capacity; operators, traces, zeta
zeros, RH, and Gates A--E.
