# RH-398 theorem ledger

## Objects and quantifiers

| ID | Frozen statement | Status |
|---|---|---|
| Q1 | `h>=1`, finite `q>=1`, every phase table `F`, and every admissible terminal clock `omega` are fixed before `X->infinity` | RH-396 interface |
| Q2 | `mu_0(k)=mu(k)` for `k>=1` and `mu_0(k)=0` for `k<=0` | definition |
| Q3 | `epsilon_F(n)=F_(n mod q)(mu_0(n-h),mu(n),mu(n+h))` and the terminal score retains the center multiplier `mu(n)` | definition |
| Q4 | the safety distance is `d=2h`, sharing the right symbol of one centered window with the left symbol of the next | definition |
| Q5 | every admissible `omega` has `1<=omega(X)<=X` and tends to infinity | RH-396 interface |
| Q6 | the fixed-table limit precedes the finite safe maximum; scalar suprema over finite `q` and fixed `h` come afterward | proved and firewalled |

## Product and telescope

| ID | Claim | Evidence |
|---|---|---|
| T1 | `t_p(d)=p^2/gcd(d,p^2)=p^(2-min(v_p(d),2))` | local CRT orbit calculation; certificate `TS01` |
| T2 | `A_m(d)=prod_p(1-min(m,t_p(d))/p^2)` | finite CRT independence, then absolute Euler-product passage; `TS02` |
| T3 | `p0=min{p prime:p does not divide d}` | definition; `TS03` |
| T4 | `A_m(d)=0` for every `m>=p0^2` | the `p0` local factor vanishes; `TS04` |
| T5 | `R_(ell,h)=A_ell-2A_(ell+1)+A_(ell+2)` | exact-run inclusion-exclusion; `TS05` |
| T6 | `R_(ell,h)>=0` is the density of an exactly bracketed positive run | finite phase-space event; `TS06` |
| T7 | the alternating sum starts at `m=1` with positive sign and ends at `p0^2-1` | `TS07`--`TS08` |
| T8 | `B_infinity(h)=sum_(m=1)^(p0^2-1)(-1)^(m+1)A_m(d)` | finite second-difference telescope plus the RH-396 endpoint; `TS09`--`TS12` |

## Path deletion and local transfer

Let `a(L)=ceil(L/2)` be the maximum independent-set size of a path of
length `L`.  Define `Lambda_T(L)` as `T a(L)` minus the sum, over all residue
classes modulo `T`, of the independent-set size after deleting that class.

| Parity of `T,L` | Exact `Lambda_T(L)` |
|---|---|
| `T` odd, `L` odd | `a(L)` |
| `T` odd, `L` even | `max(0,L/2-(T-1)/2)` |
| `T` even, `L` odd | `min(a(L),T/2)` |
| `T` even, `L` even | `0` |

For a prime `p` and collision level `e=min(v_p(d),2)`, the local path
contribution is

```text
V_(p,e)(L)=a(L)-Lambda_(p^(2-e))(L)/p^2.
```

For odd `p`, `V_(p,0)>=V_(p,1)>=V_(p,2)`.  All three values agree for odd
`L`.  For even `L<p`, the first two agree; their first strict separation is
at `L=p+1`.  The second inequality is strict for every even `L`.  Because
`d=2h`, prime `2` uses levels `1` and `2`, never the counterfactual level
`0`.  Exact strict fixtures are `(p,L)=(2,2),(3,4),(5,6),(7,8)` with local
gaps `1/4,1/9,1/25,1/49` in the relevant adjacent levels.

## Maximum and exact equality

| ID | Claim | Evidence |
|---|---|---|
| M1 | `B_infinity(h)<=B_infinity(1)` for every fixed `h>=1` | one-prime local transfer on a common finite support, then a common cofinal limit |
| M2 | if `2|h`, equivalently `4|d`, the level-`1` to level-`2` transfer at `L=2` is strict | exact-run cylinder and `ST01` |
| M3 | any odd square divisor of `h` gives a strict level-`0` to level-`2` transfer at `L=2` | `ST02`--`ST04` |
| M4 | a single factor `3`, `5`, or `7` gives strictness at `L=4`, `6`, or `8` | `ST05`--`ST07` |
| M5 | each strict local loss occurs on a positive-density exact-run CRT cylinder | `ST08`--`ST11` |
| M6 | every nonmaximizer falls into one of those strict branches | `ST12` |
| M7 | squarefree products of primes at least `11` are invisible for all possible base run lengths `1<=L<=8` | `MX01`--`MX07` |
| M8 | `B_infinity(h)=B_infinity(1)` iff `mu^2(h)=1 and gcd(h,210)=1` | exact partition, `MX08` |

