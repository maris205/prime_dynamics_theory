# RH Research Handoff

Status date: 2026-07-31

Current completed endpoint: RH-331

Completed research batch: RH-322 through RH-331

Research batch publication commit:
`6b994f35865a8215eb01a021ee08bf74e4eba083`

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
- `papers/RH-331-ten-layer-first-alias-frontier-review/README.md`
- `papers/RH-331-ten-layer-first-alias-frontier-review/UPDATED_ROADMAP.md`
- `papers/RH-331-ten-layer-first-alias-frontier-review/results/result.json`
- `papers/RH-331-ten-layer-first-alias-frontier-review/main.pdf`

The default RH-332 route is the second physical critical leg: a sharp
repelling-return affine-leg remainder in both sibling/fold directions.  The
paper must prove a phase-matched physical row theorem or a genuine local
scale obstruction.  It may not copy the first-leg RH-324 result by symmetry
without proving that symmetry for the physical kernel.

The alternative legitimate route remains actual fixed-order noisy-complement
transport plus endpoint coefficient-energy tightness.  Synthetic spectra,
finite-prefix fits, scalar repairs, more isolated exchange models, and
separate absolute majorants are not reopening inputs.

### Codex agent pipeline

The durable orchestration rules are in `AGENTS.md` and the descriptive role
profiles are in `.codex/agents/`.

- The primary agent is the RH project lead and the only route, handoff, git,
  integration, and publication owner.
- At most three subagents run concurrently:
  `rh-source-lock`, `rh-proof-auditor`, and one exclusive
  `rh-paper-writer` after a primary `GO`.
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

All five gates are false/open.  No paper in RH-322--RH-331 constructs a
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

The deterministic target inputs remain the all-order unified trace envelope
of RH-267 and the coefficient-anchor identities of RH-263/RH-268.  Finite
tables reproduce formulas only; they are never promoted to physical or
all-order asymptotics.

## 3. Decision after RH-331

Current route coordinate:

```text
first_alias_transfer_criterion_exact_actual_replacement_open
```

Use the moving first-alias clock

```text
k = log(1/sigma)/(2 log(lambda)) + O(1)
eta_sigma = k - log(1/sigma)/(2 log(lambda)) -> eta
H_k = k R^(-2k),                    R = 1.4
```

The exact observable five-slot convention is

```text
e_k = B_k + S_k + R_k + P_k - A_k.
```

For actual and frozen-model packets,

```text
Theta_k = Delta_B + Delta_S + Delta_R + Delta_P - Delta_A,
e_actual,k = e_model,k + Theta_k.
```

The exchange/observation split is gauge-dependent:

```text
X -> X+t,       E_obs -> E_obs-t,       S=X+E_obs unchanged.
```

Therefore actual replacement must compare the observable shell `S` unless a
physical identification map freezes the split before evaluation.

If the actual critical coefficient is identified with the packet and
`2k < h_sigma <= 4k`, RH-330/RH-331 give

```text
E_prefix = E_off + |e_actual,k|/(2 H_k).
```

Hence

```text
E_prefix -> 0
iff
E_off -> 0 and Theta_k = -e_model,k + o(H_k).
```

For a model already satisfying `e_model,k=o(H_k)`, the signed replacement
condition reduces exactly to `Theta_k=o(H_k)`.

For the failed RH-329 frozen model,

```text
e_model,k/A_k -> -(1-C_* C_M),       A_k/H_k -> infinity.
```

Actual closure would therefore need the tuned repair

```text
Theta_k = -e_model,k + o(H_k).
```

Conversely, `Theta_k=o(A_k)` would conditionally transfer its negative
divergence.  Neither actual estimate is known.

RH-331 proves only an abstract typed-ledger underdetermination result: two
signed ledger completions can have identical unsigned bounds and opposite
critical verdicts.  It does not construct two physical noisy operators and
does not assert that both abstract completions are physically realizable.

