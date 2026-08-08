# RH Research Handoff

Status date: 2026-08-08

Current completed endpoint: RH-388

Completed research batch: RH-352 through RH-388

Post-four-volume independent theorem edges: RH-362 through RH-388

Latest completed-paper verdict: RH-388 Routes A/B `GO`; Route C `STOP_SCOPED`

Post-RH-388 breadth audit: pending; no RH-389 assigned

Prior RH-352--RH-361 publication commit:
`91167fe163831d3360b4c4007ed600865610e9ec`

RH-366 integration commit:
`0396fab97bbe3348c8237f8734dec0e1893fd3bf`

RH-367 integration commit:
`ed2076391759499d46a3d5f64d223cf469d63bbb`.

RH-368 integration commit:
`ebcf29a4a2d248d8320067d85899b3b8039a7b12`.

RH-369 integration commit:
`77549262532625c5dec8ac514a97bcee7b4503fc`.

RH-370 integration commit:
`9ad958a1f326eae6f43f026c84ab9378a4a42f16`.

RH-371 integration commit:
`241b78a89ccbc0bad96d9ef20ee9256d61b4eaca`.

RH-372 integration commit:
`7a7b10b74722b520b145064923af8df6d4e2e73f`.

RH-373 integration commit:
`e46a0b0ef0e459fc26711c379ce8c1b68deb9c58`.

RH-374 integration commit:
`2bb3baa6a09491c2d679d10c0dbcd39587d1f831`.

RH-375 integration commit:
`071fed1b2a5d8488b9d2e35a99a753953b233584`.

RH-376 integration commit:
`0cf6179084bc8151318bb8f0955e529c12c0661a`.

RH-377 integration commit:
`3c6e5658f4147891d15dac18d303a22a46d6e289`.

RH-378 integration commit:
`08574b1bab1b9f549d4c07df97bb548d40aae51f`.

RH-379 integration commit:
`9ae9802ed17529ef4adfb81d7e2158d47c3c8d22`.

RH-380 integration commit:
`dd94b9cfebdbf5df92084ba870b10d3a4d432bee`.

RH-381 integration commit:
`b6a6355b3390f3d00091a02cf77845b4f68a4a22`.

RH-382 integration commit:
`32afe96176ac00f4f261cf7097e0342a5c5194f1`.

RH-383 integration commit:
`bea5c88ca4ae9ca75511af42296ed099c1d6b11a`.

RH-384 integration commit:
`386b66a55c9263353c7d407fd712be7e6279f1e6`.

RH-385 integration commit:
`4fdb628bd624145082553e0a2ea57b5755ec571d`.

RH-386 integration commit:
`9778e3515d45816665d672a641947b93906abf54`.

RH-387 integration commit:
`dedd8e8d2c44564e66524a646f9cf5fb9a389c77`.

RH-388 integration commit:
`8e6f89ee1e58e67c53c5f4719c05e881107113ac`.

Non-numbered corpus synthesis: RH-MVP2

Synthesis publication commit:
`85269d06977fdfe52a501a8aac0104e63ad37fba`

Four-volume synthesis publication commit:
`c0aed13a34b8bbc53061aed23738660adcd3624c`

The repository, not an old chat transcript, is the source of truth.

## 1. Continuation protocol

Work in `/root/math/prime_dynamics_theory`. Before any state-changing RH
paper, run:

```bash
git status --short --branch
git pull --rebase origin main
```

Read completely:

- `AGENTS.md`
- `RH_HANDOFF.md`
- `papers/RH-369-branch-symmetric-markov-mobius-orthogonality/README.md`
- `papers/RH-369-branch-symmetric-markov-mobius-orthogonality/UPDATED_ROADMAP.md`
- `papers/RH-369-branch-symmetric-markov-mobius-orthogonality/THEOREM_LEDGER.md`
- `papers/RH-369-branch-symmetric-markov-mobius-orthogonality/results/result.json`
- `papers/RH-369-branch-symmetric-markov-mobius-orthogonality/main.pdf`
- `papers/RH-370-fold-compatible-ulam-spike-barrier/README.md`
- `papers/RH-370-fold-compatible-ulam-spike-barrier/UPDATED_ROADMAP.md`
- `papers/RH-370-fold-compatible-ulam-spike-barrier/THEOREM_LEDGER.md`
- `papers/RH-370-fold-compatible-ulam-spike-barrier/results/result.json`
- `papers/RH-370-fold-compatible-ulam-spike-barrier/main.pdf`
- `papers/RH-371-eight-run-distance-two-capacity-obstruction/README.md`
- `papers/RH-371-eight-run-distance-two-capacity-obstruction/UPDATED_ROADMAP.md`
- `papers/RH-371-eight-run-distance-two-capacity-obstruction/THEOREM_LEDGER.md`
- `papers/RH-371-eight-run-distance-two-capacity-obstruction/results/result.json`
- `papers/RH-371-eight-run-distance-two-capacity-obstruction/main.pdf`
- `papers/RH-372-bounded-constraint-graph-transducer-certificates/README.md`
- `papers/RH-372-bounded-constraint-graph-transducer-certificates/UPDATED_ROADMAP.md`
- `papers/RH-372-bounded-constraint-graph-transducer-certificates/THEOREM_LEDGER.md`
- `papers/RH-372-bounded-constraint-graph-transducer-certificates/results/result.json`
- `papers/RH-372-bounded-constraint-graph-transducer-certificates/main.pdf`
- `papers/RH-373-composite-clock-mobius-capacity-floor/README.md`
- `papers/RH-373-composite-clock-mobius-capacity-floor/UPDATED_ROADMAP.md`
- `papers/RH-373-composite-clock-mobius-capacity-floor/THEOREM_LEDGER.md`
- `papers/RH-373-composite-clock-mobius-capacity-floor/results/result.json`
- `papers/RH-373-composite-clock-mobius-capacity-floor/main.pdf`
- `papers/RH-374-square-clock-euler-product-capacity-floor/README.md`
- `papers/RH-374-square-clock-euler-product-capacity-floor/UPDATED_ROADMAP.md`
- `papers/RH-374-square-clock-euler-product-capacity-floor/THEOREM_LEDGER.md`
- `papers/RH-374-square-clock-euler-product-capacity-floor/results/result.json`
- `papers/RH-374-square-clock-euler-product-capacity-floor/main.pdf`
- `papers/RH-375-all-clock-one-site-mobius-capacity-supremum/README.md`
- `papers/RH-375-all-clock-one-site-mobius-capacity-supremum/UPDATED_ROADMAP.md`
- `papers/RH-375-all-clock-one-site-mobius-capacity-supremum/THEOREM_LEDGER.md`
- `papers/RH-375-all-clock-one-site-mobius-capacity-supremum/results/result.json`
- `papers/RH-375-all-clock-one-site-mobius-capacity-supremum/main.pdf`
- `papers/RH-376-shift-two-chowla-run-density-boundary/README.md`
- `papers/RH-376-shift-two-chowla-run-density-boundary/UPDATED_ROADMAP.md`
- `papers/RH-376-shift-two-chowla-run-density-boundary/THEOREM_LEDGER.md`
- `papers/RH-376-shift-two-chowla-run-density-boundary/results/result.json`
- `papers/RH-376-shift-two-chowla-run-density-boundary/main.pdf`
- `papers/RH-377-mixed-exponent-run-hierarchy-two-envelope-capacity/README.md`
- `papers/RH-377-mixed-exponent-run-hierarchy-two-envelope-capacity/UPDATED_ROADMAP.md`
- `papers/RH-377-mixed-exponent-run-hierarchy-two-envelope-capacity/THEOREM_LEDGER.md`
- `papers/RH-377-mixed-exponent-run-hierarchy-two-envelope-capacity/results/result.json`
- `papers/RH-377-mixed-exponent-run-hierarchy-two-envelope-capacity/main.pdf`
- `papers/RH-378-safe-window-memory-and-online-capacity-transducers/README.md`
- `papers/RH-378-safe-window-memory-and-online-capacity-transducers/UPDATED_ROADMAP.md`
- `papers/RH-378-safe-window-memory-and-online-capacity-transducers/THEOREM_LEDGER.md`
- `papers/RH-378-safe-window-memory-and-online-capacity-transducers/results/result.json`
- `papers/RH-378-safe-window-memory-and-online-capacity-transducers/main.pdf`
- `papers/RH-379-phasewise-chowla-free-memory-supremum/README.md`
- `papers/RH-379-phasewise-chowla-free-memory-supremum/UPDATED_ROADMAP.md`
- `papers/RH-379-phasewise-chowla-free-memory-supremum/THEOREM_LEDGER.md`
- `papers/RH-379-phasewise-chowla-free-memory-supremum/results/result.json`
- `papers/RH-379-phasewise-chowla-free-memory-supremum/main.pdf`
- `papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/README.md`
- `papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/UPDATED_ROADMAP.md`
- `papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/THEOREM_LEDGER.md`
- `papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/results/result.json`
- `papers/RH-380-square-clock-monotonicity-and-finite-clock-nonattainment/main.pdf`
- `papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/README.md`
- `papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/UPDATED_ROADMAP.md`
- `papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/THEOREM_LEDGER.md`
- `papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/results/result.json`
- `papers/RH-381-prime-square-tail-rate-and-quadratic-memory-remainder/main.pdf`
- `papers/RH-382-two-scale-prime-square-tail-expansion/README.md`
- `papers/RH-382-two-scale-prime-square-tail-expansion/UPDATED_ROADMAP.md`
- `papers/RH-382-two-scale-prime-square-tail-expansion/THEOREM_LEDGER.md`
- `papers/RH-382-two-scale-prime-square-tail-expansion/results/result.json`
- `papers/RH-382-two-scale-prime-square-tail-expansion/main.pdf`
- `papers/RH-383-exact-euler-tail-partition-normal-form/README.md`
- `papers/RH-383-exact-euler-tail-partition-normal-form/UPDATED_ROADMAP.md`
- `papers/RH-383-exact-euler-tail-partition-normal-form/THEOREM_LEDGER.md`
- `papers/RH-383-exact-euler-tail-partition-normal-form/results/result.json`
- `papers/RH-383-exact-euler-tail-partition-normal-form/main.pdf`
- `papers/RH-384-prime-tail-scale-separation/README.md`
- `papers/RH-384-prime-tail-scale-separation/UPDATED_ROADMAP.md`
- `papers/RH-384-prime-tail-scale-separation/THEOREM_LEDGER.md`
- `papers/RH-384-prime-tail-scale-separation/results/result.json`
- `papers/RH-384-prime-tail-scale-separation/main.pdf`
- `papers/RH-385-polylogarithmic-clock-phasewise-memory-uniformization/README.md`
- `papers/RH-385-polylogarithmic-clock-phasewise-memory-uniformization/UPDATED_ROADMAP.md`
- `papers/RH-385-polylogarithmic-clock-phasewise-memory-uniformization/THEOREM_LEDGER.md`
- `papers/RH-385-polylogarithmic-clock-phasewise-memory-uniformization/results/result.json`
- `papers/RH-385-polylogarithmic-clock-phasewise-memory-uniformization/main.pdf`
- `papers/RH-386-vinogradov-korobov-growing-order-prime-tail-uniformization/README.md`
- `papers/RH-386-vinogradov-korobov-growing-order-prime-tail-uniformization/UPDATED_ROADMAP.md`
- `papers/RH-386-vinogradov-korobov-growing-order-prime-tail-uniformization/THEOREM_LEDGER.md`
- `papers/RH-386-vinogradov-korobov-growing-order-prime-tail-uniformization/results/result.json`
- `papers/RH-386-vinogradov-korobov-growing-order-prime-tail-uniformization/main.pdf`
- `papers/RH-387-all-order-prime-tail-integral-resummation/README.md`
- `papers/RH-387-all-order-prime-tail-integral-resummation/UPDATED_ROADMAP.md`
- `papers/RH-387-all-order-prime-tail-integral-resummation/THEOREM_LEDGER.md`
- `papers/RH-387-all-order-prime-tail-integral-resummation/results/result.json`
- `papers/RH-387-all-order-prime-tail-integral-resummation/main.pdf`
- `papers/RH-388-rank-one-p2-tail-resummation/README.md`
- `papers/RH-388-rank-one-p2-tail-resummation/UPDATED_ROADMAP.md`
- `papers/RH-388-rank-one-p2-tail-resummation/THEOREM_LEDGER.md`
- `papers/RH-388-rank-one-p2-tail-resummation/results/result.json`
- `papers/RH-388-rank-one-p2-tail-resummation/main.pdf`
- `papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/README.md`
- `papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/UPDATED_ROADMAP.md`
- `papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/THEOREM_LEDGER.md`
- `papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/results/result.json`
- `papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/main.pdf`
- `papers/RH-368-parity-factor-mobius-capacity-limit/README.md`
- `papers/RH-368-parity-factor-mobius-capacity-limit/UPDATED_ROADMAP.md`
- `papers/RH-368-parity-factor-mobius-capacity-limit/THEOREM_LEDGER.md`
- `papers/RH-368-parity-factor-mobius-capacity-limit/results/result.json`
- `papers/RH-368-parity-factor-mobius-capacity-limit/main.pdf`
- `papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md`
- `papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/UPDATED_ROADMAP.md`
- `papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/THEOREM_LEDGER.md`
- `papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json`
- `papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/main.pdf`

Retain RH-362 as the return-rank input, RH-363 as the entropy-tower input,
RH-364 as the weighted-survivor/prime-copy input, RH-365 as the unweighted
return-bouquet input, RH-366 as the Hénon Möbius-correlation input, RH-367 as
the boundary-aligned cyclic-Ulam input, RH-368 as the parity-factor capacity
input, RH-369 as the branch-symmetric Markov/Gibbs input, RH-370 as the
fold-compatible Ulam/spike input, RH-371 as the exact eight-run/cyclic-pair
capacity input, RH-372 as the bounded graph/transducer input, RH-373 as the
composite-clock capacity-floor input, RH-374 as the square-clock
Euler-product family input, RH-375 as the all-finite-clock one-site supremum
input, RH-376 as the shift-two Chowla/run-density boundary input, RH-377 as
the mixed-exponent run-hierarchy/two-envelope input, RH-378 as the
safe-window/online-transducer input, RH-379 as the phasewise Chowla-free
memory-supremum input, RH-380 as the finite-clock nonattainment/gap input,
RH-381 as the prime-square-tail rate/quadratic-remainder input, RH-382 as the
two-scale second-order/cubic-remainder input, RH-383 as the exact Euler-tail
partition-normal-form input, RH-384 as the prime-tail scale-separation input,
RH-385 as the fixed-polylogarithmic-clock phasewise-memory uniformization
input, RH-386 as the Vinogradov--Korobov growing-order prime-tail
uniformization input, RH-387 as the all-order prime-tail integral-resummation
input, RH-388 as the rank-one `P_2`-scale resummation and bounded-gap
necessity input, and RH-361 as the immediate endpoint of the still-open original
physical branch.

For corpus-level synthesis or new-route selection, also read completely:

- `papers/RH-MVP2-corpus-frontier-synthesis/README.md`
- `papers/RH-MVP2-corpus-frontier-synthesis/CROSSWALK.md`
- `papers/RH-MVP2-corpus-frontier-synthesis/THEOREM_LEDGER.md`
- `papers/RH-MVP2-corpus-frontier-synthesis/results/summary.json`
- `papers/RH-MVP2-corpus-frontier-synthesis/main.pdf`

RH-388 is now integrated.  It separates the exact rank-one prime tail from
the smooth higher-rank hierarchy and resolves the intrinsic `P_2` scale.  For
`x=p_y`, `L=log x>=512`, `c in {1,...,7}`, and every integer
`1<=K<=floor(3L)`, put

```text
V=L^(3/5)(log L)^(-1/5),
epsilon_x=0.027L^1.801 exp(-0.1853V),
K_r=x^(1-2r)/[(2r-1)L],
a_r=1/[(2r-1)L],
S_K(a)=sum_(j=0)^(K-1)(-1)^j j!a^j,
I_(2r)^[K]=K_r S_K(a_r),
Psi_c^[K]=cP_1(y)+sum_(r>=2)c^r I_(2r)^[K]/r.
```

For the exact RH-383 endpoint map `F`, let
`Gap_K=F(Psi^[K])/pi^2`.  The higher-rank source, power-kernel, and exact
factorial ledgers give

```text
pi^2 abs(Gap_P-Gap_K)
 <=x^(-3)/L[7560epsilon_x+1638/x^2+1176K!/(3L)^K],
lim_(y->infinity) max_(1<=K<=floor(3log p_y))
 abs(Gap_P-Gap_K)/P_2(y)=0.
```

The recurrence `b_(K+1)/b_K=(K+1)/(3L)<=1` pays the complete moving
integer window; finite `K` fixtures are not used as its proof.  The exact
`P_1` coordinate is essential within the frozen `P/J/I` hierarchy.
Maynard's unconditional bounded-consecutive-gap theorem and exact strict
succession imply

```text
limsup_y p_y^2 abs(P_1(y)-I_2(p_y))>=1/2,
limsup_y p_y^2 pi^2 abs(Gap_P-Gap_I)>=X_infinity,
limsup_y p_y^2 pi^2 abs(Gap_P-Gap_J)>=X_infinity.
```

The endpoint proof uses the exact direction
`grad F(0).(1,2,3,4,5,6,7)=2X_infinity`, Hessian ledger `224`, and Taylor
remainder `112`.  This is a necessity theorem only for the declared smooth
kernel hierarchy, not for every conceivable surrogate.  It proves no
convergent factorial series, larger `K` window, `P_3` or cubic precision,
complex channel, growing clock, active `c_11`, adaptive capacity, operator,
trace, zero model, RH statement, or Gate A--E conclusion.  Routes A and B
are `GO`; Route C is `STOP_SCOPED`.

RH-387 is now integrated.  It resums the entire strict prime-tail family
before any relative logarithm is taken.  For `x=p_y`, `L=log x>=512`, and
each real integer channel `1<=c<=7`, put

```text
V=L^(3/5)(log L)^(-1/5),
epsilon_x=0.027L^1.801 exp(-0.1853V),
Phi_c^P=sum_(r>=1)c^r P_r(y)/r,
Phi_c^J=integral_x^infinity -log(1-c/(t^2-1))/log(t) dt,
Phi_c^I=integral_x^infinity -log(1-c/t^2)/log(t) dt.
```

Writing the seven-vectors as `Phi^P`, `Phi^J`, and `Phi^I`, the exact RH-383
endpoint map `F` defines the actual square-clock gap and its two integral
surrogates.  The new finite-dimensional transfer proves

```text
max_c abs(Phi_c^P-Phi_c^J)<=28epsilon_x/(xL),
0<=max_c(Phi_c^J-Phi_c^I)<=14/(3x^3L),
pi^2 abs(Gap_P-Gap_J)<=3528epsilon_x/(xL),
pi^2 abs(Gap_J-Gap_I)<=588/(x^3L).
```

The proof first sums the absolute strict-Stieltjes error by nonnegative
Tonelli and only then applies a new `ell^infinity`-to-`ell^1` endpoint
Lipschitz bound `126`.  It therefore pays the infinite-order source/kernel
exchange that is outside RH-386's finite-partition theorem.  Since
`epsilon_x x^2->infinity`, this source error is larger than the `P_2` scale:
RH-387 proves no second-order or cubic precision, no complex-`c` theorem, no
growing clock or active `c_11` result, and no Gate A--E conclusion.  Its
verdict is `Route A=GO`; Route B is `STOP_SCOPED`.

RH-386 is now integrated.  It imports the Johnston--Yang explicit
Vinogradov--Korobov estimate through a versioned, hash-locked remote source
record while excluding the copyrighted PDF and source tar from the release.
For `x=p_y`, `L=log x`,

```text
V=L^(3/5)(log L)^(-1/5),
epsilon_x=0.027L^1.801 exp(-0.1853V),
P_r(y)=sum_(p>x)(p^2-1)^(-r),
K_r=x^(1-2r)/[(2r-1)L].
```

The strict Stieltjes boundary, the exact and power kernels, and the leading
kernel give a uniform growing-order theorem.  For a partition
`lambda=1^k_1 2^k_2 ...`, with

```text
d=sum_r r k_r,
R=max{r:k_r>0},
H=sum_r k_r/(2r-1),
H_2=sum_r k_r/(2r-1)^2,
```

then, whenever `L>=512` and `7R epsilon_x<=1/2`, the refined estimate is

```text
abs(log(P_lambda/M_lambda)+H/L)
 <=14d epsilon_x+d/(x^2-1)+2H_2/L^2.
```

Thus the source-and-power condition
`d epsilon_x+d/x^2->0` is robustly sufficient, and within that regime the
elementary leading equivalent holds if and only if `H/L->0`, uniformly for
finite partition families as stated in the paper.  The simpler conditions
`log d=o(V)` and `H=o(L)` suffice.  For one factor, `log R=o(V)` is uniform,
and every fixed `0<delta<0.1853` permits
`R<=exp((0.1853-delta)V)`.  For every fixed `c>0`, the family
`1^floor(cL)` tends to `exp(-c)` and proves that the `H/L` obstruction is
intrinsic.  RH-386 is
`Route A=GO`; Route B is `STOP_SCOPED`.  It proves no growing clock, active
`c_11`, adaptive capacity, effective first index, operator, trace, zero
model, RH statement, or Gate A--E conclusion.

RH-385 is now integrated.  It retains the frozen RH-379 universally safe,
phasewise-`c_11=0`, periodic lag-two class and proves that every fixed
polylogarithmic clock window is uniform.  For every fixed real `B>0`, with
`H_B(N)=floor((log N)^B)`, it proves

```text
sup_(1<=q<=H_B(N), f in F_q) abs(S_N(q,f)-L_q(f)) ->0.
```

For every integer cutoff `P>=2`, the proof retains the all-finite ledger

```text
abs(S_N(q,f)-L_q(f))
 <=4sqrt(Q)D_*(N)/N+13tau_P+6Q/N+4/N,
Q=lcm(q,(product_(p<=P)p)^2).
```

Taking `P=floor(sqrt(log log N))` and one fixed Davenport exponent `A>B/2`
pays the Fourier mass.  The restricted optimizers converge uniformly, their
maximum tends to `B_infinity`, and the nonempty square-clock diagonal gives
an explicit positive witness.  This is not polynomial-clock uniformity, a
varying-`B` theorem, active phasewise-`c_11` cancellation, an adaptive
capacity limit, or a projectively compatible infinite selector.  RH-385 is
`Route A=GO`; Route B remains `STOP_SCOPED`, and all Gates remain false/open.
The post-RH-385 source gate was later paid by the versioned Johnston--Yang
lock, and the resulting growing-order theorem is now published as RH-386.
Fixed-period logarithmic cancellation still does not activate `c_11`, and
the available Davenport theorem still does not prescribe a
super-polylogarithmic clock.  The subsequent breadth audits assigned and
published RH-387 and then RH-388 as the distinct all-order and rank-one
`P_2` theorems above.  No post-RH-388 breadth audit has yet assigned RH-389.
The geometrically selected non-Parry measure route is
`STOP_SCOPED` until a fixed geometrically selected equilibrium state and its
mixing theorem are proved.  The deterministic cyclic-Ulam strong-space route
is `STOP_SCOPED` until a fixed mesh-independent norm, a
uniform projection/lift estimate, and a common contour around `-1` are
actually supplied. RH search remains breadth-first: generate bold
source-backed candidates, evaluate
standalone discovery value as Route A and RH data-type compatibility as Route
B, then issue `GO`, `STOP_SCOPED`, or `NOT_TESTABLE`. Create a new number only
for an actual bridge, a typed `q/E_off` theorem, a rigorous physical
obstruction, or another independent theorem edge. An abstract fiber, finite
fit, deterministic reparameterization, prime-labelled factor inserted by
definition, adaptive arithmetic encoding presented as intrinsic coupling, or
inactive criterion is not a reopening input.

Follow the multi-agent workflow in `AGENTS.md`: the primary alone chooses the
route, edits this handoff, integrates, stages, commits, rebases, and pushes.
Use subagents for source lock, adversarial proof audit, one exclusive writer,
and release QA. Preserve all unrelated caches, checkpoints, LaTeX
intermediates, and TPC work. Stage only the active RH files. Pull with rebase
before every commit and again before every push.

### 1.1 Non-numbered corpus synthesis layer

`papers/RH-MVP2-corpus-frontier-synthesis/` is a provenance-preserving
umbrella survey for RH-1--RH-361. It is not RH-362 and does not change the
completed numbered endpoint. The original papers remain the atomic sources;
the synthesis records their canonical paths and selected SHA-256 hashes.

The executable inventory verifies:

- 361 unique numerical labels, exactly RH-1--RH-361;
- 365 numerical RH directories, with four empty legacy alias directories at
  RH-302, RH-303, RH-304, and RH-306;
- 29 established review anchors with a declared-range union of 349/361 IDs;
- 1,356 selected source-file hashes; and
- all five Gates and all five named forbidden macro claims remain false.

The umbrella manuscript has 6 pages. Its tests pass `7/7`, including the
four-volume archive mutation checks; the local/corpus archive verifier covers
23 publication files with zero failures; Ghostscript parses the PDF; all 17
font rows are embedded; all six rendered pages were visually checked; and the
semantic PDF is byte-identical to `main.pdf`.

The publication-scale expansion is complete as four provenance-preserving
volumes:

1. `papers/RH-MVP1-conditional-prime-dynamics-hilbert-polya-roadmap/`,
   Volume I, RH-1--RH-160;
2. `papers/RH-VOL2-physical-riesz-cloud-trace-envelope-synthesis/`,
   Volume II, RH-161--RH-241;
3. `papers/RH-VOL3-deterministic-numerator-anchor-counterloop-synthesis/`,
   Volume III, RH-242--RH-281; and
4. `papers/RH-VOL4-noisy-head-annulus-signed-completion-synthesis/`,
   Volume IV, RH-282--RH-361.

These are synthesis papers, not a new unconditional theorem chain. The 361
numbered papers remain the atomic provenance layer, and the four executable
indices cover 160, 81, 40, and 80 labels with no gap or overlap. Every volume
retains per-claim `PROVED`, `CERTIFIED`, `CONDITIONAL`, `SCOPED_NEGATIVE`, and
`OPEN` distinctions. The mathematical route coordinate stays

```text
actual_same_clock_unnormalized_head_transport_open
```

RH-362 was activated only by independent trigger 5 and is not inserted into
these four volumes. The four-volume outer archive remains frozen under
RH-MVP2 and seals the four individual archive-verification records. Its
manifest and verification hashes are explicit external inputs of RH-362, so
the post-volume paper cannot silently replace the RH-1--RH-361 foundation.

## 2. Program objective and claim boundary

The project develops a conditional prime-dynamics route inspired by the
Hilbert--Polya program. It is not a proof of the Riemann Hypothesis.

- Gate A: canonical intrinsic dynamical spectral determinant.
- Gate B: time-oriented scattering or unitary completion.
- Gate C: genuine self-adjoint generator and intrinsic `T log T` law.
- Gate D: von Mangoldt-weighted prime-power traces.
- Gate E: equality with the completed-zeta divisor.

All five Gates are false/open. No batch paper constructs a Hilbert--Polya
operator, identifies Riemann zeros, proves a von Mangoldt trace, proves
completed-zeta divisor equality, or implies RH.

The RH-352--RH-361 physical batch has two typed branches and no cross-branch
bridge:

```text
actual direct branch      = RH-352--RH-354, actual p/Y,
                             but selected or normalized
deterministic counterloop = RH-355--RH-360, unconditional only for s
cross-branch bridge       = absent
```

On one common Hardy clock:

```text
p = tau-a = q-d
d = h-s
q = p+d
h = s+d
```

`p` is the actual direct coefficient, `q` the full-trace coefficient, `h`
the actual modulus-complete Hardy head, and `s` the deterministic graded
counterloop. RH-354's normalized actual `p` tail is neither an unnormalized
complete prefix nor a `q/E_off` theorem. Deterministic `s` is not an actual
head, root set, rank law, or spectral submultiset.

RH-362 through RH-370 add a separate arithmetic-dynamical branch. RH-362
builds one marked modular cycle per prime; RH-363 inserts the resulting ranks
into a pairwise-coprime admissible-shift tower; RH-364 derives weighted
analytic domains for a certified local survivor and audits an engineered
prime-copy operator; RH-365 proves an analytic disk and odd-prime primitive
anchors for the unweighted marked bouquet; RH-366 proves a periodic/Parry
Möbius-orthogonality dichotomy, an offline adaptive correlation, exact Parry
covariances, and an open capacity bracket on that survivor; RH-367 proves the
exact aligned finite-Ulam block/sign inheritance and crossing-cell phase
defect for a cyclic postcritically finite quadratic map; RH-368 proves an
exact capacity formula and the all-order `4/pi^2` limit for the distinct
three-cell parity factor `A_{\{2\}}`; RH-369 derives a non-Parry
branch-symmetric Markov family with fixed-parameter Möbius orthogonality and
exact covariance on the RH-366 graph; RH-370 proves exact finite folding for
mirror-compatible Ulam partitions, an exterior `L^1` resolvent bridge, and a
deterministic terminal-spike/BV obstruction to the natural strong-space route;
RH-371 proves an exact eight-run reduction for the distance-two capacity and a
scoped cyclic pair-ledger obstruction; RH-372 proves exact open-path max-plus
capacity dynamic programming, a finite universal-safety test for clocked
transducers, and an unconditional one-site Möbius correlation formula with
squarefree arithmetic-progression densities. None is identified
with either typed physical branch, so the physical blocker below is unchanged.

The deterministic target side remains exact and all-order: RH-263 gives the
deterministic numerator coefficient anchor, and RH-267--RH-268 give the
deterministic all-order envelope and sharp target radius. These results do
not close the RH-241 moving noisy all-order envelope or coefficient bridge.
RH-288 remains inactive because the complete same-type physical prefix leaf
is absent.

## 3. Decision after RH-361 through RH-365

Current route coordinate:

```text
actual_same_clock_unnormalized_head_transport_open
```

The first physical blocker is

```text
D_(4k)(R)
 = sum_(2<=n<4k) |h_(sigma,n)-s_(k,n)| R^n/n
 -> 0.
```

All RH-355--RH-360 actual-head inheritance statements assume this
unnormalized, same-clock leaf; none proves it. Normalized upper-band matching
or coordinatewise relative matching does not imply it.

RH-361 proves a finite coefficient-information-class theorem. On a fixed
nonempty finite order set `I`, for positive weights and fixed signed arrays
`p,s`, every signed array `e` gives

```text
d[e] = e
q[e] = p+e
h[e] = s+e.
```

The identities hold exactly. Along `e=t v`, `v!=0`, the weighted norms of
`q[e]` and `h[e]` have no finite uniform upper bound determined by `p,s`.
The choices `e=-p` and `e=-s` give `q=0` and `h=0`, respectively, so each
norm has infimum zero. This does not say the same fiber makes both zero, that
arbitrary defects are physically realizable, or that two noisy operators
have been constructed. `E_off`, roots, ranks, multisets, and determinants
still require separate realization/identification theorems.

The deterministic terminal-lag route is closed only at its declared budget
type: geometric localization (RH-358), logarithmic inverse accuracy
(RH-359), and the exponential-transform phase diagram (RH-360). Actual
transfer remains conditional on `D_(4k)(R)->0`.

### 3.1 RH-362 independent arithmetic-dynamical branch

Fix the integral H\'enon automorphism

```text
H(x,y) = (1-6x^2-y,x)
```

and an integral point `P`. The locked source theorem is

```text
M | a_n(P)  iff  r_M(P) | n,
```

where `r_M(P)` is the return period of `P mod M` and `a_n(P)` is the gcd of
the two integral coordinate differences. For nonperiodic `P`, RH-362 proves
the exact finite identity

```text
{p : r_p(P)<K} = {p : p divides product_(1<=n<K) a_n(P)}.
```

Hence `r_p(P)` tends to infinity outside a finite set at every fixed
threshold. The concrete seed `P=(0,0)` is nonperiodic by a strict
negative-cone escape argument.

The complete marked `r_p`-cycle gives

```text
Tr(U_p^n) = r_p 1_(r_p|n),
det(I-zU_p) = 1-z^(r_p).
```

The countable tagged bouquet has finite fixed-point counts in every order and
only a formal Artin--Mazur product. Its Dirichlet specialization

```text
Z_P(s) = product_p (1-p^(-s r_p))^(-1)
```

converges normally, is holomorphic, and is zero-free on `Re(s)>0`. Its
coefficients are multiplicative `0/1` values; its logarithmic derivative has
weights `r_p log p` at `p^(j r_p)`, not von Mangoldt weights. Neither `Z_P`
nor its reciprocal crosses `s=0` meromorphically; this is not a whole-axis
natural-boundary theorem.

The natural block operator `T_s=direct_sum_p p^(-s)U_p` is compact for
`Re(s)>0`; `q Re(s)>3` is a proved sufficient Schatten condition, and the
ordinary Fredholm identity is licensed only for `Re(s)>3`. If one instead
uses `p^(-s/r_p)`, each local factor is forced to `1-p^(-s)`, but the result
forgets every return length and the direct sum lies in no finite Schatten
class. This is a scoped obstruction, not a zeta bridge.

For a conditional exact integral period `N`, almost every `r_p=N`, so the
product is `zeta(Ns)` times a finite Euler correction. This injects zeta via
the prime labels and almost-constant local periods; it is not spectral
recovery. No integral periodic point for this map is asserted.

### 3.2 RH-363 prime-return entropy tower

For every nonperiodic integral point `P` and integer `m>=1`, RH-363 defines

```text
B_m(P) = {p^(m r_p(P)) : p prime},
X_m(P) = A_(B_m(P)).
```

The family is infinite, pairwise coprime, and thin. Every `X_m(P)` has only
the zero periodic point, hence

```text
zeta_(X_m)(z) = (1-z)^(-1)
```

at every level. Its normalized entropy nevertheless retains the complete
rank data:

```text
E_m(P) = h_top(X_m(P))/log(2)
       = product_p (1-p^(-m r_p(P)))
       = Z_P(m)^(-1),
```

with `E_m` strictly increasing to one. If `Lambda_m=-log E_m` and
`M_m=sum_p p^(-m r_p)`, then the absolutely convergent multiples inversion

```text
M_m = sum_(j>=1) mu(j) Lambda_(mj)/j
```

recovers every moment. Exact infinite moment peeling and unique
factorization then recover every labeled pair `(p,r_p)`. This is an
injectivity theorem for the exact full entropy sequence, not a stable finite
or noisy-data algorithm, and it does not recover `P`.

For the first `k` primes, with primorial `W_k`, the finite approximants obey

```text
N_n = 1  iff  W_k does not divide n.
```

Their first defect is at `W_k`; its prime-wheel value depends on `k/W_k` but
is independent of `P`, `m`, and the return exponents. Their logarithmic and
reduced-zeta radii tend to

```text
R_m^* = 2^(-E_m) < 1.
```

This is the exact compact-exhaustion radius for tailwise germ convergence,
not the zeta radius of the infinite `X_m`, which is one.

Route A is `GO`. Route B is `STOP_SCOPED` at data type: a full sequence of
topological entropies is not a signed von-Mangoldt prime-power trace ledger
of one canonical operator. The tower is well-defined and functorial after
`P,m` are fixed, but engineered rather than an intrinsic global H\'enon
dynamics. Gates A--E remain false/open.

### 3.3 RH-364 weighted survivor and cubic prime-copy obstruction

RH-364 freezes the certified local survivor of

```text
H_6(x,y) = (1-6x^2-y,x)
```

at source commit `ff44f961261349848c9f65ede6a031b7e155aca9`.
Its four-state adjacency matrix has

```text
det(lambda I-A) = (lambda^2-lambda-1)(lambda^2+1),
F_n = Tr(A^n) = Lucas_n + 2 cos(n pi/2),
0 <= p_n <= F_n/n <= 4 phi^n/n.
```

The exact cone certificate gives every primitive survivor multiplier
`L_o>=kappa^(n_o)`, with `kappa=773/224`. Therefore, for every real
`beta>=0`, the weighted Euler zeta and determinant converge normally and
are zero-free on

```text
|z| < kappa^beta/phi,
```

with an explicit all-order primitive-period tail. The correction product
`C_F` is analytic and zero-free on the larger disk
`|z|<kappa^2/phi`, but the quotient identity with the complete flat and
Euler determinants is directly licensed only on the common disk
`|z|<kappa/phi`. In particular, the reported finite-section root near
`3.429` is not certified.

The common-clock prime copy

```text
T_s = direct_sum_(ell prime) ell^(-s) A
```

is bounded iff `Re(s)>=0`, compact iff `Re(s)>0`, and belongs to `S_q` iff
`q Re(s)>1`. On `Re(s)>1`,

```text
D_A(s) = det_F(I-T_s) = product_n zeta(ns)^(-p_n),
D_A(s)^(-1) = product_n zeta(ns)^(p_n).
```

The first trace and primitive ledgers are

```text
(F_1,F_2,F_3) = (1,1,4),
(p_1,p_2,p_3) = (1,0,1).
```

