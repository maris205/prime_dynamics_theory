# RH Research Handoff

Status date: 2026-07-28

Current completed endpoint: RH-241

Completed research batch: RH-232 through RH-241

Research batch commit:
`891565e599833f237576197f93eee88280a4f03e`

This is the compact entry point for a fresh Codex chat. The repository,
not an old chat transcript, is the source of truth.

## 1. Fresh-session protocol

Work in:

```text
/root/math/prime_dynamics_theory
```

At the start of the next batch:

```bash
git status --short --branch
git pull --rebase origin main
```

Read only these compact entry points before opening older papers:

- `RH_HANDOFF.md`
- `papers/RH-241-ten-layer-trace-envelope-frontier-review/README.md`
- `papers/RH-241-ten-layer-trace-envelope-frontier-review/UPDATED_ROADMAP.md`
- `papers/RH-241-ten-layer-trace-envelope-frontier-review/results/trace_envelope_frontier_review.json`
- `papers/RH-241-ten-layer-trace-envelope-frontier-review/main.pdf`

Start the next result-driven batch at RH-242. The provisional batch endpoint
is RH-251, but each actual theorem, obstruction, or numerical finding decides
the next paper. Stop after ten genuine papers, or earlier at a genuine route
stop requiring user direction.

### Chat and delegation discipline

- Use one fresh chat per ten-paper batch.
- After ten papers, update and push `RH_HANDOFF.md`, report the compact result,
  and let the user run `/new`.
- The primary chat retains only conclusions, route choices, theorem
  boundaries, blockers, and final audit/publication summaries.
- Delegate long source scans, large numerical logs, build logs, archive
  inspection, and page-by-page PDF review to subagents. They should return
  compact verdicts, exact counts, hashes when useful, and actionable blockers.
- State-changing edits and final integration remain coordinated by the primary
  agent so concurrent workers do not overwrite one another.
- Do not reconstruct a result from chat memory when a repository artifact is
  available.
- Another session works on TPC directories. Preserve all unrelated untracked
  caches/checkpoints, stage only the current RH batch, and pull/rebase both
  before committing and immediately before pushing.

## 2. Program objective and claim boundary

The project is developing a conditional prime-dynamics route inspired by the
Hilbert--Polya program. It is not a proof of the Riemann Hypothesis.

The macro gates are:

- **Gate A:** construct and identify a canonical intrinsic dynamical spectral
  determinant.
- **Gate B:** complete the non-self-adjoint dynamics to a time-oriented
  scattering or unitary object.
- **Gate C:** obtain a genuine self-adjoint generator and derive an intrinsic
  `T log T` counting law.
- **Gate D:** derive prime-power traces with von Mangoldt weights.
- **Gate E:** prove equality of the resulting spectral divisor with the
  divisor of the completed zeta function.

All five gates remain open. The active work is still inside Gate A. No paper
in the completed batch constructs a Hilbert--Polya operator, identifies
Riemann zeros as eigenvalues, proves a zeta-divisor equality, or implies RH.

## 3. Exact decision after RH-241

Current route coordinate:

```text
projection_free_relative_det2_open_uniform_trace_envelope
```

Next target:

```text
all_order_cloud_extracted_periodic_trace_envelope_with_coefficient_anchor
```

The route decision is:

1. The direct Euclidean biorthogonal Riesz projector exists at every archived
   finite endpoint but is catastrophically ill-conditioned. It is not a
   usable uniform small-noise route in the present norm.
2. Positive radial shell gaps cannot repair this by themselves; a strict
   2-by-2 theorem shows that fixed spectral gaps coexist with unbounded
   nonnormal projector norms.
3. The regularized determinant survives because a finite selected eigenvalue
   multiset factors `det_2` exactly without using a projector.
4. Divergent Hilbert--Schmidt/Frobenius mass is not a determinant obstruction.
   Nilpotent and direct-sum theorems show that arbitrarily large nonnormal
   singular-value mass can be invisible to every power trace and to `det_2`.
5. The useful complement variables are therefore the cloud-extracted power
   traces, not the whole-complement Hilbert--Schmidt norm.
6. Orders 2 through 12 are small and dual-channel coherent, but fixed finite
   jets cannot imply a normal entire family. This insufficiency has an exact
   zero-free entire-function counterexample.
7. RH-240 proves the correct sufficient theorem: a uniform all-order envelope
   `|tau_n(sigma)| <= M q^n` gives a locally bounded, zero-free normal relative
   `det_2` family on `|z| < 1/q`, with an explicit finite-head/uniform-tail
   convergence bound.
8. Two obligations remain inseparable: prove the all-order envelope and prove
   a coefficient anchor showing that the moving cloud removes only the
   singular factor rather than swallowing the intended deterministic
   numerator.

## 4. Compact conclusions from RH-232 through RH-241

- **RH-232:** exact biorthogonal projector and principal-angle formula.
  All 32 finite candidates exist, but projector norms range from about
  `40.75` to `2.260997172167218e12`; 17 exceed `1e6`.
- **RH-233:** exact fixed-gap nonnormal counterexample and contour-resolvent
  bound. Radial gaps are not pseudospectral certificates. Minimum archived
  gap/projector ratio: `6.3983e-16`.
- **RH-234:** exact projection-free finite `det_2` factor, reciprocal-divisor
  statement, and local root-stability estimate. All 6,144 product checks pass;
  maximum discrepancy: `1.8311e-15`.
