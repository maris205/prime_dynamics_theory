# RH Research Handoff

Status date: 2026-07-29

Current completed endpoint: RH-261

Completed research batch: RH-252 through RH-261

Research batch commit:
ae0752a5d5e9ac12fd0faa97e2eee273b9aad438

The repository, not an old chat transcript, is the source of truth.

## 1. Fresh-session protocol

Work in /root/math/prime_dynamics_theory.

At the start of the next batch:

    git status --short --branch
    git pull --rebase origin main

Read these compact entry points before older papers:

- RH_HANDOFF.md
- papers/RH-261-ten-layer-analytic-tail-selector-frontier-review/README.md
- papers/RH-261-ten-layer-analytic-tail-selector-frontier-review/UPDATED_ROADMAP.md
- papers/RH-261-ten-layer-analytic-tail-selector-frontier-review/results/frontier_review.json
- papers/RH-261-ten-layer-analytic-tail-selector-frontier-review/main.pdf

The next result-driven batch starts at RH-262 only after a genuinely new
reopening input. A finite fit, unbounded reweighting, or repeated frozen-window
scan is not a reopening input.

### Chat and delegation discipline

- Keep the primary chat to conclusions, route choices, theorem boundaries,
  blockers, and final audit summaries.
- Delegate long numerical experiments, source scans, build logs, archive checks,
  and page-by-page PDF review; return compact verdicts and exact counts.
- Keep state changes, final integration, staging, and commits coordinated by the
  primary session.
- Preserve unrelated untracked caches, checkpoints, and TPC work. Stage only
  the current RH batch and this handoff file.
- Pull with git pull --rebase origin main before every commit and again
  immediately before pushing.

## 2. Program objective and claim boundary

The project develops a conditional prime-dynamics route inspired by the
Hilbert--Polya program. It is not a proof of the Riemann Hypothesis.

- Gate A: canonical intrinsic dynamical spectral determinant.
- Gate B: time-oriented scattering or unitary completion.
- Gate C: genuine self-adjoint generator and intrinsic T log T law.
- Gate D: von Mangoldt-weighted prime-power traces.
- Gate E: equality with the completed-zeta divisor.

All five gates are false/open. The batch remains inside Gate A. No paper in
RH-252--RH-261 constructs a Hilbert--Polya operator, identifies Riemann zeros,
proves a zeta-divisor equality, or implies RH.

## 3. Decision after RH-261

Current route coordinate:

    legal_heads_obstructed_target_tail_exists_Ms_uncertified_quotient_finite_nonuniform_complete_certificate_zero

The RH-260 ledger has five independent obligations:

    (legal anchored head, coefficient bridge, uniform quotient tail,
     analytic target tail, certified target boundary constant)
    = (false, false, false, true, false).

Thus the current complete head--tail certificate count is exactly zero. This is
scoped to the audited finite classes and is not global nonexistence.

## 4. Compact conclusions from RH-252 through RH-261

- RH-252: RH-46 plus Hardy scaling gives the deterministic target radius
  rho*=1.42678748386407 > 1. For 0 <= R < S < rho*,
  sum_{n>=N}|a_n|R^n/n <= M_S (R/S)^N/(1-R/S). This is an exact
  all-order interface; M_S has no certified numerical upper bound. The
  convention a_1=0 is explicit.
- RH-253: The deterministic anchor dictionary extends exactly through order 28;
  order 28 enumerates 32,767 physical fixed points. The order 13--28 unit-disk
  norm is 0.0021942543215719553, the 2--28 norm is 0.496699690013014, and the
  finite root-rate fit is 0.7009986349256669. The fit is descriptive only.
- RH-254: The candidate margin expands from 16 to 32 at all 32 endpoints,
  adding 16 roots per endpoint. Maximum old/new matching error is
  7.405469102694929e-09; 21/32 windows are shell-complete and 11/32 end at a
  split conjugate pair; complete ranks are 33--64.
- RH-255: The expanded single-use shell box has 0/32 anchored passes, distance
  range 0.14358493511963313--0.42399800369340307, and maximum primal-dual gap
  5.828670879282072e-15. It excludes 62,030,604,700 eligible binary subsets
  in its margin-32 scope.
- RH-256: If P=p(A) and P^2=P, P is zero or identity on each generalized root
  space. The RH-255 consequence is limited to real, conjugate-closed
  idempotent selectors supported on the resolved RH-254 window; complex masks
  selecting one member of a conjugate pair and non-idempotent quotient
  groupings remain open. Interpolation residual is at most 7.304420162473979e-14.