Thus prime and square weights match the von Mangoldt coefficient, while
prime cubes carry `4 log p`, an exact surplus `3 log p`. For the weighted
prime lift, the natural unnormalized positive-weight product has a fractional
non-meromorphic singularity at `s=1`. Requiring the common scalar ledger to
have `Q_1=1` forces `c=L_*^beta`, then `Q_2=1` but

```text
Q_3 = 1 + 3 (L_*^3/L_3)^beta > 1.
```

The normalized infinite product is certified near `s=1` only for

```text
0 <= beta < beta_0 = 0.290834898770...
```

although the coefficient obstruction holds for every real `beta>=0`.

Route A is `GO`. Route B is `STOP_SCOPED`: the local survivor is intrinsic,
but copying it over every prime label is not a finite-field reduction,
Hasse--Weil factor, full `H_p` zeta, canonical global H\'enon operator, or
the physical noisy determinant. Gate A fails at data type, and Gate D also
fails exactly at prime cubes. Gates A--E remain false/open.

### 3.4 RH-365 return-bouquet height, analytic radius, and prime anchors

RH-365 freezes the reversing-axis seed `P_0=(0,0)` and writes

```text
x_(-1)=x_0=0,
x_(n+1)=1-6x_n^2-x_(n-1),
a_n=gcd(|x_n|,|x_(n-1)|).
```

Reversibility and the return-divisibility theorem give the exact all-order
midpoint identities

```text
a_(2k)   = |x_k-x_(k-1)|,
a_(2k+1) = |x_(k+1)-x_(k-1)|.
```

For `b_n=-x_n`, `n>=2`, the exact recursion and quadratic envelope are

```text
b_(n+1)=6b_n^2-b_(n-1)-1,
5b_n^2 <= b_(n+1) <= 6b_n^2,
5^(2^(n-1)-1) <= b_n <= 30^(2^(n-2))/6.
```

With `m=ceil(n/2)`, RH-365 proves explicit two-sided bounds for every
`n>=3`, hence `log a_n=Theta(2^(n/2))`. If

```text
c_d = #{p:r_p=d},
T_n = sum_(d|n) d c_d,
```

then `T_1=T_2=0` and

```text
T_n <= (log_2 30)n 2^(ceil(n/2)-2).
```

Therefore the marked-cycle Euler product

```text
Z_0(z)=product_p (1-z^(r_p))^(-1)
```

is holomorphic and zero-free on the strict disk `|z|<2^(-1/2)`, with

```text
sum_(n>=1) T_n r^n/n
 <= (log_2 30)(r^3+r^4)/(1-2r^2).
```

The origin Taylor radii of `log Z_0` and `Z_0` lie in
`[2^(-1/2),1]`; no exact radius, continuation, or natural boundary is
proved. For every odd prime order `ell`,

```text
{p:p|a_ell}={p:r_p=ell},
c_ell=omega(a_ell)>=1,
T_ell=ell c_ell,
[z^ell] log Z_0=c_ell.
```

This is an Euler-exponent, primitive-cycle, and logarithmic-coefficient
anchor. It is not the raw coefficient of `Z_0`: already
`[z^7]Z_0=3` while `c_7=1`, and `[z^11]Z_0=13` while `c_11=4`.

On the naive Hilbert direct sum, `direct_sum_p zU_p` is noncompact and lies
in no finite Schatten class for every `z!=0`. Thus the analytic Euler product
is not its ordinary Fredholm determinant, although `I-zU` is invertible for
`|z|<1`.

Route A is `GO`. Route B is `STOP_SCOPED`: the bouquet selects one marked
cycle from each of distinct finite-field maps, is not a full `H_p` zeta or
Hasse--Weil factor, and supplies no canonical global operator or signed
von-Mangoldt trace. Gates A--E remain false/open.

### 3.5 RH-366 Möbius orthogonality, adaptive encoding, and Parry covariance

RH-366 freezes the certified local Hénon survivor for

```text
H_6(x,y) = (1-6x^2-y,x)
```

and its primitive four-state subshift code, whose scalar signs obey the exact
distance-two rule that two `+` signs cannot occur at distance two.  With

```text
C_N(z,f) = N^(-1) sum_(n=1)^N mu(n) f(H_6^n z),
```

the paper proves six independent edges at the declared data type:

1. Every fixed periodic `z` is Möbius-orthogonal for every continuous `f`.
   The period is fixed before `N -> infinity`; no growing-period uniformity is
   asserted.
2. For transported Parry measure `nu`, a single full-measure set of points is
   simultaneously orthogonal for every continuous observable.  This is
   `nu`-almost sure, not uniform over the survivor.
3. After reading the complete positive-time Möbius sequence, an admissible
   coded point `z_mu` is selected with raw-sign correlation exactly
   `4/pi^2` (and correlation `2 sqrt(5)/pi^2` for the centered observable
   below).  This is an offline encoding theorem, not a spontaneous coupling.
4. For `F=(sqrt(5) epsilon+1)/2`, the mean is zero, variance is one, odd
   covariances vanish, and the lag-`2k` covariance is
   `(-phi^(-2))^k`.  The exact finite-prefix variance formula gives the
   unconditional bound `0 <= V_N <= sqrt(5) N`.
5. The density limit `V_N/N -> 6/pi^2` is conditional on ordinary (unweighted)
   Cesàro two-point Chowla at every fixed even shift.  Logarithmically averaged
   Chowla and the finite decimal diagnostic do not imply this limit.
6. The finite-horizon adaptive capacity `K_N` is exactly two path-MWIS
   problems, computable in `O(N)`, with

```text
4/pi^2 <= liminf K_N/N <= limsup K_N/N <= 6/pi^2.
```

No existence of `lim K_N/N` is proved.  The frozen `N=2^20` ordering test has
exceptional correlation `0.405335426`, capacity `0.492251396`, 420/1023 null
exceedances, and rank `p=421/1024=0.4111328125`; these are finite diagnostics
only.

The source locks are:

```text
henon_mobius_correlations  34490443f50cfe9af9ff93888e51e7e7e534a5a7
henon_weighted_zeta         ff44f961261349848c9f65ede6a031b7e155aca9
dyna_zeta_map               7fd3a3fdd5a6a25827a0965345459baf4a47b816
```

The package has `23/23` external-input locks, `17/17` tests, an independent
R001 checker pass with eight surrogate replays and witness residual about
`7.1e-15`, and a zero-failure archive.  The publication has 21 files; the
eight-page PDF has 20 embedded Unicode-mapped font rows and all pages pass
rendered inspection.  The semantic PDF is byte-identical to `main.pdf`.

Route A is `GO`.  Route B is `STOP_SCOPED` before Gate A: `z_mu` depends on
the full observed Möbius prefix, while the outputs are scalar orbit averages
and Parry variances rather than a canonical determinant, operator trace,
von-Mangoldt prime-power ledger, or spectral zero set.  Positive entropy means
the construction is outside the zero-entropy hypothesis of Sarnak's
conjecture.  Gates A--E remain false/open.

### 3.6 RH-367 boundary-aligned cyclic-Ulam structure and phase leakage

RH-367 freezes the postcritically finite quadratic map

```text
f_u(x)=1-u x^2,
u^3-2u^2+2u-2=0,
J=[-(u-1),1],
```

with `r=u-1`, `B_0=[-r,r]`, and `B_1=[r,1]`.  The exact band exchange is
`f(B_0)=B_1` and `f(B_1)=B_0`.  It proves, for every finite exact
cell-overlap Ulam partition with `r` as a cell boundary,

```text
P_h = [[0,A],[B,0]],       P_h s=-s,
```

where `s` is the band-sign vector.  This gives a finite-dimensional
`-1` mode and no claim about isolated continuum spectrum.

For a cell crossing `r`, with fraction `theta` in `B_0`, the projected sign
defect is exactly

```text
1-(2theta-1)^2=4theta(1-theta),
```

and a cell of width `h` contributes `4h theta(1-theta)`.  The global
stationary same-band mass and near-`-1` displacement are finite phase
diagnostics, not the local identity itself.  The frozen source scan has 33
phases at each of `N=256,512,1024,2048` plus one snapped aligned row: 136
rows, four aligned and 132 crossing.  Crossing projected mass ranges from
about `1.14e-4` to `7.71e-3`; maximum near-`-1` displacement is about
`4.91e-3`.

The cyclic source is locked at
`e7d21f646498d77e1c3213d1e4f35dc8466038ff`.  Source-lock and proof-audit
checks report 12/12 upstream tests, geometry residual at most `4.44e-16`,
and a zero-failure source protocol.  The RH-367 executable package has
23/23 external-input locks, 9/9 local tests, 21 publication files, 23
external inputs, a zero-failure archive, and a four-page PDF with 16 embedded
Unicode-mapped font rows; the semantic PDF is byte-identical to `main.pdf`.

The overlap ledger against RH-3, RH-10, and RH-55 is positive: those papers
cover continuum parity/periodograms, long-cycle/noise determinants, and a
folded-Gaussian strong--weak midpoint bridge, respectively, but do not prove
this arbitrary aligned finite-Ulam block theorem plus crossing-cell identity.
Route A is `GO`; Route B is `STOP_SCOPED` at the missing common strong-space
projector/resolvent bridge.  No universal `sqrt(sigma)` law, arithmetic
operator, prime-power trace, zeta-zero model, or RH implication is claimed.

### 3.7 RH-368 parity-factor Möbius capacity limit

RH-368 freezes the source-backed PCF three-cell partition from
`dyna_zeta_map=7fd3a3fdd5a6a25827a0965345459baf4a47b816`:

```text
A = [[0,0,1],[0,0,1],[1,1,0]],
zeta_{f|J}(z) = zeta_{A_{\{2\}}}(z) = (1+z)/(1-2z^2).
```

The binary factor `A_{\{2\}}` consists of sign words whose positive
positions lie in one parity class.  It is a distinct reduced language, not a
subset of the RH-366 distance-two language: `+-+` and `++-` separate the two
constraints in opposite directions.  For
`M_N=sum_{n<=N} mu(n)`, `P_r(N)=#{mu(n)=+1}` and
`N_r(N)=#{mu(n)=-1}` in parity class `r`, the exact finite capacity is

```text
K_N^(2) = max_r max(|-M_N+2P_r(N)|,|-M_N-2N_r(N)|).
```

Davenport's fixed-frequency estimate at `1/2` gives signed parity cancellation;
the squarefree sieve gives odd/even densities `4/pi^2` and `2/pi^2`.  Hence

```text
K_N^(2)/N -> 4/pi^2.
```

The executable endpoint is `N=2^20`, `K_N^(2)=425095`, ratio
`0.40540218353271484`; this row is diagnostic only.  The package has 11/11
source locks, 5/5 local tests, 21 publication files, 11 external inputs, a
zero-failure archive, and a three-page PDF with 20 embedded Unicode-mapped
font rows; Ghostscript, text extraction, and all three rendered pages pass.

The overlap ledger is positive and narrow: dyna_zeta_map supplies the PCF
factor, RH-366 supplies the distinct four-state distance-two capacity bracket
but no limit, and RH-367 supplies a finite-Ulam two-band theorem but no
three-cell parity-factor capacity law.  Route A is `GO`; Route B is
`STOP_SCOPED` because the optimizer reads the complete Möbius prefix and the
capacity is not a canonical trace.  Gates A--E remain false/open.

### 3.8 RH-369 branch-symmetric Markov/Gibbs family

RH-369 derives a nonadaptive one-parameter family on the frozen RH-366 graph.
With `q=1-t`, `0<t<1`,

```text
P_t = [[t,0,q,0],[1,0,0,0],[0,t,0,q],[0,1,0,0]],
pi_t = (1,q,q,q^2)/(1+q)^2.
```

For the inherited raw sign `e=(-1,-1,+1,+1)`,

```text
E_t e = -t/(2-t),
Var_t e = 4(1-t)/(2-t)^2.
```

The centered variance-one observable satisfies
`P_t^2 F_t=-(1-t)F_t` and has zero one-step covariance.  Therefore its odd
covariances vanish and its lag-`2k` covariance is `(-(1-t))^k`.  The exact
characteristic polynomial is
`(lambda-1)(lambda+1-t)(lambda^2+1-t)`, so every fixed interior parameter is
primitive and exponentially mixing.  For each fixed `t`, one `nu_t`-full set
works simultaneously for every continuous observable in the almost-sure
Möbius cancellation theorem; the set and constants depend on `t`.

For `S_(N,t)=sum_(n<=N) mu(n)F_t(sigma^n omega)`, the exact finite variance is

```text
V_(N,t) = sum mu(n)^2
          + 2 sum_(k>=1) (-(1-t))^k
              sum_(n<=N-2k) mu(n)mu(n+2k),
0 <= V_(N,t) <= ((2-t)/t)N.
```

The limit `V_(N,t)/N -> 6/pi^2` remains conditional on ordinary fixed-shift
two-point Chowla.  The Parry law of RH-366 is exactly `t=phi^(-1)`; RH-369
adds the remaining non-Parry interior family.  It does not assert a common
full-measure set, uniform endpoint control, a geometrically selected
parameter, or a canonical arithmetic trace.  Route A is `GO`; Route B is
`STOP_SCOPED`; Gates A--E remain false/open.

### 3.9 RH-370 fold-compatible Ulam quotients and deterministic spike barrier

RH-370 locks the cyclic-Ulam source at
`e7d21f646498d77e1c3213d1e4f35dc8466038ff` and audits the PCF map
`f(x)=1-u x^2` on `J=[-(u-1),1]` through the fold `q(x)=|x|` and
`T(y)=|1-u y^2|`.  It proves three separately typed facts.

First, for every genuinely mirror-compatible partition, the exact full
cell-overlap matrix has observable and mass intertwiners with the folded
matrix.  If `m` paired cells are present,

```text
chi_full(z) = z^m chi_fold(z),
P_full^T ker(A) = 0.
```

Thus all nonzero finite eigenvalues and their Jordan data are inherited; the
additional zero structure is deliberately unclassified.  The theorem does
not cover merely band-aligned, crossing, or phase-shifted grids.

Second, conditional expectations give the genuine weak statement
`E_h P_T E_h g -> P_T g` in `L^1` for every fixed `g`, and strong resolvent
convergence uniformly on compact subsets of `|z|>1`.  Since `-1` lies on the
unit circle, this is not a Riesz-projector theorem and cannot promote the
finite `-1` mode to a continuum resonance.

Third, on the standard `BV` component, the deterministic terminal profile is

```text
P_T 1 = (2 sqrt(u))^(-1) (1-y)^(-1/2),   u-1 < y < 1,
```

and adjacent terminal cell averages differ by
`(2-sqrt(2))/sqrt(u h)=0.4714757998... h^(-1/2)`.  The deterministic
projection therefore has no uniform bound in that natural strong norm.  This
is a scoped negative only; a new fractional/tower-adapted space is not ruled
out.  RH-52/RH-55 positive-noise hypotheses require `h=o(sigma^2)` and cannot
be specialized to `sigma=0`.

Route A is `GO` for the exact quotient, exterior weak bridge, and BV
obstruction.  Route B is `STOP_SCOPED` before Gate A.  Gates A--E remain
false/open; no canonical determinant, Hilbert--Polya operator, prime trace,
zero identification, or RH implication is claimed.

### 3.10 RH-371 eight-run reduction and cyclic pair-ledger obstruction

RH-371 locks the distance-two capacity source at
`henon_mobius_correlations=34490443f50cfe9af9ff93888e51e7e7e534a5a7` and
inherits RH-366 and RH-370 as explicit local inputs.  For
`sigma in {+1,-1}`, it defines the odd step-two run counts
`C_(sigma,k)(N)` and the isolated even count `E_sigma(N)`.  Every nine odd
positions at step two contain a multiple of nine, while every nonzero even
Möbius position is isolated by a multiple of four.  Therefore, for every
prefix and without fitting,

```text
W_sigma(N) = E_sigma(N) + sum_(k=1)^8 (-1)^(k+1) C_(sigma,k)(N),
K_N = max(|-M_N+2W_+(N)|,|-M_N-2W_-(N)|).
```

With `M_N=o(N)`, this gives the exact convergence criterion in terms of the
maximum of the two alternating eight-run combinations.  It does not prove
that either combination has a density or that `lim K_N/N` exists; the
individual run-density limits are sufficient but not necessary.

The synthetic period-18 words

```text
u = +++++-++0--+-----0
v = +++++---0--+---++0
```

have the same complete ordered three-symbol pair ledger only at cyclic
periodic lags, but their repeated capacities are `10q` and `12q`.  Their
open-prefix lag-2 ledgers differ, and they are not Möbius words.  This is a
scoped negative for pair data as a sufficient statistic in the general
periodic ternary class, not a nonexistence result for the Möbius capacity
limit.

The primary route decision is `Route A=GO`, `Route B=STOP_SCOPED`.  The first
Route-B blocker is the missing Möbius alternating eight-run convergence
theorem; the optimizer remains an adaptive arithmetic functional and no
physical Gate is affected.

### 3.11 RH-372 bounded constraint-graph transducer certificates

RH-372 freezes the finite graph and arithmetic inputs used by RH-366, RH-368,
and RH-371, together with `dyna_zeta_map` and the four-volume verification.
Its Route-A result is deliberately bounded.  For every finite directed graph
with vertex observable `ell`, the open-prefix capacity has the exact max-plus
recurrence

```text
D_(n+1)^+(v) =  mu(n+1) ell(v) + max_(u,v) in E D_n^+(u),
D_(n+1)^-(v) = -mu(n+1) ell(v) + max_(u,v) in E D_n^-(u),
```

and therefore is computable, with a witness, in `O(N|E|)` integer steps.  The
universal squarefree bound remains
`limsup K_N/N <= (6/pi^2)||ell||_infinity`.

For a fixed clock `q` and finite memory set `S`, the paper defines a universal
safety table check over every state, phase, and consecutive input pair.  If
the observed label is the one-site factor `g_r(mu(n))`, then Davenport
cancellation in fixed arithmetic progressions and the squarefree density give

```text
L(T) = 1/2 sum_(r mod q) delta_(q,r) [g_r(1)-g_r(-1)],
delta_(q,r) = sum_{(q,d^2)|r} mu(d)/lcm(q,d^2).
```

Every such explicit path is a lower bound for `liminf K_N/N`, and the class of
tables at fixed `(q,|S|)` is finite and exhaustible.  This is not a
classification of all mixing SFTs.  If the observable reads memory, the
formula is intentionally inactive because a higher-order Möbius correlation
theorem is absent.

Three frozen instances pass the literal universal checks: the RH-366
four-state graph with a two-state completion at `q=4`, the distinct RH-368
three-cell graph at `q=2`, and a new two-state `q=3` safe switch on RH-366.
Their exact one-site constants are respectively `4/pi^2`, `4/pi^2`, and
`9/(4*pi^2)`.  The finite audit checks `384` prefix witnesses, an endpoint
`N=2^16`, and all `729` q=2 one-state output tables (`16` safe one-site
tables; maximum coefficient `4`).

The route verdict is `Route A=GO` narrowly and `Route B=STOP_SCOPED`.  The
transducer is an offline arithmetic selector and supplies no canonical
operator, determinant, prime-power trace, zero identification, or RH
implication.  The RH-366 distance-two capacity limit and all Gates A--E remain
false/open.

### 3.12 RH-373 composite-clock Möbius capacity floor

RH-373 adds a strict lower-bound edge for the still-open RH-366 distance-two
capacity.  For any finite clock `q` and phase set `I` with
`I cap (I+2)=emptyset`, the one-site selector

```text
epsilon_n = +1 iff (n mod q) in I and mu(n)=+1;
            -1 otherwise
```

is admissible for every ternary input word.  Fixed arithmetic-progression
Möbius cancellation and squarefree densities therefore give the exact
correlation `sum_(r in I) delta_(q,r)` and a lower bound for `liminf K_N/N`.

The explicit composite clock `q=180=2^2*3^2*5` uses `80` phases.  Its density
coefficients are

```text
pi^2 delta_(180,r) = 0       if 4|r or 9|r,
                     5/96    if 4∤r, 9∤r, 5∤r,
                     1/24    if 4∤r, 9∤r, 5|r.
```

The selected set contains `68` phases of coefficient `5/96` and `12` of
coefficient `1/24`, with no cyclic distance-two conflict.  Hence

```text
liminf K_N/N >= 97/(24*pi^2) = 4/pi^2 + 1/(24*pi^2).
```

The paper also gives a literal two-state universal-safety completion on the
RH-366 four-state graph.  This is one fixed externally prescribed arithmetic
witness, not an all-clock/transducer optimum and not a capacity-limit theorem.
Route A is
`GO` narrowly; Route B is `STOP_SCOPED`.  The ordinary capacity limit,
memory-dependent Möbius correlations, all intrinsic operator/trace bridges,
and Gates A--E remain open/false.

### 3.13 RH-374 square-clock Euler-product capacity floor

RH-374 upgrades the single RH-373 certificate to an exact infinite family.
Let `3=p_1<p_2<...` be the odd primes and set

```text
P_y = product_(i<=y) p_i^2,
q_y = 4P_y,
A_y = product_(i<=y) (p_i^2-1),
E_m^(y) = product_(i<=y) (1-m/p_i^2),  1<=m<=9.
```

At the fixed clock `q_y`, every positive squarefree progression has density
`2/(A_y*pi^2)`.  On the odd phases, the squarefree word has period `P_y` and
its positive runs have length at most eight because the modulus-nine zero is
always present.  If `R_j^(y)` counts cyclic positive runs of length `j` in one
word period, then

```text
R_j^(y) = P_y(E_j^(y)-2E_(j+1)^(y)+E_(j+2)^(y)),  1<=j<=7,
R_8^(y) = P_y E_8^(y),
O_y = R_1^(y)+R_3^(y)+R_5^(y)+R_7^(y).
```

The endpoint `R_8` formula is separate; no `E_10` is defined or used.  The
exact weighted phase-MWIS, equivalently the optimum over universally safe
one-site phase/current-input factors at this fixed clock, selects `2A_y+O_y`
phases and has value

```text
B_y = (4+2O_y/A_y)/pi^2.
```

Adjoining the next odd prime `p>=5` gives

```text
A' = (p^2-1)A,
O' = (p^2-1)O + L_even,
```

where `L_even` is the number of one-sites lying in even-length old runs.  A
CRT construction preserves an exact length-eight run at every finite stage,
so `L_even>0` and `B_y` is strictly increasing.  With

```text
e_m = product_(p odd) (1-m/p^2),  e_9=0,
C = sum_(j in {1,3,5,7})(e_j-2e_(j+1)+e_(j+2))/e_1,
B_infinity = (4+2C)/pi^2,
```

the fixed-clock lower bounds imply
`liminf_(N->infinity) K_N/N >= B_infinity`.  The quantifier is: fix each `y`
before taking `N->infinity`, then take the supremum of the resulting scalar
bounds.  There is no growing clock `q(N)`, uniform-in-clock Davenport theorem,
or infinite selector.

The first exact rows have `pi^2 B_1=4`, `pi^2 B_2=49/12` at `q_2=900`, and
`pi^2 B_3=593/144` at `q_3=44100`; already `q=900` improves RH-373 by
`1/(24*pi^2)`.  Route A is `GO`; Route B is `STOP_SCOPED`.  The optimum claim
does not include arbitrary memory-dependent transducers or all finite clocks,
and the result does not prove convergence of the adaptive capacity.  It
constructs no intrinsic operator, determinant, prime-power trace, zero model,
or Hilbert--Polya object, and Gates A--E remain false/open.

### 3.14 RH-375 all-clock one-site Möbius capacity supremum

RH-375 closes the finite-clock class left open by RH-374.  For every fixed
finite `q`, let `G_q` be the universally safe `q`-periodic one-site
phase/current-input factors; the declared period need not be minimal.  Fixed
AP cancellation gives the limit `L_q(g)` for every `g in G_q`, and

```text
F(q) = max_(g in G_q) |L_q(g)|
     = max_(I cap (I+2)=emptyset) sum_(r in I) delta_(q,r).
```

The active phases of a safe factor are exactly a distance-two independent
set.  The coefficient at each phase lies in `{-1,0,1}`, while either uniform
orientation realizes every independent-set weight.  Self-loops give
`F(1)=F(2)=0`; odd clocks, exponent-one density factors, high prime powers,
`g_r(0)`, and zero-density phases are included explicitly.

If `q|Q`, a possibly nonminimal `q`-periodic factor lifts literally to clock
`Q`, so

```text
F(q) <= F(Q),
delta_(q,r) = sum_(s mod Q, s=r mod q) delta_(Q,s).
```

For the RH-374 clocks `q_y`, RH-375 proves the special saturation law

```text
q_y|Q and supp_primes(Q)=supp_primes(q_y)
    => F(Q)=F(q_y)=B_y.
```

This is not a general cyclic-cover MWIS theorem.  Writing `Q=Rq_y`, every
positive weight is divided by `R`; phases divisible by `4` split the even
cycle and phases divisible by `9` split the odd runs, so the support-MWIS
cardinality is multiplied exactly by `R`.

For arbitrary finite `q`, choose `y` covering every odd prime divisor of `q`
and set `Q=lcm(q,q_y)`.  Then `Q` has the same prime support as `q_y`, whence

```text
F(q) <= F(Q)=B_y<B_infinity.
```

Since `F(q_y)=B_y` and `B_y` increases to `B_infinity`, the exact endpoint is

```text
sup_(q finite) F(q)=B_infinity,
F(q)<B_infinity for every finite q.
```

Thus the supremum is not attained by a finite clock.  The proof uses no
bounded-scan extrapolation, growing clock `q(N)`, infinite selector, or
uniform-in-clock Davenport theorem.  Route A is `GO`; Route B is
`STOP_SCOPED`.  Memory-dependent factors, the RH-371 adaptive run envelope,
ordinary capacity convergence, intrinsic operators/traces/zeros, and Gates
A--E remain open/false.

### 3.15 RH-376 shift-two Chowla/run-density boundary

RH-376 isolates the first correlation-hard term in the RH-371 run hierarchy.
For `sigma in {-1,+1}`, `C_(sigma,2)(N)` is the number of overlapping odd
starts `1<=n<=N-2` with `mu(n)=mu(n+2)=sigma`; it is not a maximal
exact-length-two run count.  With every sum taken over this common endpoint,
write

```text
Q_2 = sum mu(n)^2 mu(n+2)^2,
U_2 = sum mu(n)   mu(n+2)^2,
V_2 = sum mu(n)^2 mu(n+2),
D_2 = sum mu(n)   mu(n+2).
```

Every even start makes one of `n,n+2` divisible by four, so all four
monomials and both signed indicators vanish.  The pointwise Boolean
expansion therefore gives, for every prefix,

```text
4C_(sigma,2) = Q_2 + sigma U_2 + sigma V_2 + D_2.
```

The squarefree-pair sieve has two distinct forbidden classes modulo every
`p^2`, including `p=2`, and hence

```text
Q_2/N -> kappa_2 = product_p (1-2/p^2).
```

Expanding one squarefree mask, fixing a divisor cutoff `R`, and applying
Davenport cancellation only in the finitely many fixed progressions modulo
`d^2` proves `U_2,V_2=o(N)`.  The tail is
`O(N/R+sqrt(N))`; the order is first `N->infinity` at fixed `R`, then
`R->infinity`.  No growing-modulus theorem is used.  Consequently

```text
4C_(sigma,2)(N)/N = kappa_2 + D_2(N)/N + o(1).
```

The frozen Teravainen--Walker logarithmic affine theorem applies to the fixed
forms `m+1,m+3`, determinant two, and zero twist.  If `D_2(N)/N` has a
Cesaro limit, one-way Abel summation gives the same logarithmic limit; the
source theorem forces it to be zero.  Thus, for either one fixed sign,

```text
C_(sigma,2)(N)/N converges
    iff D_2(N)=o(N),
```

and then both signed interval densities equal `kappa_2/4`.  This is an exact
hardness equivalence, not a proof of shift-two Chowla and not a
nonconvergence theorem.  It does not settle any `k>=3` run density, the
alternating eight-run envelope, or `K_N/N`.  Route A is `GO`; Route B is
`STOP_SCOPED`; Gates A--E remain false/open.

### 3.16 RH-377 mixed-exponent run hierarchy and two-envelope boundary

RH-377 expands every RH-371 signed window on its native odd-start endpoint.
For `I_k={0,...,k-1}` and `S subset I_k`, let

```text
T_(k,S) = sum_n product_(j in S) mu(n+2j)
                  product_(j not in S) mu(n+2j)^2,
H_(k,r) = sum_(|S|=r) T_(k,S),
```

where every level-`k` sum uses exactly
`1<=n<=N-2(k-1), n odd`.  Let `A_k` collect the even layers `r>=2` and
`B_k` the odd layers `r>=3`.  The pointwise ternary Boolean expansion gives
at every prefix

```text
2^k C_(sigma,k) = H_(k,0) + A_k + sigma(H_(k,1)+B_k).
```

For `1<=k<=8`, put

```text
e_k = product_(p odd)(1-k/p^2),
Delta_k=e_k/2.
```

The outside factor `1/2` is the odd-start density; it is not a `p=2` local
factor inside `e_k`.  A fixed finite square sieve proves
`H_(k,0)/N->Delta_k`.  For `H_(k,1)`, first freeze a bounded periodic
prime-square mask, then apply Davenport only in finitely many fixed residue
classes, and finally remove the cutoff by a large-prime-square union bound.
Thus `H_(k,1)=o(N)` without a growing modulus.

It follows that all sixteen limits `C_(sigma,k)/N`, two signs and
`1<=k<=8`, exist simultaneously if and only if the thirteen limits

```text
A_k/N, 2<=k<=8,
B_k/N, 3<=k<=8
```

exist.  The `466 -> 13` map has rank `13` and kernel dimension `453` only
as a formal block-sum map on mixed-moment coordinates.  It is not an
arithmetic minimal-dimension theorem, and one sign at one `k>=3` controls
only `A_k+sigma B_k`.

With `s_k=(-1)^(k+1)`, define

```text
U_N=sum_(k=2)^8 s_k A_k/2^k,
V_N=sum_(k=3)^8 s_k B_k/2^k,
r_0=1/pi^2+sum_(k=1)^8 s_k Delta_k/2^k.
```

The exact `P,Q,U,V` ledger and RH-371 path identity give

```text
K_N/N = 2r_0 + 2(U_N+abs(V_N))/N + o(1).
```

Hence `K_N/N` converges exactly when `(U_N+abs(V_N))/N` converges.  Neither
convergence is proved.  Full mixed-exponent cancellation would be sufficient
for the conditional constant

```text
2/pi^2 + sum_(k=1)^8 (-1)^(k+1)e_k/2^k,
```

but is not necessary and is not established.  A uniform-pair stationary
second-order ternary chain has identical raw, square-only, and exactly
one-sign layers while its first directional two-sign moment varies as
`8 epsilon/81`.  This is a synthetic algebraic witness, not a Möbius model;
it does not match Möbius squarefree density and proves no arithmetic
nonconvergence.  Route A is `GO`; Route B is `STOP_SCOPED`; Gates A--E remain
false/open.

### 3.17 RH-378 safe windows and online capacity transducers

RH-378 first fixes a finite clock `q`, a causal contiguous window length
`ell`, and ternary input `a_n in {-1,0,1}`.  A `q`-periodic window table is
universally distance-two safe if and only if the two shifted outputs are not
both positive on every compatible block of length `ell+2`.  The exact finite
test therefore has

```text
q 3^(ell+2)
```

rows.  For a score function that vanishes when the current input is zero,
the displayed monomials with previous exponents in `{0,1,2}` and current
exponent in `{1,2}` form a basis, with a unique expansion and formal
dimension `2q3^(ell-1)`.  This is a function-space statement, not an
arithmetic minimality theorem and not a theorem that its mixed Möbius
coefficients have limits.

For the `q=1` lag-two table

```text
epsilon_n=f(mu(n-2),mu(n)),   mu(j)=0 for j<=0,
```

universal safety is equivalent to the plus-edge relation having no
composable pair.  Exactly `13` of the `512` Boolean tables are safe.  Their
six score-coefficient columns have rational rank `5` and the unique relation

```text
c_22=-c_02-c_11.
```

With the common RH-376 endpoint `m<=N-2`, the exact finite ledger is

```text
L_f=c_01 M_N+c_02 Q_1+c_11 D_2+c_12 U_2+c_21 V_2+c_22 Q_2.
```

Consequently

```text
L_f/N=c_02(6/pi^2-kappa_2)
      +c_11(D_2/N-kappa_2)+o(1).
```

Exactly seven safe tables have unconditionally certified limits; their
class-optimal absolute value is `6/pi^2-kappa_2`.  For each of the other six,
RH-376 Cesaro rigidity gives

```text
L_f(N)/N converges  iff  D_2(N)=o(N).
```

Under that unproved condition their class-optimal absolute value is
`6/pi^2-kappa_2/2`, which conditionally exceeds `B_infinity`.  Both optima
are restricted to the declared thirteen-table class.  No shift-two Chowla
theorem or larger memory optimum is proved.

For each sign `sigma`, RH-378 also gives a fixed four-state Mealy machine
with state `(epsilon_(n-1),epsilon_(n-2))` and output

```text
epsilon_n=+1 iff a_n=sigma and epsilon_(n-2)=-1.
```

On every finite ternary word the two machines have scores exactly
`S_N^max` and `S_N^min`; hence `K_N` is the endpoint maximum of their two
absolute scores.  Four states are necessary only for reproducing either
one frozen orientation stream.  This is not one online machine computing
`K_N`.  In fact no single deterministic causal universally safe policy,
even with unbounded memory, can attain `abs(score)=K_N` on every input branch
at every prefix; the exact policy-tree counts through horizon four are
`8,256,65536,0`.

Finally, an explicit `q=1` stateless contiguous length-`15` table is
universally safe on every ternary input.  It reproduces either four-state
orientation stream when every step-two target-sign run has length at most
eight.  The Möbius word satisfies that hypothesis because nine same-parity
positions span all residues modulo nine.  Length `15` is minimal only in the
declared causal contiguous stateless exact-stream class.  A synthetic run of
nine same-parity target signs over `17` integer sites is the first
unrestricted counterexample; it is not a Möbius counterexample.

The finite-state identities do not prove `K_N/N` convergent.  Its arithmetic
blocker remains the RH-377 two-envelope problem.  Route A is `GO`; Route B is
`STOP_SCOPED`; Gates A--E remain false/open.

### 3.18 RH-379 phasewise Chowla-free memory supremum

RH-379 fixes a finite clock `q` before `N->infinity` and studies

```text
epsilon_n=f_(n mod q)(mu(n-2),mu(n)),
```

with universal distance-two safety on every ternary input and
`c_11(r)=0` separately at every phase in the six-term interpolation of
`z f_r(x,z)`.  If `delta_(q,r)` is the squarefree progression density and
`theta_(q,r)` is the density for which both `n-2` and `n` are squarefree,
the fixed-AP Davenport/cutoff argument gives the unconditional limit

```text
L_q(f)=sum_r [c_02(r) delta_(q,r)+c_22(r) theta_(q,r)].
```

This is a phasewise hypothesis, not a theorem that unknown phase-weighted
shift-two correlations cancel.

The exact local census exhausts all `512` Boolean tables and finds `192`
with `c_11=0`.  Every one has a payoff-dominating canonical subset among

```text
0,
J={(0,+1)},
K={(-1,+1),(+1,+1)},
I={(-1,+1),(0,+1),(+1,+1)},
```

with respective weights `0`, `delta-theta`, `theta`, and `delta`.
Subset replacement must be performed at every phase before `K` is replaced
by `I`; only inside the already canonical alphabet do `K` and `I` have the
same incoming and outgoing compatibility.  The final alphabet is `{0,J,I}`:
`I` requires predecessor `0` along addition by two, whereas `J` may follow
any canonical state.  Closing the cyclic seam on the `gcd(q,2)` phase orbits
gives the exact fixed-clock max-plus optimum `G(q)`.  Input reflection makes
the positive optimum equal to the absolute optimum.

Already

```text
G(1)=G(2)=6/pi^2-kappa_2 > F(1)=F(2)=0.
```

At the first square clock `q_1=36`, RH-379 proves the exact strict gain

```text
G(36)=9/(2*pi^2)-kappa_2/7,
G(36)-F(36)=1/(2*pi^2)-kappa_2/7>0.
```

More generally, with `q_y=4 product_(i<=y)p_i^2`,
`A_y=product_(i<=y)(p_i^2-1)`, `D_y=product_(i<=y)(p_i^2-2)`, and
`mathcal_E_y` the number of even-length positive runs in one RH-374 odd-word
period,

```text
G(q_y)=B_y+Delta_y,
Delta_y=mathcal_E_y[4/(A_y*pi^2)-kappa_2/D_y] > 0,
Delta_y -> 0.
```

The run recurrence uses the exact regime `a_y/2<b_y<a_y`.  It proves neither
monotonicity of `Delta_y` nor any arbitrary-cover saturation theorem.

