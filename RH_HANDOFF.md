# RH Research Handoff

Status date: 2026-08-01

Current completed endpoint: RH-341

Completed research batch: RH-332 through RH-341

Research batch publication commit:
`6e1478a1a02ff4c3308e829727f8fea1cfbce52c`

The repository, not an old chat transcript, is the source of truth.

## 1. Continuation protocol

Work in `/root/math/prime_dynamics_theory`.

Before the next state-changing paper:

```bash
git status --short --branch
git pull --rebase origin main
```

Read these entry points completely before older papers:

- `AGENTS.md`
- `RH_HANDOFF.md`
- `papers/RH-341-ten-layer-actual-first-alias-replacement-frontier-review/README.md`
- `papers/RH-341-ten-layer-actual-first-alias-replacement-frontier-review/UPDATED_ROADMAP.md`
- `papers/RH-341-ten-layer-actual-first-alias-replacement-frontier-review/results/result.json`
- `papers/RH-341-ten-layer-actual-first-alias-replacement-frontier-review/main.pdf`

The default RH-342 investigation is the common-clock physical signed
completion problem.  It must work on the corrected RH-334 Hardy full-trace
data type and the strict prefix `2 <= n < 4k`, and it must estimate an actual
combined signed complement, the actual head defect, or the remaining
off-alias aggregate.  An abstract completion, a finite fit, or another
inactive criterion does not by itself authorize RH-342.

The alternative legitimate route is a direct aggregate theorem for

```text
g_sigma(z) = sum_(n>=2) (tau_(sigma,n)-a_n) z^n/n
```

on one certified annulus `1.4 < rho < r_H*lambda`.  RH-300 proves that a
vanishing `H-infinity` or `H2` norm there would close the direct weighted
prefix.  No such actual noisy annular theorem is currently proved.

### Codex agent pipeline

The durable orchestration rules are in `AGENTS.md` and the descriptive role
profiles are in `.codex/agents/`.

- The primary agent is the RH project lead and the only route, handoff, git,
  integration, and publication owner.
- At most three subagents run concurrently: `rh-source-lock`,
  `rh-proof-auditor`, and one exclusive `rh-paper-writer` after a primary
  `GO`.
- Once a draft exists, `rh-release-qa` replaces one read-only station; it is
  not a fourth concurrent subagent.
- Read-only scouting for RH-(N+1) may overlap the RH-N writer, but RH-(N+1)
  is not activated until RH-N creates the required theorem edge.
- Subagents return compact evidence, exact counts, and executable blockers.
  They never commit, push, modify `RH_HANDOFF.md`, or edit overlapping paper
  directories.
- As long as a repository-backed route exists, continue without requesting
  per-paper approval.  Stop with `STOP_SCOPED` or `NOT_TESTABLE` when the
  exact route conditions fail; do not manufacture the next number.

Preserve unrelated untracked caches, checkpoints, LaTeX intermediates, and
all TPC work.  Stage only the active RH paper/batch, its archive metadata,
approved agent configuration, and this handoff when a batch closes.

Pull with `git pull --rebase origin main` before every commit and again
immediately before every push.

## 2. Program objective and claim boundary

The project develops a conditional prime-dynamics route inspired by the
Hilbert--Polya program.  It is not a proof of the Riemann Hypothesis.

- Gate A: canonical intrinsic dynamical spectral determinant.
- Gate B: time-oriented scattering or unitary completion.
- Gate C: genuine self-adjoint generator and intrinsic `T log T` law.
- Gate D: von Mangoldt-weighted prime-power traces.
- Gate E: equality with the completed-zeta divisor.

All five gates are false/open.  No paper in RH-332--RH-341 constructs a
Hilbert--Polya operator, identifies Riemann zeros, proves a von Mangoldt trace
formula, proves completed-zeta divisor equality, or implies RH.

The inherited typed branch ledgers, in coordinate order

```text
(head, bridge, tail, target, boundary)
```

remain

```text
noisy modulus spectrum       = (true, false, true,  true, true)
graded monodromy counterloop = (true, true,  false, true, true)
weighted cross-branch glue   = false
complete count               = 0
```

Their coordinatewise maximum is not a legal certificate.  The noisy
spectral complement and graded counterloop still belong to different
determinant decompositions.

The deterministic target inputs are now exact and all-order:

- RH-263 proves the deterministic numerator coefficient anchor at every
  order;
- RH-267 proves `|a_n| < 48 q_*^n` for every `n>=2`;
- RH-268 proves `a_n/q_*^n -> 1` and the sharp target radius.

