# RH Research Handoff

Status date: 2026-08-05

Current completed endpoint: RH-363

Completed research batch: RH-352 through RH-361

Post-four-volume independent theorem edges: RH-362 and RH-363

Latest route verdict: RH-363 Route A `GO`; Route B `STOP_SCOPED`

Research batch publication commit:
`91167fe163831d3360b4c4007ed600865610e9ec`

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
- `papers/RH-363-prime-return-entropy-tower/README.md`
- `papers/RH-363-prime-return-entropy-tower/UPDATED_ROADMAP.md`
- `papers/RH-363-prime-return-entropy-tower/THEOREM_LEDGER.md`
- `papers/RH-363-prime-return-entropy-tower/results/result.json`
- `papers/RH-363-prime-return-entropy-tower/main.pdf`

Retain RH-362 as the immediate arithmetic input and RH-361 as the immediate
endpoint of the still-open original physical branch.

For corpus-level synthesis or new-route selection, also read completely:

- `papers/RH-MVP2-corpus-frontier-synthesis/README.md`
- `papers/RH-MVP2-corpus-frontier-synthesis/CROSSWALK.md`
- `papers/RH-MVP2-corpus-frontier-synthesis/THEOREM_LEDGER.md`
- `papers/RH-MVP2-corpus-frontier-synthesis/results/summary.json`
- `papers/RH-MVP2-corpus-frontier-synthesis/main.pdf`

RH-363 does not automatically activate RH-364. Start with a read-only source
lock. RH search is breadth-first: generate bold source-backed candidates,
evaluate standalone discovery value as Route A and RH data-type compatibility
as Route B, then issue `GO`, `STOP_SCOPED`, or `NOT_TESTABLE`. Create a new
number only for an actual bridge, a typed `q/E_off` theorem, a rigorous
physical obstruction, or another independent theorem edge. An abstract
fiber, finite fit, deterministic reparameterization, prime-labelled factor
inserted by definition, or inactive criterion is not a reopening input.

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

RH-362 and RH-363 add a separate arithmetic-dynamical branch. RH-362 builds
one marked modular cycle per prime; RH-363 inserts the resulting ranks into a
pairwise-coprime admissible-shift tower. Neither construction is identified
with either typed physical branch, so the physical blocker below is unchanged.

The deterministic target side remains exact and all-order: RH-263 gives the
deterministic numerator coefficient anchor, and RH-267--RH-268 give the
deterministic all-order envelope and sharp target radius. These results do
not close the RH-241 moving noisy all-order envelope or coefficient bridge.
RH-288 remains inactive because the complete same-type physical prefix leaf
is absent.

## 3. Decision after RH-361 through RH-363

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

## 4. Compact conclusions from RH-352 through RH-363

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

## 5. Route firewall and reopening triggers

Do not:

- call the RH-361 coefficient fiber a physical counterexample;
- promote normalized actual `p` to unnormalized `q/E_off`;
- promote deterministic `s` to an actual spectrum, root set, or rank law;
- state a conditional `D_(4k)(R)` transfer as proved;
- identify a selected window with the full prefix or `E_off`;
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

Trigger 5 is satisfied by the independent theorem edges RH-362 and RH-363.
Triggers 1--4 remain untouched. For RH-364 and later, the shortest exact
candidates are:

1. The source-locked weighted-H\'enon route at commit
   `ff44f961261349848c9f65ede6a031b7e155aca9`: prove the intrinsic
   entropy--expansion analytic domain, the common-clock prime-lift
   Schatten/Fredholm identities, and the scalar-normalization obstruction
   whose first arithmetic defect is at prime cubes, with
   `(F_1,F_2,F_3)=(1,1,4)`.
2. A natural return-bouquet height theorem combining a primitive-divisor
   coefficient anchor with a height-controlled positive analytic radius and
   all-order trace envelope.
3. A quantitative finite-entropy-data theorem that certifies or excludes a
   finite prime/rank prefix without promoting numerical conditioning to exact
   infinite recovery.
4. An intrinsic pressure/transfer/groupoid operator producing the entropy
   tower without inserting every modulus by hand.
5. One of the original physical triggers 1--4.

The weighted-H\'enon prime lift must be called a prime lift or copy, not a
finite-field reduction, Hasse--Weil local factor, or full `H_p` zeta. Its
prime and square trace weights may match after scalar normalization, but the
cube coefficient `4 log p` is already a Gate-D obstruction. Repackaging the
same marked-cycle or entropy product is not a new trigger.

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

## 7. Reproduction and publication audit

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
the RH-363 README, UPDATED_ROADMAP, THEOREM_LEDGER, result.json, and main.pdf
completely. Retain RH-362 as the arithmetic input, RH-MVP2 as the corpus
umbrella, and RH-361 as the physical endpoint. Run git status --short
--branch and git pull --rebase origin main before any state change. Re-run
the four-volume outer archive before integrating a new paper.

RH search is breadth-first. Generate bold candidates, then evaluate each by
Route A for standalone theorem value and Route B for exact RH data-type
compatibility. Issue GO, STOP_SCOPED, or NOT_TESTABLE; do not create a paper
number only to maintain output velocity.

RH-363 is an independent trigger-5 theorem edge and does not activate RH-364
automatically. The shortest source-locked candidate is the weighted-Henon
prime-lift package at commit ff44f961261349848c9f65ede6a031b7e155aca9:
intrinsic entropy--expansion analytic bounds, exact Schatten/Fredholm
regions, and the first scalar-normalized trace mismatch at prime cubes with
(F_1,F_2,F_3)=(1,1,4). Independently retain the natural bouquet-height,
finite entropy-data, intrinsic pressure-operator, and original same-clock
physical routes.

Do not call a prime lift a finite-field reduction, Hasse--Weil factor, or
full H_p zeta. Do not promote the entropy tower or positive-integer Euler
samples to a Riemann-zero model. Keep the four-volume foundation immutable
and Gates A--E false/open until their exact definitions are proved.
```