For an arbitrary fixed `q`, lift to `Q_y=lcm(q,q_y)` after `y` contains all
odd prime divisors of `q`.  Retain every `I` phase and only those `J` phases
whose predecessor is forced nonsquarefree by a supported prime square.  The
retained phases form a one-site independent set of weight at most
`F(Q_y)=B_y`; every discarded `J` is charged to `p^2 | n-2` for some
`p>p_y`, of total density at most `sum_(p>p_y)p^(-2)`.  Taking `N->infinity`
at each fixed clock before `y->infinity`, and using the embedded RH-375
one-site subclass for the reverse inequality, proves

```text
sup_(q finite) G(q)=B_infinity.
```

RH-379 deliberately leaves finite-clock attainment/nonattainment open; that
is the independently locked RH-380 refinement.  Genuinely active
`c_11(r)!=0` first requires phase-weighted shift-two Cesaro cancellation.
No growing clock, adaptive-capacity limit, intrinsic dynamical operator,
trace, zero identification, Hilbert--Polya construction, RH implication, or
Gate A--E result follows.  Route A is `GO`; Route B is `STOP_SCOPED`.

### 3.19 RH-380 square-clock monotonicity and finite-clock nonattainment

RH-380 stays inside the exact RH-379 class: the clock `q` is finite and fixed
before `N->infinity`, every lag-two phase table is universally distance-two
safe, and `c_11(r)=0` holds phasewise.  For the RH-374 square clocks write

```text
q_y=4 product_(i<=y)p_i^2,
A_y=product_(i<=y)(p_i^2-1),
D_y=product_(i<=y)(p_i^2-2),
mathcal_E_y=sum_(ell even)R_ell^(y),
L_y=sum_(ell even)ell R_ell^(y),
M_y=sum_(ell odd)(ell-1)R_ell^(y).
```

If `s=p_(y+1)^2`, an all-order deletion ledger over each old run proves

```text
mathcal_E_(y+1)=(s-2)mathcal_E_y+M_y.
```

Combining this with the locked RH-374 odd-run recurrence and the exact
RH-379 square-clock formula gives

```text
G(q_(y+1))-G(q_y)
 =2(L_y-2mathcal_E_y)/(pi^2 A_y(s-1))
  +M_y[4/pi^2-H_(y+1)]/[A_y(s-1)],
H_y=kappa_2 A_y/D_y.
```

The persistent length-eight run supplies

```text
L_y-2mathcal_E_y=2R_4^(y)+4R_6^(y)+6R_8^(y)>=6,
```

so `G(q_y)` is strictly increasing and each increment is at least
`12/[pi^2 A_y(s-1)]`.  This is monotonicity of `G(q_y)`, not of the RH-379
correction `Delta_y=G(q_y)-B_y`.

RH-380 also proves a separator-dependent saturation theorem.  If
`q_y|Q=R q_y` and `Q` has exactly the same prime support as `q_y`, then the
fine `delta` and `theta` weights scale by `1/R`; forced mod-4 and mod-9
zero-weight phases split the addition-by-two cycles into repeated finite
paths.  Consequently

```text
G(Q)=G(q_y).
```

The hypothesis is essential: `Q=180=5*36` adds the prime five and is a
certified negative control to general-multiple saturation, with
`G(180)>G(36)`.  For any fixed finite `q`, choose `y` containing all odd
prime divisors of `q` and put `Q=lcm(q,q_y)`.  Clock lifting and the special
saturation theorem yield

```text
G(q)<=G(Q)=G(q_y)<B_infinity,
B_infinity-G(q)>=12/[pi^2 A_y(p_(y+1)^2-1)]>0.
```

Thus no finite clock attains the RH-379 supremum in the declared class.
RH-380 proves neither a general cyclic-cover theorem nor anything for active
phasewise `c_11`, growing `q(N)`, or the RH-377 adaptive envelope.  The
prime-square-tail rate is a successor trigger, not an RH-380 result.  No
intrinsic operator, trace, zero identification, Hilbert--Polya construction,
RH implication, or Gate A--E result follows.  Route A is `GO`; Route B is
`STOP_SCOPED`.

### 3.20 RH-381 prime-square-tail rate and quadratic memory remainder

RH-381 retains the exact RH-379/RH-380 class and the fixed-clock-first order
of limits.  Put

```text
a_(j+1)=1/(p_(j+1)^2-1),
T_y=sum_(j>=y)a_(j+1)=sum_(p>p_y)1/(p^2-1),
S_y=sum_(j>=y)a_(j+1)^2,
U_m^(j)=E_m^(j)/E_1^(j),
u_m=e_m/e_1.
```

The RH-374 run ledger gives the exact normalized numerator

```text
X_j=(L_j-2mathcal_E_j)/A_j
   =2U_4^(j)-4U_5^(j)+6U_6^(j)-8U_7^(j)+10U_8^(j),
X_infinity=2u_4-4u_5+6u_6-8u_7+10u_8
          >=6e_8/e_1>0.
```

For each `4<=m<=8`, factorwise comparison of the finite Euler ratio with
its tail product yields

```text
0<=U_m^(j)-u_m<=(m-1)T_j.
```

The coefficient ledger is `6+16+30+48+70=170`, hence

```text
abs(X_j-X_infinity)<=170T_j.
```

The exact RH-379 product and the RH-380 run interpretation give

```text
0<=4/pi^2-H_(j+1)<=(4/pi^2)T_(j+1),
0<=M_j/A_j<=1.
```

The two tail identities, with no prime-distribution input, are

```text
sum_(j>=y)a_(j+1)T_j=(T_y^2+S_y)/2<=T_y^2,
sum_(j>=y)a_(j+1)T_(j+1)=(T_y^2-S_y)/2<=T_y^2/2.
```

Finite telescoping of the exact RH-380 increment followed by the already
proved `G(q_j)->B_infinity` limit therefore proves

```text
abs(B_infinity-G(q_y)-(2X_infinity/pi^2)T_y)
 <=342T_y^2/pi^2,
(B_infinity-G(q_y))/T_y -> 2X_infinity/pi^2>0.
```

The remainder ledger is exactly `2*170+2=342`.  Every `T_y` is positive by
the infinitude of odd primes, and `T_y->0` follows from the elementary
integer-square tail; no PNT is used.  RH-381 does not identify an exact
second-order coefficient, replace `T_y` by a `p_y` scale, introduce a
growing clock, settle the RH-377 adaptive envelope, activate nonzero
phasewise `c_11`, or construct an intrinsic operator, trace, zero model, or
Gate A--E result.  Route A is `GO`; Route B is `STOP_SCOPED`.

### 3.21 RH-382 two-scale prime-square-tail expansion

RH-382 retains the same fixed-finite-clock, universally safe,
phasewise-`c_11=0` class.  With

```text
a_(j+1)=1/(p_(j+1)^2-1),
T_y=sum_(j>=y)a_(j+1),
S_y=sum_(j>=y)a_(j+1)^2,
u_m=e_m/e_1,
X_infinity=2u_4-4u_5+6u_6-8u_7+10u_8,
Y_infinity=6u_4-16u_5+30u_6-48u_7+70u_8,
m_infinity=2u_3-4u_4+6u_5-8u_6+10u_7-12u_8,
```

the exact RH-381 increment sum and all-order product inequalities prove, for
every `y>=1`,

```text
B_infinity-G(q_y)
 =(2X_infinity/pi^2)T_y
  +((Y_infinity+2m_infinity)/pi^2)T_y^2
  +((Y_infinity-2m_infinity)/pi^2)S_y+R_y,
abs(R_y)<=3301T_y^3/(6pi^2)<551T_y^3/pi^2.
```

The pointwise finite-ratio ledgers are

```text
abs(X_j-X_infinity-Y_infinity*T_j)<=(931/4)T_j^2,
abs(M_j/A_j-m_infinity)<=63T_j,
abs((4/pi^2-H_(j+1))-(4/pi^2)T_(j+1))
 <=(2/pi^2)T_(j+1)^2.
```

The numerator channel costs `931/2`; the memory channel costs `254/3`.
Thus `931/2+254/3=3301/6=550+1/6<551`.  The opposite signs of `S_y` are
forced by the exact identities

```text
sum a_(j+1)T_j=(T_y^2+S_y)/2,
sum a_(j+1)T_(j+1)=(T_y^2-S_y)/2.
```

The terminal run remains `R_8=P_yE_8`; `E_9=0` occurs only through the
licensed length-seven second difference, and no `E_10` is introduced.  An
exact one-tail `p=71` artifact keeps the numerator `+Y*S` term fixed and
flips only the memory `-2m*S` sign: the correct residual/bound ratio is
`0.042746686479386`, whereas the wrong sign gives
`7.335622869337969`.  This is a finite exact mutation test, not evidence for
the all-`y` theorem.

RH-382 does not suppress `S_y`, replace `T_y` by a `p_y` asymptotic, use
PNT, introduce `q(N)`, activate nonzero phasewise `c_11`, settle the RH-377
adaptive envelope, or construct an intrinsic operator, trace, zero model,
or Gate A--E result.  Route A is `GO`; Route B is `STOP_SCOPED`.

### 3.22 RH-383 exact Euler-tail partition normal form

RH-383 retains the same fixed-finite-clock, universally safe,
phasewise-`c_11=0` class.  For

```text
a_(j+1)=1/(p_(j+1)^2-1),
P_r(y)=sum_(j>=y)a_(j+1)^r,
Phi_c(y)=sum_(r>=1)c^r P_r(y)/r,
C(V)=1-2V_2+2V_3-2V_4+2V_5-2V_6+2V_7-2V_8,
W(V)=V_2-2V_3+2V_4-2V_5+2V_6-2V_7+2V_8,
```

the square-clock gap has the exact endpoint form

```text
U_m^(y)=u_m exp(Phi_(m-1)(y)),
H_y=(4/pi^2)exp(-Phi_1(y)),
pi^2(B_infinity-G(q_y))
 =2(C(u)-C(U^(y)))-4W(U^(y))(1-exp(-Phi_1(y))).
```

For a nonempty partition `lambda=1^k_1...d^k_d`, put

```text
degree(lambda)=d,
P_lambda(y)=product_r P_r(y)^k_r,
z_lambda=product_r r^k_r k_r!,
alpha=(-2,2,-2,2,-2,2,-2),
beta=(1,-2,2,-2,2,-2,2),  indexed by m=2,...,8.
```

Absolute convergence and finite partition expansion give

```text
pi^2(B_infinity-G(q_y))
 =sum_(d>=1) sum_(lambda partition d) gamma_lambda P_lambda(y),
gamma_lambda
 =-(2/z_lambda)sum_(m=2)^8 alpha_m u_m (m-1)^d
  -(4/z_lambda)sum_(m=2)^8 beta_m u_m
    [(m-1)^d-product_r((m-1)^r-1)^k_r].
```

The `m=2` summand vanishes for every nonempty partition.  In the independent
increment compiler the tail-product sign is `(-1)^length(lambda)` and the
loss sign is `(-1)^(length(lambda)+1)`, not degree parity.  Its memory term
uses the strict successor tail `j+1`.  Endpoint coefficients `alpha/beta`
remain distinct from increment coefficients

```text
XI=(2,-4,6,-8,10),       indexed by m=4,...,8,
ETA=(2,-4,6,-8,10,-12), indexed by m=3,...,8,
xi_m=-alpha_m(m-1)-2beta_m,
eta_m=-beta_m(m-2).
```

The first two homogeneous layers reproduce RH-381 and RH-382 exactly.  The
new cubic coefficients are

```text
gamma_(1,1,1)
 =4u_3-(22/3)u_4+(20/3)u_5+2u_6-(68/3)u_7+(178/3)u_8,
gamma_(2,1)
 =4u_3+10u_4-52u_5+134u_6-268u_7+466u_8,
gamma_(3)
 =-8u_3+(100/3)u_4-(248/3)u_5+164u_6
   -(856/3)u_7+(1364/3)u_8.
```

For every exact integer `D>=1`, with `rho_y=7T_y<=7/8`, the remainder in
the unscaled gap satisfies

```text
abs(R_(D,y))<=(92/(3pi^2))rho_y^(D+1)
             <(31/pi^2)rho_y^(D+1).
```

The exact majorant ledger is `20+32/3=92/3`; it uses
`sum abs(XI_m)u_m<=35/4` and `sum abs(ETA_m)u_m<=14`.  Terminal
`R_8=mathcal_P_yE_8`, the licensed `E_9=0`, and the absence of `E_10` remain
explicit.  Repeated endpoint or inert coefficient labels in the artifact
are declared bookkeeping copies, not distinct theorems.

RH-383 does not replace its exact power sums by `p_y` asymptotics, use PNT,
introduce `q(N)`, activate nonzero phasewise `c_11`, settle the RH-377
adaptive envelope, or construct an intrinsic operator, trace, zero model,
or Gate A--E result.  Route A is `GO`; Route B is `STOP_SCOPED`.

### 3.23 RH-384 prime-tail scale separation

RH-384 retains the fixed-finite-clock, universally safe,
phasewise-`c_11=0` class and adds a separately frozen prime-counting input.
For each fixed integer `r>=1`, with `x=p_y` and
`f_r(t)=(t^2-1)^(-r)`, strict Stieltjes summation gives

```text
P_r(y)=sum_(p>x)f_r(p)
      =-pi(x)f_r(x)-integral_x^infinity pi(t)f_r'(t)dt.
```

The negative endpoint term is essential: the integral contributes the
apparent coefficient `2r/(2r-1)`, and the boundary subtracts `1`.  The prime
number theorem therefore yields

```text
P_r(y)~1/[(2r-1)p_y^(2r-1)log p_y].
```

For every fixed partition `lambda=1^k_1...d^k_d` of degree `d` and length
`ell=sum k_r`, finite multiplication gives

```text
P_lambda(y)
 ~[product_r(2r-1)^(-k_r)]
   p_y^(-(2d-ell))(log p_y)^(-ell).
```

In particular, with `T_y=P_1(y)` and `S_y=P_2(y)`,

```text
p_y log(p_y)T_y ->1,
3p_y^3 log(p_y)S_y ->1,
S_y/T_y^2 ->0,
T_y^3/S_y ->0,
S_y/[T_y^3 log(p_y)^2] ->1/3.
```

Write

```text
A=2X_infinity/pi^2,
B=(Y_infinity+2m_infinity)/pi^2,
C=(Y_infinity-2m_infinity)/pi^2.
```

The exact RH-382 expansion then implies

```text
p_y log(p_y)(B_infinity-G(q_y)) ->A,
[p_y log(p_y)]^2(B_infinity-G(q_y)-A T_y) ->B,
[B_infinity-G(q_y)-A T_y-B T_y^2]/S_y ->C,
3p_y^3 log(p_y)[B_infinity-G(q_y)-A T_y-B T_y^2] ->C,
[B_infinity-G(q_y)-A T_y-B T_y^2]
  /[T_y^3 log(p_y)^2] ->C/3.
```

The directed interval certificate proves

```text
1.5463476716710499204 <= Y_infinity-2m_infinity
                      <= 1.5484488989771761113,
```

so `C>0`; the twice-subtracted residual is eventually positive and its ratio
to `T_y^3` tends to `+infinity`.  The interval is for the unnormalized
numerator `Y_infinity-2m_infinity`, not for `C` itself.

The exact interface uses `p>p_y` and first atom `p_(y+1)`.  Inclusive versus
strict endpoint and current versus successor prime are exact-interface
distinctions but are invisible to the leading PNT asymptotic.  Limit 2 must
subtract exact `A T_y`; limits 3--5 must subtract exact
`A T_y+B T_y^2`.  Replacing either by a bare-PNT surrogate is unsupported at
the smaller scales.

RH-384 proves no uniformity for growing `r`, degree, length, or clock; no
effective PNT remainder or computable eventual-sign threshold; no active
phasewise-`c_11` cancellation or adaptive-capacity limit; and no intrinsic
operator, trace, zero model, or Gate A--E result.  Route A is `GO`; Route B is
`STOP_SCOPED`.

### 3.24 RH-385 polylogarithmic-clock phasewise-memory uniformization

For every fixed real `B>0`, put `H_B(N)=floor((log N)^B)`.  Let `F_q` be
exactly the finite RH-379 class of universally distance-two-safe,
`q`-periodic lag-two tables with `c_11(r)=0` phasewise, and set

```text
S_N(q,f)=N^(-1)sum_(n<=N)mu(n)
           f_(n mod q)(mu_0(n-2),mu(n)),
L_q(f)=sum_(r mod q)[c_02(r)delta_(q,r)+c_22(r)theta_(q,r)],
mu_0(m)=mu(m) for m>=1 and 0 for m<=0.
```

RH-385 proves the triangular-array theorem

```text
sup_(1<=q<=H_B(N), f in F_q) abs(S_N(q,f)-L_q(f)) ->0.
```

The proof is quantitative before the final limit.  For every `N>=3`, integer
`P>=2`, `q>=1`, and `f in F_q`, define

```text
M_P=(product_(p<=P)p)^2,
Q=lcm(q,M_P),
tau_P=sum_(p>P)p^(-2),
D_*(N)=max_(X in {N,N-2}) sup_alpha
       abs(sum_(n<=X)mu(n)exp(2pi i alpha n)).
```

Then

```text
abs(S_N(q,f)-L_q(f))
 <=4sqrt(Q)D_*(N)/N+13tau_P+6Q/N+4/N.
```

Here `Q` is a valid common period, not necessarily the minimal period.  The
ledger is exact: Fourier channels `1+1+2=4`; finite squarefree-tail costs
`1+1+2+4=8`; limiting tail costs `1+4=5`, hence `13`; periodic-mean costs
`2+4=6`; and the two zero-padding channels at `n=1` cost `2+2=4`.  The
`n=2` padding entry vanishes because `eta_P(0)=0`.  A legal table with
`c_21=-2` forces the third Fourier cost and prevents dropping the factor two.

Choose `P=floor(sqrt(log log N))`, eventually at least two.  The elementary
bound `log M_P<=2P log P=o(log log N)` gives
`Q<=(log N)^(B+o(1))`.  RH-366 supplies
`D_*(N)/N<<_A(log N)^(-A)` uniformly in frequency for every fixed `A>0`, so
one fixed `A>B/2` closes the bound.

Writing

```text
G_N(q)=max_(f in F_q)abs(S_N(q,f)),
G(q)=max_(f in F_q)abs(L_q(f)),
```

the finite-set max lemma and RH-379 yield

```text
sup_(q<=H_B(N))abs(G_N(q)-G(q)) ->0,
max_(q<=H_B(N))G_N(q) ->B_infinity.
```

For the explicit diagonal, use `q_y=4 product_(i<=y)p_i^2` only after the
budget contains `q_1=36`; below that threshold the exact state is
`no_square_clock_available`.  Once nonempty,
`y_B(N)=max{y:q_y<=H_B(N)}` tends to infinity and the RH-379 positive
optimizer at `q_(y_B(N))` tends to `B_infinity`.

The theorem fixes `B`; it does not cover `B=B(N)`, `q=N^epsilon`, or an
unrestricted clock supremum.  It does not activate nonzero `c_11`, control
the RH-377 adaptive envelope, prove convergence of `K_N/N`, construct a
projective infinite selector, give an effective threshold, or create an
intrinsic determinant, trace, zero model, or Gate A--E object.  Route A is
`GO`; Route B is `STOP_SCOPED`.

### 3.25 RH-386 Vinogradov--Korobov growing-order prime-tail uniformization

Let `x=p_y`, `L=log x`, and

```text
V(L)=L^(3/5)(log L)^(-1/5),
epsilon_x=0.027L^1.801 exp(-0.1853V(L)).
```

The external source lock fixes Johnston--Yang, Theorem 1.4, equation (1.8),
which gives `abs(vartheta(t)-t)<=t epsilon_t` for `t>=23`.  The lock records
the exact arXiv-v2 PDF and source-tar URLs, hashes, byte counts, page count,
DOI, locators, and redistribution restriction.  Network replay is opt-in;
the publication contains the metadata lock and verifier but not either
external payload.

For each integer `r>=1`, define

```text
h_r(t)=(t^2-1)^(-r)/log t,
J_r(x)=integral_x^infinity h_r(t)dt,
I_(2r)(x)=integral_x^infinity t^(-2r)/log t dt,
K_r(x)=x^(1-2r)/[(2r-1)L].
```

The strict endpoint is essential:

```text
P_r(y)=integral_(x,infinity)h_r(t)d vartheta(t)
      =-vartheta(x)h_r(x)-integral_x^infinity vartheta(t)h'_r(t)dt,
P_r(y)=(p_(y+1)^2-1)^(-r)+P_r(y+1).
```

For `L>=512`, the source envelope decreases.  The exact logarithmic hazard

```text
q_r(t)=-h'_r(t)/h_r(t)
      =2rt/(t^2-1)+1/(t log t)
```

is decreasing, `J_r>=h_r/q_r`, and `xq_r(x)<=3r`.  Consequently

```text
abs(P_r/J_r-1)<=(6r+1)epsilon_x<=7r epsilon_x,
abs(log(P_r/J_r))<=14r epsilon_x
```

when `7r epsilon_x<=1/2`.  The two kernel comparisons are

```text
0<=log(J_r/I_(2r))<=r/(x^2-1),
abs(log(I_(2r)/K_r))<=1/[(2r-1)L],
0<=log(I_(2r)/K_r)+1/[(2r-1)L]
  <=2/[(2r-1)^2L^2].
```

For a nonempty partition `lambda=1^k_1 2^k_2 ...`, put

```text
d=sum_r r k_r,
ell=sum_r k_r,
R=max{r:k_r>0},
H=sum_r k_r/(2r-1),
H_2=sum_r k_r/(2r-1)^2.
```

If `L>=512` and `7R epsilon_x<=1/2`, multiplication gives the exact finite
ledgers

```text
abs(log(P_lambda/J_lambda))<=14d epsilon_x,
abs(log(P_lambda/I_lambda))<=14d epsilon_x+d/(x^2-1),
abs(log(P_lambda/M_lambda)+H/L)
 <=14d epsilon_x+d/(x^2-1)+2H_2/L^2.
```

Hence `d_y epsilon_(p_y)+d_y/p_y^2->0` yields the exact- and power-kernel
equivalents.  Under the same condition,
`P_(lambda_y)/M_(lambda_y)->1` if and only if `H_y/L_y->0`.  For finite
nonempty families `F_y`, put `D_y=sup_(lambda in F_y)d(lambda)<infinity` and
`H_y^*=sup_(lambda in F_y)H(lambda)<infinity`.  If
`D_y epsilon_(p_y)+D_y/p_y^2->0`, the exact- and power-kernel conclusions are
uniform over `F_y`, and the leading conclusion is uniform if and only if
`H_y^*/L_y->0`.  In particular, `log d_y=o(V(L_y))` and `H_y=o(L_y)` are
sufficient for a sequence.  For one factor, `log R_y=o(V(L_y))` is uniform,
and the explicit window `R_y<=exp((0.1853-delta)V(L_y))` is valid for every
fixed `0<delta<0.1853`.  For every fixed `c>0`, the all-ones family
`lambda_y=1^floor(cL_y)` has ratio `P_lambda/M_lambda->exp(-c)`, proving
the `H/L` obstruction is real.

RH-386 does not make the first valid index effective, enlarge the clock or
phasewise table class, activate nonzero `c_11`, settle `K_N/N`, or construct
an operator, trace, zero model, RH statement, or Gate object.  Route A is
`GO`; Route B remains `STOP_SCOPED`.

### 3.26 RH-387 all-order prime-tail integral resummation

Retain the RH-386 notation `x=p_y`, `L=log x`, `epsilon_x`, `P_r(y)`,
`J_r(x)`, and `I_(2r)(x)`.  RH-387 works only with `L>=512` and the seven
real integer channels `1<=c<=7`.  It defines

```text
Phi_c^P=sum_(r>=1)c^r P_r(y)/r,
Phi_c^J=sum_(r>=1)c^r J_r(x)/r
       =integral_x^infinity -log(1-c/(t^2-1))/log(t) dt,
Phi_c^I=sum_(r>=1)c^r I_(2r)(x)/r
       =integral_x^infinity -log(1-c/t^2)/log(t) dt.
```

All series and integrals are nonnegative and absolutely convergent.  The
strict Stieltjes estimate is used before taking relative logarithms:

```text
abs(P_r-J_r)<=epsilon_x{2x h_r(x)+J_r},
h_r(x)=(x^2-1)^(-r)/L.
```

Summing this absolute bound with weights `c^r/r` and using
`-log(1-z)<=z/(1-z)` gives, with `b=1+c<=8`,

```text
abs(Phi_c^P-Phi_c^J)
 <=3c epsilon_x/[xL{1-b/x^2}]
 <4c epsilon_x/(xL).
```

The exact-to-power logarithmic integrand is nonnegative and at most
`c/[t^4{1-b/x^2}]<=2c/t^4`, so

```text
0<=Phi_c^J-Phi_c^I
 <=c/[3x^3L{1-b/x^2}]
 <2c/(3x^3L).
```

The implication `L>=512 => x=e^L>2^512>256` places `Phi^P`, `Phi^J`, and
`Phi^I` and their joining segments inside `[0,1/2]^7`.  For the frozen
RH-383 endpoint arrays and Euler products,

```text
sum_(m=2)^8 abs(alpha_m)u_m<=7,
sum_(m=2)^8 abs(beta_m)u_m<=49/8.
```

The three derivative channels of the exact endpoint map have coefficients
`2,4,4`.  Pairing the `ell^infinity` input norm with the dual `ell^1`
gradient norm and using `e^(1/2)<2` yields

```text
sup_(z in [0,1/2]^7) norm(grad F(z))_1<126.
```

With `Gap_P=B_infinity-G(q_y)=F(Phi^P)/pi^2` and the two analytic surrogates
`Gap_J=F(Phi^J)/pi^2`, `Gap_I=F(Phi^I)/pi^2`, the final theorem is

```text
pi^2 abs(Gap_P-Gap_J)<=3528epsilon_x/(xL),
pi^2 abs(Gap_J-Gap_I)<=588/(x^3L),
pi^2 abs(Gap_P-Gap_I)
 <=3528epsilon_x/(xL)+588/(x^3L).
```

This is an infinite-order source/kernel exchange followed by a new endpoint
Lipschitz transfer, not a substitution into the RH-386 finite-partition
ledger.  The available source error satisfies `epsilon_x x^2->infinity`, so
the theorem deliberately does not resolve the `P_2`, second-order, or cubic
scale.  It also proves no complex-channel statement, simultaneous prefix and
prime-index limit, active `c_11`, growing clock, adaptive capacity, operator,
trace, zero model, RH statement, or Gate A--E conclusion.  Route A is `GO`;
Route B remains `STOP_SCOPED`.

### 3.27 RH-388 rank-one `P_2`-scale resummation and necessity

Retain `x=p_y`, `L=log x>=512`, the channels `c in {1,...,7}`, and the
RH-387 tails.  For every integer `1<=K<=floor(3L)` and every `r>=2`, define

```text
K_r=x^(1-2r)/[(2r-1)L],
a_r=1/[(2r-1)L],
S_K(a)=sum_(j=0)^(K-1)(-1)^j j!a^j,
I_(2r)^[K]=K_r S_K(a_r),
Psi_c^[K]=cP_1(y)+sum_(r>=2)c^r I_(2r)^[K]/r.
```

The rank-one coordinate remains the exact strict prime tail.  Strict
Stieltjes transfer is applied only for `r>=2`.  Writing
`R(z)=-log(1-z)-z`, the source and exact-to-power ledgers are

```text
max_c abs(sum_(r>=2)c^r(P_r-J_r)/r)<60epsilon_x/(x^3L),
max_c sum_(r>=2)c^r(J_r-I_(2r))/r<13/(x^5L).
```

The common denominator is paid explicitly:

```text
D_c(x)^(-1)
 =[(1-x^(-2))(1-(1+c)/x^2)]^(-1)
 <536870912/536797185<36/35<5/4.
```

The finite geometric identity gives the exact factorial remainder

```text
G(a)-S_K(a)=(-a)^K integral_0^infinity e^(-v)v^K/(1+av)dv,
abs(I_(2r)-I_(2r)^[K])<=K_r a_r^K K!,
max_c abs(sum_(r>=2)c^r(I_(2r)-I_(2r)^[K])/r)
 <=(28/3)x^(-3)K!/[L(3L)^K].
```

Every `Psi^[K]` lies in `[0,1/2]^7`.  With
`b_K=K!/(3L)^K`, the recurrence
`b_(K+1)/b_K=(K+1)/(3L)<=1` proves `b_K<=1/(3L)` over the
complete integer window.  This universal recurrence, not the twelve finite
regression fixtures, pays the moving-`K` quantifier.

The endpoint ledgers are

```text
sup_(z in [0,1/2]^7) norm(grad F(z))_1<126,
sup_(z in [0,1/2]^7) sum_(i,j)abs(partial_(i,j)F(z))<224,
abs(F(z)-grad F(0).z)<=112 norm(z)_infinity^2
  for z in [0,1/2]^7.
```

Consequently

```text
pi^2 abs(Gap_P-Gap_K)
 <=x^(-3)/L[7560epsilon_x+1638/x^2+1176K!/(3L)^K],
lim_(y->infinity) max_(1<=K<=floor(3log p_y))
 abs(Gap_P-Gap_K)/P_2(y)=0.
```

For necessity, Maynard's unconditional theorem supplies infinitely many
consecutive prime pairs `x=p_y`, `q=p_(y+1)=x+h` with integer `h<=600`.
Exact succession gives

```text
x^2[(P_1-I_2)_y-(P_1-I_2)_(y+1)]->1,
limsup_y p_y^2 abs(P_1(y)-I_2(p_y))>=1/2.
```

The seven-coordinate jump tends to `(1,2,3,4,5,6,7)`, while

```text
grad F(0).(1,2,3,4,5,6,7)=2X_infinity>0.
```

The Hessian remainder is `o(x^(-2))`; hence

```text
limsup_y p_y^2 pi^2 abs(Gap_P-Gap_I)>=X_infinity,
limsup_y p_y^2 pi^2 abs(Gap_P-Gap_J)>=X_infinity,
limsup_y abs(Gap_P-Gap_I)/P_2(y)=infinity,
limsup_y abs(Gap_P-Gap_J)/P_2(y)=infinity.
```

Necessity is restricted to the frozen `P/J/I` smooth-kernel hierarchy.
RH-388 makes no assertion about every possible surrogate, factorial-series
convergence, a larger `K` window, `P_3` or cubic precision, complex channels,
growing clocks, active `c_11`, adaptive capacity, operators, traces, zeros,
RH, or Gates A--E.  Routes A and B are `GO`; Route C is `STOP_SCOPED`.

## 4. Compact conclusions from RH-352 through RH-388

- **RH-352:** Actual growing lower-even normalized `p` is exponentially
  small and actual `Y` tracks `S-P` on `J_k->infinity`, `J_k=o(k)`; the
  selected `Y` aggregate has the proved positive lower-scale obstruction,
  but no unnormalized prefix theorem follows.
- **RH-353:** Actual critical/first-lower normalized `Y` has the phase-free
  two-coordinate gap (with the recorded `>1/9` lower bound); it is not a
  direct-`p` lower bound.
- **RH-354:** Actual parity-free direct `p` has a normalized tail theorem
  above a moving cut; low orders, the unnormalized prefix, and `q/E_off`
  remain open.
- **RH-355:** Complete deterministic strict-upper burden and terminal share;
  actual transfer is conditional on `D_(4k)(R)->0`.
- **RH-356:** Deterministic mesoscopic crossover and integer phase; actual
  transfer remains conditional.
- **RH-357:** Complete deterministic linear-depth endpoint profile and floor
  phases; actual transfer remains conditional.
- **RH-358:** Deterministic terminal-lag geometric TV localization and first
  two moments; not an eigenvalue or root-counting law.
- **RH-359:** Deterministic logarithmic accuracy, inverse-window law, and
  correction limit set `[0,1]`; actual transfer remains conditional.
- **RH-360:** Deterministic subcritical, critical-window, and supercritical
  exponential-tilt phase diagram at the declared budget type.
- **RH-361:** Exact typed separation and finite-fiber nonpromotion theorem;
  no physical counterexample or spectral conclusion is constructed.
- **RH-362:** Exact prime-return Euler dichotomy, zero-free nonperiodic
  product, restricted Fredholm realization, periodic finite-correction
  branch, and inverse-clock non-Schatten obstruction. It is independent of
  the physical route and closes no Gate.
- **RH-363:** Exact admissible entropy tower, identical collapsed periodic
  zetas, multiples--M\"obius rank tomography, universal primorial first
  defect, and sharp finite-radius exhaustion discontinuity. The tower is an
  engineered functor and closes no Gate.
- **RH-364:** Certified all-order weighted survivor disk and tail, larger
  correction-product disk with a strict quotient firewall, exact prime-copy
  Schatten/Fredholm regions, fractional weighted singularity, and common
  scalar normalization failure first at prime cubes. The copy is engineered
  and closes no Gate.
- **RH-365:** Exact reversibility midpoint compression, double-exponential
  gcd height, an all-order marked-bouquet fixed-point envelope, a strict
  zero-free disk, odd-prime primitive/logarithmic anchors, a raw-coefficient
  firewall, and a naive-direct-sum noncompactness theorem. The bouquet remains
  marked and noncanonical and closes no Gate.
- **RH-366:** Fixed-periodic and Parry-almost-sure Möbius orthogonality for
  continuous observables; an explicitly offline Möbius-adapted point with
  correlation `4/pi^2`; exact Parry covariance and unconditional linear
  variance bound; a conditional `6/pi^2` variance-density limit; and an exact
  `O(N)` adaptive-capacity bracket. The capacity limit and any intrinsic
  arithmetic coupling remain open, and the package closes no Gate.
- **RH-367:** Exact aligned finite-Ulam anti-diagonal block structure and
  band-sign `-1` inheritance for the PCF two-band map; exact crossing-cell
  projection defect `4theta(1-theta)` and width-weighted defect
  `4h theta(1-theta)`; and a 136-row finite phase audit. No continuum
  projector/resolvent bridge or universal noise exponent is proved, and the
  package closes no Gate.
- **RH-368:** Source-locked PCF three-cell factor `A_{\{2\}}`; exact finite
  capacity formula for one-parity positive words; Davenport parity
  cancellation and odd/even squarefree densities yielding the all-order
  limit `K_N^(2)/N -> 4/pi^2`. This is not the RH-366 distance-two capacity,
  not a canonical arithmetic coupling, and closes no Gate.
- **RH-369:** Derived branch-symmetric Markov family on the RH-366 graph;
  exact stationary law, fixed-parameter mixing, all-lag covariance,
  simultaneous almost-sure Möbius orthogonality for every continuous
  observable, and the finite bound `V_(N,t)<=((2-t)/t)N`. The Chowla density
  remains conditional, no uniform-in-`t` theorem is claimed, and no Gate is
  closed.
- **RH-370:** Exact finite folding quotient for mirror-compatible Ulam
  partitions, an `L^1`/exterior-resolvent bridge, and a terminal square-root
  spike giving a sharp `h^(-1/2)` BV projection barrier. The quotient is not
  a continuum spectral theorem, arbitrary partitions and zero-noise limits
  remain open, and no Gate is closed.
- **RH-371:** Exact all-prefix eight-run reduction of the RH-366 distance-two
  capacity, plus a cyclic-only pair-ledger obstruction using synthetic
  period-18 words. The Möbius run-envelope density and capacity limit remain
  open; the witness is not a Möbius sequence, and no Gate is closed.
- **RH-372:** Exact open-path max-plus DP for finite constraint graphs; a
  universal-safety/one-site transducer theorem with squarefree AP densities;
  finite fixed-`(q,m)` enumeration; and three certified finite instances,
  including `4/pi^2`, `4/pi^2`, and `9/(4*pi^2)` one-site lower constants.
  Memory-dependent labels, the RH-366 capacity limit, all intrinsic operator
  and prime-trace bridges, and Gates A--E remain open/false.
- **RH-373:** A general independent phase-selector lemma and an explicit
  composite-clock `q=180` certificate on RH-366.  The `80`-phase set has no
  cyclic distance-two conflict; exact `180`-progression squarefree densities
  and fixed-AP Möbius cancellation give the unconditional floor
  `liminf K_N/N >= 97/(24*pi^2) = 4/pi^2 + 1/(24*pi^2)`.  A literal two-state
  universal-safety completion passes all `3240` table rows.  This is one fixed
  externally prescribed arithmetic witness, not an all-clock optimum or a
  capacity-limit theorem; memory-dependent correlations, intrinsic operators,
  prime traces, and Gates A--E remain open/false.
- **RH-374:** A strictly increasing square-clock family of exact fixed-clock
  one-site optima, with a prime-adjoining recurrence and an exact
  Euler-product limit floor for `liminf K_N/N`.  The theorem fixes each clock
  before the asymptotic limit; it proves neither an all-clock or
  memory-dependent optimum nor convergence of the adaptive capacity, and all
  operator/trace/zero claims and Gates A--E remain false/open.