## 4. Compact conclusions from RH-322 through RH-331

- **RH-322:** For one physical folded row, the half-line pushforward has an
  exact `L1` Gaussian-tail error, the limiting profile is Lipschitz in the
  clearance parameter, all polynomial moments converge, and distinct phases
  give distinct profiles.  This is one row, not a trace law.

- **RH-323:** The oriented affine `(V,U,W)` Gaussian chain has an exact joint
  density, retained-coordinate `L1` isometry, marginal contraction, and
  extended-skew-normal output.  It is an affine probability model, not the
  physical two-leg kernel; leakage probabilities are not parity weights.

- **RH-324:** The first physical critical leg has exact fold/state-boundary
  tails, an explicit curved-to-tangent error, and a sharp strictly positive
  `O(sigma)` remainder.  Exponential affine accuracy is false.  The comparison
  `sigma=o(R^(-2k))` is only a local scale comparison.

- **RH-325:** Retaining transported incoming laws gives an exact path-Duhamel
  criterion.  If all `O(k)` rows were phase-matched `O(sigma)`, the path error
  would be `O(k sigma)=o(H_k)`.  A separate trace criterion needs a physical
  stability exponent
  `gamma < 0.3503698834605293...`.  Same-seed composability and a
  dimension-free Markov-to-trace bound are both disproved by explicit
  counterexamples.

- **RH-326:** Hardy normalization fixes the parity/counterloop/alias signs and
  yields the exact even-order convention `+P-A`.  The scalar phase ratio
  tends to `C_* C_M lambda^eta`.  Ordinary decimals are not interval
  certificates, and local probability data remain unidentified with the raw
  trace packet.

- **RH-327:** The actual basepoint-localized trace partitions exactly as
  `T=B+S+R`.  A synthetic two-state exchange/reset construction proves that
  branch-blind power data do not identify the signed shell.  The physical
  shell scale, contrast, sign, probability-to-trace observation, and signed
  far remainder remain open.  The current manuscript explicitly defines
  `f`, `Delta_k^clr`, and the fixed phase `eta`; its clearance asymptotic is an
  imported archived interface, not a new theorem of RH-327.

- **RH-328:** With physical exchange fields supplied in advance, the exact
  matching equation is

  ```text
  e = L(c_phys^(2k)-y) + E_obs + R,
  y = c0^(2k) + (A-P-B)/L.
  ```

  It gives sharp power/radius precision laws and uncertainty intervals.  A
  counterexample shows that a zero best-case reachability distance need not
  imply physical matching.

- **RH-329:** A frozen exact-rational graded exchange model with
  `L=A`, `c_iso=4/5`, `c0=3/5`, and zero boundary/observation/far slots has
  `e/A -> -(1-C_*C_M)` and `e/H -> -infinity`, even though the reachability
  screen eventually passes.  This is a strict isolated-model negative result,
  not an actual full-trace divergence theorem and not one all-order operator.

- **RH-330:** The exact actual/model identity, observable-shell gauge
  firewall, all-`4k` two-channel Duhamel expansion, sharp grouped signed
  enclosure, and RH-329 repair/no-go transfer laws are proved.  Separate
  absolute majorants are sufficient but not necessary.  Every physical
  replacement hypothesis remains inactive.

- **RH-331:** The ten-layer review normalizes the typed chain, proves the
  conditional prefix equivalence, and proves a scoped abstract typed-ledger
  underdetermination proposition.  It records zero discharged actual bridge
  obligations, weighted cross-branch glue false, complete count zero, and all
  Gates A--E false.

## 5. Route firewall and actual reopening triggers

Do not promote the batch beyond its hypotheses:

- One physical leg does not imply a two-leg or all-cycle theorem.
- Retained-path probability control does not imply cyclic trace control.
- A lower conditioning bound cannot be used as the upper bound required by
  the RH-325 trace criterion.