This closes only the deterministic target inputs.  It does **not** close the
RH-241 moving cloud-extracted uniform envelope, the no-over-extraction
coefficient bridge, any moving noisy coefficient theorem, or Gate A.  Finite
tables reproduce formulas only; they are never promoted to physical or
all-order asymptotics.

## 3. Decision after RH-341

Current route coordinate:

```text
synchronized_actual_first_alias_signed_completion_open
```

Use the physical natural clock and common cut

```text
k = log(1/sigma)/(2 log(lambda)) + O(1)
eta_sigma = k - log(1/sigma)/(2 log(lambda))
H_k = k R^(-2k),                    R = 7/5
u = 4k,                             prefix 2 <= n < u
```

The corrected Hardy full-trace constituent is, for every `n>=2`,

```text
q_(sigma,k,n) = B_n + S_n + R_n + P_n - A_(k,n).
```

The direct modulus-complement coefficient and the noisy-head/counterloop
defect satisfy

```text
p_n = tau_(sigma,n)-a_n = q_n-d_n,
d_n = h_(sigma,n)-s_(k,n).
```

For the nonnegative weighted prefix budgets,

```text
P_u = sum_(2<=n<u) |p_n| R^n/n,
E_u = sum_(2<=n<u) |q_n| R^n/n,
D_u = sum_(2<=n<u) |d_n| R^n/n,
```

RH-340 proves exactly

```text
|P_u-E_u| <= D_u.
```

At `u=4k`, the noisy and deterministic analytic tails vanish.  The remaining
same-clock sufficient input for the RH-288 prefix leaf is

```text
D_(4k) -> 0,
E_off,(4k) -> 0,
q_(sigma,k,2k) = o(H_k).
```

None of these three limits is proved.

RH-338 and RH-339 isolate mandatory physical boundary-orbit atoms at orders
`2k` and `2k-2`.  Direct prefix closure would force

```text
C_k^0-d_(sigma,k,2k) = D_k^orb + o(H_k),
C_k^--d_(sigma,k,2k-2) = D_(k-1)^orb + o(H_(k-1)).
```

The required relative precisions are respectively
`o((beta R)^(-2k))` and `o((beta R)^(-2(k-1)))`.  A proof that takes separate
absolute values of orbit, diffuse, and head pieces contains a divergent
two-atom submajorant and is `STOP_SCOPED`.

RH-341 proves an information-class underdetermination theorem: the currently
proved identities and atom scales admit an abstract cancelling completion
and an abstract noncancelling completion.  These are algebraic signed ledgers,
not two physical noisy operators.  Consequently neither aggregate physical
closure nor nonclosure follows without a new moving-order physical theorem.

## 4. Compact conclusions from RH-332 through RH-341

- **RH-332:** The actual repelling-return second hybrid row has an exact
  physical formula and strictly positive order-`sigma` coefficients in both
  repelling orientations.  Exponential and `o(sigma)` accuracy are false, and
  a moving source gives an order-one obstruction to a global uniform row
  bound.  This is a local retained-row theorem, not a two-leg or cyclic trace
  theorem.

- **RH-333:** The canonical raw mass-one full-line forward affine reference
  has a strictly positive retained-preclosing-path `L1` escape gap on every
  fixed first-alias phase.  Hence its `O(k sigma)` and `o(H_k)` retained-path
  comparison fails.  Endpoint closure, cyclic bridges, Doob transforms,
  truncated/folded references, and cyclic traces remain `NOT_TESTABLE`.

- **RH-334:** Absolute-value folding gives the corrected physical basepoint
  localization and exact signed/folded trace identity.  The old positive-`x`
  localization fails already at order two.  The exact five-slot object is a
  Hardy full-trace constituent; it is not the modulus complement without the
  head defect `d`.

- **RH-335:** The parity Riesz projector defines a real signed cell measure
  and an exact localized ledger, but its cell allocation is a frozen gauge
  among infinitely many zero-total extensions.  The adapted-norm physical
  upper-exponent route remains `STOP_SCOPED/NOT_TESTABLE` because the required
  all-leg and trace-observation upper bounds are absent.

- **RH-336:** The projector-gauge cell must be exponentially small to be
  target-negligible, and a fixed finite partition has a super-target
  maximizing cell.  A positive row-stochastic isospectral family preserves
  every power trace while moving corrected cells.  This is nonphysical finite
  algebra and does not decide physical signed cancellation.

- **RH-337:** The exact RH-329 rational clock is strictly faster than the
  physical algebraic clock, so its phase tends to minus infinity and it is
  rejected as a bounded-phase comparator.  On the correct clock, available
  relative `o(1)` remainders are exponentially too weak; target-scale
  parity--alias replacement remains `NOT_TESTABLE`.

