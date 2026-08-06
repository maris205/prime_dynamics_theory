# RH Research Handoff

Status date: 2026-08-06

Current completed endpoint: RH-367

Completed research batch: RH-352 through RH-367

Post-four-volume independent theorem edges: RH-362 through RH-367

Latest route verdict: RH-367 Route A `GO`; Route B `STOP_SCOPED`

Prior RH-352--RH-361 publication commit:
`91167fe163831d3360b4c4007ed600865610e9ec`

RH-366 integration commit:
`0396fab97bbe3348c8237f8734dec0e1893fd3bf`

RH-367 integration commit: recorded by the release commit that adds this
handoff entry and the RH-367 publication package.

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
- `papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/README.md`
- `papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/UPDATED_ROADMAP.md`
- `papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/THEOREM_LEDGER.md`
- `papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/results/result.json`
- `papers/RH-367-boundary-aligned-cyclic-ulam-phase-leakage/main.pdf`
- `papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/README.md`
- `papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/UPDATED_ROADMAP.md`
- `papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/THEOREM_LEDGER.md`
- `papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/results/result.json`
- `papers/RH-366-mobius-orthogonality-adaptive-encoding-and-parry-covariance/main.pdf`

Retain RH-362 as the return-rank input, RH-363 as the entropy-tower input,
RH-364 as the weighted-survivor/prime-copy input, RH-365 as the unweighted
return-bouquet input, RH-366 as the Hénon Möbius-correlation input, RH-367 as
the boundary-aligned cyclic-Ulam input, and RH-361 as the immediate endpoint
of the still-open original physical branch.

For corpus-level synthesis or new-route selection, also read completely:

- `papers/RH-MVP2-corpus-frontier-synthesis/README.md`
- `papers/RH-MVP2-corpus-frontier-synthesis/CROSSWALK.md`
- `papers/RH-MVP2-corpus-frontier-synthesis/THEOREM_LEDGER.md`
- `papers/RH-MVP2-corpus-frontier-synthesis/results/summary.json`
- `papers/RH-MVP2-corpus-frontier-synthesis/main.pdf`

RH-367 does not automatically activate RH-368. The next breadth-first source
lock must compare the remaining external theorem packages, especially a
common strong-space projector/resolvent bridge for cyclic Ulam data and the
capacity-limit/nonadaptive-measure continuations of the certified Hénon
Möbius package, against the completed RH-1--RH-367 corpus. RH search
remains breadth-first: generate bold source-backed candidates, evaluate
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

RH-362 through RH-367 add a separate arithmetic-dynamical branch. RH-362
builds one marked modular cycle per prime; RH-363 inserts the resulting ranks
into a pairwise-coprime admissible-shift tower; RH-364 derives weighted
analytic domains for a certified local survivor and audits an engineered
prime-copy operator; RH-365 proves an analytic disk and odd-prime primitive
anchors for the unweighted marked bouquet; RH-366 proves a periodic/Parry
Möbius-orthogonality dichotomy, an offline adaptive correlation, exact Parry
covariances, and an open capacity bracket on that survivor; RH-367 proves the
exact aligned finite-Ulam block/sign inheritance and crossing-cell phase
defect for a cyclic postcritically finite quadratic map. None is identified
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

## 4. Compact conclusions from RH-352 through RH-367

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
RH-367. Triggers 1--4 remain untouched. RH-365 closes the natural
return-bouquet height/radius route at its declared scope, RH-366 closes the
declared periodic/typical/capacity audit, and RH-367 closes the declared
finite-Ulam alignment/phase-defect audit. For RH-368 and later, the shortest
exact candidates are:

1. A common strong-space projector/resolvent theorem that genuinely connects
   the RH-367 finite-Ulam family to a declared continuum operator. Without
   this bridge, no spectral limit may be inferred from phase scans.
2. A capacity-limit theorem (or a rigorous nonexistence/scoped negative) for
   `lim K_N/N` under the distance-two constraint. Pair correlations alone do
   not control this nonlinear maximum-weight functional.
3. A nonadaptive-measure theorem identifying geometrically or dynamically
   selected invariant measures, beyond Parry, for which a quantitative
   Möbius theorem holds without reading the arithmetic sequence.
4. A general constraint-graph classification of mixing subshifts admitting
   explicit arithmetic-adapted points and graph-dependent capacity brackets.
5. A genuine composite-order primitive-divisor upgrade, such as an eventual
   Zsigmondy theorem or a `p`-adic lifting bound strong enough to force new
   primes. No such theorem is present in the locked source.
6. A sharp return-rank multiplicity theorem strong enough to determine the
   exact origin radius or a genuine boundary law for `Z_0`. RH-365 supplies
   only the bracket `[2^(-1/2),1]`.
7. A quantitative finite-entropy-data theorem that certifies or excludes a
   finite prime/rank prefix without promoting numerical conditioning to exact
   infinite recovery.
8. An intrinsic pressure/transfer/groupoid operator producing the entropy
   tower without inserting every modulus by hand.
9. One of the original physical triggers 1--4.

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

The only fresh candidate is the boundary-aligned cyclic-Ulam structural
package at
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

## 8. Continuation prompt

```text
Continue RH research in /root/math/prime_dynamics_theory. Treat the
repository as the sole source of truth. Read AGENTS.md, RH_HANDOFF.md, and
the RH-367 README, UPDATED_ROADMAP, THEOREM_LEDGER, result.json, and main.pdf
completely. Retain RH-362 as the return-rank input, RH-363 as the entropy
tower, RH-364 as the weighted survivor/prime-copy input, RH-365 as the
return-bouquet input, RH-366 as the Möbius-correlation input, RH-367 as the
boundary-aligned cyclic-Ulam input, RH-MVP2 as the corpus umbrella, and RH-361
as the physical endpoint.
Run git status --short --branch and git pull --rebase origin main before any
state change. Re-run the four-volume outer archive before integrating a new
paper.

RH search is breadth-first. Generate bold candidates, then evaluate each by
Route A for standalone theorem value and Route B for exact RH data-type
compatibility. Issue GO, STOP_SCOPED, or NOT_TESTABLE; do not create a paper
number only to maintain output velocity.

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

For the next breadth-first source lock, investigate the RH-367 roadmap in
order: (i) a common strong-space projector/resolvent theorem connecting the
finite-Ulam family to a declared continuum operator; (ii) existence or a
proved scoped negative for `lim K_N/N`; (iii) nonadaptive invariant measures
with quantitative Möbius orthogonality; (iv) general constraint-graph capacity
laws; (v) the composite primitive-divisor, sharp-radius, finite-entropy-data,
intrinsic globalization, cyclic-noise, and original same-clock physical
routes. Evaluate each by Route A and Route B before assigning RH-368. In
parallel retain the exact source locks and the four-volume foundation.

Do not call the RH-364 prime lift a finite-field reduction, Hasse--Weil
factor, or full H_p zeta. Do not promote the entropy tower, weighted Euler
samples, bouquet coefficients, or adaptive Mobius coding to a Riemann-zero
model. Keep the four-volume foundation immutable and Gates A--E false/open
until their exact definitions are proved.
```