Thus

```text
max_(h>=1) B_infinity(h)=B_infinity(1),
argmax B_infinity={h>=1:mu^2(h)=1 and gcd(h,210)=1}.
```

The conjunction is essential.  Neither squarefreeness alone nor coprimality
to `210` alone is sufficient.

## Complement and quantitative gap

| ID | Claim | Evidence |
|---|---|---|
| C1 | for primes `p>=11`, `h=p^2` lies outside the maximizer set | exact square branch |
| C2 | `0<B_infinity(1)-B_infinity(p^2)<=1/p^2` | a positive `L=2` cylinder and the total even-run weight bound |
| C3 | the complement supremum equals `B_infinity(1)` | let the fixed prime `p` tend to infinity after evaluating each fixed lag |
| C4 | the complement supremum is not attained | exact equality iff the maximizer criterion |
| C5 | `p0(h)>=5` implies `3|d` and `B_infinity(h)<=B_infinity(3)` | local transfer reduction |
| C6 | `B_infinity(1)-B_infinity(3)>1/36750>2/1334025` | positive-density exact-run cylinder with factors `1/2,1/25,1/49,tail>3/5,local loss 1/9` |

The square sequence is a sequence of separately fixed scalar lags.  It is not
an assertion about an `h(X)` terminal limit.

## Joint and retained endpoints

| ID | Claim | Evidence |
|---|---|---|
| J1 | `C_h(q)<B_infinity(h)` for every fixed `h` and finite `q` | RH-396 Theorem 1.3, equation (22) |
| J2 | `sup_(q finite)C_1(q)=B_infinity(1)` | RH-396 Theorem 1.3, equation (22) |
| J3 | `sup_(h>=1,q finite)C_h(q)=B_infinity(1)` | J1--J2 and M1 |
| J4 | no finite pair attains the joint supremum | strict part of J1 |
| J5 | `inf_(h>=1)B_infinity(h)=3/pi^2`, unattained | retained RH-396 Corollary 1.4, equation (23) |

## Frozen identities

| Object | Frozen identity |
|---|---|
| RH-397 direct predecessor | commit `dd63a109dcfa72365c749e0b183820d2611af733` |
| RH-396 analytic endpoint source | commit `cd57086fa90939d56656c3f952a08ffad9aabefe` |
| Git closure | 184 objects in `172+8+4`, digest `e7341caa25f0787a2e48a4d9c156e0d785b6c2a5516172bdfb25c2ac45377ea8` |
| logical closure | `184+4=188`, digest `4cc752fb7baae977bb15a9420101c5ed37727b1f3f7eecf72afce9dec3c73b13` |
| certificate | 72 rows, 36,635 canonical bytes, SHA-256 `d47de091a8fe5a134ba4bbf8ac4689f53b54786d45dc3bfc7061c99b46bea741` |
| result | 187,434 pretty bytes, SHA-256 `b22bd32fd515cbe98ee1fc946cef7e695273fdffd002cb5e29281ceba7e263f7` |
| schema | 961,955 pretty bytes, SHA-256 `5852ea6e0718185cd063ec56fd5ace000464f95741a2299e15dcd5405d447e8e` |
| manuscript source | 27,562 bytes, SHA-256 `96aa193b9fe66b613cf3ba95807e17c02b10e244e1d4a76bdbc5544e4337bdbf` |
| bibliography | 468 bytes, SHA-256 `dc4ea72d618069df20559cd7af7ab5b6d6c7405516427dbf544248b672810161` |
| publication PDF | 358,870 bytes, 11 A4 pages, SHA-256 `b5ac3c2f5489815dc4c98c64c88bb64d818c4ca3789dc789027332e968cfe96f` |
| compile log | 27,083 bytes, SHA-256 `54e9a49ad184cd8f7f3afe003c3ae52aa684c84c6976915f3f6cc8253011eb49` |

## Claim ceiling

Outside scope are growing or adaptive data; `h` or `q` depending on `X`;
uniform rates; ordinary Cesaro limits; prelimit maximization; causal rules;
monotonicity in `h`; an analytic inference from the finite certificate;
operators, traces, zeta zeros, RH, and Gates A--E.