- **RH-338:** The corrected physical critical far slot contains a canonical
  negative boundary-orbit atom of alias size and super-target normalized
  magnitude.  Aggregate far closure requires diffuse signed compensation at
  exponentially small relative error.  No aggregate far verdict follows.

- **RH-339:** Every one-alias cut contains the lower sideband `2k-2` and its
  own super-target physical boundary-orbit atom.  Off-alias closure requires
  signed compensation at that order.  The fully signed coefficient and
  `E_off` remain `NOT_TESTABLE`.

- **RH-340:** Reapplying the exact mass bound at `u=4k` closes both analytic
  tails on the physical clock.  The exact prefix synchronization inequality
  reduces the remaining problem to the critical, off-alias, and head budgets.
  Both orbit compensation equations are necessary, while a separate-absolute
  orbit/diffuse/head proof is impossible.

- **RH-341:** The ten-layer review normalizes the entire chain, keeps RH-241
  moving noisy obligations distinct from the later deterministic target
  theorems, and proves abstract signed-completion underdetermination.  It
  records ten scoped conclusions, zero discharged aggregate physical
  replacement obligations, and all Gates A--E false.

## 5. Route firewall and actual reopening triggers

Do not promote the batch beyond its hypotheses:

- A sharp local hybrid row is not an all-cycle trace theorem.
- A retained probability path is not a cyclic trace observation.
- A frozen projector gauge or isospectral matrix family is not a physical
  noisy quadratic operator.
- The RH-329 wrong-clock scalar family cannot test physical bounded-phase
  replacement.
- A mandatory negative orbit atom is not a lower bound for the fully signed
  coefficient.
- Closing the critical order does not close `E_off`.
- Closing the full-trace prefix does not close the separate head/counterloop
  budget unless `D_(4k)->0` is proved on the same clock.
- An abstract completion is a logical insufficiency witness, not a physical
  construction.
- Tail closure and an inactive criterion do not activate RH-288 or Gate A.

Admissible reopening inputs are:

1. A physical moving-order theorem for
   `X_k^0=C_k^0-d_(sigma,k,2k)` proving the critical compensation or a
   nonzero `H_k`-normalized failure.
2. A physical moving-order theorem for
   `X_k^-=C_k^--d_(sigma,k,2k-2)` proving the lower-sideband compensation or
   a nonzero `H_(k-1)`-normalized failure.
3. An alias-inclusive theorem for the remaining signed off-alias weighted
   background on the strict prefix `n<4k`.
4. Actual noisy-head/counterloop transport proving `D_(4k)->0` in the same
   Hardy normalization, or a genuine physical obstruction.
5. A direct aggregate annular theorem for `g_sigma` on one certified
   `1.4<rho<r_H*lambda` annulus.
6. Only after the direct prefix and both analytic tails close in one physical
   determinant data type may RH-288 be activated; Gate A still separately
   requires a canonical intrinsic physical determinant.

If a positive route fails, publish only a theorem-backed local obstruction,
an explicit physical counterexample, or a precise `NOT_TESTABLE` stop.  Do
not fill the next paper with another finite fit, wrong-clock comparator,
nonphysical similarity family, separate absolute majorant, or restatement of
an inactive criterion.

## 6. Default RH-342--RH-351 signed-completion route

This is a research order, not advance authorization for ten paper numbers.
Each number activates only after the preceding theorem edge exists.

1. **RH-342: Common-Hardy noisy-head/counterloop source lock.**  Freeze the
   actual head and counterloop coefficient types, ranks, aliases, and strict
   prefix on `u=4k`; prove an exact transport interface or a source-backed
   identification obstruction.
2. **RH-343: Alias-inclusive head-defect transport.**  Seek an actual
   zero-padded root, Fourier, contour, or aggregate norm theorem strong enough
   for `D_(4k)->0`; otherwise prove a sharp information-class or physical
   obstruction without claiming actual divergence.
3. **RH-344: Critical combined-complement decomposition.**  Freeze the
   corrected physical components of `X_k^0` before evaluation and isolate the
   diffuse families that could compensate the critical orbit atom.
4. **RH-345: Critical signed compensation theorem or obstruction.**  Prove
   `X_k^0=D_k^orb+o(H_k)` or a nonzero target-normalized failure in the actual
   data type.
5. **RH-346: Lower-sideband combined-complement decomposition.**  Repeat the
   exact physical freeze at `2k-2`, including the radial sideband and all
   remaining corrected cells.