- The scalar parity/alias phase law is not a target-scale replacement theorem.
- The RH-327 exchange completion and RH-329 audit are synthetic/graded models,
  not identifications of the noisy operator.
- Best-case shell reachability is not physical matching.
- A scalar signed repair is not an operator construction.
- Closing the `n=2k` packet does not close `E_off`.
- Closing the one-alias weighted prefix does not close the independent noisy
  head/counterloop determinant budget.
- No Gate A--E status change follows from an inactive transfer criterion.

Admissible reopening inputs are:

1. A second-physical-leg and all-cycle phase-transport theorem at
   `O(k sigma)=o(H_k)`, or a rigorous physical obstruction.
2. A gauge-fixed observation map proving
   `q_(sigma,k,2k)=B+S+R+P-A` in one common trace data type.
3. Physical two-channel prefix/suffix stability and signed Duhamel group
   enclosures at scale `o(H_k)`.
4. Target-scale parity/alias replacement and an aggregated signed far
   remainder theorem.
5. A punctured one-alias theorem proving `E_off->0`, including neighboring
   sidebands `n=2k+j`.
6. Synchronized actual noisy-head/counterloop transport closing the separate
   determinant-gluing budget.

If a positive route fails, publish only a theorem-backed local obstruction,
an explicit physical counterexample, or a precise `NOT_TESTABLE` stop.  Do
not fill the next paper with another finite fit or a restatement of the
conditional criterion.

## 6. Default RH-332--RH-341 actual-replacement route

1. **RH-332: Sharp physical repelling-return affine-leg remainder.**
   Treat the second critical physical leg in both sibling/fold directions;
   prove the sharp phase-matched row error or a local scale obstruction.
2. **RH-333: Full boundary-cycle clearance-phase transport.**
   Propagate the common phase and incoming moments through all `2k` legs;
   target `O(k sigma)=o(H_k)` or prove a phase/stability stop.
3. **RH-334: Gauge-fixed physical first-alias observation map.**
   Freeze windows, pullback, sectors, and observation before evaluation and
   prove the actual five-slot coefficient identity, or an exact
   sector/nonuniqueness obstruction.
4. **RH-335: Adapted-norm two-sibling trace-observation stability.**
   Seek a physical upper exponent
   `gamma < 0.3503698834605293...`; do not substitute an inherited lower
   bound.
5. **RH-336: Physical signed two-channel Duhamel cancellation.**
   Retain all `4k` hybrid terms and prove a signed enclosure for
   `Delta_B+Delta_S`, or a nonzero normalized physical obstruction.
6. **RH-337: Target-scale parity--alias replacement.**
   Upgrade leading scalar laws to rigorous interval/remainder estimates
   sufficient for `Delta_P-Delta_A=o(H_k)`, or isolate a target-scale
   obstruction.
7. **RH-338: Signed far-complement trace remainder.**
   Prove aggregated `Delta_R=o(H_k)` without separate absolute summation, or
   isolate a real nonvanishing periodic-orbit family.
8. **RH-339: Punctured one-alias weighted-background theorem.**
   Prove `E_off->0` on `2k<h<=4k`, including neighboring sidebands, or prove
   a positive sideband lower obstruction.
9. **RH-340: Synchronized noisy-head/counterloop determinant gluing.**
   Close the head budget on the identical clock and activate RH-288 only if
   the critical, off-alias, and head budgets all close.
10. **RH-341: Ten-layer actual first-alias replacement frontier review.**
    Audit the unique positive, negative, or still-open coordinate, validate
    individual/batch archives, and update this handoff.

Dependency spine:

```text
RH-332 -> RH-333 -> RH-334 -> RH-335 -> RH-336
RH-337 ----------------------------------|
RH-334 -> RH-338 ------------------------|
RH-336 + RH-337 + RH-338 -> RH-339 -> RH-340 -> RH-341
```

RH-332/333, RH-337, and read-only preparation for RH-338 may be researched
in parallel.  RH-334 must freeze the observation type before RH-338 becomes
a formal replacement theorem.

