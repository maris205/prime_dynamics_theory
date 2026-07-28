# RH Research Handoff

Status date: 2026-07-28

Current completed endpoint: RH-251

Completed research batch: RH-242 through RH-251

Research batch commit:
`37ddb33c81e8875226ffb646aac0efc3bc45467e`

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
- `papers/RH-251-ten-layer-superloop-anchor-frontier-review/README.md`
- `papers/RH-251-ten-layer-superloop-anchor-frontier-review/UPDATED_ROADMAP.md`
- `papers/RH-251-ten-layer-superloop-anchor-frontier-review/results/frontier_review.json`
- `papers/RH-251-ten-layer-superloop-anchor-frontier-review/main.pdf`

Start the next result-driven batch at RH-252.  The next route is conditional
on a genuinely new reopening input; each actual theorem, obstruction, or
numerical finding decides the next paper.  Stop earlier at a genuine route
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

## 3. Exact decision after RH-251

Current route coordinate:

```text
exact_superloop_quotient_frozen_anchor_class_obstructed_open_new_selector_uniform_tail
```

Next target:

```text
new_anchored_selector_outside_frozen_resolved_window_with_uniform_quotient_block_certificate_and_target_tail
```

The route decision is:

1. RH-242 gives an exact fixed-noise graded periodic-superloop identity for
   the cloud-extracted traces.  It is projection-free, but the counterloops
   are signed/complex and do not by themselves provide a positive majorant.
2. RH-243 independently fixes the deterministic numerator coefficient target:
   `a_n = r_H^(-n)[P_n - 1 - (-1)^n + 2 1_(2|n) lambda^(-n/2)]`.  This anchor
   is not an identification of the current moving cloud.
3. RH-245 gives the exact orthogonal quotient identity `tau_n=Tr(C^n)`;
   it uses a norm-one orthogonal projection, not the ill-conditioned Riesz
   projector.  RH-246 turns a uniform contractive block power into the needed
   geometric envelope, but its 17-endpoint diagnostic is not uniform.
4. RH-247 proves that cancellation-blind separate absolute majorants are
   superunit (`1.253165...` to `3.556834...` root rates); grouped signed
   quotient cancellations remain the only live majorant route.
5. RH-244 excludes all 543 anchored shell prefixes at all 32 frozen endpoints.
   RH-248 strengthens this to the full single-use shell zonotope: prefixes,
   contiguous intervals, binary shell subsets, and the convex box relaxation
   all have zero passes with dual certificates.
6. RH-249 shows that unbounded nonnegative shell weights create 26 formal fits
   and six failures, but require maximum weights from `40.5844` to
   `5.8018e10`; these are moment-reweighting pathologies, not legal spectral
   multiplicities.
7. RH-250 states the exact finite-head/analytic-tail gluing interface, yet the
   current complete certificate count is zero.  The all-order quotient tail,
   deterministic target tail, and coefficient bridge therefore remain open.

## 4. Compact conclusions from RH-242 through RH-251

- **RH-242:** 14,584 exact finite-noise superloops and 352 archived residuals;
  both residual signs occur at every order.
- **RH-243:** exact deterministic coefficient dictionary; anchor norm
  `0.49450543569144195`; even symmetric numerator subsequence only.
- **RH-244:** 543 frozen shell prefixes, 0/32 anchored passes; best mismatch
  range `0.39723767197524446`--`0.48457639371229216`.
- **RH-245:** 17 quotient endpoints, zero rank mismatches; maximum partition
  error `3.99e-15`, maximum archive discrepancy `6.31e-12`.
- **RH-246:** exact block-power envelope criterion; finite `q_12`
  `0.3932995547481413`, diagnostic tail at `R=1` `1.7991531976413385e-05`.
- **RH-247:** 352 separate-absolute cases, all superunit root rates
  `1.253165378203787`--`3.5568338003788416`.
- **RH-248:** 5,012 intervals and 139,572,890 binary subsets scanned in
  addition to prefixes; convex-box distance range
  `0.14649763462315904`--`0.4240179027308174`, 0/32 passes.
- **RH-249:** cone result 26 formal passes/6 failures; minimum required cap
  `40.58443731031147`, maximum `58018432630.629776`.
- **RH-250:** zero complete head/tail certificates; relaxed-head to finite-tail
  ratio `8142.588125081018`.
- **RH-251:** finite ledger 16,191 items, audit failures 0; all Gates A--E
  remain false/open.

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
- **Frozen anchored shell class:** RH-244 and RH-248 rule out the entire
  single-use prefix/interval/binary/box class in the archived candidate
  windows; RH-249's unbounded cone fits are not admissible multiplicities.
- **Separate absolute loops:** RH-247's Perron contribution forces a
  superunit rate. Any future majorant must preserve signed quotient
  cancellation.
- **Head/tail shortcut:** RH-250's interface is exact, but RH-246's finite
  diagnostic cannot be promoted to a uniform all-order theorem.

A negative result should be published as a scoped route obstruction. It must
not be promoted to global nonexistence unless the theorem actually has that
scope.

## 6. Selected route for RH-252 and later

The next paper may open only with one genuinely new input:

1. an expanded resolved candidate window with an anchored reachability audit;
2. a signed/complex selector derived from invariant quotient structure, rather
   than arbitrary shell reweighting;
3. a uniform small-noise theorem for a quotient block power; or
4. an analytic all-order tail bound for the deterministic numerator target.

The preferred coordinate is
`new_anchored_selector_outside_frozen_resolved_window_with_uniform_quotient_block_certificate_and_target_tail`.
Do not rerun zero-target prefixes or reweight the frozen window and call that
progress.  If no trigger supplies both a legal anchored head and a uniform
quotient/target tail, publish the scoped route stop and request user direction.

## 7. Review and publication audit

The RH-242--RH-251 research batch is committed at:

```text
37ddb33c81e8875226ffb646aac0efc3bc45467e
```

Final compact audit:

- 194 committed files and 14,576 inserted lines;
- 29/29 tests passed across all ten paper directories (run one directory at a
  time to avoid same-basename pytest collection collisions);
- 10/10 individual publication archives verified with zero failures;
- individual archive manifests contain 17 files for RH-242--RH-250 and 19 for
  RH-251; the batch archive verifies 172 files with zero failures;
- all ten PDFs compile successfully, with page counts
  `4,4,3,3,2,2,2,2,2,3` (27 pages total);
- final LaTeX logs contain no errors, undefined citations/references, empty
  bibliography warnings, or overfull boxes;
- semantic PDFs and `main.pdf` are both committed for every paper;
- aggregate scientific ledger contains 16,191 finite items and zero audit
  failures;
- all five macro gates remain explicitly false/open.

The primary session performed the compile, hash, log, test, and archive audit;
the delegated publication pass is an additional independent page/claim check.

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
papers/RH-251-ten-layer-superloop-anchor-frontier-review/
```

The immediate next action in a fresh session is RH-252 only after a reopening
trigger is identified; keep the all-order envelope, legal anchored selector,
and deterministic coefficient bridge as separate explicit obligations.
