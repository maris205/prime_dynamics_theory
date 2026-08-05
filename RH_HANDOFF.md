# RH Research Handoff

Status date: 2026-08-04

Current completed endpoint: RH-361

Completed research batch: RH-352 through RH-361

Research batch publication commit:
`91167fe163831d3360b4c4007ed600865610e9ec`

Non-numbered corpus synthesis: RH-MVP2

Synthesis publication commit:
`85269d06977fdfe52a501a8aac0104e63ad37fba`

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
- `papers/RH-361-ten-layer-signed-completion-and-upper-counterloop-review/README.md`
- `papers/RH-361-ten-layer-signed-completion-and-upper-counterloop-review/UPDATED_ROADMAP.md`
- `papers/RH-361-ten-layer-signed-completion-and-upper-counterloop-review/THEOREM_LEDGER.md`
- `papers/RH-361-ten-layer-signed-completion-and-upper-counterloop-review/results/result.json`
- `papers/RH-361-ten-layer-signed-completion-and-upper-counterloop-review/main.pdf`

For corpus-level synthesis or new-route selection, also read completely:

- `papers/RH-MVP2-corpus-frontier-synthesis/README.md`
- `papers/RH-MVP2-corpus-frontier-synthesis/CROSSWALK.md`
- `papers/RH-MVP2-corpus-frontier-synthesis/THEOREM_LEDGER.md`
- `papers/RH-MVP2-corpus-frontier-synthesis/results/summary.json`
- `papers/RH-MVP2-corpus-frontier-synthesis/main.pdf`

RH-361 does not automatically activate RH-362. Start with a read-only source
lock. Create a new number only for an actual bridge, a typed `q/E_off`
theorem, a rigorous physical obstruction, or another independent theorem
edge. An abstract fiber, finite fit, deterministic reparameterization, or
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

The umbrella manuscript has 6 pages. Its tests pass `3/3`; the local/corpus
archive verifier covers 18 publication files with zero failures; Ghostscript
parses the PDF; all 17 font rows are embedded; all six rendered pages were
visually checked; and two forced rebuilds are byte-identical. The semantic
PDF is byte-identical to `main.pdf`.

The preferred expansion, if larger thematic syntheses are useful, is to keep
RH-MVP1 for RH-1--RH-160 and derive three provenance-preserving volumes:

1. RH-161--RH-241: physical Riesz packets, temporal clouds, relative
   determinants, and the trace-envelope frontier;
2. RH-242--RH-281: deterministic numerator anchors, selectors, analytic
   tails, and counterloops; and
3. RH-282--RH-361: noisy heads, weighted/annular endpoints, first alias, and
   actual-versus-deterministic signed completion.

These would be synthesis papers, not a new unconditional theorem chain. They
must retain per-claim `PROVED`, `CERTIFIED`, `CONDITIONAL`,
`SCOPED_NEGATIVE`, and `OPEN` labels. The mathematical route coordinate stays

```text
actual_same_clock_unnormalized_head_transport_open
```

RH-362 remains inactive unless one of the theorem-backed triggers in section
5 is met.

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

The batch has two typed branches and no cross-branch bridge:

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

The deterministic target side remains exact and all-order: RH-263 gives the
deterministic numerator coefficient anchor, and RH-267--RH-268 give the
deterministic all-order envelope and sharp target radius. These results do
not close the RH-241 moving noisy all-order envelope or coefficient bridge.
RH-288 remains inactive because the complete same-type physical prefix leaf
is absent.

## 3. Decision after RH-361

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

## 4. Compact conclusions from RH-352 through RH-361

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

## 5. Route firewall and reopening triggers

Do not:

- call the RH-361 coefficient fiber a physical counterexample;
- promote normalized actual `p` to unnormalized `q/E_off`;
- promote deterministic `s` to an actual spectrum, root set, or rank law;
- state a conditional `D_(4k)(R)` transfer as proved;
- identify a selected window with the full prefix or `E_off`;
- use finite rows as physical or asymptotic evidence; or
- extend the deterministic terminal-lag sequence by reparameterization alone.