Checkpoint stops:

- After RH-333: no all-leg phase theorem means no actual trace-Duhamel claim.
- After RH-335: no physical upper exponent below the threshold means RH-336
  can only seek a signed obstruction.
- After RH-338: the critical packet gets no actual verdict until the boundary,
  parity/alias, and far signed pieces share one clock and data type.
- After RH-339: a closed critical packet without `E_off->0` is not a closed
  weighted prefix.
- At RH-340: determinant gluing activates only when the critical, off-alias,
  and head/counterloop budgets all close.

## 7. Reproduction and publication audit

Use the shared environment and avoid new cache noise:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
```

Final RH-322--RH-331 audit:

- Tests: 132/132 passed across ten independent directories, with per-paper
  counts `6,6,8,8,10,12,14,38,26,4`.
- RH-331 result regeneration is deterministic and its tests compare generated
  layer data directly with `batch_status()` to prevent stale JSON.
- Individual archives: 10/10 verified with zero failures.  RH-322--RH-330
  contain 15 publication files each; RH-331 contains 19.
- Batch archive: 154 publication files, zero failures.
- The ten paper trees contain 176 RH files after per-paper archive metadata;
  the publication commit added 48 paths, including seven durable agent-policy
  files.
- PDFs: page counts are `4,4,4,4,5,6,6,5,6,4`, for 48 pages total.
  All 10 semantic PDFs are byte-identical to `main.pdf`; all have extractable
  text.
- Ghostscript parsed 10/10 PDFs.  All 176 reported font rows are embedded.
- All ten LaTeX logs have zero warnings, undefined citations/references,
  rerun notices, and overfull/underfull boxes.
- Page-level review of RH-331 found no clipping, overlap, blank-page anomaly,
  formula/table overflow, footer conflict, or rendering defect.  Earlier
  paper QA and the final batch structural checks remain archived in their
  paper state.
- All nine upstream result files contain five false Gate values; RH-331
  normalizes those 45 values and keeps its own five false, for 50/50 false.
- `AGENTS.md` and five TOML profiles parse cleanly under the installed shared
  Python/TOML environment.  The configured subagent ceiling is three.
- Unrelated caches, checkpoints, LaTeX intermediates, and TPC work remain
  untracked and unstaged.

RH-331 result SHA-256:
`a80341159525b4b6186e7506b1585f50956fded54bfb57fc50d8da1176b72f4c`

RH-331 PDF SHA-256:
`dc3f074b9ef6a3809f9156b2819d42945f998d0710e0485f8a83bfd7abe4dfdd`

RH-322--RH-331 batch manifest SHA-256:
`60fee25984ef45e85c620935342c1f0dee218ffbd30d493047e2d444fc414774`

The compact review is
`papers/RH-331-ten-layer-first-alias-frontier-review/`.

## 8. Continuation prompt

```text
Continue RH research in /root/math/prime_dynamics_theory.  Treat the
repository as the sole source of truth.  Read AGENTS.md, RH_HANDOFF.md, and
the RH-331 README, UPDATED_ROADMAP.md, result.json, and main.pdf completely.
Run git status --short --branch and git pull --rebase origin main.  Start
RH-332 on the second physical repelling-return critical leg.  Use the primary
agent plus at most three subagents according to .codex/agents/: source lock,
adversarial proof audit, and one exclusive paper writer after GO; replace one
station with release QA after the draft.  Prove the phase-matched physical
row remainder in both sibling/fold directions, including its sharp leading
coefficient, or publish a rigorous local scale obstruction.  Do not infer
the second leg from RH-324, do not identify forward probability with cyclic
trace, and do not activate RH-325/RH-330 without all their actual hypotheses.
Keep finite rows as reproduction checks, preserve unrelated TPC/cache work,
and keep Gates A--E and all Hilbert--Polya/RH claims false/open.
```