- **RH-375:** Exact squarefree-density weighted MWIS optimization for every
  finite clock, monotonicity under clock divisibility, special same-support
  square-clock saturation, and the nonattained supremum
  `sup_(q finite)F(q)=B_infinity`.  This closes only the universally safe
  one-site class; memory, growing clocks, adaptive capacity convergence,
  intrinsic operators/traces/zeros, and Gates A--E remain open/false.
- **RH-376:** Exact common-endpoint Boolean reduction of each signed
  two-site run interval to a squarefree-pair term, two one-sign masked terms,
  and the raw shift-two correlation.  The first three terms are unconditional;
  a frozen logarithmic affine theorem plus one-way Abel summation makes
  existence of either interval density equivalent to ordinary shift-two
  Cesaro Chowla, with value `kappa_2/4`.  The theorem proves neither Chowla
  nor nonconvergence, does not settle the eight-run capacity envelope, and
  closes no Gate.
- **RH-377:** Exact all-prefix mixed-exponent transform for all sixteen
  signed windows; unconditional zero-sign and one-sign layers; a thirteen
  aggregate simultaneous-density boundary; and the sharper exact
  two-envelope criterion for `K_N/N`.  Its `466 -> 13` rank is formal only,
  the conditional Euler constant is unproved, the stationary witness is
  synthetic rather than Möbius, and no capacity limit or Gate is closed.
- **RH-378:** Exact compatible-block safety for fixed finite windows; the
  complete `512/13` lag-two census and rank-five score ledger; seven
  unconditional versus six shift-two-Chowla-hard tables; two fixed
  four-state machines realizing the two capacity orientations on every
  prefix; a deterministic single-policy obstruction; and a narrowly minimal
  length-`15` stateless realization on the Möbius run-cutoff class.  The two
  machines are not one online optimizer, finite memory proves no capacity
  limit, and no operator, trace, zero, or Gate is constructed.
- **RH-379:** Exact phasewise-`c_11=0` cancellation and `512/192` local census;
  canonical subset reduction to a three-state cyclic max-plus optimizer;
  exact strict memory gains at `q=1` and `q=36`; the square-clock identity
  `G(q_y)=B_y+Delta_y` with positive vanishing correction; and the exact
  all-finite-clock supremum `sup_q G(q)=B_infinity`.  The theorem does not
  decide finite-clock attainment, cancel active phase-weighted shift-two
  terms, or prove an adaptive-capacity limit, operator, trace, zero, or Gate.
- **RH-380:** Exact all-order even-run deletion recurrence and square-clock
  increment; strict monotonicity of `G(q_y)`; separator-specific
  same-prime-support saturation; and the strict quantitative conclusion
  `G(q)<B_infinity` for every fixed finite clock in the RH-379 class.  It
  does not prove `Delta_y` monotone, a general cover law, the successor tail
  rate, active phasewise shift-two cancellation, adaptive-capacity
  convergence, an operator, trace, zero, or Gate.
- **RH-381:** Exact first-order prime-square-tail rate for the RH-380
  square-clock gap, with positive Euler-product coefficient and the uniform
  all-order remainder `342T_y^2/pi^2`.  The theorem uses no PNT and fixes
  every finite clock before its prefix limit.  It does not claim a
  second-order coefficient, a `p_y` asymptotic, active phasewise
  shift-two cancellation, growing clocks, adaptive-capacity convergence,
  an operator, trace, zero model, or Gate.
- **RH-382:** Exact two-scale second-order expansion of the square-clock gap,
  with separate `T_y^2` and `S_y` channels, forced opposite memory sign,
  and the uniform cubic remainder `3301T_y^3/(6pi^2)<551T_y^3/pi^2`.
  Terminal `R_8`, `E_9=0`, and the absence of `E_10` are paid explicitly.
  It does not use PNT, rewrite in `p_y`, activate nonzero `c_11`, introduce
  growing clocks, settle adaptive capacity, or construct any Gate object.
- **RH-383:** Exact absolutely convergent Euler-tail endpoint and partition
  normal form for the square-clock gap, with a finite coefficient compiler,
  all-order disappearance of the `m=2` channel, exact recovery of the first
  two homogeneous layers, a new cubic block, and the uniform arbitrary-order
  remainder `(92/(3pi^2))(7T_y)^(D+1)`.  It keeps partition length distinct
  from degree, uses the strict successor tail, and does not use PNT, rewrite
  in `p_y`, enlarge the phasewise-`c_11=0` class, settle adaptive capacity,
  or construct any Gate object.
- **RH-384:** Fixed-`r` prime-tail and fixed-partition `p_y`/log asymptotics,
  with the strict Abel boundary and exact coefficient `1/(2r-1)`; the scale
  separation `T_y^3=o(S_y)=o(T_y^2)`; and five normalized square-clock gap
  limits with a proof-grade positive `S_y` coefficient.  It uses exact
  arithmetic subtractions at smaller scales and proves no effective PNT
  rate, growing parameter, class enlargement, adaptive-capacity result, or
  Gate object.
- **RH-385:** Uniform convergence of the full RH-379 phasewise-`c_11=0`
  class over every fixed polylogarithmic clock window, with the exact
  `4/13/6/4` cutoff ledger, uniform transfer to finite optimizers, convergence
  of the restricted maximum to `B_infinity`, and an explicit nonempty
  square-clock diagonal witness.  It does not cover polynomial clocks,
  varying `B`, active `c_11`, the full adaptive capacity, or any Gate object.
- **RH-386:** Quantitative prime-tail comparison uniformly over growing
  single orders and growing finite partition families, using the explicit
  Johnston--Yang Vinogradov--Korobov estimate.  It proves the exact
  source/kernel/leading ledgers, the uniform `log d=o(V)` window, the sharp
  leading-kernel criterion `H/L->0`, and the all-ones limit `exp(-c)`.  The
  external source is hash-locked but not redistributed.  It does not enlarge
  clocks or the phasewise class, activate `c_11`, settle adaptive capacity,
  make an effective threshold, or construct any Gate object.
- **RH-387:** Infinite-order resummation of all seven real prime-tail
  coordinates into strict-source and power-kernel logarithmic integrals,
  followed by the exact RH-383 endpoint map.  It proves the coordinate
  constants `28` and `14/3`, the endpoint Lipschitz constant `126`, and the
  gap constants `3528` and `588`.  The certified source error is larger than
  the `P_2` scale, so no second-order or cubic precision, complex channel,
  growing clock, active `c_11`, adaptive capacity, or Gate object follows.
- **RH-388:** Uniform `P_2`-scale factorial resummation of every higher rank
  while retaining the exact strict `P_1` coordinate.  It proves the
  coordinate constants `60`, `13`, and `28/3`, the complete moving window
  `1<=K<=floor(3L)`, and the endpoint constants `7560/1638/1176`.  Maynard's
  bounded consecutive gaps prove the complementary sharp `1/2` scalar and
  `X_infinity` endpoint limsup obstruction for the fully smooth `P/J/I`
  hierarchy.  No universal surrogate obstruction, factorial convergence,
  `P_3` precision, class enlargement, or Gate object follows.

## 5. Route firewall and reopening triggers

Do not:

- call the RH-361 coefficient fiber a physical counterexample;
- promote normalized actual `p` to unnormalized `q/E_off`;
- promote deterministic `s` to an actual spectrum, root set, or rank law;
- state a conditional `D_(4k)(R)` transfer as proved;
- identify a selected window with the full prefix or `E_off`;
- identify `[z^ell] Z_0` with the prime-order primitive anchor;
- identify the locally finite bouquet ledger `T_n` with a trace-class
  Hilbert-space trace;
- call the RH-366 offline optimizer a spontaneous or canonical arithmetic
  coupling;
- promote the finite `0.492...` capacity diagnostic to an asymptotic constant;
- promote the conditional `V_N/N -> 6/pi^2` statement to an unconditional
  theorem or infer ordinary Chowla from the finite variance rows;
- identify a Möbius-weighted orbit average or a Parry variance with a
  von-Mangoldt trace, spectral determinant, or Riemann-zero model;
- promote the RH-367 finite Ulam `-1` mode to an isolated continuum resonance;
- promote a finite phase scan or fitted noise slope to a universal asymptotic
  law;
- identify the crossing-cell local identity `4h theta(1-theta)` with the
  global stationary leakage observable for every discretization;
- identify the RH-368 parity-factor `A_{\{2\}}` capacity with the RH-366
  distance-two capacity, or claim that one admissible language contains the
  other;
- promote the RH-368 endpoint row `0.405402...` to evidence for the limit;
- identify the adaptive parity-factor optimizer with a nonadaptive orbit,
  canonical operator trace, or von-Mangoldt ledger;
- call the RH-369 family geometrically selected by the Hénon map or treat the
  externally chosen `t` as canonical arithmetic data;
- claim a common full-measure set or a uniform theorem over all
  `t in (0,1)`, or include the degenerate endpoints;
- promote the RH-369 conditional `V_(N,t)/N -> 6/pi^2` statement to an
  unconditional two-point Chowla theorem;
- identify the RH-369 Markov covariance with a prime trace, determinant, or
  Riemann-zero model;
- promote the RH-370 finite nonzero quotient spectrum to a continuum
  resonance or Riesz projector;
- apply the RH-370 quotient to non-mirror, crossing, or phase-shifted grids;
- treat the RH-370 `L^1` exterior resolvent as a contour theorem at `-1`;
- substitute `sigma=0` into the positive-noise hypotheses of RH-52/RH-55;
- treat the RH-370 finite quotient audit or spike rows as asymptotic or
  universal noise evidence;
- treat the RH-371 eight-run identity as a convergence theorem for its
  normalized run frequencies or for `K_N/N`;
- call the RH-371 cyclic pair ledger an open-prefix ledger, or use its
  synthetic words as a Möbius counterexample;
- infer nonexistence of the Möbius capacity limit from the periodic witness;
- promote RH-372's fixed-`(q,m)` table enumeration to a classification of all
  mixing SFTs;
- apply the RH-372 one-site density formula to a memory-dependent observable
  without a higher-order Möbius theorem;
- call a safe transducer an intrinsic operator, determinant, prime-power trace,
  zero model, or RH proof;
- call the RH-373 `q=180` selector an optimizer over all clocks, a proof that
  `lim K_N/N` exists, or a replacement for the RH-371 run-envelope theorem;
- promote `97/(24*pi^2)` from one fixed arithmetic lower certificate to the
  adaptive capacity limit, to a universal transducer supremum, or to a Gate;
- treat the two-state RH-373 completion as a new dynamical operator, a
  spontaneous arithmetic coupling, a prime-power trace, or a zero model;
- extend the RH-374 run second-difference formula to `j=8` or introduce an
  `E_10`: the endpoint is separately `R_8=P_y E_8`;
- call the RH-374 value `B_y` optimal over arbitrary memory-dependent
  transducers, all finite clocks, or the adaptive RH-366 capacity;
- turn the scalar supremum `B_infinity` into a growing-clock `q(N)` selector,
  a uniform-in-clock Davenport theorem, an infinite arithmetic orbit, or a
  proof that `lim K_N/N` exists;
- identify the RH-374 selector family or Euler products with an intrinsic
  operator, determinant, prime-power trace, Riemann-zero model, Hilbert--Polya
  construction, or any Gate A--E result;
- require the declared clock in RH-375 to be the minimal period; the
  divisibility lift intentionally permits a nonminimal `q`-periodic factor;
- replace the special RH-375 same-prime-support saturation proof by a general
  cyclic-cover MWIS scaling law, or project an arbitrary lifted independent
  set back to the base clock;
- call `B_infinity` a maximum attained at a finite clock, extend the supremum
  to memory-dependent factors, or identify it with `lim K_N/N`;
- infer the all-clock theorem from the bounded `q<=256` scan, introduce
  `q=q(N)`, or exchange the clock and prefix limits without a uniform theorem;
- turn the RH-375 prescribed factors into intrinsic dynamics, an operator,
  determinant, prime-power trace, zero model, Hilbert--Polya construction, or
  RH proof;
- call `C_(sigma,2)` a maximal exact-length-two run count, or change the
  common endpoint independently in its four-term identity;
- read the RH-376 logarithmic affine theorem as an unconditional natural
  shift-two Chowla theorem, reverse the one-way Abel implication, or use a
  divisor modulus growing with `N`;
- infer convergence or nonconvergence of either signed interval density, the
  eight-run envelope, or `K_N/N` from the RH-376 equivalence or finite rows;
- promote the RH-376 scalar arithmetic interval count to an intrinsic
  dynamical observable, operator trace, prime-power ledger, zero model, or
  Gate result;
- call the RH-377 `466 -> 13` formal block rank the arithmetic minimal
  dimension of actual Möbius correlations, or infer separate `A_k/B_k`
  convergence from only one signed density;
- promote the RH-377 full mixed-exponent cancellation hypothesis or its
  finite Euler diagnostic to an unconditional capacity constant;
- infer convergence or nonconvergence of `(U_N+abs(V_N))/N` or `K_N/N`
  from the exact RH-377 reduction or its finite prefix rows;
- treat the RH-377 stationary ternary witness as a Möbius sequence,
  squarefree-density model, or arithmetic counterexample;
- identify the RH-377 envelope with an intrinsic operator, determinant,
  prime-power trace, zero model, Hilbert--Polya construction, or Gate result;
- call the RH-378 displayed monomials a unique basis, promote their formal
  dimension or the lag-table rank to an arithmetic correlation minimum, or
  infer unknown mixed-moment limits from finite interpolation;
- call either RH-378 scoped lag-table constant an optimum over arbitrary
  memory transducers; in particular, the larger value
  `6/pi^2-kappa_2/2` remains conditional on `D_2=o(N)`;
- infer convergence or nonconvergence of the RH-377 envelope or `K_N/N`
  from the RH-378 finite-state realization or the endpoint rows;
- call the two fixed RH-378 orientation machines one deterministic online
  policy computing `K_N`, or extend the single-policy obstruction to
  offline, horizon-aware, randomized, approximate, or Möbius-only policies;
- promote the four-state lower bound beyond exact reproduction of one frozen
  orientation stream, or promote the length-`15` lower bound beyond `q=1`
  causal contiguous stateless exact-stream rules on the run-at-most-eight
  class;
- claim that the length-`15` formula equals the recursion on every ternary
  input, or treat its `17`-site synthetic counterexample as a Möbius
  counterexample;
- identify an RH-378 window table or Mealy state with an intrinsic operator,
  determinant, prime-power trace, zero model, Hilbert--Polya construction,
  or Gate result;
- call RH-379 a classification of unrestricted lag-two or finite-memory
  tables: it requires `c_11(r)=0` separately at every fixed phase;
- import the RH-378 relation `c_22=-c_02-c_11` from its thirteen self-
  compatible `q=1` tables into the RH-379 `192`-table phase census;
- replace `K` by `I` before the RH-379 canonical subset reduction, or claim
  that their compatibility agrees against arbitrary unreduced neighbors;
- call the `q=36` gain the first same-clock memory gain: `q=1` already has
  `G(1)>F(1)=0`;
- promote `Delta_y>0` and `Delta_y->0` to monotonicity, or infer a general
  same-support memory saturation law from the RH-379 square-clock formula;
- call `sup_(q finite)G(q)=B_infinity` a finite-clock maximum, a growing-clock
  `q(N)` theorem, an adaptive-capacity limit, or a uniform-in-clock
  Davenport estimate;
- cancel nonzero active `c_11(r)` terms without a phase-weighted ordinary
  shift-two theorem, or identify an RH-379 table with an intrinsic operator,
  determinant, prime-power trace, zero model, Hilbert--Polya construction,
  or Gate result;
- promote strict monotonicity of the RH-380 values `G(q_y)` to monotonicity
  of `Delta_y=G(q_y)-B_y`;
- extend the RH-380 identity `G(Q)=G(q_y)` to a general multiple or cyclic
  cover: it requires identical prime support and the forced mod-4/mod-9
  separators, and `Q=180` is the locked negative control;
- turn RH-380 finite-clock nonattainment into a growing-clock `q(N)` theorem,
  an adaptive-capacity limit, or a uniform-in-clock Davenport estimate;
- present the RH-381 prime-square-tail expansion as proved by RH-380, or
  infer it from finite values without an all-order remainder estimate;
- identify the RH-380 max-plus selector with an intrinsic operator,
  determinant, prime-power trace, zero model, Hilbert--Polya construction,
  or Gate result;
- call the RH-381 six-row exact fixture or directed interval rows asymptotic
  evidence; the all-`y` result is symbolic and the rows are reproduction
  only;
- suppress the independent quadratic scale
  `S_y=sum_(j>=y)a_(j+1)^2`, infer an exact second-order coefficient from the
  RH-381 first-order theorem, or replace `T_y` by a `p_y` asymptotic without
  a separately sourced prime-tail theorem;
- extend the RH-381 rate outside the fixed-finite-clock phasewise-`c_11=0`
  class, introduce `q(N)`, exchange the clock and prefix limits, or infer
  convergence of the RH-377 envelope or adaptive capacity;
- identify the RH-381 Euler-tail arithmetic selector with an intrinsic
  operator, determinant, prime-power trace, zero model, Hilbert--Polya
  construction, or Gate result;
- collapse the RH-382 power sum `S_y` into a fixed multiple of `T_y^2`, or
  change the memory coefficient from `Y_infinity-2m_infinity` to
  `Y_infinity+2m_infinity`;
- extend the RH-374 run second-difference formula to length eight, invent an
  `E_10` term, or omit the exact `E_9=0` contribution licensed at length
  seven;
- treat the RH-382 finite gap rows or `p=71` wrong-sign mutation as evidence
  for the all-`y` theorem rather than reproduction of the symbolic proof;
- promote RH-382 to a `p_y` asymptotic, PNT statement, growing-clock theorem,
  active phasewise-`c_11` cancellation, adaptive-capacity limit, intrinsic
  operator, determinant, trace, zero model, Hilbert--Polya construction, or
  Gate result;
- replace the RH-383 partition-length sign by total-degree parity, or replace
  its strict successor tail `j+1` by the current tail `j`;
- conflate RH-383 endpoint coefficients `alpha/beta` with increment
  coefficients `XI/ETA`, or inherit the special RH-381/RH-382 remainder
  constants `342` or `3301/6` as its arbitrary-order majorant;
- call the inert-`c`, endpoint-labelled, or low-order bookkeeping copies in
  the RH-383 artifact distinct theorems, or treat its finite rows as the
  proof of absolute convergence or the infinite partition identity;
- promote RH-383 to a PNT or `p_y` scale theorem, growing-clock theorem,
  active phasewise-`c_11` cancellation, adaptive-capacity limit, intrinsic
  operator, determinant, trace, zero model, Hilbert--Polya construction, or
  Gate result;
- omit the negative strict-endpoint Abel boundary in RH-384 or replace its
  net constant `1/(2r-1)` by the integral-only coefficient
  `2r/(2r-1)`;
- call `p>=p_y` or a `p_(y+1)` right-hand scale a leading-asymptotic
  counterexample: those are exact-interface distinctions but have the same
  leading fixed-`r` PNT asymptotic;
- replace exact `A T_y` in RH-384 limit 2, or exact
  `A T_y+B T_y^2` in limits 3--5, by bare-PNT surrogates whose uncontrolled
  error may dominate the next scale;
- identify the certified interval for `Y_infinity-2m_infinity` with the
  normalized coefficient `C` before dividing by `pi^2`;
- promote RH-384 to an effective threshold or rate, uniform growing-`r` or
  growing-partition theorem, growing-clock theorem, active phasewise-`c_11`
  cancellation, adaptive-capacity limit, intrinsic operator, determinant,
  trace, zero model, Hilbert--Polya construction, or Gate result;
- use finite rows as physical or asymptotic evidence; or
- extend the deterministic terminal-lag sequence by reparameterization alone.

The admissible reopening triggers before RH-362 were:

1. An actual same-clock `D_(4k)(R)->0` theorem, or a genuine physical
   obstruction to it.
2. A typed actual full-trace `q` or complete `E_off` theorem.
3. An unnormalized complete direct-prefix theorem, including orders below
   the RH-354 moving cut.
4. The RH-241 moving noisy all-order envelope plus its no-over-extraction
   coefficient bridge.
5. Another independent source-backed theorem edge.

Trigger 5 is satisfied by the independent theorem edges RH-362 through
RH-388. Triggers 1--4 remain untouched. RH-365 closes the natural
return-bouquet height/radius route at its declared scope, RH-366 closes the
declared periodic/typical/distance-two capacity audit, RH-373 closes the
declared fixed composite-clock phase-selector floor route, and RH-374 closes
the declared square-clock family/Euler-product floor route. RH-375 closes the
all-finite-clock universally safe one-site supremum but not the adaptive
capacity limit. RH-367 closes the
declared finite-Ulam alignment/phase-defect audit, and RH-368 closes the
declared `A_{\{2\}}` parity-factor capacity route. RH-369 closes the declared
fixed-parameter branch-symmetric Markov/Gibbs route. RH-370 closes the
declared fold-compatible quotient/exterior-bridge/BV-barrier audit. RH-371
closes only the declared exact eight-run reduction and cyclic pair-ledger
obstruction; it does not close the capacity-limit route. RH-372 closes only
the fixed-resource graph/transducer certificate route. RH-373 closes only the
explicit q=180 arithmetic lower certificate. RH-374 closes only the declared
square-clock one-site family. RH-375 closes only the declared all-finite-clock
one-site class. RH-376 closes only the declared shift-two interval-density
hardness theorem. RH-377 closes only the declared mixed-exponent hierarchy
and two-envelope reduction; it does not close the capacity limit. RH-378
closes only the fixed-window safety, `q=1` lag-two classification, and exact
online-orientation realization route; it proves neither its Chowla-hard
subclass nor the capacity limit. RH-379 closes only the fixed-finite-clock,
phasewise-`c_11=0` max-plus and supremum route; it does not close active
phase-weighted shift-two cancellation or the adaptive capacity limit.
RH-380 closes only the finite-clock attainment question, exact run
recurrence, strict square-clock monotonicity, and separator-specific
same-support saturation inside that same class.  It does not prove the
normalized prime-square-tail rate, enlarge the class, or close the adaptive
capacity limit. RH-381 closes only the normalized first-order
prime-square-tail rate and explicit quadratic remainder inside that class.
It does not identify the second-order coefficients, replace `T_y` by a
`p_y` asymptotic, enlarge the class, or close the adaptive capacity limit.
RH-382 closes only the two-scale second-order expansion and uniform cubic
remainder inside that same class.  It does not prove an arbitrary-order
normal form, replace `T_y` by a `p_y` asymptotic, enlarge the class, or close
the adaptive capacity limit.  RH-383 closes only the exact Euler-tail
endpoint/partition normal form, absolute convergence, all-order `m=2`
cancellation, cubic layer, and uniform arbitrary-order remainder inside that
same class.  It does not supply a PNT scale dictionary, enlarge the class, or
close the adaptive capacity limit.  RH-384 closes only the fixed-`r`,
fixed-partition prime-tail scale dictionary and normalized gap limits inside
that class.  It does not provide effective PNT error, growing-parameter
uniformity, active phasewise cancellation, a growing clock, or an adaptive
capacity limit.  RH-385 closes only fixed-`B` polylogarithmic-clock
uniformity, restricted-max transfer, and the nonempty square-clock diagonal
inside the phasewise-`c_11=0` class.  It does not cover polynomial clocks,
varying `B`, active phasewise cancellation, the adaptive capacity, or any
Gate.  RH-386 closes the quantitative-PNT source gate, growing-order
single-tail uniformity, growing finite partition families, and the sharp
`H/L` leading-kernel criterion.  It does not provide an effective first
index, growing clock, active phasewise cancellation, adaptive capacity, or
any Gate.  RH-387 closes only the all-order absolute source-to-integral
resummation and endpoint Lipschitz transfer on the seven real channels.  Its
certified error is larger than the `P_2` scale, and it does not provide
second-order precision, complex-channel uniformity, a growing clock, active
phasewise cancellation, adaptive capacity, or any Gate.  RH-388 closes the
rank-one-retained `P_2`-scale factorial resummation and the bounded-gap
necessity theorem only inside the frozen `P/J/I` hierarchy.  It does not
prove factorial-series convergence, a larger `K` window, a universal
surrogate obstruction, `P_3` precision, a complex channel, growing clock,
active phasewise cancellation, adaptive capacity, or any Gate.  For RH-389
and later, the shortest exact candidates are:

1. A genuine phase-weighted shift-two or higher-order Möbius correlation
   theorem controlling active `c_11(r)` terms, the
   RH-377 envelope or a larger memory-dependent transducer class.
2. A nonadaptive geometrically selected measure theorem.  The 2026-08-07
   source lock is `STOP_SCOPED`: RH-369's non-Parry `P_t` is externally
   selected, while the weighted-Hénon and cyclic-Ulam sources do not prove a
   fixed non-Parry equilibrium state with the required mixing theorem.
3. A new fractional/tower-adapted strong-space projector/resolvent theorem
   that genuinely connects the RH-367 finite-Ulam family to a declared
   continuum operator.  The 2026-08-07 source lock is `STOP_SCOPED` until a
   fixed mesh-independent norm, uniform projection/lift estimate, and common
   contour around `-1` are explicitly proved.
4. A genuine composite-order primitive-divisor upgrade, such as an eventual
   Zsigmondy theorem or a `p`-adic lifting bound strong enough to force new
   primes. No such theorem is present in the locked source.
5. A sharp return-rank multiplicity theorem strong enough to determine the
   exact origin radius or a genuine boundary law for `Z_0`. RH-365 supplies
   only the bracket `[2^(-1/2),1]`.
6. A quantitative finite-entropy-data theorem that certifies or excludes a
   finite prime/rank prefix without promoting numerical conditioning to exact
   infinite recovery.
7. An intrinsic pressure/transfer/groupoid operator producing the entropy
   tower without inserting every modulus by hand.
8. One of the original physical triggers 1--4.

RH-364 closes the declared weighted-H\'enon prime-copy audit. It must still be
called a prime lift or copy, not a finite-field reduction, Hasse--Weil local
factor, or full `H_p` zeta. Its prime and square trace weights match after
the unique scalar normalization, but the cube coefficient `4 log p` is an
exact Gate-D obstruction for that construction. Repackaging the same local
survivor, marked-cycle, or entropy product is not a new trigger.

RH-365 closes the declared unweighted return-bouquet height/radius audit. Its
odd-prime anchor must remain a primitive Euler/logarithmic coefficient, not a
raw zeta coefficient or a composite-order Zsigmondy theorem. Repackaging the
same midpoint identities, radius lower bound, or noncompact direct sum is not
a new trigger.

RH-366 closes the declared Hénon Möbius typical/exceptional and adaptive-
capacity audit. Its exceptional point is selected only after the full
positive-time Möbius sequence is known; its covariance and variance results
are Parry-measure statements; and its finite capacity bracket does not assert
a limit. Repackaging the same offline coding, finite plateau, or conditional
Chowla comparison is not a new trigger. Any successor must supply a new
source-backed theorem or a proved scoped negative in a distinct data type.

RH-367 closes the declared boundary-aligned cyclic-Ulam audit. Its finite
anti-diagonal block theorem and local crossing-cell identity must not be
repackaged as a continuum spectral theorem; its phase scan and noisy slopes
are finite diagnostics only. A successor must either prove the missing
strong-space projector/resolvent bridge or supply a genuinely different
source-backed edge.

RH-368 closes the declared PCF `A_{\{2\}}` parity-factor capacity audit. Its
 `4/pi^2` limit belongs to the distinct one-parity factor and must not be
 rebranded as the RH-366 distance-two limit, a nonadaptive orbit law, or a
 canonical arithmetic trace. Any successor must supply a new graph, a new
 nonadaptive measure theorem, the missing Ulam bridge, or one of the original
 physical triggers.

RH-369 closes the declared branch-symmetric Markov/Gibbs family audit.  The
Parry point is inherited from RH-366, while the non-Parry interior family is
derived and noncanonical.  Reparameterizing the same family, weakening the
fixed-`t` quantifiers, or restating its covariance is not a new trigger.  A
successor must supply a geometrically selected measure, a general graph
theorem, the missing Ulam bridge, the distance-two capacity limit, or one of
the original physical triggers.

RH-372 closes only the bounded constraint-graph certificate route.  Its
max-plus recurrence is finite-prefix exact; its transducer limits use only
fixed-clock squarefree densities and Davenport cancellation; and its finite
`(q,m)` enumeration is not an all-graph or all-memory classification.  A
memory-dependent observable is outside the theorem until a higher-order
Möbius correlation result is proved.  The three frozen tables are offline
selectors and do not become intrinsic dynamics, determinants, prime-power
traces, or zero sets by reparameterization.

RH-373 closes only the declared fixed composite-clock phase-selector floor
route.  Its `q=180` witness is an explicit `80`-phase independent set with
`liminf K_N/N >= 97/(24*pi^2)`.  This improves the RH-366 lower floor but does
not prove an ordinary capacity limit, an all-clock supremum, or a
memory-dependent correlation theorem.  The two-state graph completion is a
literal universal-safety certificate and remains an externally prescribed
arithmetic selector; it is not an intrinsic operator, determinant, prime-power
trace, zero model, or RH proof.  A successor must supply a genuine
composite-clock family theorem, the
RH-371 run-envelope limit/negative, a higher-order correlation theorem, or a
different source-backed edge.

RH-374 closes only the square-clock one-site family and its Euler-product
floor.  Its exact `B_y` is an optimum at the declared fixed clock `q_y`, not
over arbitrary memory or all clocks.  The passage to `B_infinity` takes the
supremum of scalar fixed-clock lower bounds after `N->infinity`; it does not
construct `q(N)` or prove the adaptive capacity limit.  Repackaging the same
family, its finite rows, or the Euler products is not a new trigger.  A
successor must prove the cofinal all-clock one-site theorem, the RH-371
run-envelope limit/negative, a genuine memory-correlation theorem, or another
source-backed edge.

RH-375 closes only the all-finite-clock universally safe one-site class.  Its
exact nonattained supremum is `B_infinity`; it is not a maximum over memory
tables, a growing-clock theorem, or the adaptive capacity limit.  The special
saturation proof depends on the square-clock support and cannot be repackaged
as a general cover-MWIS law.  A successor must address the RH-371 run
correlations, a genuine memory-dependent arithmetic theorem, a geometrically
selected measure, the blocked Ulam bridge, or another source-backed edge.

RH-376 closes only the shift-two signed interval-density boundary.  Its
common-endpoint identity and three unconditional terms reduce existence of
either density to ordinary shift-two Cesaro Chowla, but do not prove or
disprove that open statement.  The logarithmic input is used only after a
natural limit is assumed; it cannot be repackaged as unconditional natural
cancellation.  A successor must address the mixed-exponent hierarchy, its
two-envelope capacity combination, a genuine memory theorem, or another
source-backed edge.

Even `D_(4k)(R)->0` would transfer only named moment/budget laws. Root, rank,
spectral-submultiset, and canonical determinant identification remain
separate. RH-288 activates only after the complete direct prefix and both
analytic tails close in one physical determinant data type.

## 6. Historical RH-362 investigation

The original RH-362 physical investigation began read-only with:

```text
h_(sigma,n)       = actual modulus-complete Hardy-head moment
s_(k,n)           = deterministic graded counterloop moment
d_(sigma,k,n)     = h_(sigma,n)-s_(k,n)
2 <= n < 4k
```

Search for a cross-order identity, conservation law, contour/Fourier
formula, operator estimate, or other source-backed restriction on the actual
defect. Keep the unnormalized `D_(4k)`, RH-355 normalized `Delta_k^up`, and
coordinatewise relative matching distinct. Audit clock, order range,
uniformity, signs, data type, and loss ledger. If no actual theorem, rigorous
physical obstruction, or independent theorem edge exists, return
`NOT_TESTABLE` and do not create RH-362.

The 2026-08-04 RH-362 source lock returned `NOT_TESTABLE` at repository
`HEAD=9902699`: RH-342 fixes the actual-head and deterministic-shell types,
RH-355 fixes the exact unnormalized `D_(4k)(R)` leaf, and RH-303 supplies only
a fixed-order consequence of an already-open annular hypothesis. RH-287 and
RH-294 use slower or unspecified diagonal clocks without head transport.
RH-352--RH-354 remain selected/normalized actual results, while RH-340,
RH-342, RH-343, and RH-355 provide only information-class or absolute-
majorant negatives, explicitly not physical `D` behavior. No source pays the
common-clock all-order defect budget, and no physical obstruction or
independent admissible theorem edge was found. Retain the route coordinate
`actual_same_clock_unnormalized_head_transport_open` and do not create RH-362.
An independent adversarial proof audit reached the same `NOT_TESTABLE`
verdict: normalized-to-unnormalized promotion, selected-window-to-full-prefix
promotion, and absolute-majorant-to-signed-obstruction promotion all fail
without a new actual theorem.

The parallel alternative-route scan also found no reopening edge. RH-241's
`all_order_trace_envelope` and `coefficient_anchor` flags remain false; RH-300
has only an inactive annular `H^\infty/H^2` criterion. RH-287 and RH-294 use
rate-free or arbitrarily slow diagonal clocks and do not prove physical-head
transport. RH-334/RH-339/RH-344/RH-346/RH-348 supply exact typed `q` identities
only; they do not bound the aggregate `E_off` or the defect `d`. Thus the
typed `q/E_off` route is also `NOT_TESTABLE`, and the route coordinate remains
`actual_same_clock_unnormalized_head_transport_open`.

A repository-wide sweep of every ten-layer review from RH-241 through RH-361
found no overlooked active branch. The fixed-noise quotient/anchor reviews
RH-241--RH-271 lack a uniform noisy envelope/anchor realization; RH-281 and
RH-291 lack aggregate noisy-cloud/head transport; RH-301 and RH-311 retain
zero cross-branch completions; RH-321 is sharp only for synthetic spectral
realizability; RH-331 and RH-341 leave actual signed replacement open; and
RH-351/RH-361 end at the current signed-completion/head defect. The earlier
RH-82/RH-83 effective-rank object is not identified with the RH-284
modulus-complete spectral head. This exhausts the repository-backed candidate
branches without producing an RH-362 `GO`.

### 6.1 Post-synthesis consolidation and external-route audit

For route selection, retain RH-MVP2 as the single short corpus umbrella. It
must not replace or silently concatenate the 361 atomic sources. The
publication-scale four-volume expansion in section 1.1 is now complete and
improves exposition and provenance only; it does not change the mathematical
frontier, create a theorem edge, or activate RH-362.

A parallel post-synthesis theorem scan at
`HEAD=273c07b0ca58be600f18d41c7198570665b97549` returned `GO=0`:

- The operator route found no source-locked injection
  `J_sigma: W_k -> A_sigma`, no bound for
  `E_sigma=A_sigma J_sigma-J_sigma W_k`, and no common moving contour with
  controlled resolvents. Kato/Keller--Liverani stability concerns fixed
  isolated spectral clusters; trace-ideal continuity first requires a
  same-space Schatten defect; and Grushin/Feshbach theory first requires the
  enlarged problem to be constructed. None supplies the rank-growing physical
  bridge. The narrow executable diagnostic is to define `J_sigma` on one
  frozen first-alias clock and outward-certify `E_sigma` and both contour
  resolvent suprema. A finite pass would be feasibility evidence only.
- The complex-analytic route found that strict outer-circle Hardy control,
  Bergman compactness, Montel/Vitali, regularized Fredholm determinants, and
  Tauberian remainder theorems all require a uniform actual norm, fixed-order
  actual complement transport, positivity/monotonicity, or an explicit
  same-clock remainder that the corpus does not provide. RH-300 already gives
  the sharp inactive outer-circle criterion and an endpoint counterexample;
  RH-276 prevents raw Hilbert--Schmidt compactness; RH-294--RH-295 prevent a
  rate-free diagonal from being accelerated to the physical logarithmic
  clock. These tools restate the missing leaf rather than pay it.
- A cyclic affine-Gaussian candidate survives only as a research direction.
  For full-line affine Gaussian rows
  `Y_j=a_j X_(j-1)+b_j+beta_j Z_j`, their composition has total slope `A`,
  shift `B`, and variance `V`, and for `A!=1` its diagonal integral is exactly
  `int_R phi_(sqrt(V))((1-A)x-B) dx=1/abs(1-A)`; for `A=1` it
  diverges. The associated cyclic width is `sqrt(V)/abs(1-A)`, so raw
  forward variance growth alone does not obstruct a cyclic diagonal
  functional. However the full-line kernel has infinite Hilbert--Schmidt norm
  and this diagonal integral is not by itself an `L^2(R)` operator trace. It
  is the affine residual-determinant mechanism already underlying RH-9, not
  an identification with the physical compact trace. After compact
  truncation and row normalization, the path indicator decreases the
  full-line integral while the product of inverse row normalizers increases
  it; the full-line identity supplies no one-sided correction bound. The
  actual folded kernel on `[0,1]` still requires simultaneous control of all
  intermediate boundaries, nonlinear curvature, folding, parity/shell terms,
  and the physical frozen observation map. RH-333 does not refute such a
  cyclic bridge, while RH-334 explicitly leaves its probability-to-trace
  identification open.