6. **RH-347: Lower-sideband signed compensation theorem or obstruction.**
   Prove `X_k^-=D_(k-1)^orb+o(H_(k-1))` or a genuine target-normalized failure.
7. **RH-348: Punctured one-alias aggregate.**  Control the rest of
   `E_off,(4k)` without separate absolute splitting, or isolate an additional
   physical sideband obstruction.
8. **RH-349: Joint same-clock prefix theorem.**  Combine head, critical, and
   off-alias results only if they share the identical clock, cutoff, and Hardy
   coefficient type.
9. **RH-350: Determinant-gluing activation audit.**  Apply RH-288 only if the
   direct prefix and both tails are proved in one physical determinant data
   type; otherwise publish the exact inactive leaf.
10. **RH-351: Ten-layer signed-completion frontier review.**  Audit the unique
    positive, negative, or still-open coordinate and update this handoff.

The direct annular route may supersede several intermediate layers if a
genuine actual theorem is found.  Conversely, failure of RH-342 source
identification stops the numbered pipeline; it does not authorize a paper
that merely repeats `NOT_TESTABLE` without a new strict conclusion.

Checkpoint stops:

- After RH-343: no actual head transport means no claim that `p` and `q`
  prefixes are asymptotically equivalent.
- After RH-345: no critical signed verdict means determinant prefix closure
  remains open regardless of off-alias progress.
- After RH-347: no lower-sideband signed verdict means `E_off` remains open.
- After RH-348: closing two selected orders does not close the remaining
  weighted background.
- At RH-350: determinant gluing activates only when every RH-288 hypothesis
  is present on one physical data type.

## 7. Reproduction and publication audit

Use the shared environment and avoid new cache noise:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
```

Final RH-332--RH-341 audit:

- Tests: 135/135 passed across ten independent directories, with per-paper
  counts `12,14,17,17,20,11,11,11,12,10`.
- RH-341 result regeneration is deterministic and its tests compare generated
  layer data directly with the executable review ledger.
- Individual archives: 10/10 verified with zero failures.  RH-332--RH-340
  contain 15 publication files each; RH-341 contains 19.
- Batch archive: 154 publication files, zero failures.
- The ten controlled paper trees contain 176 files after individual and batch
  archive metadata.
- PDFs: page counts are `7,6,8,6,5,5,5,4,5,5`, for 56 pages total.
  All 10 semantic PDFs are byte-identical to `main.pdf`; all have extractable
  text.
- Ghostscript parsed 10/10 PDFs.  All 185 reported font rows are embedded.
- All ten LaTeX logs have zero warnings, undefined citations/references,
  rerun notices, and overfull/underfull boxes.
- Page-level review of RH-341 found no clipping, overlap, blank-page anomaly,
  formula/table overflow, footer conflict, or rendering defect.
- Strict JSON parsing passed for 32/32 result/archive files with no duplicate
  keys or nonfinite values.
- The nine upstream result files contain 45 false Gate values; RH-341 adds
  five more, for 50/50 false.
- Unrelated caches, checkpoints, LaTeX intermediates, and TPC work remain
  untracked and unstaged.

RH-341 result SHA-256:
`916ba23910e1125284097bf91fa706e921e169da9192b66d9296a8a05b506e64`

RH-341 PDF SHA-256:
`161e887bf0f9d5df1c4bd111c9f36f3030b7facc3eedcb8ff8a86b36f75f272a`

RH-332--RH-341 batch manifest SHA-256:
`b349d2e792dfc3215a27d6d2ce35e692bee6d34dc493c884f6043bbaf0376e2e`

The compact review is
`papers/RH-341-ten-layer-actual-first-alias-replacement-frontier-review/`.

## 8. Continuation prompt

```text
Continue RH research in /root/math/prime_dynamics_theory.  Treat the
repository as the sole source of truth.  Read AGENTS.md, RH_HANDOFF.md, and
the RH-341 README, UPDATED_ROADMAP.md, result.json, and main.pdf completely.
Run git status --short --branch and git pull --rebase origin main.  Begin with
a read-only RH-342 source lock on the actual noisy-head/counterloop defect at
the physical cut u=4k and the corrected RH-334 Hardy coefficient type.  Use
the primary agent plus at most three subagents: source lock, adversarial proof
audit, and one exclusive paper writer only after GO; replace one station with
release QA after a draft.  Create RH-342 only if the repository supports an
exact transport theorem, a genuine physical obstruction, or another strict
scoped result.  Do not turn the RH-341 abstract completions into physical
operators, do not use RH-329's wrong clock, do not split mandatory atoms from
their signed complements by separate absolute values, and do not activate
RH-288 or Gates A--E without every exact hypothesis.
```