Admissible RH-362 triggers are:

1. An actual same-clock `D_(4k)(R)->0` theorem, or a genuine physical
   obstruction to it.
2. A typed actual full-trace `q` or complete `E_off` theorem.
3. An unnormalized complete direct-prefix theorem, including orders below
   the RH-354 moving cut.
4. The RH-241 moving noisy all-order envelope plus its no-over-extraction
   coefficient bridge.
5. Another independent source-backed theorem edge.

Even `D_(4k)(R)->0` would transfer only named moment/budget laws. Root, rank,
spectral-submultiset, and canonical determinant identification remain
separate. RH-288 activates only after the complete direct prefix and both
analytic tails close in one physical determinant data type.

## 6. Default RH-362 investigation

RH-362 is read-only until a theorem edge is found. Freeze:

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

For route selection, retain RH-MVP2 as the single corpus umbrella. It is the
short provenance and frontier map; it must not replace or silently concatenate
the 361 atomic sources. If a publication-scale expansion becomes useful, use
RH-MVP1 as Volume I and the three thematic ranges in section 1.1 as Volumes
II--IV. Such volumes are deferred while the purpose is to find a new theorem
edge: writing them now would improve exposition but would not change the
mathematical frontier or activate RH-362.

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

The three scans therefore return `NOT_TESTABLE` or `STOP_SCOPED`, not a
physical obstruction and not RH-362. A valid cyclic reopening must first
define a compact/folded/normalized cyclic reference in the RH-334 trace data
type and prove an all-leg observation/prefix/suffix upper bound on the physical
first-alias clock. Its first decisive correction-factor test is
`C_(sigma,k)=1+o((beta R)^(-2k))` on the complete `2k` signed path sum and
frozen basepoint window. A nonunit fixed-phase limit would support a rigorous
scoped negative; a positive result would only open the subsequent all-leg
curvature/Duhamel and stability-weight obligations. Until then keep
`actual_same_clock_unnormalized_head_transport_open`.

## 7. Reproduction and publication audit

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
d7e894ddd74b615673bf264d1950051bdd6b61e746ba8b53b19f0f909f34219a

RH-MVP2 PDF
75ed330838b7073d249eea0d01538d819d4b8fde60257792077b01b846c4f914

RH-MVP2 corpus inventory
61650327a6eb0e4b64bf2a94aed3b725927ac8d9deca4bf898a13e2660e7e907

RH-MVP2 dependency manifest
a75b3d69187670bb01ae57252f7e4643076f44bc6cb879c252dd2fab01694290

RH-MVP2 summary
b831f1a8141b853d29cdeb7dda852560bd032d77b5d187ab93a6e697504755a5

RH-MVP2 archive verification
c56fde30b784d73270cda1ce7f784e341a7cd26ddbc943242f0b237cc4b4f189
```

## 8. Continuation prompt

```text
Continue RH research in /root/math/prime_dynamics_theory. Treat the
repository as the sole source of truth. Read AGENTS.md, RH_HANDOFF.md, and
the RH-361 README, UPDATED_ROADMAP, THEOREM_LEDGER, result.json, and main.pdf
completely. Run git status --short --branch and git pull --rebase origin main
before any state change. Begin with a read-only source lock on the actual
same-clock defect d=h-s and the unnormalized D_(4k)(R) obligation.

RH-362 is not activated by RH-361 alone. Create it only for an actual bridge,
a typed q/E_off theorem, a rigorous physical obstruction, or another
independent theorem edge. Do not treat the RH-361 coefficient fiber as a
physical counterexample. Do not identify deterministic counterloop moments
with actual spectral data. Keep Gates A--E false/open until their exact
definitions are proved.
```