Those three physical scans returned `NOT_TESTABLE` or `STOP_SCOPED`, not a
physical obstruction. A valid cyclic reopening must first
define a compact/folded/normalized cyclic reference in the RH-334 trace data
type and prove an all-leg observation/prefix/suffix upper bound on the physical
first-alias clock. Its first decisive correction-factor test is
`C_(sigma,k)=1+o((beta R)^(-2k))` on the complete `2k` signed path sum and
frozen basepoint window. A nonunit fixed-phase limit would support a rigorous
scoped negative; a positive result would only open the subsequent all-leg
curvature/Duhamel and stability-weight obligations. Until then keep
`actual_same_clock_unnormalized_head_transport_open`.

### 6.2 Independent trigger-5 activation on 2026-08-05

The later external-source lock changed the numbered decision without changing
the physical one. Frozen commits are:

```text
henon_prime_returns  c37d191672d30de49b2054be3a03cf2db068694f
dyna_zeta_map        7fd3a3fdd5a6a25827a0965345459baf4a47b816
```

Seven source/foundation hashes match. Independent proof audit returned `GO`
for the low-rank identity, marked-cycle determinant, locally finite formal
bouquet, zero-free Euler product, coefficient and logarithmic-derivative
laws, origin obstruction, Schatten/Fredholm regions, periodic branch, and
inverse-clock obstruction. The audit explicitly rejected promotion to a
Hasse--Weil factor, full `H_p` zeta, canonical physical determinant,
von-Mangoldt trace, Hilbert--Polya operator, Riemann-zero identification,
completed-zeta divisor equality, or RH.

The first arithmetic-dynamical blocker is now a canonical identification
theorem: one must turn the marked-point-dependent, one-cycle-per-prime bouquet
across distinct finite fields into an intrinsic global dynamics/operator
without prescribing the desired Euler weights. Until such a theorem exists,
Gate A remains false.

### 6.3 RH-366 independent source lock and route decision on 2026-08-06

The certified `henon_mobius_correlations` package was frozen at

```text
34490443f50cfe9af9ff93888e51e7e7e534a5a7
```

with the inherited local-survivor foundation locked to
`henon_weighted_zeta=ff44f961261349848c9f65ede6a031b7e155aca9` and the
cross-checking zeta source locked to
`dyna_zeta_map=7fd3a3fdd5a6a25827a0965345459baf4a47b816`.  Source-lock and
proof-audit agents independently returned `PASS`, with no files changed.
The exact package separates fixed-periodic orthogonality, Parry-almost-sure
orthogonality, the post-hoc Möbius-adapted point, the Parry covariance/variance
theorem, the conditional Chowla density, and the finite adaptive-capacity
algorithm and bracket.  Finite diagnostics remain scoped to their frozen
protocol and null model.

The primary route decision is `Route A=GO`, `Route B=STOP_SCOPED`.
The first Route-B mismatch is prior to Gate A: the exceptional point is
selected after reading the full Möbius sequence, and the measured quantities
are scalar orbit averages and Parry variances rather than a canonical
operator trace, determinant, or von-Mangoldt prime-power ledger. Gates A--E
remain false/open, and the physical coordinate remains
`actual_same_clock_unnormalized_head_transport_open`.

### 6.4 RH-367 source lock, overlap ledger, and route decision (2026-08-06)

At that historical stage, the only fresh candidate was the boundary-aligned
cyclic-Ulam structural package at
`cyclic_ulam_map=e7d21f646498d77e1c3213d1e4f35dc8466038ff`.  Its exact claims
are: the PCF two-band exchange; the `L^1` sign mode; for every partition with
the band boundary as a cell edge, the row-stochastic block form
`P=[[0,A],[B,0]]` and `Ps=-s`; and the crossing-cell projection defect
`4h theta(1-theta)`.  It explicitly does not prove a universal
`sqrt(sigma)` law, an isolated continuum resonance, or a strong-space
perturbation theorem.

The overlap audit is positive but narrow:

- RH-3 uses the same band-merging geometry to prove a continuum/Koopman
  parity eigenmode, periodograms, and (under a component-gap hypothesis) a
  Perron--Frobenius decomposition.  It does not prove the arbitrary
  finite-partition cell-overlap block theorem or the crossing-cell phase
  defect.
- RH-10 uses the same map for exact periodic counts, boundary crowding,
  noncommuting long-cycle/noise limits, and parity-renormalized determinants.
  It does not supply the aligned-versus-misaligned Ulam theorem or the local
  phase-leakage identity.
- RH-55 proves a midpoint--Ulam bridge and strong--weak contour transfer for a
  conditioned folded-Gaussian kernel.  It does not establish the PCF
  two-band finite-Ulam sign inheritance or its crossing-cell defect.

Thus the cyclic package is a distinct finite-dimensional theorem/diagnostic
edge after this ledger, not a rebranding of RH-3, RH-10, or RH-55.  Independent
source-lock and proof-audit checks returned `GO` narrowly, with 12/12 upstream
tests and no source changes.  The final RH-367 decision is
`Route A=GO`, `Route B=STOP_SCOPED`, with scope restricted to exact aligned
block/sign inheritance, the local crossing-cell identity, and the frozen
phase protocol.  The Route-B blocker is the absent common strong-space
projector/resolvent theorem; finite noisy slopes remain diagnostics.  Gates
A--E remain false/open and the physical coordinate is unchanged.

### 6.5 RH-368 source lock, parity-factor theorem, and route decision (2026-08-06)

RH-368 locks `dyna_zeta_map` at
`7fd3a3fdd5a6a25827a0965345459baf4a47b816`.  The source's PCF three-cell
matrix is `[[0,0,1],[0,0,1],[1,1,0]]`, and its binary factor
`A_{\{2\}}` has all positive positions in one parity class.  This language is
distinct and non-comparable by inclusion with RH-366's four-state
distance-two language.  The source also supplies the boundary-aware factor
zeta identity `(1+z)/(1-2z^2)`; RH-368 uses it only as a provenance anchor.

The exact finite capacity identity is

```text
K_N^(2) = max_r max(|-M_N+2P_r(N)|,|-M_N-2N_r(N)|).
```

Davenport's fixed frequency estimate at `1/2` supplies signed parity
cancellation, while the squarefree sieve supplies odd/even densities
`4/pi^2` and `2/pi^2`; therefore `K_N^(2)/N -> 4/pi^2`.  The independent
proof audit checked the parity formula against exhaustive words through
`N=12` and flagged the non-comparability boundary explicitly.  Route A is
`GO`; Route B is `STOP_SCOPED` at adaptive data type, before Gate A.  The
RH-366 distance-two capacity remains open, and no canonical operator, prime
trace, zeta-zero model, Hilbert--Polya construction, or RH implication is
claimed.

### 6.6 RH-369 source lock, Markov-family theorem, and route decision (2026-08-06)

RH-369 locks `henon_mobius_correlations` at
`34490443f50cfe9af9ff93888e51e7e7e534a5a7` and inherits only the certified
four-state graph, sign observable, Hénon conjugacy, Parry specialization, and
finite-state almost-sure proof template.  A repository-wide search confirms
that the family `P_t` is not present in the source; it is declared and proved
as a new derived family, never as a geometrically selected object.

For `q=1-t`, `0<t<1`, the independent source-lock and adversarial proof
audits verified exactly

```text
pi_t = (1,q,q,q^2)/(1+q)^2,
E_t e = -t/(2-t),
Var_t e = 4q/(2-t)^2,
P_t^2 F_t = -q F_t,
pi_t diag(F_t)P_tF_t = 0,
chi_(P_t)(lambda) = (lambda-1)(lambda+q)(lambda^2+q).
```

Thus the odd covariances vanish, the lag-`2k` covariance is `(-q)^k`, and
the fixed-parameter chain has nontrivial spectral radius `sqrt(q)<1`.
The RH-366 Chebyshev--Borel--Cantelli argument extends to every fixed
interior parameter and gives one `nu_t`-full set simultaneous for all
continuous observables.  The exact weighted-variance identity and the bound
`0<=V_(N,t)<=((2-t)/t)N` are unconditional; the `6/pi^2` density is retained
only under ordinary fixed-shift Chowla.

The audits also locked the failure boundaries: `t=0` is deterministic
periodic, `t=1` has zero raw variance, the mixing rate degenerates as
`t downarrow 0`, the normalized observable degenerates as `t uparrow 1`, and
no common full-measure set over uncountably many parameters is claimed.
Route A is `GO`; Route B is `STOP_SCOPED` at the externally selected symbolic
measure, before Gate A.  Gates A--E and the original physical coordinate are
unchanged.

### 6.7 RH-370 source lock, fold theorem, and route decision (2026-08-06)

RH-370 freezes `cyclic_ulam_map` at
`e7d21f646498d77e1c3213d1e4f35dc8466038ff`, with RH-367, RH-14, RH-52,
RH-55, and the RH-MVP2 four-volume verification as explicit source inputs.
The source audit has `9/9` matching hashes; the upstream cyclic-Ulam test
suite is `12/12`.

The proof audit accepts the finite statement only for mirror-compatible cells:
the observable and mass intertwiners, the annihilated mirror kernel, and the
characteristic factor `chi_full(z)=z^m chi_fold(z)` are exact finite algebra.
The `L^1` conditional-expectation argument is valid for fixed functions and
resolvents on compact subsets of `|z|>1`.  It does not surround `-1`.
The terminal formula and four scaling rows verify the deterministic jump
coefficient `0.4714757998... h^(-1/2)`, which blocks a uniform standard-BV
deterministic projector.  The audit rejects arbitrary aligned partitions,
zero-noise specialization of positive-noise schedules, continuum spectral
promotion, and every Gate claim.

The primary route decision is `Route A=GO`, `Route B=STOP_SCOPED`.  The first
Route-B blocker is the missing common strong-space projector/resolvent
theorem; the declared reopening is a fractional/tower-adapted space or a
different partition theorem.  RH-371 was the completed next edge at this
historical point; the remaining capacity-limit and strong-space routes led to
RH-372.

### 6.8 RH-371 source lock, eight-run theorem, and route decision (2026-08-06)

RH-371 freezes `henon_mobius_correlations` at
`34490443f50cfe9af9ff93888e51e7e7e534a5a7`, with RH-366, RH-370, and the
four-volume verification as explicit source inputs.  The source-lock and
proof-audit stations agree on `Route A=GO` narrowly and
`Route B=STOP_SCOPED`; neither changed a file.

The exact new edge is the all-prefix identity

```text
C_(sigma,k)(N) = #{odd n <= N-2(k-1): mu(n+2j)=sigma for 0<=j<k},
E_sigma(N) = #{n <= N: n=2 mod 4, mu(n)=sigma},
W_sigma(N) = E_sigma(N) + sum_(k=1)^8 (-1)^(k+1) C_(sigma,k)(N).
```

The modulo-9 run cutoff and the even-path isolation prove this identity for
every `N`; the two path extrema then give
`K_N=max(|-M_N+2W_+|,|-M_N-2W_-|)`.  Since `M_N=o(N)`, the exact remaining
question is convergence of the maximum of the two normalized alternating
eight-run combinations.  No repository theorem proves that convergence or
the existence/value of `lim K_N/N`.

The second edge is a scoped data-type obstruction.  The period-18 synthetic
words `u=+++++-++0--+-----0` and `v=+++++---0--+---++0` have identical
cyclic ordered pair ledgers at all lags but capacities `K_(18q)(u^q)=10q`
and `K_(18q)(v^q)=12q`.  Their open-prefix lag-2 ledgers differ, so the claim
is explicitly cyclic/periodic only; the words are not Möbius and do not show
that the actual Möbius limit fails.

Independent release audit: `9/9` source locks; local tests `5/5`; formula
versus independent DP `1000/1000`; cyclic pair cells `162/162`; repeated
capacity rows through `q=256`; endpoint `N=2^20`; individual archive `21`
publication files plus `9` external inputs with zero failures.  The PDF has
`5` pages, Ghostscript and text extraction pass, all pages were visually
checked, and the complete LaTeX log has no actionable warnings or errors.
The semantic PDF is byte-identical to `main.pdf`.  All Gates A--E remain
false/open.

### 6.9 RH-372 source lock, bounded transducer theorem, and route decision (2026-08-06)

RH-372 freezes the following source commits:

```text
henon_mobius_correlations  34490443f50cfe9af9ff93888e51e7e7e534a5a7
dyna_zeta_map              7fd3a3fdd5a6a25827a0965345459baf4a47b816
RH-366 release              6da1b94deaa865bbb297546f3de238433184772a
RH-368 release              ebcf29a4a2d248d8320067d85899b3b8039a7b12
RH-371 release              241b78a89ccbc0bad96d9ef20ee9256d61b4eaca
```

The source-lock station supplied nine exact file hashes, including the
finite-graph capacity implementation, the RH-366/RH-368 frozen artifacts,
the RH-371 run reduction, the four-volume verification, and the dyna-zeta
quadratic section.  The proof audit independently checked the phase convention,
the all-state/all-input safety quantifier, the one-site firewall, the
squarefree density constants, and the direction of the liminf lower bound.
Both agree on `Route A=GO` narrowly and `Route B=STOP_SCOPED`.

The release artifact reports `384` prefix witness rows at `N<=128`, endpoint
`N=2^16`, `3/3` safe one-site path instances, and the exhaustive q=2 one-state
audit `729` total / `16` safe-one-site / maximum coefficient `4`.  Local tests
pass `15/15`; the individual archive contains `21` publication files and `9`
external inputs with zero failures.  The PDF is five pages with `18` embedded
font rows; Ghostscript and text extraction pass, all five rendered pages pass
visual inspection, and the final LaTeX log has no actionable warnings,
undefined references, overfull boxes, or errors.  Gates A--E remain
false/open.

### 6.10 RH-373 source lock, phase-selector theorem, and route decision (2026-08-07)

RH-373 freezes the following source commits and releases:

```text
henon_mobius_correlations  34490443f50cfe9af9ff93888e51e7e7e534a5a7
RH-366 release              0396fab97bbe3348c8237f8734dec0e1893fd3bf
RH-371 release              241b78a89ccbc0bad96d9ef20ee9256d61b4eaca
RH-372 release              7a7b10b74722b520b145064923af8df6d4e2e73f
RH-MVP2 archive             c0aed13a34b8bbc53061aed23738660adcd3624c
```

The source-lock and proof-audit stations first tested the proposed
fractional/tower-adapted deterministic Ulam bridge.  The frozen
`cyclic_ulam_map` source at
`e7d21f646498d77e1c3213d1e4f35dc8466038ff` defines finite cell-overlap
matrices but no explicit common Banach norm or projector.  RH-370 supplies
only fixed-vector `L^1` convergence and resolvents on compact subsets of
`|z|>1`; its deterministic terminal spike makes the standard-BV projection
norm grow like `h^(-1/2)`.  RH-14 declares a tower/spike space without the
norm and Ulam projection estimates needed here, while RH-52 and RH-55 retain
positive-noise hypotheses.  Therefore the proposed deterministic
strong-space bridge is `STOP_SCOPED`, and the unspecified fractional norm is
`NOT_TESTABLE`.  The reopening input is an explicit fixed mesh-independent
space, a uniform projection or lift estimate, and a common contour isolating
`-1`.

The independent capacity audit found a different Route-A edge.  For every
fixed finite clock `q` and every phase set `I` with
`I cap (I+2)=emptyset`, the selector that outputs `+1` exactly on
`(n mod q) in I` and `mu(n)=+1` is universally distance-two safe.  Davenport
fixed-frequency cancellation, finite Fourier inversion, and squarefree
progression densities give the exact limiting correlation
`sum_(r in I) delta_(q,r)`.

For `q=180`, the explicit `80`-phase set has zero cyclic distance-two
conflicts.  An independent regeneration found `68` phases of weight `5/96`,
`12` of weight `1/24`, and no zero-weight phase, giving

```text
68*(5/96) + 12*(1/24) = 97/24,
liminf K_N/N >= 97/(24*pi^2).
```

The same audit independently rebuilt the literal two-state completion and
checked all `2*180*3^2=3240` state/phase/input-pair rows, the one-site
observable, `2048` exact prefix witnesses, and the endpoint `N=2^16`.  At
the endpoint the selector and transducer scores are both `26852`, the exact
capacity is `32320`, and the graph path passes.  These finite rows only
reproduce the certificate; the asymptotic theorem comes from the fixed-clock
arithmetic proof.

The route verdict is `Route A=GO` narrowly and `Route B=STOP_SCOPED`.  The
result improves the fixed lower floor by `1/(24*pi^2)` but proves neither the
ordinary RH-366 capacity limit nor an optimum over clocks or memory budgets.
It supplies no intrinsic operator, determinant, prime-power trace, zero
identification, or RH implication.  Gates A--E remain false/open.

### 6.11 RH-374 source lock, square-clock family theorem, and route decision (2026-08-07)

RH-374 freezes the following source commits and releases:

```text
henon_mobius_correlations  34490443f50cfe9af9ff93888e51e7e7e534a5a7
RH-366 release              0396fab97bbe3348c8237f8734dec0e1893fd3bf
RH-371 release              241b78a89ccbc0bad96d9ef20ee9256d61b4eaca
RH-372 release              7a7b10b74722b520b145064923af8df6d4e2e73f
RH-373 release              e46a0b0ef0e459fc26711c379ce8c1b68deb9c58
RH-MVP2 archive             c0aed13a34b8bbc53061aed23738660adcd3624c
```

The source-lock station replaced a proposed larger finite scan with the exact
square-clock family `q_y=4 product_(i<=y)p_i^2`.  CRT gives the fixed-clock AP
densities and exact positive-run counts.  The proof audit independently
checked the cyclic seams, the two copies of the odd word inside `q_y`, the
weighted-MWIS optimum `2A_y+O_y`, the prime-adjoining deletion argument, and
the fixed-`y`-before-`N` quantifier.  The critical endpoint correction is
frozen: the second-difference formula holds only for `1<=j<=7`, while
`R_8=P_yE_8`; no `E_10` is used.

Independent exact arithmetic reproduces

```text
y=1: q=36,      A=8,       O=0,     selected=16,      pi^2 B=4
y=2: q=900,     A=192,     O=8,     selected=392,     pi^2 B=49/12
y=3: q=44100,   A=9216,    O=544,   selected=18976,   pi^2 B=593/144
y=4: q=5336100, A=1105920, O=72440, selected=2284280, pi^2 B=57107/13824.
```

For `q=900`, all `8100` universal-safety rows pass, the `392` selected phases
have zero cyclic distance-two conflicts, and the finite endpoint `N=2^16`
has selector score `27174` below exact capacity `32320`.  These rows reproduce
the certificate only.  The asymptotic theorem follows from the fixed-clock AP
proof and the scalar supremum argument; the stored decimal Euler enclosure is
explicitly diagnostic rather than theorem evidence.

The route verdict is `Route A=GO` and `Route B=STOP_SCOPED`.  RH-374 closes
the declared square-clock one-site family but not the all-clock one-site
supremum, arbitrary-memory transducers, the RH-371 run envelope, or the
adaptive RH-366 capacity limit.  No operator, determinant, prime-power trace,
zero identification, Hilbert--Polya construction, or RH result is claimed.
Gates A--E remain false/open.

### 6.12 RH-375 source lock, all-clock supremum, and route decision (2026-08-07)

RH-375 freezes the following source commits and releases:

```text
henon_mobius_correlations  34490443f50cfe9af9ff93888e51e7e7e534a5a7
RH-366 release              0396fab97bbe3348c8237f8734dec0e1893fd3bf
RH-371 release              241b78a89ccbc0bad96d9ef20ee9256d61b4eaca
RH-372 release              7a7b10b74722b520b145064923af8df6d4e2e73f
RH-373 release              e46a0b0ef0e459fc26711c379ce8c1b68deb9c58
RH-374 release              2bb3baa6a09491c2d679d10c0dbcd39587d1f831
RH-MVP2 archive             c0aed13a34b8bbc53061aed23738660adcd3624c
```

Two independent audits verified the arbitrary-clock density formula, the
active-set MWIS reduction, both orientations, `q=1,2` self-loops, odd clocks,
high prime powers, and density aggregation under `q|Q`.  They also checked the
critical saturation step adversarially: a general cyclic cover need not scale
its MWIS, but the square-clock support does because the forced `4`-zero and
`9`-zero phases split the two parity components.  This proves cofinality and
strict finite nonattainment without any bounded-scan extrapolation.

The exact artifact exhausts `4680` one-site tables (`249` universally safe),
`2046` phase subsets, eight divisibility audits with `58` density fibers, and
ten cofinal lifts.  The largest lift is `343|308700`, with `193536` positive
phases, MWIS cardinality `132832`, and `pi^2F=593/144`.  The scan through
`q=256` is explicitly reproduction-only; its maximum `97/24` occurs at
`q=180` and is not theorem evidence.

The route verdict is `Route A=GO` and `Route B=STOP_SCOPED`.  RH-375 closes
the all-finite-clock universally safe one-site class exactly at the
nonattained supremum `B_infinity`.  It does not close memory-dependent
factors, a growing-clock regime, the RH-371 run envelope, or the adaptive
capacity limit.  At the RH-375 endpoint, the next independently audited
Route-A candidate was the RH-376 two-site run/shift-two Chowla-hardness
theorem, now integrated in Section 6.13.  The geometrically selected
non-Parry measure and deterministic strong-space Ulam routes remain
`STOP_SCOPED`.  No Gate A--E conclusion is changed.

### 6.13 RH-376 source lock, shift-two boundary, and route decision (2026-08-07)

RH-376 freezes thirteen repository files and five Git releases:

```text
RH-371 release              241b78a89ccbc0bad96d9ef20ee9256d61b4eaca
RH-374 release              2bb3baa6a09491c2d679d10c0dbcd39587d1f831
RH-375 release              071fed1b2a5d8488b9d2e35a99a753953b233584
TPC-193 release             14d7a1dfd82b0575b43a65c8254fce3cf53acda5
RH-MVP2 archive             c0aed13a34b8bbc53061aed23738660adcd3624c
```

Independent proof and numerical audits reconstructed the common-endpoint
identity, checked that all even starts vanish, and verified the squarefree
normalization including the `p=2` local factor.  They also checked the
cutoff order in the one-sign terms, the exact Teravainen--Walker forms
`m+1,m+3` with determinant two, the bounded reindexing error, and the
one-way Abel implication.  No logarithmic-to-natural promotion occurs.

The exact executable audit checks `1048574` pointwise identities,
`1048576` cumulative prefixes, `524287` even starts, and `1024` RH-371
endpoints (`2048` sign cells).  All checks pass.  The route verdict is
`Route A=GO` and `Route B=STOP_SCOPED`.  At that historical stage, the next
Route-A candidate was the independently audited RH-377 mixed-exponent run
hierarchy and two-envelope
capacity reduction.  Its `466 -> 13` statement must remain a formal
block-sum rank calculation, and its stationary ternary witness must not be
called a Möbius counterexample.  The first unresolved arithmetic object is
the convergence of `(U_N+|V_N|)/N`; no Gate A--E conclusion changes.

### 6.14 RH-377 source lock, mixed hierarchy, and route decision (2026-08-07)

RH-377 freezes thirteen repository files and four Git releases:

```text
RH-371 release              241b78a89ccbc0bad96d9ef20ee9256d61b4eaca
RH-374 release              2bb3baa6a09491c2d679d10c0dbcd39587d1f831
RH-376 release              0cf6179084bc8151318bb8f0955e529c12c0661a
RH-MVP2 archive             c0aed13a34b8bbc53061aed23738660adcd3624c
```

Independent proof and numerical audits reconstructed the native endpoints,
the odd-prime `e_k` products and external odd-start factor `1/2`, the fixed
cutoff order in `H_(k,1)`, the sixteen-to-thirteen equivalence, and the
formal-rank firewall.  They also checked the exact `P,Q,U,V` decomposition,
the absolute-value residual bound, the two-envelope equivalence, and the
arbitrary-distinct-time stationary-chain proof.  The chain's odd-lattice
normalization is compared consistently as `2/3` versus `e_1=8/pi^2`, or
equivalently `1/3` versus `Delta_1=4/pi^2` in the original `N`
normalization.

The executable audit checks `19680` Boolean cases, the exact `466 -> 13`
rank and kernel, `1048548` native window updates, `4194304` cumulative
signed identities, and `262144` path/decomposition/residual prefixes.  The
synthetic certificate checks `27` transitions, `9` pair-stationarity cells,
`502` raw moments, `502` square-only moments, and `1793` one-sign masked
moments.  All checks pass.

The route verdict is `Route A=GO` and `Route B=STOP_SCOPED`.  At that
historical stage, the next independently source-locked and adversarially
audited Route-A candidate was
RH-378: finite-window safety/moment expansion, complete lag-two safe-table
classification, and two fixed online capacity-orientation transducers.  Its
lag-two hard class still requires RH-376 shift-two Cesaro Chowla, and its
full capacity asymptotics still require the RH-377 envelope.  No Gate A--E
conclusion changes.

### 6.15 RH-378 source lock, safe memory, and route decision (2026-08-07)

RH-378 freezes thirty-three repository files and eight Git releases:

```text
RH-366 release              0396fab97bbe3348c8237f8734dec0e1893fd3bf
RH-371 release              241b78a89ccbc0bad96d9ef20ee9256d61b4eaca
RH-372 release              7a7b10b74722b520b145064923af8df6d4e2e73f
RH-374 release              2bb3baa6a09491c2d679d10c0dbcd39587d1f831
RH-375 release              071fed1b2a5d8488b9d2e35a99a753953b233584
RH-376 release              0cf6179084bc8151318bb8f0955e529c12c0661a
RH-377 release              3c6e5658f4147891d15dac18d303a22a46d6e289
RH-MVP2 archive             c0aed13a34b8bbc53061aed23738660adcd3624c
```

Independent proof and numerical audits reconstructed the compatible-block
test, the current-zero interpolation basis, all `512` lag-two tables, the
`13` safe relations, the rank-five coefficient matrix, and the exact
six-term common-endpoint ledger.  They independently checked the separation
between seven unconditional tables and six RH-376 shift-two-Chowla-hard
tables, including the conditional `B_infinity` comparison.

The executable audit checks two `243`-row graph lifts, `72` Mealy safety
rows, `88572` ternary words through length ten, and the exact causal-policy
tree counts `8,256,65536,0`.  At the Möbius endpoint `2^20` it checks
`2097152` orientation-extremum equalities, `1048576` all-prefix lag-ledger
identities, and `2097152` recursive/window equalities.  The parity-window
certificate checks all `512` assignments and records the exact `17`-site
unrestricted counterexample.  All checks pass.

The route verdict is `Route A=GO` and `Route B=STOP_SCOPED`.  At that
historical stage, independent source and proof locks established the next
phase-dependent,
phasewise-`c_11=0` lag-two edge: an exact three-state cyclic max-plus
optimizer, a strict same-clock gain at `q=36`, and the cofinal identity
`sup_(q finite)G(q)=B_infinity`.  RH-379 was therefore activated.  The lock
does not prove finite-clock attainment or nonattainment.  Unrestricted memory
still requires phase-weighted shift-two or higher mixed Möbius cancellation.
No Gate A--E conclusion changes.

### 6.16 RH-379 source lock, phasewise memory supremum, and route decision (2026-08-07)

RH-379 freezes twenty-eight released predecessor files and five Git releases;
mutable root policy and handoff files are intentionally outside its
publication source lock:

```text
RH-374 release              2bb3baa6a09491c2d679d10c0dbcd39587d1f831
RH-375 release              071fed1b2a5d8488b9d2e35a99a753953b233584
RH-376 release              0cf6179084bc8151318bb8f0955e529c12c0661a
RH-378 release              08574b1bab1b9f549d4c07df97bb548d40aae51f
RH-MVP2 archive             c0aed13a34b8bbc53061aed23738660adcd3624c
```

Independent source, proof, numerical, manuscript, schema, and release audits
reconstructed the phasewise fixed-AP cancellation, all `512` truth tables,
the exact `192`-table `c_11=0` class, the subset-first canonical reduction,
and the three-state cyclic max-plus DP including the `q=1,2` self-loops.
They checked the squarefree and squarefree-pair local factors, input
reflection, the exact `q=36` gain, the square-clock run recurrence and
vanishing correction, and the retained-one-site plus prime-square-tail proof
of the arbitrary-fixed-clock upper bound.

The final executable suite has `15/15` tests.  It checks all `262144`
ordered reflection-neighbor pairs, ten exact `q|720` density-aggregation
fixtures, twelve density normalizations, six small clocks, four larger exact
clock fixtures, three square-clock run rows, and four cofinal lift/decompose
certificates.  Directed interval arithmetic has exact-Fraction containment
tests and an explicit fail-closed ambiguous comparison.  Full result
regeneration is byte-identical, all twenty-eight source digests match, and
the recursive Draft 2020-12 schema validates with zero errors.

The route verdict is `Route A=GO` and `Route B=STOP_SCOPED`.  At that
historical stage, two independent post-RH-379 audits established the next
RH-380 theorem edge: an exact recurrence
for even-run counts, strict monotonicity of `G(q_y)`, special same-support
memory saturation, and therefore finite-clock nonattainment of `B_infinity`
inside the same phasewise-`c_11=0` class.  Active nonzero `c_11(r)` remains
`STOP_SCOPED` at phase-weighted shift-two Cesaro cancellation.  No Gate A--E
conclusion changes.

### 6.17 RH-380 source lock, finite-clock nonattainment, and route decision (2026-08-07)

RH-380 freezes twenty-four immutable predecessor files and four Git releases;
mutable root policy and handoff files are intentionally excluded:

```text
RH-374 release              2bb3baa6a09491c2d679d10c0dbcd39587d1f831
RH-375 release              071fed1b2a5d8488b9d2e35a99a753953b233584
RH-379 release              9ae9802ed17529ef4adfb81d7e2158d47c3c8d22
RH-MVP2 archive             c0aed13a34b8bbc53061aed23738660adcd3624c
```

Independent proof and numerical audits reconstructed the deletion rule for
every run length `1<=ell<=8`, the exact even-run recurrence, all three frozen
increment anchors, and the persistent `R_8>=1` strict term.  They separately
checked the same-support theorem by residuewise `delta/theta` scaling,
cause-specific mod-4/mod-9 separators, and a generic three-state cyclic
max-plus dynamic program.  The `Q=180` new-prime case is retained as a
strict negative control to any general-multiple interpretation.

The final executable suite has `15/15` tests.  It checks three direct run
rows, twenty-four deletion fixtures, four prime-adjoining transitions, nine
same-support refinements, `10152` fine-residue density identities, `121428`
exact max-plus comparisons, and seven arbitrary-clock/lcm-gap fixtures.
Result regeneration is byte-identical, the recursively closed Draft 2020-12
schema validates with zero errors, all twenty-four source digests match both
the live files and the declared release blobs, and the single-paper archive
contains twenty-eight publication members plus twenty-four external inputs
with zero failures.

The route verdict is `Route A=GO` and `Route B=STOP_SCOPED`.  At that
historical stage, two independent post-RH-380 audits proved the next RH-381
theorem edge: with
`T_y=sum_(p>p_y)(p^2-1)^(-1)`, the normalized gap has leading constant
`2X_infinity/pi^2` and a fully explicit quadratic remainder bounded by
`342T_y^2/pi^2`.  This successor uses only Euler-product tails and the exact
RH-380 increment; it needs no PNT.  Active nonzero `c_11(r)` remains
`STOP_SCOPED` at phase-weighted shift-two Cesaro cancellation, and the
RH-377 adaptive envelope remains open.  No Gate A--E conclusion changes.

### 6.18 RH-381 source lock, prime-square-tail rate, and route decision (2026-08-07)

RH-381 is published at
`b6a6355b3390f3d00091a02cf77845b4f68a4a22`.  It freezes twenty-five
immutable predecessor files and four Git releases; mutable root policy and
handoff files are intentionally excluded:

```text
RH-374 release              2bb3baa6a09491c2d679d10c0dbcd39587d1f831
RH-379 release              9ae9802ed17529ef4adfb81d7e2158d47c3c8d22
RH-380 release              dd94b9cfebdbf5df92084ba870b10d3a4d432bee
RH-MVP2 archive             c0aed13a34b8bbc53061aed23738660adcd3624c
```

Independent proof and numerical audits reconstructed the Euler-ratio form of
`X_j`, the positive `X_infinity` anchor, the `170` factorwise ledger, the
exact `H_(j+1)` tail product, the `M_j/A_j` site-count bound, both tail-sum
identities, and the finite-telescope-to-cofinal-limit argument.  They also
found and repaired two default-precision `Decimal` leaks before freezing the
independently regenerated `6851`-byte interval payload.  Float/Boolean
constant aliases, non-finite JSON, duplicate source-lock rows, and
group/commit rebinding now fail closed.

The final executable suite has `20/20` tests.  It checks six exact run/Euler
rows, four exact finite tail-identity rows, six outward interval rows at
precision `60`, `9592` primes through `100000`, exact source-object
regeneration, optimized-mode execution, schema closure, and adversarial
archive mutations.  Result regeneration is byte-identical, all twenty-five
source files match their declared release blobs, and the single-paper archive
contains twenty-eight publication members plus twenty-five external inputs
with zero failures.

The route verdict is `Route A=GO` and `Route B=STOP_SCOPED`.  At that
historical stage, independent post-RH-381 audits identified the candidate
later published as RH-382: a two-scale
second-order expansion in `T_y^2` and
`S_y=sum_(p>p_y)(p^2-1)^(-2)` with a uniform cubic remainder.  It must retain
the signed `S_y` channel, the terminal length-eight contribution, and the
fixed-clock-first scope.  Active nonzero `c_11(r)` remains `STOP_SCOPED` at
phase-weighted shift-two Cesaro cancellation, and the RH-377 adaptive
envelope remains open.  No Gate A--E conclusion changes.

### 6.19 RH-382 source lock, two-scale expansion, and route decision (2026-08-07)

RH-382 is published at
`32afe96176ac00f4f261cf7097e0342a5c5194f1`.  It freezes thirty-three
immutable predecessor files and five Git releases; mutable root policy and
handoff files are intentionally excluded:

```text
RH-374 release              2bb3baa6a09491c2d679d10c0dbcd39587d1f831
RH-379 release              9ae9802ed17529ef4adfb81d7e2158d47c3c8d22
RH-380 release              dd94b9cfebdbf5df92084ba870b10d3a4d432bee
RH-381 release              b6a6355b3390f3d00091a02cf77845b4f68a4a22
RH-MVP2 archive             c0aed13a34b8bbc53061aed23738660adcd3624c
```

The group sizes are `7/8/8/8/2`, and the aggregate source digest is
`7b62b7e77ad313a52a07851e700aff197c2cc4bc3d910c6a464cd3cec0b55cb6`.
Independent proof and numerical audits reconstructed the Euler-ratio
Bonferroni bounds, the `931/4` numerator ledger, the `63` memory ledger, the
two exact quadratic tail identities, the `254/3` memory budget, and the
combined `3301/6` cubic budget.  They also separately checked the terminal
`R_8=P_yE_8`, the licensed `E_9=0`, and the absence of `E_10`.

The final executable suite has `22/22` tests.  It checks twenty-four finite
product rows, four Bonferroni rows, four quadratic/cubic telescope rows, four
finite endpoint-gap rows, optimized Python, ambient Decimal contexts, strict
JSON/schema behavior, exact source-object regeneration, and adversarial
archive mutations.  The exact certificate is `22543` canonical bytes with
SHA-256
`5fe227102a0a88307b5788f55d61bbbe07a17e5158aca11cfbbc79ec9e0cb624`.
The single-paper archive contains twenty-nine publication members plus
thirty-three external inputs with zero failures.

The independent RH-383 symbolic scout compared three exact gap channels on
`67/67` finite tails, `1084/1084` endpoint partition coefficients,
`144/144` increment-channel coefficients, `1151/1151` all-order `m=2`
cancellations, and `804/804` arbitrary-order remainder rows for
`1<=D<=12`; all `20/20` sign, denominator, terminal, and low-order mutations
were rejected.  These rows are a reproduction and adversarial layer, not the
proof of the infinite identities.

The route verdict was `Route A=GO` and `Route B=STOP_SCOPED`.  At that
historical stage, independent post-RH-382 source, proof, and symbolic audits
established the candidate later published as RH-383 in Section 6.20: an exact
Euler-tail cluster/exponential normal form in all power sums
`P_r(y)=sum_(p>p_y)(p^2-1)^(-r)`, with a finite partition coefficient
algorithm, exact all-order `m=2` cancellation, a new cubic block, and a
uniform arbitrary-order truncation bound.  The first two homogeneous layers
reproduce RH-381 and RH-382 exactly.  Active nonzero `c_11(r)` remains
`STOP_SCOPED` at phase-weighted shift-two Cesaro cancellation, and the RH-377
adaptive envelope remains open.  No Gate A--E conclusion changes.

### 6.20 RH-383 source lock, partition normal form, and route decision (2026-08-08)