- **RH-235:** exact nilpotent and nontrivial direct-sum separation of trace
  spectrum from Hilbert--Schmidt mass. Maximum archived `|tau_2|` is
  `0.1295196`, versus HS-squared upper `308.7520`; largest ratio is `2.36e6`.
- **RH-236:** 384 endpoint/order trace cases through order 12, computed without
  a complement eigendecomposition. Maximum unit-disk jet is `0.0759200`;
  fine-scale maximum is `0.0106624`; global observed root rate is `0.3598883`.
- **RH-237:** finite logarithmic-jet metric, radius-transfer theorem, and
  dual-channel audit. All 16 unit-disk comparisons pass `0.02`; maximum
  distance is `0.0141455`.
- **RH-238:** exact first-admissible shell selector and parameter-monotonicity
  theorem. The rule `epsilon_sigma = sigma` succeeds at 32/32 endpoints;
  ranks range from 5 to 38; minimum slack is `4.728e-5`.
- **RH-239:** exact finite-jet contraction and exact no-finite-jet normality
  theorem. All 30 adjacent and 16 channel triangle bounds pass, while actual
  adjacent errors are not monotonically contracting.
- **RH-240:** exact geometric trace-envelope normality theorem and quantitative
  coefficient-to-determinant convergence estimate. The first uncontrolled
  order is 13; the all-order hypothesis is not yet proved.
- **RH-241:** ten-layer review and revised Gate-A roadmap. Aggregate finite
  ledger: 7,280 items; identity failures: 0.

## 5. Route firewall and reopening triggers

Do not silently return to stopped or insufficient shortcuts:

- **Direct Euclidean Riesz route:** dormant unless a genuinely new adapted
  function space, interval overlap bound, or uniform contour-resolvent theorem
  is supplied.
- **Radial-gap shortcut:** ruled out as a standalone implication by RH-233.
- **Whole-complement Hilbert--Schmidt route:** too strong and bypassed; its
  failure is not evidence that the determinant route fails.
- **Fixed finite-jet extrapolation:** insufficient by RH-239, regardless of
  how attractive orders 2--12 look.
- **Numerical geometric fits:** descriptive only; they cannot be promoted to
  the all-order envelope.
- **Adaptive residual near zero:** proves finite compressibility, not the
  correct deterministic normalization. A separate coefficient anchor is
  mandatory.

A negative result should be published as a scoped route obstruction. It must
not be promoted to global nonexistence unless the theorem actually has that
scope.

## 6. Selected route for RH-242 through RH-251

Begin RH-242 by deriving an exact finite-noise periodic-loop representation
for the cloud-extracted traces `tau_n(sigma)`. The proof obligation is not
merely a new numerical atlas: it must expose where the selected cloud is
removed and which cancellations survive uniformly in both orbit length `n`
and noise `sigma`.

The provisional result-driven sequence is:

1. exact periodic-loop formula for cloud-extracted traces;
2. cloud subtraction at the loop or generating-function level;
3. independent short-orbit coefficient anchor for the deterministic
   numerator;
4. cancellation-preserving grouping of periodic contributions;
5. uniform long-orbit majorant in a justified noise--order regime;
6. rigorous gluing of a certified finite head to the analytic tail;
7. anchored adaptive selection rather than zero-target selection;
8. outward validation of the finite head in both discretization channels;
9. application of RH-240 to obtain a locally uniform relative determinant;
10. a ten-layer review deciding whether local Gate-A progress is genuine.

Let actual results reorder or split these papers. If an absolute loop bound
recreates the RH-229 Hilbert--Schmidt wall, test grouped cancellation before
stopping. If neither an all-order grouping nor an independent anchor is
available, record the exact first missing theorem and stop for user direction
instead of manufacturing additional finite-order variants.

## 7. Review and publication audit

The RH-232--RH-241 batch is committed at:

```text
891565e599833f237576197f93eee88280a4f03e
```

Final compact audit:

- 194 committed files and 15,698 inserted lines;
- 25/25 tests passed across all ten paper directories;
- 10/10 individual publication archives verified with zero failures;
- batch archive verified 172 files for RH-232 through RH-241 with zero
  failures;
- all ten PDFs compile successfully, with page counts
  `4,3,4,3,3,3,4,3,4,6` (37 pages total);
- final LaTeX logs contain no errors, undefined citations/references, empty
  bibliography warnings, or overfull boxes;
- semantic PDFs and `main.pdf` are both committed for every paper;
- aggregate scientific ledger contains 7,280 finite items and zero identity
  failures;
- the research commit was rebased over concurrent TPC work and pushed with
  `HEAD...origin/main = 0 0` at completion.

The PDFs were compile/log audited in the primary session. A future formal
publication pass may still delegate full page-by-page visual inspection and
independent claim review.

## 8. Reproduction notes

Use the shared environment and avoid generating new cache noise:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
```

The order-12 sparse trace atlas takes about one minute and can use substantial
memory at the 4096-dimensional endpoint. Prefer archived JSON for ordinary
route planning; rerun expensive experiments only when a new claim depends on
reproduction.

For the full current review, use:

```text
papers/RH-241-ten-layer-trace-envelope-frontier-review/
```

The immediate next action in a fresh session is RH-242: periodic-loop
realization of the cloud-extracted trace sequence, with the all-order envelope
and coefficient anchor kept as separate explicit theorem obligations.