- RH-257: Weighted moment germs factor as prod_j(1-lambda_j z)^(w_j);
  single-valued meromorphic continuation requires integral combined exponents.
  Arbitrary signed fits hit tolerance at 32/32 endpoints but integer fits are
  0/32, with 20--34 fractional weights per endpoint, maximum weights
  39.6394--3.0223426080311285e11, and monodromy defect essentially 2.
- RH-258: The first monodromy-legal unit-cap lattice w_j in {-1,0,1} has
  0/32 passes, distances 0.10607370900129424--0.3534900682213731, zero
  reported MILP gaps, and implicitly covers 39,417,456,084,975,216 lattice
  points. Larger caps and operator realization remain open.
- RH-259: The ordered-Schur quotient audit reaches 23 endpoints (17 inherited
  plus 6 new) through dimension 1024. All 23 C^12 powers are contractive, but
  q12 ranges from 0.22185212659640824 to 0.5056418005507071; the finite
  unit-disk tail diagnostic is 0.0005654507945432548. Nine archived endpoints,
  interval enclosures, uniform small-noise control, and the continuum bridge
  remain open.
- RH-260: The updated first-omitted-order gluing theorem adds head,
  quotient-tail, and target-tail budgets plus exponential determinant conversion.
  RH-255 and RH-258 supply 0 head passes in 64 class-endpoint cases; RH-259 is
  finite/nonuniform; RH-252 supplies target-tail existence but not M_S. Of five
  obligations exactly one is true; complete count 0; 44 source-consistency
  checks have zero failures.
- RH-261: The ten-layer review records 842 finite review records and 17 internal
  checks with zero failures, preserves every scope qualifier, and defines
  RH-262 reopening triggers. The RH-261 batch archive verifies 172 files with
  zero failures.

## 5. Route firewall and RH-262 reopening triggers

Do not promote finite data or scoped obstructions beyond their hypotheses:

- The order 13--28 target fit is not an all-order envelope.
- A truncated boundary scan is not a certified M_S.
- The RH-255/RH-258 head obstructions do not exclude larger windows, larger
  integer caps, non-conjugate complex masks, or an operator-derived
  non-idempotent quotient.
- Arbitrary fractional signed moments are not determinant selectors because of
  monodromy.
- 23 finite Schur blocks do not imply a uniform small-noise theorem.
- No Gate A--E status changes follow from a finite diagnostic.

The admissible RH-262 triggers are:

1. An interval or otherwise rigorous computable upper bound for
   M_S=sup_{|z|=S}|log G(z/r_H)| at a useful 1<S<rho*.
2. A legal invariant selector outside the audited single-use and unit-cap
   classes, with an actual cloud-to-deterministic coefficient bridge.
3. A uniform quotient block-power theorem covering the missing archived
   endpoints and the continuum bridge.
4. A larger integer-cap audit paired with an actual operator realization.

If none supplies the relevant obligations, publish the scoped route stop and
request user direction rather than implying global nonexistence.

## 6. Reproduction and publication audit

Use the shared environment and avoid new cache noise:

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider

Final RH-252--RH-261 audit:

- Tests: 35/35 passed across ten directories.
- Individual archives: 10/10 verified, zero failures; RH-252--RH-260
  manifests contain 17 files each and RH-261 contains 19.
- Batch archive: 172 files, zero failures.
- PDFs: pages 3,2,2,2,2,2,2,2,3,4 (24 total); every semantic PDF is byte
  identical to main.pdf and all ten logs have zero errors, undefined
  citations/references, empty-bibliography warnings, rerun warnings, and
  overfull/underfull boxes.
- Every result JSON explicitly keeps Gate A--E false/open.
- Unrelated untracked caches, checkpoints, LaTeX intermediates, and TPC work
  remain unstaged.

The next compact review is
papers/RH-261-ten-layer-analytic-tail-selector-frontier-review/.
Do not rerun the dimension-1024 experiment unless a new claim depends on
reproduction.

## 7. Next-session prompt

    Continue RH research. Enter /root/math/prime_dynamics_theory and run
    git status --short --branch followed by git pull --rebase origin main.
    The repository is the sole source of truth. Read RH_HANDOFF.md and the
    RH-261 README, UPDATED_ROADMAP.md, frontier_review.json, and main.pdf.
    Proceed to RH-262 only after a genuine reopening trigger: certified M_S,
    a legal selector outside audited classes with a coefficient bridge, a
    uniform quotient theorem covering missing endpoints and the continuum,
    or a larger integer cap with operator realization. Finite fits are not
    all-order theorems; Gate A--E remain false/open; do not imply a
    Hilbert--Polya operator, Riemann-zero identification, zeta-divisor
    equality, or RH.