RH-383 is published at
`bea5c88ca4ae9ca75511af42296ed099c1d6b11a`.  It freezes forty-one
immutable predecessor files and six Git releases; mutable root policy and
handoff files are intentionally excluded:

```text
RH-374 release              2bb3baa6a09491c2d679d10c0dbcd39587d1f831
RH-379 release              9ae9802ed17529ef4adfb81d7e2158d47c3c8d22
RH-380 release              dd94b9cfebdbf5df92084ba870b10d3a4d432bee
RH-381 release              b6a6355b3390f3d00091a02cf77845b4f68a4a22
RH-382 release              32afe96176ac00f4f261cf7097e0342a5c5194f1
RH-MVP2 archive             c0aed13a34b8bbc53061aed23738660adcd3624c
```

The group sizes are `7/8/8/8/8/2`, and the aggregate source digest is
`492100fe3b6b823a39b58cec25b0dcddf6d52c02bd1941f0978611f01a2b8db9`.
Independent proof, symbolic, numerical, integrity, and release audits
reconstructed the endpoint `C/W` identity, the partition and ordered-
increment compilers, the partition-length sign, the strict successor tail,
all-order `m=2` cancellation, the low-order and cubic blocks, and the exact
`92/3` majorant.

The final executable suite has `25/25` tests.  It freezes `67` endpoint
rows, `864` A/F rows, `432` Q-labelled rows, `1084` gamma-labelled rows,
`144` channel comparisons, `33` low-order bundles, the cubic and terminal
ledgers, `1151` labelled `m=2` checks, `804` remainder rows, and `20/20`
genuine formula/interface mutations.  The repeated labels are disclosed as
bookkeeping copies rather than distinct theorems.  The exact certificate is
`12245` canonical bytes with SHA-256
`9e2742fcdb2f626909eeb528c5081c9ace5414a1e6466c15b8b6800f427b6f16`.
The single-paper archive contains twenty-nine publication members plus
forty-one external inputs with zero failures.

The route verdict is `Route A=GO` and `Route B=STOP_SCOPED`.  RH-383 proves
the exact absolutely convergent Euler-tail endpoint/partition normal form,
all-order disappearance of the `m=2` channel, a new cubic layer, and the
uniform arbitrary-order remainder inside the fixed phasewise-`c_11=0`
class.  It does not use PNT or provide a `p_y` scale theorem.

At that historical stage, independent post-RH-383 source and proof audits
gave `GO` to the candidate later published as RH-384 in Section 6.21.  Its
repository PNT source is RH-2,
release `836426546db31e2737e877182848c538ed4cd436`, with frozen hashes

```text
main.tex
5f2538e648c2ed850b94a03c072a3526f31bcc0c70c90639f65601507f52e532

references.bib
bd86702192cd4bc6d1c2975c7da4b305541e0c5943f13c5edf044686f0faf2ab
```

and Montgomery--Vaughan DOI `10.1017/CBO9780511618314`.  RH-368/RH-371
record Möbius consequences of PNT but are not the source for the needed
prime-counting asymptotic.  Abel summation gives, for each fixed `r>=1`,

```text
P_r(y)~1/[(2r-1)p_y^(2r-1)log p_y].
```

Combining this scale dictionary with RH-382 gives the five normalized gap
limits in the RH-384 contract and proves that `S_y` lies strictly between
`T_y^2` and `T_y^3`.  A precision-80 outward computation certifies
`1.5463476716710499204<=Y_infinity-2m_infinity<=1.5484488989771761113`,
so the twice-subtracted coefficient is positive.  At that historical stage
this remained a candidate; its completed manuscript and release audits are
recorded in Section 6.21.  Active nonzero `c_11(r)` and the RH-377 adaptive envelope
remain open; no Gate A--E conclusion changes.

### 6.21 RH-384 source lock, prime-tail scales, and route decision (2026-08-08)

RH-384 is published at
`386b66a55c9263353c7d407fd712be7e6279f1e6`.  It freezes fifty-one
immutable predecessor files and eight Git releases; mutable root policy and
handoff files are intentionally excluded:

```text
RH-374 release              2bb3baa6a09491c2d679d10c0dbcd39587d1f831
RH-379 release              9ae9802ed17529ef4adfb81d7e2158d47c3c8d22
RH-380 release              dd94b9cfebdbf5df92084ba870b10d3a4d432bee
RH-381 release              b6a6355b3390f3d00091a02cf77845b4f68a4a22
RH-382 release              32afe96176ac00f4f261cf7097e0342a5c5194f1
RH-383 release              bea5c88ca4ae9ca75511af42296ed099c1d6b11a
RH-MVP2 archive             c0aed13a34b8bbc53061aed23738660adcd3624c
RH-2 PNT release            836426546db31e2737e877182848c538ed4cd436
```

The group sizes are `7/8/8/8/8/8/2/2`, and the aggregate source digest is
`90434e0468ecc062cb522da096a267748725b5dca8e59c642bb7711f45a3e0e4`.
The RH-2 source locks Montgomery--Vaughan's prime number theorem provenance;
the exact strict-endpoint Abel identity and its negative boundary are proved
inside RH-384 rather than inferred from finite rows.

The final executable suite has `20/20` tests.  The exact certificate contains
eight fixed-`r` rows, sixty-six fixed-partition rows through degree eight,
forty-eight strict-successor rows, five scale ledgers, five normalized-gap
ledgers, ten precision-80 numerical rows, and twenty genuine mutations.  The
exact certificate is `48689` canonical bytes with SHA-256
`01c91e57a01de9841f282327ab2f6e1a9368e136393ddab7a2cfe6b019a519c8`.
The inclusive/current-endpoint variants are explicitly interface checks,
not false claims that the leading PNT asymptotic changes.

The interval code traps hostile Decimal contexts, rounds each upper tail
loss before forming a lower product, and validates exact-Fraction
containment.  Official Draft 2020-12 metaschema and instance validation pass.
The single-paper archive contains twenty-nine publication members plus
fifty-one external inputs with zero failures.

The route verdict is `Route A=GO` and `Route B=STOP_SCOPED`.  RH-384 proves
the fixed-`r` and fixed-partition prime-tail scale dictionary, the strict
placement `T_y^3=o(S_y)=o(T_y^2)`, the five normalized gap limits, and the
positive twice-subtracted coefficient.  It supplies no effective PNT rate,
uniform growing-parameter theorem, active phasewise correlation, growing
clock, adaptive-capacity result, or Gate A--E conclusion.  No RH-385 is
assigned merely by continuing the Euler-tail expansion.

### 6.22 Post-RH-384 breadth-first audit and RH-385 contract (2026-08-08)

The first synthesis check is a direct corollary, not a new paper.  Put

```text
R_y=B_infinity-G(q_y)-A T_y-B T_y^2-C S_y.
```

The RH-383 cubic compiler and the RH-384 scale dictionary give

```text
R_y/T_y^3 -> gamma_(1,1,1)/pi^2,
[R_y-gamma_(1,1,1)T_y^3/pi^2]/(T_y S_y)
 -> gamma_(2,1)/pi^2.
```

Directed evaluations certify

```text
2.2754488766457144244 <= gamma_(1,1,1)
                      <= 2.2761510512327535499,
11.9522528185973202595 <= gamma_(2,1)
                       <= 11.9588363283136544645.
```

More generally, the fixed-cell ordering follows mechanically from the
already published partition compiler and PNT scale dictionary.  These facts
pay no new estimate, uniformity, or source budget, so the primary records them
as corollaries and does not assign them RH-385.

The genuinely new edge is a restricted growing-clock theorem.  For fixed
`B>0`, let `F_q` be the RH-379 universally safe, phasewise-`c_11=0`,
`q`-periodic lag-two families and define

```text
S_N(q,f)=N^(-1)sum_(n<=N)mu(n)
           f_(n mod q)(mu_0(n-2),mu(n)),
L_q(f)=sum_(r mod q)[c_02(r)delta_(q,r)+c_22(r)theta_(q,r)].
```

Here `mu_0(m)=mu(m)` for `m>=1` and is zero for `m<=0`.  Independent proof
and numerical audits establish

```text
sup_(1<=q<=floor((log N)^B), f in F_q)
 abs(S_N(q,f)-L_q(f)) ->0.
```

For any integer cutoff `P>=2`, set

```text
M_P=(product_(p<=P)p)^2,
Q=lcm(q,M_P),
tau_P=sum_(p>P)p^(-2),
D_*(N)=max_(X in {N,N-2}) sup_alpha
       abs(sum_(n<=X)mu(n)exp(2pi i alpha n)).
```

The proof-grade ledger is

```text
abs(S_N(q,f)-L_q(f))
 <=4sqrt(Q)D_*(N)/N+13tau_P+6Q/N+4/N.
```

The three Fourier channels cost respectively `sqrt(Q)`, `sqrt(Q)`, and
`2sqrt(Q)`; the last factor is forced by legal tables with `abs(c_21)=2`.
Choosing `P=floor(sqrt(log log N))`, eventually at least two, gives
`M_P=(log N)^(o(1))`.  RH-366's uniform-in-frequency Davenport estimate
then closes the Fourier term for any fixed exponent `A>B/2`.

With

```text
G_N(q)=max_(f in F_q)abs(S_N(q,f)),
G(q)=max_(f in F_q)abs(L_q(f)),
```

the max lemma and RH-379 imply

```text
sup_(q<=floor((log N)^B))abs(G_N(q)-G(q)) ->0,
max_(q<=floor((log N)^B))G_N(q) -> B_infinity.
```

The square clocks also give an explicit diagonal witness after the admissible
set is nonempty.  If
`y_B(N)=max{y:q_y<=floor((log N)^B)}`, then `y_B(N)->infinity` and the
certified positive optimizer at `q_(y_B(N))` has score tending to
`B_infinity`.

The core theorem inputs are RH-366 release
`0396fab97bbe3348c8237f8734dec0e1893fd3bf` and RH-379 release
`9ae9802ed17529ef4adfb81d7e2158d47c3c8d22`, with main-source hashes

```text
RH-366 main.tex
7df165bd63d43f52dc217dea6691d231d8e40c00c148ab7e1aa4abcac55060fb

RH-379 main.tex
c5d97a227398a4f1d46a39fdec73ffb86aeb9bfc0f16296be7023b187b497090
```

RH-375 and RH-378 remain the squarefree-density and six-monomial interface
inputs.  The primary route verdict was `Route A=GO`; the paper number RH-385
was assigned to this polylogarithmic-clock uniformization theorem.  Its full
artifact, manuscript, integrity, and release gates later passed in Section
6.23.  Route B remains
`STOP_SCOPED`.  Polynomial clocks such as `q=N^epsilon` are unsupported
because a fixed log-power Davenport saving cannot pay their Fourier mass.
Active `c_11` still meets ordinary shift-two Chowla already at `q=1`, and the
theorem supplies no upper bound for arbitrary adaptive words and hence no
limit for `K_N/N`.  It also supplies no effective finite threshold,
projectively compatible infinite selector, intrinsic operator, trace, zero
model, or Gate A--E result.

### 6.23 RH-385 release, polylogarithmic clocks, and route decision (2026-08-08)

RH-385 is published locally at
`4fdb628bd624145082553e0a2ea57b5755ec571d`.  It freezes sixty-seven
immutable inputs in groups `51/8/8`: the inherited RH-384 closure, the
standard RH-384 release group, and the standard RH-366 theorem group.  Every
live file equals its declared release blob; mutable root policy and handoff
files are excluded.  The aggregate digest is
`14a401e81d5d1868a8b3148478ca26f8975d0bde08b0a0117d4808571a2c5d79`.

The exact theorem is the fixed-`B` triangular-array convergence in Section
3.24, together with its all-finite `4/13/6/4` bound, uniform transfer to
restricted optimizers, maximum limit `B_infinity`, and nonempty square-clock
diagonal.  The proof source-locks RH-366 release
`0396fab97bbe3348c8237f8734dec0e1893fd3bf` for uniform-frequency Davenport
cancellation and RH-379 release
`9ae9802ed17529ef4adfb81d7e2158d47c3c8d22` for the fixed-clock phasewise
class and exact supremum.

The executable package checks `512` truth tables, all `4608` interpolation
values, `192` phasewise-`c_11=0` tables, and `24` coefficient vectors, each
of multiplicity eight.  It freezes coefficient maxima `l1=3` and squared
`l2=5`, the cutoff periods `4,36,900,44100`, coprime and noncoprime LCM
fixtures, normalized-DFT costs `1/1/2`, square-channel means, tail/padding
ledgers, small-clock max-plus comparisons, and `24/24` genuine rejected
mutations.  The canonical certificate is `472145` bytes with SHA-256
`3100168ed679a02c2d97496a2457ff512c2327764ca884b248ad312a6af8eea8`.

The final suite passes `27/27`.  Exact result/schema regeneration, optimized
Python, strict finite JSON and exact types, official Draft 2020-12 schema,
sealed-digest rebinding, source identity, and archive mutations all pass or
fail closed as declared.  The individual archive has `29` publication
members and `67` external inputs with zero failures.  The outer replay stays
at `4` volumes, `73` members, `1548` dependency hashes, `8` result hashes,
`361` numbered sources, and zero failures.

The two publication PDFs are byte-identical.  The final PDF has `8` A4 pages,
`385944` bytes, and `24` embedded, subsetted, Unicode-mapped font rows.
Ghostscript, text extraction, complete LaTeX/BibTeX scans, and all `8/8`
rendered pages pass.  Independent proof and numerical release audits report
zero blocker and zero minor.

The route verdict is `Route A=GO` and `Route B=STOP_SCOPED`.  RH-385 pays a
new restricted limit-exchange budget, but it proves no polynomial or
unrestricted clock theorem, varying-`B` law, active phasewise-`c_11`
cancellation, adaptive-capacity limit, effective threshold, projective
selector, intrinsic operator, prime-power trace, zero model, or Gate A--E
conclusion.

### 6.24 Post-RH-385 breadth-first source audit (2026-08-08)

The next breadth-first audit compared three nonphysical arithmetic routes.
At that checkpoint the repository-only verdict was `STOP_SCOPED`, and no
RH-386 was assigned.  The first source gate described below was later paid
and the resulting theorem published as RH-386 in Section 6.25.

At that checkpoint, the mathematically strongest conditional route was
uniform prime-tail asymptotics for growing indices.  Put `x=p_y`, `L=log x`,
and

```text
I_s(x)=integral_x^infinity t^(-s)/log(t) dt,
P_r(y)=sum_(p>x)(p^2-1)^(-r).
```

If an immutable source explicitly supplied absolute constants in the global
quantitative prime number theorem for Chebyshev's `vartheta`,

```text
vartheta(t)=t+O(C_pi t exp(-c_pi sqrt(log t))),
```

then strict Abel summation would give, uniformly in the permitted range,

```text
P_r(y)=x^(1-2r)/[(2r-1)L]
 *{1+O_(C_pi,c_pi)(1/[(2r-1)L]
                    +r exp(-c'_pi sqrt(L))+r/x^2)}.
```

Consequently every `R_y` with `log R_y=o(sqrt(L))` would satisfy

```text
sup_(1<=r<=R_y)
 abs((2r-1)x^(2r-1)L P_r(y)-1) ->0.
```

For a partition `lambda=product_r r^k_r`, define

```text
d=sum_r r k_r,
ell=sum_r k_r,
H(lambda)=sum_r k_r/(2r-1).
```

The exact-kernel product has logarithmic relative error
`O(d exp(-c'_pi sqrt(L))+d/x^2)`.  Replacing the kernels by the elementary
RH-384 leading product adds `O(H(lambda)/L)`.  Thus growing families require
`log sup d=o(sqrt(L))`, and the elementary leading formula additionally
requires `sup H(lambda)=o(L)`; `ell=o(L)` suffices.  The `H/L` term is a
genuine long-partition obstruction at this precision.

At that checkpoint, this route was not source-licensed.  RH-2 and RH-384
froze only qualitative PNT.  TPC-9 had constants depending on a fixed weight
without the seminorm control needed when `r` grows; TPC-16 treated a uniformly
bounded smooth family; TPC-7's displayed exponential estimate was for
different Möbius quantities.  Importing a global `vartheta` remainder from
folklore would have violated the controlling provenance rule.  The audited
anchors were:

```text
RH-384 release  386b66a55c9263353c7d407fd712be7e6279f1e6
RH-2 release    836426546db31e2737e877182848c538ed4cd436
TPC-9 release   ad77517ad8b06bf89f45cc682739b052c5560411
TPC-16 release  eaa2b3546eb1cb5e8b3ef5d847aca24fae6faf66
TPC-7 release   f3dd7e649461671fa63c83174c4a4bdb365f078c
```

The active-`c_11` route also remains `STOP_SCOPED`.  TPC-137 proves a fixed
bounded periodic coefficient theorem only in terminal logarithmic average;
it supplies neither ordinary Cesaro convergence nor growing-period
uniformity.  Moreover universal safety does not bound the period of the
`c_11` profile.  The edge tables

```text
A={(-1,+1)}, B={(-1,-1)}, C={(+1,+1)}
```

have `c_11=(-1/2,-1/2,+1/2)` and compatible transitions
`A->A`, `A->B`, `B->C`, `C->A`.  For every odd `q>=3`, placing `q-2` copies
of `A` followed by `B,C` on the `+2` phase cycle gives a universally safe
profile of minimal period `q`.  Already at `q=1`, RH-378's six active tables
meet the ordinary shift-two Cesaro Chowla term.  TPC-137 release
`0a67723ee2d0dd3171ee294816b8902b6e65285d` does not remove either blocker.

No prescribed super-polylogarithmic clock window is source-backed.  RH-366
gives every fixed logarithmic saving separately, while the worst periodic
DFT mass costs `sqrt(Q)`.  TPC-167 controls a phase-`L^2` quantity and TPC-158
leaves generic pointwise phases open; neither controls all atoms and all
table weights.  A non-effective diagonal with a stepwise exponent tending to
infinity follows directly from RH-385, but it has no prescribed rate and is
not a new theorem edge.

The earliest action identified at that checkpoint was to add one immutable
source object with the exact global `vartheta` remainder, theorem locator,
metadata, and hash.  Section 6.25 records that later source lock and the
resulting RH-386 proof.  Active `c_11`, polynomial clocks, adaptive capacity,
and Gates A--E remained untouched.

### 6.25 RH-386 source lock, growing-order theorem, and release (2026-08-08)

The missing analytic input was supplied by a versioned lock for Daniel R.
Johnston and Andrew Yang, *Some explicit estimates for the error term in the
prime number theorem*, JMAA 527(2), article 127460 (2023), DOI
`10.1016/j.jmaa.2023.127460`.  The proof uses only Theorem 1.4, equation
(1.8).  The frozen author-manuscript PDF has SHA-256
`565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2`,
`278380` bytes, and `22` pages.  Its source tar has SHA-256
`572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd`,
and source `main.tex` has SHA-256
`2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602`.
The remote lock records the arXiv nonexclusive license and Elsevier
copyright boundary; none of those external bytes is redistributed.

Independent proof reconstruction closed the strict Stieltjes boundary,
hazard, exact-to-power kernel, power-to-leading kernel, partition aggregation,
uniform-family quantifiers, and sharpness obstruction.  The canonical ledger
under the Section 3.25 hypotheses `L>=512` and
`7R epsilon_x<=1/2` is

```text
abs(log(P_lambda/J_lambda))<=14d epsilon_x,
abs(log(P_lambda/I_lambda))<=14d epsilon_x+d/(x^2-1),
abs(log(P_lambda/M_lambda)+H/L)
 <=14d epsilon_x+d/(x^2-1)+2H_2/L^2.
```

It yields growing-order single-tail uniformity, uniform finite partition
families, and the exact leading-equivalent criterion `H/L->0`.  For every
fixed `c>0`, the family `1^floor(cL)` tends to `exp(-c)`, so degree growth
alone cannot replace the `H/L` condition.

The artifact freezes `96=16+8+66+6` oracle rows, `24/24` theorem mutations,
`7/7` auxiliary attacks, and `1522/1522` scalar-leaf attacks.  Its local Git
closure is `59` blobs (`51+8`) with aggregate digest
`6247477a1744ccfe676ebd1c20b4d659c597ce0749f3d3a9a0b1c8aa2c87069d`,
plus one remote logical source lock whose canonical object SHA-256 is
`d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786`.
The canonical certificate is `29717` bytes with SHA-256
`64761d3a85afdee4682982ad545d20a66d2ed69926764bcc9580e0dc8c5f8710`.

Two independent final audits returned `GO / ACCEPT`, zero blocker and zero
minor.  The route verdict is `Route A=GO`; Route B remains `STOP_SCOPED`.
No active `c_11`, growing-clock, adaptive-capacity, operator, trace, zero,
RH, or Gate conclusion is imported.

### 6.26 RH-387 all-order resummation proof and release (2026-08-08)

The post-RH-386 breadth audit compared three routes.  Active phasewise
`c_11` remained stopped at ordinary shift-two Cesaro cancellation, and the
clock route supplied no prescribed stronger window beyond RH-385.  The
selected route instead combined RH-383's absolutely convergent endpoint
normal form with RH-386's absolute strict-Stieltjes source estimate.  This
route is not a finite-partition corollary: every order is first resummed by
Tonelli into a closed logarithmic integral, and only then is the resulting
seven-vector passed through the endpoint map.

The exact coordinate ledgers are

```text
max_(1<=c<=7)abs(Phi_c^P-Phi_c^J)<=28epsilon_x/(xL),
0<=max_(1<=c<=7)(Phi_c^J-Phi_c^I)<=14/(3x^3L).
```

The frozen endpoint coefficients give `7` and `49/8`; the derivative split
is `2/4/4`; and the resulting `ell^infinity`-to-`ell^1` Lipschitz constant is
`126`.  Therefore the published gap constants are exactly

```text
126*28=3528,
126*(14/3)=588.
```

The executable artifact freezes `42=12+7+7+14+2` oracle rows and rejects
`24/24` genuine field-level mutations.  Its immutable source closure has
`68` Git blobs grouped `59/8/1` with ordered digest
`19def5cbed919da8e9652012cf011f3b5728efd4b24a9eef0911bb7346467d27`,
plus the remote logical Johnston--Yang lock.  The full logical digest is
`5016397fe59962954514b3b42d68e9de6dfeff0dae949791b01c6a516f5c61fe`,
and the canonical remote-lock digest remains
`d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786`.
The external PDF, source tar, and source `main.tex` are not redistributed.

Independent proof/release and source/integrity audits both returned
`GO / ACCEPT`, zero blocker and zero minor.  The route verdict is
`Route A=GO`; Route B remains `STOP_SCOPED`.  Because
`epsilon_x x^2->infinity`, the release explicitly forbids promoting the
`588/(x^3L)` surrogate difference to a `P_2`-scale approximation of the
actual gap.  Complex channels, active `c_11`, growing clocks, adaptive
capacity, operators, traces, zeros, RH, and Gates A--E remain outside scope.

### 6.27 RH-388 rank-one `P_2` proof and release (2026-08-08)

The post-RH-387 breadth audit compared all-order factorial refinement,
bounded-gap obstruction, complex-channel extension, active-`c_11`, and
stronger-clock routes.  The selected theorem combines two nontrivial edges:
exact rank-one retention is sufficient for uniform `P_2` accuracy, while
Maynard's actual bounded consecutive prime gaps show that smoothing rank one
fails at that scale inside the frozen `P/J/I` hierarchy.

The positive proof applies the RH-386 strict-Stieltjes estimate only for
`r>=2`, then uses the exact finite geometric remainder for every higher
rank.  The coordinate constants are exactly

```text
60, 13, 28/3,
```

and the RH-383 endpoint Lipschitz constant `126` produces

```text
126*60=7560,
126*13=1638,
126*(28/3)=1176.
```

The complete moving window is paid by the symbolic recurrence for
`b_K=K!/(3L)^K`; the twelve finite `K` rows are explicitly regression only.
The negative proof uses Maynard Theorem 1.3, the integer-valued gap
implication, exact strict succession, the endpoint Hessian bound `224`, and
the direction `grad F(0).(1,...,7)=2X_infinity`.  Its sharp limsup constants
are `1/2` and `X_infinity`; the finite `1/16` row is eventual and nonsharp.

The executable artifact freezes `56=12+7+12+7+10+8` rows and rejects
`24/24` genuine field-level mutations.  The immutable Git closure contains
`77` release blobs grouped `68/8/1`, with ordered digest
`d7f2ee43f56631c8f3442db8fcc6fb423a801b5af7607351623cd449a92c3f73`.
The ordered Johnston--Yang and Maynard canonical remote digests are

```text
d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786
bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e
```

and the resulting `79`-input logical digest is
`bffce602d6e3b568eb96662820f08aa457ff5d0de4065f3c9eeac53d8d8dfa39`.
Neither external source payload is redistributed.  Both verifiers are
offline by default; both explicit opt-in source replays passed.

The final release has `36` publication members plus manifest and verification
report, hence exactly `38` RH-388 files in integration commit
`8e6f89ee1e58e67c53c5f4719c05e881107113ac`.  The test suite is `58/58`,
the archive has zero failures, and both independent final audits returned
zero blocker and zero minor.  Routes A and B are `GO`; Route C is
`STOP_SCOPED`.  Factorial convergence, an enlarged `K` window, universal
surrogate necessity, `P_3` precision, complex channels, active `c_11`,
growing clocks, adaptive capacity, operators, traces, zeros, RH, and Gates
A--E remain outside scope.

## 7. Reproduction and publication audit

Final RH-367 audit:

- Source locks: `23/23`; cyclic source commit
  `e7d21f646498d77e1c3213d1e4f35dc8466038ff`; overlap sources RH-3, RH-10,
  RH-55 and the four-volume verification all match their frozen hashes.
- Upstream cyclic checks: `12/12` tests; geometry maximum residual
  `4.44e-16`; phase scan `136` rows (`4` aligned, `132` crossing).
- Local tests: `9/9`; source audit passes; all Gates and forbidden-claim
  booleans remain false.  Individual archive: `21` publication files and
  `23` external inputs, zero failures.
- PDF: `4` pages and `209,891` bytes; `16` embedded, subsetted,
  Unicode-mapped font rows; Ghostscript parsing and text extraction pass; all
  `4/4` rendered pages were visually inspected.
- Complete LaTeX logs have no undefined references, overfull/underfull boxes,
  actionable warnings, or rerun notices.  The semantic PDF is byte-identical
  to `main.pdf`.

RH-367 final hashes:

```text
main.tex
b6d59b16169a73b386db927618e3be198c2a369e13c907fd837d3057f8369ecb

PDF
ad5381a2164b84f455b043f2352b932d8d9c6b258dc6afc520b769653027a90e

result
473fb75147bf38c47f38d1f2254ae1ca0cef64cd30e3731eafa51e59ef39be7f

manifest
89aea280c88426dca3ccd85d54ffde15019bac27ef17b6b53f0ef087e547a99b

verification
dacd22835634f71cb40e046729b7add9230c80470c1d3feca30ec12300d7246a
```

Final RH-369 audit:

- Source locks: `7/7`; frozen inputs include
  `henon_mobius_correlations=34490443f50cfe9af9ff93888e51e7e7e534a5a7`,
  the RH-366 release, and the four-volume verification.
- Tests: `6/6`; exact rational parameter checks at `t=1/2,2/3,3/4`,
  `3/3` parameter rows, and `42/42` finite variance rows through `N=14`.
- Individual archive: `21` publication files and `7` external inputs, zero
  failures.
- PDF: `5` pages and `328,575` bytes; `22` embedded Unicode-mapped font rows;
  Ghostscript and text extraction pass; all `5/5` rendered pages were
  visually inspected.
- Complete LaTeX logs have no undefined references, overfull/underfull boxes,
  actionable warnings, or rerun notices.  The semantic PDF is byte-identical
  to `main.pdf`.

RH-369 final hashes:

```text
main.tex
069ef17b8e61f65ce7e8cfe1cb822ddef7a7728b787de36039aa5f15b3f78ac1

PDF
ee1a4a4bbd27bd1e5f01c9affb0f6ad0afd23920d3c4ea8643aaa66e215b8c92

result
e030a11932b4c34ba11ce2207b2393f65ebdca1c9b585a4d5d60a3d370106a32

manifest
de6945eae1a1ac03d70aab087163c762dded696f5175e1ed2745b39b49ce5ffc

verification
df8ad0301938109c45847e4d62025c37bc41d230391cc60b5a716e856203c9c4
```

Final RH-370 audit:

- Source locks: `9/9`; cyclic-Ulam upstream tests: `12/12`.
- Local tests: `5/5`; strict result checks: `4/4`; source and claim
  firewalls pass.  Individual archive: `21` publication files and `9`
  external inputs, zero failures.
- PDF: `5` pages; `20` font rows are embedded (`19` Unicode-mapped and one
  Type3 custom row without a ToUnicode map); Ghostscript, text extraction,
  and all `5/5` rendered pages pass.  The semantic PDF is byte-identical to
  `main.pdf`; the complete
  LaTeX log has no actionable warning or error.
- The four finite quotient rows and four spike-scaling rows are exact or
  reproduction checks only; no row is treated as spectral-limit evidence.

RH-370 final hashes:

```text
main.tex
f1fa2b7890d67b86e0dd5716b9a9259264afec1c836bdb6d601dff19e9b05689

PDF
272ce8de4ecf908ff5e5778b2744d44eb4bf31f225722d65e9669514c6a9b2cb

result
b69e0e7084f4b1abda93c3cbcb609dcc69449dc1506c7252dc1364373286c376

manifest
038739f50c3bbd773b011cfad4a2f70be3989135e260c0fd88a023dfed32c61f

verification
25eeb20f882443835389ae0637b7066a189b485e35b4809c404a3877e50de2ac
```

Final RH-368 audit:

- Source locks: `11/11`; frozen commits include
  `dyna_zeta_map=7fd3a3fdd5a6a25827a0965345459baf4a47b816`, the RH-366 release,
  the RH-367 release, and the four-volume verification.
- Tests: `5/5`; finite formula versus exhaustive `A_{\{2\}}` words through
  `N=12`; source audit and claim firewall pass.
- Individual archive: `21` publication files and `11` external inputs, zero
  failures.
- PDF: `3` pages and `299,799` bytes; `20` embedded Unicode-mapped font rows;
  Ghostscript and text extraction pass; all `3/3` rendered pages were
  visually inspected.
- Complete LaTeX logs have no undefined references, overfull/underfull boxes,
  actionable warnings, or rerun notices.  The semantic PDF is byte-identical
  to `main.pdf`.

RH-368 final hashes:

```text
main.tex
8829edbf3c4f449f0a555a456e011559e3dfeeef7268dc5e8547ea42595848cb

PDF
eb995fab1d0c0eab87ec5f201b1d573e3a55f1985bc76725b2b34e6ba886ecb7

result
dab505dd68e6cb011bb5e8b5ae6dce4268be7fa0431bc2ebbe921cb562f0a4d8

manifest
2dde9095c506f3a862295994e0433a1eda4a7c0a12b215c3f04db0143a75bf38

verification
ec4472f3ead9f305215808f9799ca01048dfa6abc88a23c093fd8a94017a5699
```

Final RH-366 audit:

- Source locks: `23/23`; frozen external commits include
  `henon_mobius_correlations=34490443f50cfe9af9ff93888e51e7e7e534a5a7`,
  `henon_weighted_zeta=ff44f961261349848c9f65ede6a031b7e155aca9`, and
  `dyna_zeta_map=7fd3a3fdd5a6a25827a0965345459baf4a47b816`.
- Tests: `17/17`; the independent upstream R001 checker passes, with `8/8`
  surrogate replays and witness residual approximately `7.1e-15`.
- Individual archive: `21` publication files and `23` external inputs, zero
  failures.
- PDF: `8` pages and `271,477` bytes; `20` embedded Unicode-mapped font rows;
  Ghostscript parsing and text extraction pass; all `8/8` rendered pages were
  visually checked.
- Complete LaTeX/BibTeX logs are clean; the semantic PDF is byte-identical to
  `main.pdf`; all Gates A--E and all named forbidden macro claims remain
  false/open.

RH-366 final hashes:

```text
main.tex
7df165bd63d43f52dc217dea6691d231d8e40c00c148ab7e1aa4abcac55060fb

PDF
fb74ac4675a75c2b76cd24767a9095445b7e661b8a6a28bec1489c31183904bf

result
6a125ca90b0964945f95b39397b6e83f15a23ad24c94d2e8b9c90d320db8e418

manifest
1f978b49cbb7f3c99a7dfffdd6de85fe7e73c085f611d944280dc724ace5e45c

verification
9d23bfdc732f62e41e24269356fc0ffbfa82a95fab3ee24245082f3c97292770
```

Final RH-365 audit:

- Source locks: `15/15`; the four-volume replay remains `4` volumes, `361`
  numbered sources, `73` archive members, `1,548` dependency hashes, `8`
  result hashes, and zero failures.
- Tests: `15/15`; individual archive: `21` publication files and `15`
  external inputs, zero failures; strict JSON parsing passes `4/4` files.
- PDF: `9` pages and `283,695` bytes; `21` font rows, all embedded and
  subsetted with Unicode maps; Ghostscript and text extraction pass; all
  `9/9` rendered pages were visually checked.
- Complete LaTeX/BibTeX logs contain zero errors, undefined references or
  citations, overfull/underfull boxes, actionable warnings, or rerun notices.
- The semantic PDF is byte-identical to `main.pdf`; all five Gates and all
  `15` named forbidden macro claims remain false/open.

RH-365 final hashes:

```text
main.tex
cf70fb8a3bb2b9fb4158e75c91426ff07c4f501523cee02bbc7e1a13f1982e1f

PDF
a14dae97006f81ace467a1712d50a28f002ae0f83029714f4ce0c5d912eb5a7c

result
18d4f7f30533df2f741c53f402fdcae71f73c7da3dbc963c348be86b270ca55a

manifest
b4b2d3442521272be11009a1b6d285b59e4f807cb560dfc2cbdc2efd5ff3635a

verification
73e921c26666a5711054787f07d58bfd63a1c005a1ec05e00d4ccee74d4ea05a
```

Final RH-364 audit:

- Source locks: `13/13`; the four-volume replay remains `4` volumes, `361`
  numbered sources, `73` archive members, `1,548` dependency hashes, `8`
  result hashes, and zero failures.
- Tests: `14/14`; individual archive: `20` publication files and `13`
  external inputs, zero failures.
- PDF: `9` pages and `293,839` bytes; `22` font rows, all embedded and
  subsetted with Unicode maps; Ghostscript and text extraction pass; all
  `9/9` rendered pages were visually checked.
- Complete LaTeX/BibTeX logs contain zero errors, undefined references or
  citations, overfull/underfull boxes, actionable warnings, or rerun notices.
- The semantic PDF is byte-identical to `main.pdf`; all five Gates and all
  `15` named forbidden macro claims remain false/open.

RH-364 final hashes:

```text
main.tex
44df56838023323b55fbb0e90e7b47d8d697686dbfddfb245ff3a5dd70917345

PDF
e179b63ce9b83fbb0863515b98ec03fe46724ab9cb87e3e489f339bd9b5a4166

result
2d02e456330fb5a7ca161b0cea58ae6f6781ad76c077599e98fd91485cc89478

manifest
a20f865623330cb16902938b4e613538a51e4c0a9beb5289aead13da8f19fdda

verification
9a4d5aa2a970de87d0b9cae0e5dd7a79b0da03333a84362437221845727268e7
```

Final RH-363 audit:

- Source locks: `7/7`; the four-volume replay remains `4` volumes, `361`
  numbered sources, `73` archive members, `1,548` dependency hashes, `8`
  result hashes, and zero failures.
- Tests: `14/14`; individual archive: `20` publication files and `7`
  external inputs, zero failures.
- PDF: `9` pages and `317,243` bytes; `24` font rows, all embedded and
  subsetted with Unicode maps; Ghostscript and text extraction pass; all
  `9/9` rendered pages were visually checked.
- Complete LaTeX/BibTeX logs contain zero errors, undefined references or
  citations, overfull/underfull boxes, actionable warnings, or rerun notices.
- The semantic PDF is byte-identical to `main.pdf`; all five Gates and all
  `13` named forbidden macro claims remain false/open.

RH-363 final hashes:

```text
main.tex
4e6bdede6775ff4e21fae928c40ce65aea1887e633684beabd5b4a75f8d7d5f3

PDF
d7de817c343b00c12049899d714055f0e7833dc5c4bfea1444936d5424890b43

result
e448b70e0fa04e8a8ac1a0be36e13e504564e641969d5512f1b8a50e5a935d01

manifest
f72820fa375e04e9995e2de354d365d5fc8e4abcb0eabbdf1a9a45befde5bfc7

verification
3bcb282ffa80e8c2c7ae7a1067b6161e06ba14c84e5a89f1521530c5b9fdd0c6
```

Final RH-362 audit:

- Source locks: `7/7`, including the four-volume manifest and independent
  verification.
- Four-volume replay: `4` volumes, `361` numbered sources, `73` archive
  members, `1,548` dependency hashes, `8` result hashes, zero failures.
- Tests: `15/15`, including archive membership, path, and source-commit
  mutation rejection.
- Individual archive: `20` publication files and `7` external inputs, zero
  failures.
- PDF: `7` pages; `20` font rows, all embedded; Ghostscript and text
  extraction pass; all `7/7` pages visually checked.
- Complete LaTeX/BibTeX logs are clean; the semantic PDF is byte-identical to
  `main.pdf`.
- Gates A--E and all 13 forbidden macro claims remain false/open.

RH-362 final hashes:

```text
main.tex
1d3909ad8b97d6bb0fc8c861ae0c702908f992cd33c8c1a7a57349b2f8925ccc

PDF
c237ed39e4160c594a70788cc799d089c43edea613825b71691f21cbb33c73f7

result
5edf4ed048e10a008f00a03d62a934630caba1724af529878910892cea7001fc

manifest
8b0f06ace63e8d78cf3d91b11365db23d5109f387c8e72218ed2e55b72109d56

verification
1358d2f26cc344c55a3fdeb8dd49c34c256d4c07fede915d8927f7b416a8c720
```

Final RH-352--RH-361 audit:

- Tests: `324/324`; per paper `28,30,35,44,30,31,35,37,34,20`.
- Publication files: `17,17,17,17,17,17,18,18,18,20`; all ten individual
  archives verified, zero failures.
- Batch archive: `176` files, zero failures; controlled tree: `198` files.
- PDF pages: `6,5,5,6,6,6,6,5,5,7`, total `57`.
- Font rows: `18,18,20,18,20,19,21,19,19,20`, total `192`, all embedded.
- Strict JSON: `32/32`; Ghostscript: `10/10`; RH-361 visual review: `7/7`.
- All LaTeX/BibTeX logs are clean; semantic PDFs are byte-identical to
  `main.pdf`; the cold rebuild is byte-identical.
- Upstream/all-batch Gates: `45/45 false`, `50/50 false`.
- Upstream/all-batch forbidden claims: `129/129 false`, `149/149 false`;
  per-paper counts `15,14,13,14,14,14,14,15,16,20`.

Final hashes:

```text
RH-361 main.tex
f8ef8517834a8f2d861c9fa2432396d37de34d8d9b2ae17fa710ed095d2893bc

RH-361 PDF
8c81805456299b3ebae9ed4ec4b87270bc8783ef8eb4b15699f0d893fe3782af

RH-361 result
97e8b712b58efc4cda9f5cb5ddc54b6e5b3a041ae227e8839a425212baa38a0b

RH-361 manifest
c5ca0b2eceb7f13c1c24e274d264569f3718cfc76766021e66dae65b1cc0b4f2

RH-361 verification
64dfe296467d2ba97e0f1871f6da96e3e1157920c86a373225dce7b81244ec62

RH-352--RH-361 batch manifest
3533dd009cd4f90a683d937f5d80a5e73e20166a3cea5f76fdbc422b260533f2

RH-352--RH-361 batch verification
46ebbd8a76edbf4a7e76efada06ee51971d932bd7fec732f47b4d80bcc3109d8

RH-MVP2 main.tex
32d0826c731ab7aa5273529e1e9d7b9652cbef775334b23acce28ad7156e6913

RH-MVP2 PDF
ed6a93f52c39a659ef2e6e5905e625a83d2943f86093f5911421db3645ce7dba

RH-MVP2 corpus inventory
c557f83480be297650eb94390b18e5f17f041819aba85d23cc9c37ac09dfaa19

RH-MVP2 dependency manifest
ec8470e98618c0684a9a942b8ca608832c4856bbebb927ae00d2cfeafcce10b2

RH-MVP2 summary
3cf3261c0c2c6fbe7511b16615f032edfcbd6b6b1e0c73f5e2ef932a1e6a694c

RH-MVP2 archive verification
8be16281d3f6af1be1a172ccb6443cf1af138ccd786c9236378c3fcad6f4d72e
```

Four-volume synthesis audit:

- Atomic indices: `160,81,40,80`, total `361/361`, with disjoint consecutive
  ranges and four preserved empty legacy aliases in Volume IV.
- Tests: Volume I--IV `11,4,4,4`; RH-MVP2 including archive-mutation tests
  `7`; total `30/30`.
- Individual archive files: `16,19,19,19`; outer four-volume archive `73`,
  zero failures.
- Outer replay: `1,548` dependency hashes and `8` result hashes, zero
  failures. RH-MVP2's own publication archive contains `23` files.
- PDF pages: Volume I--IV `13,7,6,9`, plus RH-MVP2 `6`, total `41`.
- Font rows: `20,13,15,19,17`, total `84`, all embedded. Ghostscript parsed
  `5/5`; text extraction and required boundary phrases passed `5/5`.
- All five complete LaTeX logs are clean. The five semantic PDFs are
  byte-identical to their `main.pdf`; all `41/41` rendered pages were checked.
- Gates A--E and every named forbidden macro claim remain false/open. The
  release was non-numbered and did not itself activate RH-362.

Four-volume release hashes:

```text
Volume I main.tex / PDF / archive verification
b9451acd42136ab1d705a72401d5edbdc5f1ce45fea1ce76e7732664240b21e8
64ece95279b7e5e6194ddf7f6dcb01fbdb0a30b77f14d26f33b764a3c91c07ef
03f9577fcba8a63f74208c54636837141d65a8de70e6aaba573bd3ca834ccf81

Volume II main.tex / PDF / archive verification
5b9874b680a968c887d6ba99e9f8cf3da9aae14e5fb4d26c7fb8bcb83b56da41
e05c1f39941c4fd1b79c3ede17cd054e3098c80cf1d65367143f205440bcdcd6
7aa0f5d5ae3f6bf6116d5694ea1e95fee28b3bf6ab63a3a90e7e4c9568b1bb74

Volume III main.tex / PDF / archive verification
0d1fbaed123fc7e877d7253eeb4d442e81279cb35075e9783771d6e4d5adb89b
ca3a7d697957babb39dd9c70000c8b38687cf8efbe7207f8519756f4ab0c426a
58795f5821eaf16d90d641e3fa67025b2ed0e643576b18e12624e3d44d1c985c

Volume IV main.tex / PDF / archive verification
ba7a9a2849e0219cdab2a733a9f7865e97cfd0d278ca4bbc1cad8528eacb76cc
fc16b61241d5fc3fd1cfde292b1bb8c9d685af2ce026e518ddd8dceceaee9c4e
7c7ffee7fd1a742c48285fc7412ffbdc4943b382d5693bb5b246561860317be8

Four-volume manifest / verification
24dcf3c6e74c5252e7e278d9141a656c6b97bb30fad6578da8c193cc1063a897
b27f120f77c4bbf3afd3a4486fd800a8de93a2db52236c835809aa488d113751
```

Final RH-371 audit:

- Source locks: `9/9`; frozen `henon_mobius_correlations`, RH-366, RH-370,
  and four-volume inputs match.  Local tests: `5/5`; strict result/schema
  checks pass; the prefix formula agrees with independent DP for `1000/1000`
  prefixes, cyclic pair cells pass `162/162`, and both periodic capacity
  identities pass through `q=256`.
- Individual archive: `21` publication files and `9` external inputs, zero
  failures.  The endpoint is `N=2^20`; all finite rows are reproduction
  checks only.  The four-volume replay remains `4` volumes, `73` archive
  members, `1,548` dependency hashes, `8` result hashes, and zero failures.
- PDF: `5` pages and `216,162` bytes; `17` font rows are embedded (one Type3
  custom row has no Unicode map); Ghostscript, text extraction, and all
  `5/5` rendered pages pass.  The semantic PDF is byte-identical to
  `main.pdf`; complete LaTeX/BibTeX logs have no actionable warnings or
  errors.
- The cyclic witness is synthetic and its open-prefix ledger differs.  The
  eight-run identity is exact for every prefix but supplies no run-density or
  capacity-limit theorem.  Gates A--E and all forbidden macro claims remain
  false/open.

RH-371 final hashes:

```text
main.tex
fa2b1e37c5daf791b9d44cb424f63457014d8ca5b8293e524f66c14425a31a0e

PDF
60452b1bffb40a7151576a59e0e9cfadeffa7e37df54b26a11c58921b867307c

result
00210432e5169df7b450b8a764e67547a1fd4f1213714d51d9d98b80fc9ca657

manifest
e1a2bae4719ce520e0a94d9c7e34518d085e8afd9271a88f5faae77125b08b0a

verification
a2bcfaafe2b118cc5479f948b318a02ee7754ad3fb21e222b1e67498446ff81a
```

Final RH-372 audit:

- Source locks: `9/9`; frozen commits and the four-volume verification match.
- Tests: `15/15`; exact max-plus/brute-force checks, three universal
  safety/one-site/path checks, memory-dependent-label rejection, and the
  `729`-table enumeration all pass.
- Individual archive: `21` publication files plus `9` external inputs, zero
  failures.  The endpoint is `N=2^16`; all finite rows are reproduction
  checks only.
- PDF: `5` pages, `18` embedded font rows, Ghostscript and text extraction
  pass, and all `5/5` rendered pages were visually checked.  The final
  LaTeX/BibTeX log has no actionable warnings or errors; the distribution PDF
  is byte-identical to `main.pdf`.
- The one-site constants are `4/pi^2`, `4/pi^2`, and `9/(4*pi^2)`.  The
  fixed-resource theorem does not prove the RH-366 capacity limit, a
  memory-dependent correlation law, an intrinsic operator, a prime-power
  trace, a zero identification, or RH.  Gates A--E remain false/open.

RH-372 final hashes:

```text
main.tex
059f8bee897d6b4b4cfdf0bbb9fb7908b1cb27b53691097b725f54fcd2724b90

PDF
511ce2e4dc78a4c4a5a1c0132d692f6a929d18300c4fa5a831d79a0dbd5efe99

result
8256ddc3e50c7ab641e0ee8dceffc3e18cfd0877fff667613fb30ff23f632163

manifest
41920434a5ea69171dd7408236b8f4810df731d95932b1d8b77df154ac26828f

verification
4c1ca9cc56fba3de5ea47a9fcc4e1026847579387ecd823f045816323045dcb9
```

Final RH-373 audit:

- Source locks: `10/10`; the frozen Hénon Möbius package, RH-366, RH-371,
  RH-372, and the four-volume verification match.
- Tests: `6/6`; the exact phase counts, cyclic distance-two independence,
  rational density sum, universal-safe completion, one-site observable,
  prefix capacity witnesses, result ledger, and archive contract all pass.
- Independent regeneration checks all `3240` universal table rows and `2048`
  prefixes.  At `N=2^16`, selector and transducer scores both equal `26852`,
  the exact capacity is `32320`, and the graph path passes.  These rows are
  reproduction checks rather than asymptotic evidence.
- Individual archive: `21` publication files plus `10` external inputs, zero
  failures.  The four-volume outer replay remains `4` volumes, `73` archive
  members, `1,548` dependency hashes, `8` result hashes, `361` numbered
  sources, and zero failures.
- PDF: `4` pages and `308,516` bytes, with `23` embedded font rows;
  Ghostscript and text extraction pass.  The complete LaTeX/BibTeX log has
  zero warning, error, undefined-reference, overfull, or underfull matches;
  the distribution PDF is byte-identical to `main.pdf`.
- The repository-locked ARS-style final integrity audit passes `48/48`
  normalized claim families, all `4/4` bibliography records, `4/4` citation
  keys with zero dangling or orphan entries, and all seven AI-research
  failure modes.  The finite checks are not used as proof of the asymptotic
  statement.  No all-clock optimum, capacity limit, unrestricted
  memory-dependent law, operator, trace, zero identification, or RH claim is
  made.  Gates A--E remain false/open.

RH-373 final hashes:

```text
main.tex
2242a03b03e31707f44595930db7a8ff11cee7df1134ac0b575ef12e2d9feba5

PDF
aa44dee00b9601afce5ac7d89294070b482d8c0dff5d303103f01101dc3fe6f4

result
96cb93d97abffed83f57b90fec996ea51dcc199fec05063995b974f480d31773

manifest
f54d39659015eedafda65551c844544bb718e9326cd70c194e4a896b27c74e87

verification
cf18d1993f41792e7e36dc5a670bea2347230e966338b677fe3b1bb07e636991
```

Final RH-374 audit:

- Source locks: `12/12`; the frozen Hénon Möbius package, RH-366, RH-371,
  RH-372, RH-373, and the four-volume verification match.
- Tests: `10/10`; exact Fraction rows, direct cyclic run/MWIS checks for the
  first three clocks, all three prime-adjoining recurrences, the endpoint
  `R_8` convention, q=900 universal safety, result ledger, and archive
  contract pass.
- Independent regeneration checks six formula rows, `3/3` direct run
  formulas, `3/3` brute MWIS values, `3/3` recurrences, all `8100` q=900
  universal rows, and `2048` prefix witnesses.  At `N=2^16`, the selector
  score is `27174` and exact capacity is `32320`.  These are reproduction
  checks, not asymptotic evidence.
- Individual archive: `21` publication files plus `12` external inputs, zero
  failures.  The four-volume replay remains `4` volumes, `73` archive
  members, `1,548` dependency hashes, `8` result hashes, `361` numbered
  sources, and zero failures.
- PDF: `6` pages and `336,521` bytes, with `22` embedded font rows;
  Ghostscript, text extraction, and all `6/6` rendered pages pass.  The
  complete LaTeX/BibTeX log has zero actionable warning, error, undefined,
  overfull, or underfull matches; the semantic PDF is byte-identical to
  `main.pdf`.
- The repository-locked ARS integrity pass found no unresolved reference,
  claim-scope, implementation, or finite-to-asymptotic issue.  The
  Euler-product formula is exact, while its stored decimal enclosure is
  diagnostic only.  No all-clock or arbitrary-memory optimum, capacity
  convergence, operator, trace, zero identification, Hilbert--Polya object,
  or RH claim is made.  Gates A--E remain false/open.

RH-374 final hashes:

```text
main.tex
2129075ec4bae1c5f0f25fcd09cec273fe322d44116d51e5191e3cade4fb9f6d

PDF
62754af2b5e9f433c4317c642a7e5054b4178f272b965bd1cd0ae054e8b06f99

result
ca492e96bd557b966d7924ee7acca7eceb9248dafe513a674f36f78891438bdd

manifest
7c9569bb42fe52f7281e58e2acb175efffe80fbd49f2e022c048c8bb35a1f811

verification
ef4b196b0eb8ee74cde1697014919bbf8be6c93eea65984a575b886cda065de6
```

Final RH-375 audit:

- Tests: `12/12`; regenerated `result.json` is byte-identical and satisfies
  its closed Draft 2020-12 schema with no duplicate JSON keys.
- Independent exact regeneration checks `4680` factor tables (`249`
  universally safe), `2046` phase subsets (`317` safe), eight divisibility
  audits with `58` density fibers, ten cofinal lifts, and the bounded
  `q<=256` reproduction scan.  The largest lift `343|308700` has `193536`
  positive phases, MWIS `132832`, and `pi^2F=593/144`; every check passes.
- Source locks: `21/21`; all seven declared Git object IDs exist.  The
  bibliography has seven entries and eight body citations, with zero dangling
  or orphan keys.  The repository-locked ARS audit and all seven research
  failure-mode checks pass after two provenance-wording corrections.
- Individual archive: `22` publication files plus `21` external inputs, zero
  failures.  The four-volume replay remains `4` volumes, `73` members, `1548`
  dependency hashes, `8` result hashes, `361` numbered sources, and zero
  failures; its manifest SHA-256 is
  `24dcf3c6e74c5252e7e278d9141a656c6b97bb30fad6578da8c193cc1063a897`.
- PDF: `6` pages and `330169` bytes, with `24/24` fonts embedded.
  Ghostscript, text extraction, full LaTeX/BibTeX log scans, semantic-PDF
  identity, and all `6/6` rendered pages pass.  A fresh temporary compile has
  identical text and page pixels; binary metadata timestamps alone differ.
- No general cyclic-cover MWIS theorem, finite-clock attainment, growing
  clock, memory/adaptive-capacity convergence, intrinsic operator, trace,
  zero identification, Hilbert--Polya object, or RH claim is made.  Gates
  A--E remain false/open.

RH-375 final hashes:

```text
main.tex
7d96987b0236d2788a781565bc03195c59ad2b72d07f1ff8988f8a3fef4a5117

PDF
cc31194cdf51f4ae7aa643100c87b2d26b274da872b0c117620bf182a4400616

result
81d905c2476abc36fdd1ab0e468ad33d85f4df9db35afbd3bc79bf0771fe0a08

manifest
3f589d91b87ca8c924ccd2cfb30fa8d04eadd9e73e90474b7149bd7bc855d92f

verification
f07fecea09e819d7f1edc1afea923f61fdaac2f5758afa7129e785baed90d6bd

integrity audit
ce31660540a1e71a576634ae64ff5db19408aadee8cf79ffe09a7f6793427ab6
```

Final RH-376 audit:

- Tests: `8/8`; isolated regeneration of `result.json` is byte-identical and
  the closed Draft 2020-12 schema has zero errors or duplicate JSON keys.
- Independent exact regeneration checks `1048574` pointwise Boolean
  identities, `1048576` cumulative prefixes, `524287` even-start zero rows,
  and `1024` RH-371 endpoints (`2048` sign cells).  The three frozen rows at
  `N=1024,65536,1048576` match exactly.  These are reproduction checks only.
- Source locks: `13/13`; all five declared Git objects exist.  The
  bibliography has six entries and six unique cited keys, with zero dangling
  or orphan references.  Davenport, Mirsky, and Teravainen--Walker metadata
  match their frozen repository sources.
- Individual archive: `22` publication files plus `13` external inputs, zero
  failures.  The four-volume replay remains `4` volumes, `73` members, `1548`
  dependency hashes, `8` result hashes, `361` numbered sources, and zero
  failures.
- PDF: `6` pages and `313218` bytes, with `20/20` fonts embedded, subsetted,
  and Unicode-mapped.  Ghostscript, text extraction, complete LaTeX/BibTeX
  log scans, semantic-PDF identity, and all `6/6` rendered pages pass.
- The repository-locked ARS audit has zero remaining blocker or minor.  No
  ordinary Chowla theorem, density nonconvergence, higher-run limit,
  adaptive-capacity convergence, intrinsic operator, trace, zero
  identification, Hilbert--Polya object, or RH claim is made.  Gates A--E
  remain false/open.

RH-376 final hashes:

```text
main.tex
414728a8ac2e29add0ec9a4e11fc4d2dd3991be8c5de696c3bd2d5ebbd25b70e

PDF
8af92d63b279f0b3d7db027ba3c2d22d6116827574f167f55f7c53c1cdb5b01a

result
8e320b70c168a640dab60e94ba965947c388372f46ce8268fde9ae11d1d6df91

manifest
22a9851ca0694c5ffe58683b6cde5c00c37ac653ef9c346a8848210e86b9affb

verification
a7a6bb0e4b6bbee41007277bbabf409902b0c2c9aad6e2f06e2f8c95f8de4b33

integrity audit
00c5697d3a09fe6485300757c9e3a3f5ea208abc8f3cad77cc58c4d047ac67d7
```

Final RH-377 audit:

- Tests: `8/8`; isolated regeneration of `result.json` is byte-identical,
  four JSON files have zero duplicate keys, and the closed Draft 2020-12
  schema passes.
- Independent exact regeneration checks `19680` Boolean cases, formal rank
  `13` and kernel `453` on `466` coordinates, `1048548` native window
  updates, `4194304` cumulative signed identities, and `262144`
  path/decomposition/residual prefixes.  All frozen endpoint rows match.
- The stationary witness independently passes `27` transition rows, `9`
  stationarity cells, `502` raw cases, `502` square-only cases, and `1793`
  one-sign masked cases.  The directional moments are exactly
  `(8 epsilon/81,0,0)`.
- Source locks: `13/13`; all four declared Git objects exist.  The
  bibliography has four entries with zero dangling or orphan citations.
  The repository-locked ARS proof/integrity audit has no remaining blocker
  or minor.
- Individual archive: `22` publication files plus `13` external inputs,
  zero failures.  The four-volume replay remains `4` volumes, `73` members,
  `1548` dependency hashes, `8` result hashes, `361` numbered sources, and
  zero failures.
- PDF: `8` pages and `339397` bytes, with `22/22` fonts embedded and
  subsetted.  Ghostscript, text extraction, full LaTeX/BibTeX log scans,
  semantic-PDF identity, and all `8/8` rendered pages pass.
- No mixed-coordinate cancellation, capacity convergence, arithmetic
  counterexample, intrinsic operator, trace, zero identification,
  Hilbert--Polya object, or RH claim is made.  Gates A--E remain false/open.

RH-377 final hashes:

```text
main.tex
35a3d2b9eecede4f526490dc184b24e5530762933922962df04c3436e2d39433

PDF
508cabee3e4f760ace80c1ef26f70f93afb0e2548dc28496aa47c900b6a26b86

result
0abfb9b4d268675acba95186027816ad50c504142c04a7d92b57c2f387c7d144

manifest
c7d1825f0ca5c95f5410a3b6ddeddd2d4a25c520c856c84b52f55f2e176729c5

verification
e4eced0db77e901dd1182234b0932257eb9c3eb48d90e89b2e13c12d8d342785
```

Final RH-378 audit:

- Tests: `9/9`; isolated regeneration of `result.json` is byte-identical,
  four JSON files have zero duplicate keys, and the closed Draft 2020-12
  schema passes.
- Independent exact regeneration checks `512` lag tables, `13` universally
  safe tables, `8` coefficient vectors, rank `5`, two `243`-row graph lifts,
  `72` Mealy safety rows, `88572` ternary words, and the causal-policy counts
  `8,256,65536,0`.
- At `N=2^20`, all `2097152` orientation-extremum equalities, `1048576`
  all-prefix lag ledgers, and `2097152` recursive/window equalities pass.  The
  `512` parity-window safety cases and the `17`-site counterexample also pass.
- Source locks: `33/33`; all eight declared Git objects exist.  The
  bibliography has nine entries and nine unique cited keys, with zero
  dangling or orphan citations.  The repository-locked ARS proof/integrity
  audit has no remaining blocker or minor.
- Individual archive: `22` publication members plus `33` external inputs,
  zero failures.  The four-volume replay remains `4` volumes, `73` members,
  `1548` dependency hashes, `8` result hashes, `361` numbered sources, and
  zero failures; the MVP2 suite remains `7/7`.
- PDF: `8` pages and `262139` bytes, with all `20` font entries embedded.
  Ghostscript, text extraction, full LaTeX/BibTeX log scans, semantic-PDF
  identity, isolated recompilation, and all `8/8` rendered pages pass.
- No shift-two Chowla theorem, adaptive-capacity convergence, unrestricted
  memory optimum, intrinsic operator, trace, zero identification,
  Hilbert--Polya object, or RH claim is made.  Gates A--E remain false/open.

RH-378 final hashes:

```text
main.tex
ebc5cb3eaf33ad2ecf1d65c3ab202a4ea6d23bbbbeeecc685ac65cbf1ea10ff0

PDF
562687110524fb3e6dd0784256bc28ab7e9dc4403f432f6b3b9fafb995b323b3

result
31c546f308453e155e203e717e50b7dea560fbe57bbe88a81524ab34736ed83f

schema
0a3f226f61228030eb0eb26ed44a8f3caef46dca1395137904a2a1e2ba61fbf0

manifest
dc8386048291d43558685c0fd068eb754865e07f0c1e01774a541443eb483e0f

verification
0e75c96a8dd01e2ea7e0d1c2b23618ddc07b9ea336ba6294df62ba22ecc509ce
```

Final RH-379 audit:

- Tests: `15/15`; complete `result.json` regeneration is byte-identical,
  every one of the twenty-eight source digests is recomputed, JSON duplicate
  keys are rejected, and the recursively closed Draft 2020-12 schema
  validates with zero errors.
- The exact certificate exhausts `512` local tables and the `192`
  phasewise-`c_11=0` rows, checks all `262144` ordered reflection-neighbor
  pairs, ten `q|720` density-aggregation fixtures, twelve density
  normalizations, six small clocks, four larger exact clocks, three
  square-clock run rows, and four cofinal lift/decomposition rows.  All pass.
- Source locks: `28/28`; all five declared Git objects exist.  The
  bibliography has six entries and six cited keys with zero dangling or
  orphan citations.  ARS integrity, reviewer, formatter, and post-seal proof
  audits report zero blocker and zero minor.
- Individual archive: `28` publication members plus `28` external inputs,
  zero failures.  The four-volume replay remains `4` volumes, `73` members,
  `1548` dependency hashes, `8` result hashes, `361` numbered sources, and
  zero failures; the MVP2 suite remains `7/7`.
- PDF: `9` pages and `373809` bytes, with all `23` font entries embedded.
  Ghostscript, text extraction, LaTeX/BibTeX log scans, semantic-PDF byte
  identity, and all `9/9` rendered pages pass.  There are no warnings,
  undefined references, overfull/underfull boxes, or rerun notices.
- No active phase-weighted shift-two cancellation, finite-clock attainment
  or nonattainment, adaptive-capacity convergence, intrinsic operator,
  prime-power trace, zero identification, Hilbert--Polya object, RH claim, or
  Gate A--E conclusion is made.

RH-379 final hashes:

```text
main.tex
c5d97a227398a4f1d46a39fdec73ffb86aeb9bfc0f16296be7023b187b497090

PDF
a5cf5b0a80354e7d0d3d3b55023440a7631af2c6c4a36d5e4c579df898f5555f

result
a209b922ad6235263bb5213d090a2fb0ad0bcfdd0168788e64115b33d95a4ca8

schema
0af712350369e3f7e4a51ce5a8ee1179928e9397372b7b1040183dc3668406df

manifest
56d63973f4f1db11c15e5ccc9b1bc7051df6c572f5422bf03020208f0bf8b29d

verification
bea3911afd9d1e43b842ec4d9abfa78ece0b8f5c9e92d4e744c146c0fe590fc7

integrity audit
2136d7531c4dc88198293b9b7d30210c0caac1b6e9f4ee9fb5c14b0ce6a11e64

review audit
214162877e2457e473f72dd4a6d768f2fa40075b20c6314e7e6ef6042556fde7
```

Final RH-380 audit:

- Tests: `15/15`; complete `result.json`, dependency manifest, and archive
  verification regeneration are byte-identical.  The recursively closed
  Draft 2020-12 schema validates with zero errors, and duplicate JSON keys
  are rejected.
- The exact certificate checks three direct run rows, twenty-four per-run
  deletion fixtures, four prime-adjoining transitions, all three frozen
  increment anchors, nine same-support refinements, `10152` fine-residue
  `delta/theta` scaling identities, `121428` generic three-state max-plus
  comparisons, seven arbitrary-clock/lcm-gap fixtures, and the `Q=180`
  new-prime negative control.  All pass without an ambiguous comparison.
- Source locks: `24/24`; all four declared Git objects exist and every locked
  live file is byte-identical to its declared release blob.  ARS integrity,
  proof, reviewer, formatter, numerical, and post-seal release audits report
  zero blocker and zero content minor.
- Individual archive: `28` publication members plus `24` external inputs,
  zero failures.  The four-volume replay remains `4` volumes, `73` members,
  `1548` dependency hashes, `8` result hashes, `361` numbered sources, and
  zero failures; the MVP2 suite remains `7/7`.
- PDF: `8` pages and `371156` bytes, with all `24` font entries embedded,
  subsetted, and Unicode-mapped.  Ghostscript, text extraction, LaTeX/BibTeX
  scans, semantic-PDF byte identity, and all `8/8` rendered pages pass.
  Hand-written staged files pass whitespace/EOF checks; the generated TeX
  `main.log` is excluded from the repository diff-check by established
  project convention.
- No `Delta_y` monotonicity, general cover saturation, nonzero phasewise
  `c_11` cancellation, growing clock, adaptive-capacity convergence,
  intrinsic operator, prime-power trace, zero identification, Hilbert--Polya
  object, RH claim, or Gate A--E conclusion is made.

RH-380 final hashes:

```text
main.tex
6110b876e1b31fe79e7ff72e5058d97179575cf1dccce86e8c7c0a049d57451f

PDF
813206ae797072ca258e27e6afaf5d077f7f0203db72dcd224754cc49ab5fbcc

result
e7e6bc2acc46b9346e2fdd90306e9f8c5fb18c193ed0601466bbf4e01a92be33

schema
62bb03f0e61043bdeda0bf49afcbc0877d95115ca677e7cda20a73d955c5a57f

manifest
e9b66366f12fbfb22b68909bba42b8a98dbcb321630fddf1152dc7f4206a6ca3

verification
36de5a06cd8121c361335697e70892b6ad22bac0ad3910ce8c6d3226a22eb9d2

integrity audit
c2c5a3f029adcb9aa26c3fd4c3095565981718dab2dab7c05f306355ff6535d6

review audit
546d79382dce14200a6ed638e0889c98eb9427b621cb7c17f32829a4345f591b

format audit
70fbad6af9b74cd5e6712a5bff487319bb8426f63007c3896d0bf252f820a472
```

Final RH-381 audit:

- Tests: `20/20`; complete `result.json`, dependency manifest, and archive
  verification regeneration are byte-identical.  The recursively closed
  Draft 2020-12 schema validates with zero errors, duplicate keys and
  non-finite JSON constants are rejected, and the certificate is unchanged
  under optimized Python execution.
- The exact artifact checks six run/Euler rows, four finite tail-identity
  rows, and six directed interval rows at precision `60`.  The exact fixture
  is `2574` bytes; the outward interval fixture is `6851` bytes and matches
  two independent no-import reconstructions.  The `170` and `342` ledgers,
  fixed cutoff/precision, exact integer types, and digest all fail closed.
- Source locks: `25/25`; every live file is byte-identical to its declared
  release blob.  The stored source-lock object equals a fresh reconstruction,
  including unique paths, groups, commits, counts, and aggregate digests.
  ARS integrity, proof, reviewer, citation, formatter, numerical, and
  post-seal release audits report zero blocker and zero minor.
- Individual archive: `28` publication members plus `25` external inputs,
  zero failures.  The four-volume replay remains `4` volumes, `73` members,
  `1548` dependency hashes, `8` result hashes, `361` numbered sources, and
  zero failures.
- PDF: `7` pages and `339394` bytes, with all `22` font entries embedded,
  subsetted, and Unicode-mapped.  Ghostscript, text extraction,
  LaTeX/BibTeX scans, semantic-PDF byte identity, and all `7/7` rendered
  pages pass.
- No exact second-order coefficient, `p_y` asymptotic, PNT substitution,
  nonzero phasewise `c_11` cancellation, growing clock, adaptive-capacity
  convergence, intrinsic operator, prime-power trace, zero identification,
  Hilbert--Polya object, RH claim, or Gate A--E conclusion is made.

RH-381 final hashes:

```text
main.tex
b1025502880530602f134ea5bdc6dcde34e2cdfd18fb364cb104343d456b643a

PDF
0ddb244cb80d95d04c077303f6ed924f8751ef4efde8137a97cfc1830e8767ca

result
a7a869f40af0a17656b28a07fe58e337d9b8e619d13de8bc671326912f875ffd

schema
ed1788580270f03bdcbb43172edf149f086b76564697dd93e1556282855aad5b

manifest
c837578e05b27d3ac4c622da38a958aeba3adbb01985b1ce0b63bde0ed3d1521

verification
acf8b2381d76bbef5e8d1434f8c0ed3057d15ebed9f62ad4590278c25f30f19a

integrity audit
86a554d61197c0246fc00a6eea668291df183b129b82cbc89f90bfb0b90e33c1

review audit
bac2c233e689dbed5c7e67249706eb0916c581d1d7f10af14dfbfc517ef1aaf5

format audit
a68aec3f3a74d7bedcd7e8dc65721673b3bcc09f340ff79d4f35befac82706ce

replay audit
3c80624456515eccbded3ef91e6c63cd9e00bed3f969758a773728813327e633

visual audit
56990313ecd967e8412652dfe679bf3ec3c4fe448ea220c1a2f5bc84db58b11a
```

Final RH-382 audit:

- Tests: `22/22`; isolated `result.json` and recursively closed Draft 2020-12
  schema regeneration are byte-identical.  Optimized Python, ambient Decimal
  contexts, duplicate keys, non-finite constants, numeric aliases, unsafe
  paths, duplicate membership, release rebinding, source drift, and semantic
  PDF drift are all covered by fail-closed tests.
- The exact artifact checks twenty-four product-expansion rows, four
  Bonferroni rows, four quadratic/cubic telescope rows, four finite endpoint
  gap rows, and the terminal `R_8/E_9/no-E_10` ledger.  The `p=71` mutation
  changes only the memory `S_y` sign: the correct residual/bound ratio is
  `0.042746686479386`, while the wrong sign gives `7.335622869337969`.
  These rows reproduce and attack the proof; they are not a finite fit.
- Source locks: `33/33`, grouped `7/8/8/8/2`; every live file is
  byte-identical to its declared release blob.  The aggregate digest is
  `7b62b7e77ad313a52a07851e700aff197c2cc4bc3d910c6a464cd3cec0b55cb6`.
  Independent mathematical, manuscript, numerical, integrity, and post-seal
  release audits report zero blocker and zero minor.
- Individual archive: `29` publication members plus `33` external inputs,
  zero failures.  The four-volume replay remains `4` volumes, `73` members,
  `1548` dependency hashes, `8` result hashes, `361` numbered sources, and
  zero failures.
- PDF: `8` A4 pages and `327524` bytes, with all `21` font entries embedded,
  subsetted, and Unicode-mapped.  Ghostscript, text extraction, complete
  LaTeX/BibTeX scans, semantic-PDF byte identity, and all `8/8` rendered pages
  pass.
- No arbitrary-order normal form, `p_y` asymptotic, PNT substitution,
  nonzero phasewise `c_11` cancellation, growing clock, adaptive-capacity
  convergence, intrinsic operator, prime-power trace, zero identification,
  Hilbert--Polya object, RH claim, or Gate A--E conclusion is made.

RH-382 final hashes:

```text
main.tex
929b4304390036843c5e4f0d165f3be45d683e36f2a7537a3a5d14ed197b5d0c

PDF
099f87a612a7b5b51ed50b05de2c6a4304d0f85efcb30e15106329767a8783ee

result
960ef6ce017ad62b6c552ed30a41b9f0c3e41a9a217ef103c4a3f812c80a71d2

schema
573b631820edd3b911b9792f9587fee07a03cf13ecefd03a6247d115cfa42394

manifest
e4e37eaf66552ce5402df2c565be3c1d682d4a01315221a89846eb3bd88def15

verification
60535bdd85f7e8303a0f7d2cb3d3ef56173f3bfccc2790d511c817714e874139

integrity audit
4955436c073210fe6dac10d41d1a9f69ef9fad52cd55f85c2c28701cb22ddc90

review audit
c049c7f4aa4c4023cbb2577d9384c82c6c7aafe21bd94a1bb7b950d1374ae5a5

format audit
1dfa00485af1672384e8ee1e1a9fe9c7af28b1350b11622abac4f74ef179f630

replay audit
e6fb1110f2dedf20a0f94d8d02fe87c87e7a403f29639d265b111673ef865ac1

visual audit
2bf180c1fb5565f42100f7624a2309f7de7ad3461759af94abc63778c76e1849
```

Final RH-383 audit:

- Tests: `25/25`; isolated result/schema regeneration and optimized Python
  execution are exact.  The artifact independently compares endpoint,
  ordered-increment, and A/F-telescope compilers and rejects all `20/20`
  genuine formula/interface mutations.
- The exact certificate is `12245` bytes with SHA-256
  `9e2742fcdb2f626909eeb528c5081c9ace5414a1e6466c15b8b6800f427b6f16`.
  It checks `67` endpoint rows, `864` A/F rows, `432` Q-labelled rows,
  `1084` gamma-labelled rows, `144` channel comparisons, `33` low-order
  bundles, the cubic and terminal ledgers, `1151` labelled `m=2` checks, and
  `804` remainder rows.  All label redundancy is declared explicitly.
- Source locks: `41/41`, grouped `7/8/8/8/8/2`; every live source equals its
  declared release blob.  The aggregate digest is
  `492100fe3b6b823a39b58cec25b0dcddf6d52c02bd1941f0978611f01a2b8db9`.
  Independent proof, symbolic, manuscript, numerical, integrity, and
  post-seal release audits report zero blocker and zero minor.
- Individual archive: `29` publication members plus `41` external inputs,
  zero failures.  The four-volume replay remains `4` volumes, `73` members,
  `1548` dependency hashes, `8` result hashes, `361` numbered sources, and
  zero failures.
- PDF: `9` A4 pages and `368911` bytes, with all `25` font entries embedded,
  subsetted, and Unicode-mapped.  Ghostscript, text extraction, complete
  LaTeX/BibTeX scans, semantic-PDF byte identity, and all `9/9` rendered pages
  pass.  Six standard declarations are present and match the audit record.
- No PNT or `p_y` rewrite, active phasewise-`c_11` cancellation, growing
  clock, adaptive-capacity convergence, intrinsic operator, prime-power
  trace, zero identification, Hilbert--Polya object, RH claim, or Gate A--E
  conclusion is made.

RH-383 final hashes:

```text
main.tex
b1030a1203685121ddc99504d0d8a5b389611b41e47a1009fea70a0215ab3bb3

PDF
a3d467a54e99b8de0ff9da796cad3423e0683115b5998517e6493f95e77592b0

result
519f585f4cf867c0d41ae674c3fb16bc0fbcf529af32131ad1afbba6692355ab

schema
8985f41cd7043b58d3b2fa9ee387bd6da4cb9d6156d3e5226acf57123674c118

manifest
f29eca0431b24ad5c453ba71c7198e01a9eec165521577eea3401e4bc71d8c90

verification
1deb5d7347c5d84070bbe048d34e50487692e80fc4d5cbbe5e1480d4bee7bab1

core
7f976ebb09374d0df339a71947e4c4dd7d49c7bc226ab05ac7de481f1e26defb

integrity audit
f8b16b31bb513751e2158af13bbc38950873cfeef26adeb20f01611a0613908a

review audit
2fd954c3610fc3a84dafa9b3f7a593e78bbe588c63db150e172a434ed5ddd543

format audit
6825342d35ee0baf734320aa0983a96a669755e60aa740593210500b6b3cca20

replay audit
07ea25fdfcf63ff5851ce1cf2c0498dee1063101de0a7c2130ab1ceb714d7de1

visual audit
8c442fb66adc1ef92fda58ccf052d2f61a5de1a6e8ebe3e074531e5164967e92
```

Final RH-384 audit:

- Tests: `20/20`; isolated result/schema regeneration, optimized Python,
  hostile Decimal contexts, official Draft 2020-12 metaschema validation,
  strict JSON, exact types, and source/provenance mutations all pass or fail
  closed as declared.
- The exact certificate is `48689` bytes with SHA-256
  `01c91e57a01de9841f282327ab2f6e1a9368e136393ddab7a2cfe6b019a519c8`.
  It checks `8` fixed-`r` constants, all `66` partitions through degree
  eight, `48` exact successor identities, `5` scale and `5` normalized-gap
  ledgers, `10` directed numerical rows, and `20/20` genuine mutations.
- Source locks: `51/51`, grouped `7/8/8/8/8/8/2/2`; every live source
  equals its declared release blob.  The aggregate digest is
  `90434e0468ecc062cb522da096a267748725b5dca8e59c642bb7711f45a3e0e4`.
  Independent source, proof, manuscript, symbolic, numerical, integrity, and
  post-seal release audits report zero blocker and zero minor.
- Individual archive: `29` publication members plus `51` external inputs,
  zero failures.  The four-volume replay remains `4` volumes, `73` members,
  `1548` dependency hashes, `8` result hashes, `361` numbered sources, and
  zero failures.
- PDF: `8` A4 pages and `366799` bytes, with all `23` font entries embedded
  and Unicode-mapped.  Ghostscript, text extraction, complete LaTeX/BibTeX
  scans, semantic-PDF byte identity, and all `8/8` rendered pages pass.
- No effective PNT rate or threshold, growing parameter or clock, active
  phasewise-`c_11` cancellation, adaptive-capacity convergence, intrinsic
  operator, prime-power trace, zero identification, Hilbert--Polya object,
  RH claim, or Gate A--E conclusion is made.

RH-384 final hashes:

```text
main.tex
f38a39739ec472c3d0c846638739e9e5cb57b6679f60f8f90ba1e2a6188186ef

PDF
87f3ef9b67af90c204907121946c1fe736573321b3eb526623f8bb9352b29f74

result
4365c693461cdc4d5d986c97e7dcf4bbfcac6ff2136e1a20779d4b4e46078c69

schema
04cac47501a66e6c82640517cc980e0efc8f5142e682dd1c1216bd6cd13cefbf

manifest
c2e06f6054f92e71fb5a2c2bb7e281c4afee3bd63b706308aab5779ae055f8a3

verification
c73facf2230e5c88cf552bd254f8f44bbc21fb96a54efe3ce7eac0ae92c11657

core
ea3473d63e25351d7bd6737eeb0bc8309dcf5f19746a89c4ced7c0d1f1713ebc

integrity audit
b0b756fe729c62d68e88f9f4653713f69f0a06fb036ff6e902dd232b6421a27d

review audit
64c8dd307ecad685cadcc5744b481817d0dfe1c001042e9a096a58f201f0f703

format audit
8a181a553117f97fde3121dc7470803210838a84251747be9eb0744505193b25

replay audit
d6591d95203e4516ac8020f8d596ddeab38d51c4420696824b9fe681cd7d18c3

visual audit
787981a0639c89c0f7aa940a9861c8c6152a00843429329c700e7927866ebd14
```

Final RH-385 audit:

- Tests: `27/27`; exact result/schema regeneration, optimized Python,
  strict JSON and exact-type validation, official Draft 2020-12 schema,
  sealed constants, source/provenance mutation checks, and archive replays
  all pass or fail closed as declared.
- The canonical certificate is `472145` bytes with SHA-256
  `3100168ed679a02c2d97496a2457ff512c2327764ca884b248ad312a6af8eea8`.
  It contains `512` truth rows, `4608` interpolation rows, `192`
  phasewise-zero tables, `24` coefficient vectors of multiplicity eight,
  and `24/24` genuine rejected mutations.
- Source locks: `67/67`, grouped `51/8/8`; every live source equals its
  declared release blob.  The aggregate digest is
  `14a401e81d5d1868a8b3148478ca26f8975d0bde08b0a0117d4808571a2c5d79`.
  Independent proof, numerical, integrity, manuscript, and post-seal release
  audits report zero blocker and zero minor.
- Individual archive: `29` publication members plus `67` external inputs,
  zero failures.  The four-volume replay remains `4` volumes, `73` members,
  `1548` dependency hashes, `8` result hashes, `361` numbered sources, and
  zero failures.
- PDF: `8` A4 pages and `385944` bytes, with all `24` font entries embedded,
  subsetted, and Unicode-mapped.  Ghostscript, text extraction, complete
  LaTeX/BibTeX scans, semantic-PDF byte identity, and all `8/8` rendered
  pages pass.
- No polynomial or unrestricted clock theorem, varying-`B` theorem, active
  phasewise-`c_11` cancellation, adaptive-capacity convergence, projective
  selector, effective threshold, intrinsic operator, prime-power trace, zero
  identification, RH claim, or Gate A--E conclusion is made.

RH-385 final hashes:

```text
main.tex
2900021c4273c572b661f0d117884f4faa149a7e945c5a4ce1243ea47ec18368

PDF
61b6949f38b21887c97115a07ed09e7155b9363ba98b7983a11412a4a1ced448

result
c4aae9e8f49ea44079ff4b4bde8acb64b007a05d310ec80986a36be3c59cf85b

schema
09ebd32d1a32d4181a5932d3afde3ee95834785f9e898877aad6dce480d6e201

manifest
27ea430ed69e1ff9cc3f59e8be4121e68d5c1ad791dee62a5eaa7808699d5447

verification
c90465137056c7430386cf3e99461d080fcc1922319a0154ed81515fc8e038a1

core
fa03003b7f14811896b156a410e1ef8106450529b5b90622cff9e6e37a76d9bc

integrity audit
afdfbb420ad721b0014e4d6b5da812f58aa991384fb097f49a4010506b292eb2

review audit
fa304dabe60bd3a531293795af3e21c81a396a37fe09d2e4adb0605d51aa39dc

format audit
b91a89f227ff9c9701e60a2b1f17865fc45d54f9dbc4d4b2fabc4b544f9d3641

replay audit
800065b36ec6a5820f9af7961d5a4228f2cc88e20a123978a598848d1a1dd3c0

visual audit
ea22b202bd3b53576edc7f26871cf7f93d98f3994ebc1ee9b5b63006ba3d2569
```

Final RH-386 audit:

- Tests: `77/77`; exact result/schema regeneration, optimized Python,
  field-level verification with the builder disabled, all `1522` scalar-leaf
  attacks, strict JSON and exact types, official Draft 2020-12 schema,
  remote-source failure modes, source identity, and archive mutations all
  pass or fail closed as declared.
- The canonical certificate is `29717` bytes with SHA-256
  `64761d3a85afdee4682982ad545d20a66d2ed69926764bcc9580e0dc8c5f8710`.
  It contains `96=16+8+66+6` oracle rows, `24/24` theorem mutations, and
  `7/7` auxiliary source/JSON attacks.
- Source closure: `59` immutable Git blobs grouped `51/8`, plus one remote
  logical Johnston--Yang lock.  Offline verification makes zero requests;
  live opt-in replay matches the PDF, source tar, and source `main.tex`
  hashes.  The remote lock-object SHA-256 is
  `d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786`.
  No external payload is redistributed.
- Individual archive: `33` publication members, `59` Git inputs, one remote
  lock, and zero failures.  The four-volume replay remains `4` volumes,
  `73` members, `1548` dependency hashes, `8` result hashes, `361` numbered
  sources, and zero failures.
- PDF: `8` A4 pages and `371254` bytes, with all `22` font entries embedded,
  subsetted, and Unicode-mapped.  Ghostscript, text extraction, complete
  LaTeX/BibTeX scans, semantic-PDF byte identity, and all `8/8` rendered
  pages pass.
- Two independent proof/release audits report zero blocker and zero minor.
  No effective first index, growing clock, active phasewise-`c_11`
  cancellation, adaptive-capacity convergence, intrinsic operator,
  prime-power trace, zero identification, RH claim, or Gate A--E conclusion
  is made.

RH-386 final hashes:

```text
main.tex
d4dcd69877b04c382ba5cdc27918f841a40709c8064908c5063fecd222552269

PDF
f05f74be2e8ad392bbba98f5488706912a0ece48e9b372ddf14b9d4e32d5de8d

result
b59fc7921ef89d556fbc81a409ada9304fafc92424b0f4a79f97aa4d57f25ff4

schema
a5f679c5ceccbb485dc526512994e0c2fa66dd94c69c8aed479599bdfb386330

manifest
11a4512c58c83c9be4b363ea37656810a3608497a2817d6b710251b8fee9ee69

verification
2cceb2aadfeea534211416e4e6dcd29af62a91733b1fff82f994a57bca42bd7b

core
c09dc16518730f88c88ed7a382c43ff5c87e76ad8f4eb3c76929ddf2438edbcf

external source lock
d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058

integrity audit
9d03e2f224a512fa742e7ae875afeb19879d1e74644f339cf0316b6ef680a578

review audit
fdf9d36fa3b06c1c52fa5df422a8b9470918c5d81a47228d4d15df2c8302fcba

format audit
6bdb51ff934f5abf86409b9b93a4e06934f528162a73984274d2558e16751aa0

replay audit
47365767d759baf0967eb5a60bc17247cf1bd01feaf58578ef561d13a0b1dfeb

visual audit
8122c2f417141cfdc675affc4f9d7a46b7a98c854e5f94a617826306a112b2c9

remote-source audit
46f70473ebc4a7b5edb2911354e00fd6847476d30de9a42fd662e04a9be4e999
```

Final RH-387 audit:

- Tests: `47/47`; exact result/schema regeneration, optimized Python,
  field-level verification with the fresh builder disabled, strict JSON and
  exact types, official Draft 2020-12 schema, remote-source failure modes,
  source identity, and archive mutations all pass or fail closed as declared.
- The canonical certificate is `10785` bytes with SHA-256
  `3c89e51662bbc2f1c7712f4205ff8cde88e9eb80636e2779d06154e914459b4b`.
  It contains `42=12+7+7+14+2` oracle rows and `24/24` genuine mutations.
- Source closure: `68` immutable Git blobs grouped `59/8/1`, plus one remote
  logical Johnston--Yang lock.  Offline verification makes zero requests;
  live opt-in replay matches the PDF, source tar, and source `main.tex`
  hashes.  The remote lock-object SHA-256 is
  `d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786`.
  No external payload is redistributed.
- Individual archive: `33` publication members, `68` Git inputs, one remote
  lock, and zero failures.  The four-volume replay remains `4` volumes,
  `73` members, `1548` dependency hashes, `8` result hashes, `361` numbered
  sources, and zero failures.
- The integration commit contains exactly `35` RH-387 files: the `33`
  publication members plus `results/dependency_manifest.json` and
  `results/archive_verification.json`.
- PDF: `6` A4 pages and `336464` bytes, with all `21` font entries embedded,
  subsetted, and Unicode-mapped.  Ghostscript, text extraction, complete
  LaTeX/BibTeX scans, semantic-PDF byte identity, clean rebuild rendering,
  and all `6/6` rendered pages pass.
- Two independent final audits report zero blocker and zero minor.  The
  `P_2`/second-order firewall, real-channel restriction, active-`c_11`,
  clock, adaptive-capacity, operator, trace, zero, RH, and Gate boundaries
  remain intact.

RH-387 final hashes:

```text
main.tex
f03d935192e9cfd122de3e85569062e836f15ef6375e9772fd114b160d0b184b

PDF
465ae4c9e6e08b47c3f69fa650cb0a92dac8457943403a5847a97a48c577c450

result
d71c69de7e5d05c5ac558a17d2a6089815334d19b43a74ecfde219affcc1e16c

schema
c90e39f473234e5e0e103dba171cc9cdfdaff9be9b88fbb9ea75059ee9429d6e

manifest
6727517f72e5cd9cebaf9443e89516252acd9a872def7be95e9e17b7a9b191dc

verification
b588459ca593fc54fc8b849a361a08206bb640bb447d2272cfdc00aa8cedc7ae

core
136ecd57027966ee8d5cad9d428c941228baf5824e5cd11e1f43b94cdc51b85e

external source lock
d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058

integrity audit
e19b5d53849d9690f8703b06e461715a4b9083cdca443aeedee420abc0f8b1c5

review audit
dde9f4fc3abcbe6afd22c9949e2abca2249509ec8a4e86473ba0a5f84abe29ac

format audit
bae52cafa1dab8b40a26f3a1adac65b4e7cce913f9ba42bc8585f06cef0ac655

replay audit
88c758b8eacab36e7c182dc6d675486f13ad98091a0395f289b3c670b5b7a00b

visual audit
3bdd50f1b74ae74c3a3c60c0f8348e68a1c0db67ecbb7be55a5bed69ee1a6a5c

remote-source audit
0a7bc0f194bf2d109d940d23325e99591786ba044157ba4853e94a851e4016d5
```

Final RH-388 audit:

- Tests: `58/58`; exact normal and optimized result/schema/manifest/report
  regeneration, independent field validation, strict JSON and exact types,
  official Draft 2020-12 schema, both remote-source failure modes, source
  identity, and archive mutations all pass or fail closed as declared.
- The canonical certificate is `14531` bytes with SHA-256
  `373d870847bb0bf134aa1eba30c5e4d2c3a01dba470af9c75ebacadd81976371`.
  It contains `56=12+7+12+7+10+8` rows and rejects `24/24` genuine
  field-level mutations; finite factorial rows are regression only.
- Source closure: `77` immutable Git blobs grouped `68/8/1`, plus the
  ordered Johnston--Yang and Maynard remote logical locks.  The logical
  input count is `79`, both default verifiers make zero requests, and both
  live opt-in replays pass.  All four external payload hashes are absent
  from the release tree and archive.
- Individual archive: `36` publication members, `77` Git inputs, two remote
  logical locks, and zero failures.  Integration commit
  `8e6f89ee1e58e67c53c5f4719c05e881107113ac` contains exactly `38`
  RH-388 files: the `36` members plus manifest and verification report.
- PDF: `10` A4 pages and `362578` bytes, with all `22` font rows embedded,
  subsetted, and Unicode-mapped.  Ghostscript, text extraction, complete
  LaTeX/BibTeX scans, semantic-PDF byte identity, and all `10/10` rendered
  pages pass.
- Two independent final audits and the incremental EOF reseal report zero
  blocker and zero minor.  The hierarchy-only necessity boundary and all
  factorial, `P_3`, complex-channel, clock, active-`c_11`, adaptive-capacity,
  operator, trace, zero, RH, and Gate firewalls remain intact.

RH-388 final hashes:

```text
main.tex
e2b04590643db06266649551f92942a1d3a261af4a8270aede017787e3392dca

references.bib
10d7ef89df233a8f8b516466d324fcd048c20053903045f26a2e867faeba04f3

PDF
e4e58fba1fbf8481ca258380d64a634fdce82ecb1811da837270e2f63f8c0da9

main.log
7e29a541e13a1d00221d6745c3ae754c21016e5eb6c9c62b5d7c0d1c83703d57

result
b80e29174e6616bc7f4c2de999069ba9d745d80d7c46f88ae8046bf2b5b41665

schema
283182d019009b282f4e653efe1dbbc4ab48510046e65ddd77ca4e9db968cbb5

manifest
107280822a7be75c1774d56d3c7622cb44ebf1de4f9fda29a34487312f93f5c2

verification
c1a7eb141aeccf01dd9d0e52829a889e2ca56ae585f9f1904b78871379025760

core
96d85b44d905d35015450f8d196a52a6ecbe0a79857dce49d4a188ca74c43432

Johnston--Yang external source lock
d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058

Maynard external source lock
9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba

integrity audit
6414ad6d4365e9c6edd0fa3b3738e87bd7be9f6e2d27a351cd77e3de39b0f36d

review audit
428e3bbee2ab8957e232f51b610626ce0811226d4255dd332ed1e8c108afcdd8

format audit
0f41a4b4982622b6c896774e7219beac2281ecd3bf4081f7ec9863ebd7c4071a

replay audit
52679e4192c63c32749c0052bcd7fb8fcfc2feac080f4f05cdcbdb9f90023430

visual audit
ac3b9dd6c90549a6f95c7c250ce6e8a692869383c6e424ae70a654aa51aac06a

remote-source audit
a713384ac17bb2a86a59acd9949700276d4355702b8e49cc805397c6704e803f
```

## 8. Continuation prompt

````text
Continue RH research in /root/math/prime_dynamics_theory. Treat the
repository as the sole source of truth. Read AGENTS.md, RH_HANDOFF.md, and
the RH-388 README, UPDATED_ROADMAP, THEOREM_LEDGER, result.json, and main.pdf
completely. Retain RH-362 as the return-rank input, RH-363 as the entropy
tower, RH-364 as the weighted survivor/prime-copy input, RH-365 as the
return-bouquet input, RH-366 as the Möbius-correlation input, RH-367 as the
boundary-aligned cyclic-Ulam input, RH-368 as the parity-factor capacity
input, RH-369 as the branch-symmetric Markov/Gibbs input, RH-370 as the
fold-compatible Ulam/spike input, RH-371 as the exact eight-run/cyclic-pair
capacity input, RH-372 as the bounded graph/transducer certificate input,
RH-373 as the composite-clock capacity-floor input, RH-374 as the square-clock
Euler-product family input, RH-375 as the all-finite-clock one-site supremum
input, RH-376 as the shift-two Chowla/run-density boundary input, RH-377 as
the mixed-exponent run-hierarchy/two-envelope input, RH-378 as the
safe-window/online-transducer input, RH-379 as the phasewise Chowla-free
memory-supremum input, RH-380 as the square-clock monotonicity and
finite-clock nonattainment input, RH-381 as the prime-square-tail
rate/quadratic-remainder input, RH-382 as the two-scale
second-order/cubic-remainder input, RH-383 as the exact Euler-tail
partition-normal-form input, RH-384 as the prime-tail scale-separation input,
RH-385 as the fixed-polylogarithmic-clock phasewise-memory uniformization
input, RH-386 as the Vinogradov--Korobov growing-order prime-tail
uniformization input, RH-387 as the all-order prime-tail integral-resummation
input, RH-388 as the rank-one `P_2`-scale resummation and bounded-gap
necessity input, RH-MVP2 as the corpus umbrella, and RH-361 as the physical
endpoint.
Run git status --short --branch and git pull --rebase origin main before any
state change. Re-run the four-volume outer archive before integrating a new
paper.

RH search is breadth-first. Generate bold candidates, then evaluate each by
Route A for standalone theorem value and Route B for exact RH data-type
compatibility. Issue GO, STOP_SCOPED, or NOT_TESTABLE; do not create a paper
number only to maintain output velocity.

RH-388 is the current independent trigger-5 theorem edge and does not close
any physical Gate.  Put `x=p_y`, `L=log x>=512`, `c in {1,...,7}`, and for
every integer `1<=K<=floor(3L)` define

```text
V=L^(3/5)(log L)^(-1/5),
epsilon_x=0.027L^1.801 exp(-0.1853V),
K_r=x^(1-2r)/[(2r-1)L],
a_r=1/[(2r-1)L],
S_K(a)=sum_(j=0)^(K-1)(-1)^j j!a^j,
I_(2r)^[K]=K_rS_K(a_r),
Psi_c^[K]=cP_1(y)+sum_(r>=2)c^rI_(2r)^[K]/r.
```

For the exact endpoint map `F`, retain

```text
pi^2 abs(Gap_P-Gap_K)
 <=x^(-3)/L[7560epsilon_x+1638/x^2+1176K!/(3L)^K],
lim_(y->infinity) max_(1<=K<=floor(3log p_y))
 abs(Gap_P-Gap_K)/P_2(y)=0.
```

The exact `P_1` term is never smoothed in this positive theorem.  The full
integer window is paid by `b_(K+1)/b_K=(K+1)/(3L)<=1`, not by the finite
fixtures.  Maynard's bounded consecutive gaps and exact succession give

```text
limsup_y p_y^2 abs(P_1-I_2)>=1/2,
limsup_y p_y^2 pi^2 abs(Gap_P-Gap_I)>=X_infinity,
limsup_y p_y^2 pi^2 abs(Gap_P-Gap_J)>=X_infinity.
```

Keep this necessity statement restricted to the frozen `P/J/I` hierarchy.
Do not infer factorial-series convergence, a larger `K` window, a universal
surrogate obstruction, `P_3` or cubic precision, complex channels,
simultaneous prime-index/prefix limits, growing clocks, active `c_11`,
adaptive capacity, operators, traces, zeros, RH, or Gate conclusions.

RH-387 remains the preceding all-order absolute resummation theorem.  Its
`126/3528/588` endpoint transfer is valid, but its actual-gap source error is
larger than `P_2`.  RH-388 pays that scale only by retaining exact `P_1` and
transferring ranks `r>=2`; do not rewrite this rank separation as a direct
RH-387 corollary.

RH-386 remains the preceding growing-order theorem edge.  Put `x=p_y`,
`L=log x`,

```text
V=L^(3/5)(log L)^(-1/5),
epsilon_x=0.027L^1.801 exp(-0.1853V).
```

For every nonempty finite partition `lambda=1^k_1 2^k_2 ...`, retain

```text
d=sum_r r k_r,
R=max{r:k_r>0},
H=sum_r k_r/(2r-1),
H_2=sum_r k_r/(2r-1)^2,
abs(log(P_lambda/M_lambda)+H/L)
 <=14d epsilon_x+d/(x^2-1)+2H_2/L^2.
```

The finite ledger assumes `L>=512` and `7R epsilon_x<=1/2`.  Under
`d_y epsilon_(p_y)+d_y/p_y^2->0`, these hold eventually, the exact- and
power-kernel ratios tend to one, and the elementary leading ratio tends to
one if and only if `H_y/L_y->0`.  For finite nonempty families `F_y`, put
`D_y=sup_(lambda in F_y)d(lambda)<infinity` and
`H_y^*=sup_(lambda in F_y)H(lambda)<infinity`.  If
`D_y epsilon_(p_y)+D_y/p_y^2->0`, exact- and power-kernel convergence is
uniform over `F_y`, and leading convergence is uniform if and only if
`H_y^*/L_y->0`.  The convenient sequence-level sufficient conditions are
`log d_y=o(V(L_y))` and `H_y=o(L_y)`.  For one factor,
`log R_y=o(V(L_y))` is uniform, and the fixed-delta window is
`R_y<=exp((0.1853-delta)V(L_y))` only for `0<delta<0.1853`.  For every fixed
`c>0`, the all-ones family `1^floor(cL_y)` tends to `exp(-c)`.

Keep the endpoint strict, retain the negative Stieltjes boundary, and do not
drop the exact `d/(x^2-1)` or `H/L` terms.  The Johnston--Yang source is a
versioned remote logical lock; its PDF and source tar are not redistributed.
Do not infer an effective first index, growing clock, active `c_11`, adaptive
capacity, operator, trace, zero model, RH statement, or Gate conclusion.

RH-385 remains the preceding independent trigger-5 theorem edge and does not close
any physical Gate.  For every fixed `B>0`, with
`H_B(N)=floor((log N)^B)`, it proves

```text
sup_(1<=q<=H_B(N), f in F_q)abs(S_N(q,f)-L_q(f)) ->0,
sup_(q<=H_B(N))abs(G_N(q)-G(q)) ->0,
max_(q<=H_B(N))G_N(q) ->B_infinity.
```

The class `F_q` is exactly the RH-379 universally safe phasewise-`c_11=0`
class.  For every integer cutoff `P>=2`, retain the all-finite estimate

```text
abs(S_N(q,f)-L_q(f))
 <=4sqrt(Q)D_*(N)/N+13tau_P+6Q/N+4/N,
Q=lcm(q,(product_(p<=P)p)^2).
```

Keep `B` fixed; call `Q` a valid common period, not a minimal period; and
define the square-clock diagonal only after clock `36` is admissible.  Do not
extend this to `B=B(N)`, polynomial or unrestricted clocks, active `c_11`,
the adaptive capacity, a projective selector, an effective threshold, or any
Gate object.

RH-384 remains the preceding prime-tail scale edge.  For every fixed integer
`r>=1`, it proves

```text
P_r(y)=sum_(p>p_y)(p^2-1)^(-r)
      ~1/[(2r-1)p_y^(2r-1)log p_y],
T_y^3=o(S_y),
S_y=o(T_y^2).
```

It proves the fixed-partition scale dictionary and five normalized gap
limits.  Limits below first order subtract exact `A T_y`, and the `S_y`-scale
limits subtract exact `A T_y+B T_y^2`; never replace those terms by bare-PNT
surrogates.  The certified positive numerator is
`1.5463476716710499204<=Y_infinity-2m_infinity<=1.5484488989771761113`.
Keep every `q_y` fixed before `N->infinity` and every `r` and partition fixed
before `y->infinity`; do not claim an effective threshold, uniform growing
parameter, active nonzero phasewise `c_11`, `q(N)`, or adaptive-capacity
convergence.

RH-383 remains the preceding exact-normal-form edge.  It proves the
absolutely convergent endpoint/partition compiler, all-order `m=2`
cancellation, the RH-381/RH-382 low layers, a new cubic block, and
`abs(R_(D,y))<=(92/(3pi^2))(7T_y)^(D+1)` for every exact integer `D>=1`.
Do not replace partition length by degree, the strict successor tail by the
current tail, or claim RH-383 itself proved the RH-384 PNT scale dictionary.

RH-382 remains the preceding two-scale edge.  It proves the exact expansion

```text
B_infinity-G(q_y)
 =(2X_infinity/pi^2)T_y
  +((Y_infinity+2m_infinity)/pi^2)T_y^2
  +((Y_infinity-2m_infinity)/pi^2)S_y+R_y,
abs(R_y)<=3301T_y^3/(6pi^2)<551T_y^3/pi^2.
```

Do not call the finite `p=71` mutation the proof, suppress `S_y`, change its
memory sign, invent `E_10`, or claim RH-382 itself proved the RH-383
arbitrary-order normal form.

RH-381 remains the preceding prime-square-tail edge.  It proves
`abs(B_infinity-G(q_y)-(2X_infinity/pi^2)T_y)<=342T_y^2/pi^2` and the positive
normalized gap limit inside the same fixed-clock class.  Do not call its
quadratic bound an exact second-order coefficient or claim RH-381 itself
proved the RH-382 two-scale expansion.

RH-380 remains the preceding finite-clock edge.  It proves the all-order
even-run recurrence, exact square-clock increment, strict monotonicity of
`G(q_y)`, separator-specific same-prime-support saturation, and
`G(q)<B_infinity` for every fixed finite clock in the RH-379 class.  Do not
call `Delta_y` monotone, replace the separator theorem by a general cover
law, or claim RH-380 itself proved the RH-381 tail rate.

RH-379 remains the preceding phasewise-memory edge.  It proves fixed-phase
cancellation for `c_11(r)=0`, the complete `512/192` census, subset-first
canonical reduction, the exact three-state cyclic max-plus optimizer, strict
memory gains at fixed clocks, the positive vanishing square-clock correction,
and `sup_(q finite)G(q)=B_infinity`.  Do not extend it to active nonzero
`c_11(r)`, a growing clock, the RH-377 envelope, or adaptive-capacity
convergence.

RH-378 remains the preceding safe-window/online-transducer edge.  It proves
the exact compatible-block safety test, the complete `512/13` `q=1`
lag-table classification and rank-five endpoint ledger, two fixed four-state
machines realizing the two capacity orientations, the deterministic
single-policy obstruction, and the scoped length-`15`
realization/minimality theorem.  Keep the seven unconditional tables separate
from the six shift-two-Chowla-hard tables.  Do not call the two machines one
online optimizer, extend either minimality statement beyond its declared
model, treat the `17`-site word as Möbius, or infer capacity convergence.

RH-377 remains the preceding mixed-hierarchy edge.  It proves the exact
all-prefix mixed identity, the unconditional laws
`H_(k,0)/N->e_k/2` and `H_(k,1)=o(N)`, the simultaneous sixteen-density to
thirteen-aggregate equivalence, and
`K_N/N=2r_0+2(U_N+abs(V_N))/N+o(1)`.  Do not call the `466 -> 13` formal rank
an arithmetic minimality theorem, infer separate aggregate limits from one
sign, promote the conditional Euler constant, treat the stationary ternary
witness as Möbius, or claim that the envelope or capacity converges.

RH-376 remains the preceding shift-two theorem edge.  It proves the exact
common-endpoint identity
`4C_(sigma,2)=Q_2+sigma U_2+sigma V_2+D_2`, the unconditional asymptotics
`Q_2/N->kappa_2` and `U_2,V_2=o(N)`, and the equivalence between existence of
either signed two-site interval density and ordinary shift-two Cesaro Chowla.  The density,
if it exists, is `product_p(1-2/p^2)/4` for both signs.  Do not call the
interval a maximal exact-length-two run, turn the logarithmic rigidity input
into unconditional natural cancellation, claim convergence or
nonconvergence, or infer the eight-run envelope or `K_N/N` limit.

RH-375 remains the preceding all-clock one-site edge.  For every fixed finite
clock it proves the exact squarefree-density weighted phase MWIS `F(q)`,
clock-divisibility monotonicity, special same-prime-support square-clock
saturation, and the nonattained supremum `B_infinity`.  The period need not
be minimal.  Do not replace the special `4`/`9` zero-split proof by a general
cover-MWIS law, introduce `q(N)`, or promote the result to memory or adaptive
capacity convergence.

RH-374 remains the preceding square-clock family edge.  It proves the exact
fixed-`q_y` values `B_y`, strict prime-adjoining monotonicity, and the
Euler-product floor.  Keep its run formula restricted to `1<=j<=7` with
`R_8=P_yE_8` separately, and fix `y` before `N->infinity`.

RH-373 remains the preceding fixed-certificate edge.  For every fixed finite
clock it proves the independent phase-selector correlation formula, and at
q=180 it gives `liminf K_N/N >= 97/(24*pi^2)`.  Do not promote this prescribed
arithmetic witness to an all-clock optimum, the adaptive capacity limit, or a
memory-dependent correlation theorem.

RH-372 remains the preceding bounded-resource edge.  It proves exact finite
graph max-plus DP, a universal-safe transducer/one-site theorem, and three
finite certificates.  Do not promote fixed-resource enumeration to an
all-SFT classification or apply its one-site formula to memory-dependent
labels.

RH-371 remains the preceding independent edge.  It proves the exact all-prefix
eight-run reduction and a cyclic pair-ledger obstruction described below.  Do
not promote either result to a capacity-limit theorem, an open-prefix pair
identity, or an arithmetic trace.

RH-370 remains the preceding independent edge: it proves exact finite folding
for mirror-compatible partitions, an `L^1` bridge only outside the unit
circle, and a deterministic standard-BV spike barrier.  Do not promote the
finite quotient to a continuum resonance, apply it to arbitrary grids,
specialize positive noise to zero, or call the spike rows asymptotic evidence.

RH-371's eight-run identity is an all-prefix theorem, but it does not prove
run-density convergence or the existence of the Mobius capacity limit.  Its
period-18 words are synthetic and match pair data only cyclically; their
open-prefix ledgers differ.  Do not present this scoped obstruction as a
Mobius counterexample, a nonexistence theorem, or a trace/determinant model.

RH-365 is an independent trigger-5 theorem edge and does not close any
physical Gate. It proves exact midpoint compression, the two-sided height
scale log a_n=Theta(2^(n/2)), the all-order envelope
T_n<=log_2(30)n2^(ceil(n/2)-2), the zero-free disk |z|<2^(-1/2), odd-prime
primitive/logarithmic anchors, and the naive-direct-sum noncompactness
theorem. Do not identify a raw coefficient [z^ell]Z_0 with c_ell, promote the
odd-prime anchors to a composite-order Zsigmondy theorem, claim the exact
radius or a natural boundary, or identify the bouquet with a full H_p zeta,
Hasse--Weil factor, canonical operator, or von-Mangoldt trace.

RH-366 is an independent trigger-5 theorem edge and does not close any
physical Gate. It proves fixed-periodic and Parry-almost-sure Möbius
orthogonality, an offline Möbius-adapted correlation 4/pi^2, exact Parry
covariance with `0 <= V_N <= sqrt(5)N`, and the exact O(N) capacity bracket
`4/pi^2 <= liminf K_N/N <= limsup K_N/N <= 6/pi^2`. Do not promote offline
coding to spontaneous arithmetic coupling, the finite capacity plateau to a
limit, the conditional Chowla consequence to an unconditional theorem, or
any orbit average/variance to a prime-power trace or Riemann-zero model.

RH-367 is an independent trigger-5 theorem edge and does not close any
physical Gate. It proves exact aligned finite-Ulam block/sign inheritance and
the crossing-cell identity `4h theta(1-theta)` for the declared PCF map. Do
not promote the finite `-1` mode to an isolated continuum resonance, the
phase scan to an asymptotic law, or fitted noisy slopes to a universal
`sqrt(sigma)` theorem.

RH-368 is an independent trigger-5 theorem edge and does not close any
physical Gate. It proves the exact finite capacity and all-order
`K_N^(2)/N -> 4/pi^2` for the distinct PCF parity factor `A_{\{2\}}`.
Do not identify this with RH-366's distance-two capacity, claim an inclusion
between the two languages, promote the endpoint row to asymptotic evidence,
or turn the adaptive optimizer into a nonadaptive orbit or canonical trace.

RH-369 is an independent trigger-5 theorem edge and does not close any
physical Gate. It proves exact stationary, covariance, fixed-parameter
almost-sure Möbius, and finite-variance laws for the derived family `P_t` on
the RH-366 graph. Do not call `t` geometrically selected, claim a common
full-measure set or uniform endpoint theorem, make the conditional Chowla
density unconditional, or identify the covariance with a prime trace.

RH-388 is complete; do not rewrite it as the next candidate.  Its exact
rank-one retention, higher-rank factorial resummation, full moving-`K`
window, bounded-gap necessity theorem, two remote source locks, release
archive, and two independent final audits are closed.  No post-RH-388
breadth audit has yet assigned RH-389.  Run that audit before creating
another number, and require a genuinely new source-backed theorem rather
than a repackaging of the RH-388 `P_2` ledger or its hierarchy-only
obstruction.

RH-387 remains complete as the preceding all-order absolute-resummation
theorem.  Its strict source/power kernels and `126/3528/588` endpoint
transfer are closed; do not erase the exact-rank separation that makes the
RH-388 scale theorem possible.

RH-386 remains complete as the preceding source/growing-order theorem.  Its
remote source gate, finite-partition family quantifiers, sharp `H/L`
criterion, and release archive are closed; do not conflate those finite
relative-logarithm statements with RH-387's all-order absolute resummation.

TPC-137 does not reopen active `c_11`: it proves fixed-periodic terminal
logarithmic cancellation, not ordinary Cesaro or growing-period uniformity.
Safe active profiles can have every odd minimal period, and the `q=1`
ordinary shift-two Chowla blocker remains.  RH-366 likewise gives each fixed
logarithmic saving separately, so no prescribed super-polylogarithmic or
polynomial clock window is licensed.  A non-effective diagonal with a
stepwise exponent tending to infinity is a direct RH-385 corollary, not a new
edge.  Preserve the immutable four-volume foundation and Gates A--E while
these active-`c_11` and clock routes remain stopped.

Do not call the RH-364 prime lift a finite-field reduction, Hasse--Weil
factor, or full H_p zeta. Do not promote the entropy tower, weighted Euler
samples, bouquet coefficients, or adaptive Mobius coding to a Riemann-zero
model. Keep the four-volume foundation immutable and Gates A--E false/open
until their exact definitions are proved.
````
