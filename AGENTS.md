# Repository multi-agent research protocol

This file is the durable, scoped workflow policy for the RH and TPC research
programs that share this repository.  Dynamic mathematics, current endpoints,
open hypotheses, and next-paper triggers live in the corresponding handoff, not
in this file.

## Scope router and shared authority

- RH work on `RH_HANDOFF.md` or `papers/RH-*` follows the RH workflow below.
- TPC work on `TPC_HANDOFF.md` or `papers/tpc-*` follows the TPC workflow below.
- Repository-wide git, preservation, destructive-action, and release-ownership
  rules apply to both programs.  Where a scoped workflow is stricter, use the
  stricter rule.
- Treat repository files and committed artifacts as the source of truth.  Old
  chat text and memory may help navigation but cannot override current files.
- Only one release-owning primary session may stage, commit, rebase, or push in
  this shared repository at a time.  Preserve unrelated RH work during TPC runs
  and unrelated TPC work during RH runs.
- Across both programs, the primary may use at most three concurrent subagents;
  the primary occupies the fourth session slot.
- Never auto-stash, reset, checkout, clean, delete, overwrite, or silently stage
  pre-existing work.  Stop when synchronization is unsafe.
- A user-authorized root-policy reconciliation may be committed locally before
  the otherwise-required rebase only when a tracked/untracked `AGENTS.md`
  collision makes pull unsafe.  Such a coordination commit must contain only
  the authorized policy file, must preserve both scoped policies, and must be
  rebased onto current `origin/main` before any push.

## RH workflow

The RH program uses a sequential research pipeline with one project lead and
at most three concurrent subagents.  The repository is the sole source of
truth; old chat text is context only.

### Primary agent: RH project lead

The primary agent represents the project owner for routine execution.  It is
the only agent allowed to:

- choose the active RH route and assign the next paper number;
- integrate edits outside the writer's exclusive paper directory;
- modify `RH_HANDOFF.md`;
- stage files, commit, rebase, or push;
- issue the final `GO`, `STOP_SCOPED`, or `NOT_TESTABLE` verdict.

When repository-backed mathematics supplies a real route, continue without
asking for per-paper permission.  Never create a new number merely to keep the
pipeline busy.  A failed positive route becomes a rigorous scoped negative
paper only when the negative statement is itself proved or validated.

### Three concurrent RH subagent stations

1. `rh-source-lock`
   - Read-only.
   - Locks definitions, constants, clocks, normalization, source provenance,
     domains, uniformity, and exact hypotheses from the repository.
   - Returns a compact evidence table, exact file/line anchors, and executable
     blockers.  It does not draft claims.
2. `rh-proof-auditor`
   - Read-only and adversarial.
   - Checks every implication, asymptotic scale, quantifier, sign, data type,
     conditional hypothesis, and finite-to-asymptotic boundary.
   - Searches specifically for model/actual substitution, probability/trace
     substitution, unsigned/signed substitution, schema exploits, and Gate
     promotion.
3. `rh-paper-writer`
   - Starts only after the primary agent records `GO` for one exact paper.
   - Has exclusive write ownership of that one `papers/RH-N-*` directory.
   - Produces the manuscript, theorem ledger, roadmap, executable artifact,
     tests, and build script.  It never commits, pushes, edits another paper,
     or modifies either handoff file.

After a draft exists, replace one read-only station with `rh-release-qa`.
Release QA independently runs result regeneration, tests, LaTeX/log checks,
PDF text/font/rendering checks, archive verification, and a final claim
firewall audit.  It reports compact verdicts and exact counts and does not
modify publication state unless the primary agent explicitly assigns a single
mechanical repair.

### RH pipeline

```text
primary route decision
  |-- source-lock investigates the next admissible theorem
  |-- proof-auditor attacks the current theorem and its scope
  `-- paper-writer writes only after GO

draft -> release-QA -> primary integration -> pull --rebase -> commit
      -> pull --rebase -> push -> next route decision
```

Do not write dependent RH papers concurrently.  Read-only scouting for the
next paper may overlap the current writer, but the next number is activated
only after the current paper creates the required theorem edge.

### Mandatory RH verdicts and stops

- `GO`: the exact theorem, validated numerical result, counterexample, or
  scoped negative statement is supported in the declared data type.
- `STOP_SCOPED`: the attempted route fails, and the repository supports a
  precise bounded negative conclusion or a named missing hypothesis.
- `NOT_TESTABLE`: the required source, identification map, interval
  certificate, or executable observation is absent; do not manufacture a
  paper verdict.

Stop automatic publication when any of these holds:

- repository/source-lock mismatch;
- actual/model identification is absent where the claim requires it;
- a required moving-order or uniform theorem is absent;
- signed cancellation is replaced only by separate absolute bounds;
- a physical normalization, clock, or loss budget is unpaid;
- any test, checker, PDF, log, or archive verification is nonzero;
- rebase is unsafe or the declared route is exhausted.

### RH claim firewall

Finite tables are reproduction checks, never asymptotic evidence.  Synthetic
matrices, graded families, scalar repairs, and abstract ledgers are not actual
noisy operators.  Local probability laws are not trace observations without
an identification theorem.  Conditional criteria remain inactive until all
their hypotheses are proved on one common clock.

Gates A--E remain false/open unless a paper proves the exact gate definition
in `RH_HANDOFF.md`.  Never imply that the repository has constructed a
Hilbert--Polya operator, identified Riemann zeros, proved a von Mangoldt trace
formula, proved completed-zeta divisor equality, or proved RH.

### RH repository and release discipline

- Read `RH_HANDOFF.md` and the latest review paper completely before changing
  the route.
- Preserve unrelated untracked caches, checkpoints, LaTeX intermediates, and
  all TPC work.
- Stage only the active RH batch, its archive metadata, approved project-agent
  configuration, and `RH_HANDOFF.md` when the batch closes.
- Use `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider` for tests.
- Build the semantic PDF, scan the complete LaTeX log, verify text extraction,
  embedded fonts, Ghostscript parsing, and every rendered page.
- Build and verify both individual and batch SHA-256 publication archives.
- Run `git pull --rebase origin main` before every commit and again immediately
  before every push, except for the explicitly authorized root-policy
  reconciliation described in the shared rules above.

More specific instructions in a nested `AGENTS.md` override this file only for
that subtree.  Dynamic mathematics, completed endpoints, open hypotheses, and
the next route remain in `RH_HANDOFF.md`; the RH section contains durable
workflow policy only.

## TPC workflow

This TPC section defines durable program behavior. It does not record the current
paper number, current route verdict, or next-paper trigger. For TPC work, those
dynamic facts live only in the repository-root `TPC_HANDOFF.md` and committed
artifacts.

### TPC scope and authority

- These TPC-specific rules apply to `TPC_HANDOFF.md`, `papers/tpc-*`, and any task that
  advances or audits the TPC program. The preservation and git-safety rules apply to the
  whole repository.
- Treat the current repository files and committed artifacts as the source of truth.
  Old chats, memory, and historical handoff cells are not current-state evidence.
- Start from the handoff header and the entry sections named there. Expand historical
  sections only when a current entry explicitly points to them.
- Never hard-code the current endpoint, next paper number, active STOP_SCOPED cell, or
  provenance range into durable agent configuration. Re-read them from the handoff.

### TPC primary-agent startup

The primary agent owns repository synchronization. At the start of TPC mathematical,
production, or release work it must run:

```powershell
git status --short --branch
git pull --rebase origin main
Get-Content -Raw -Encoding UTF8 TPC_HANDOFF.md
$env:PYTHONDONTWRITEBYTECODE = "1"
```

- Inspect status before pulling. If existing work makes rebase unsafe, stop and report.
- Preserve every pre-existing tracked and untracked path. Do not reset, checkout, clean,
  auto-stash, delete, overwrite, or silently include unrelated work.
- For a TPC mathematical gate or production/release run, execute the complete current
  read-only startup regression listed in handoff section 1. Any nonzero checker fails
  closed. Configuration-only or documentation-only work need not run the mathematical
  suite unless it changes TPC artifacts or the handoff.
- Never run TPC-27--32 legacy certificate scripts while they unconditionally rewrite
  committed JSON. They are excluded until a genuine read-only `--check` entry exists.
- Do not use broad test discovery, `make all`, or repository-wide generator commands
  unless their full collection/execution path has been audited not to invoke an artifact
  writer indirectly.
- Subagents do not pull, rebase, or otherwise synchronize the shared worktree.

### TPC orchestration model

The primary agent acts as the user's operational project representative within the
standing workflow authorization. If a real theorem-backed route exists and every gate
passes, continue through the next finite audit, paper, validation, and release without
asking for per-paper permission again. This authorization never supplies missing
mathematics, expands destructive authority, or creates a paper number by itself.

Use at most three spawned agents concurrently:

1. `tpc_source_lock`: read-only theorem, packet, and provenance research.
2. `tpc_proof_auditor`: independent read-only adversarial proof and schema review.
3. `tpc_paper_writer`: the sole writer for one primary-agent-approved paper directory.
4. `tpc_release_qa`: a post-writing release gate; schedule it only after the writer has
   stopped, reusing one of the three subagent slots.

- Keep the main thread to conclusions, route decisions, first blockers, and final audit
  summaries. Delegate long formula checks, source scans, schema exploit reviews, build
  logs, and page-by-page PDF QA.
- Prefer parallel read-heavy work. Never run two write-capable agents on the same paper
  or shared release files at once.
- Subagents may not spawn further agents unless the primary agent explicitly delegates
  a bounded fan-out and confirms a free concurrency slot.
- The primary agent alone edits `TPC_HANDOFF.md`, `AGENTS.md`, `.codex/`, cross-paper
  provenance files, and release-wide manifests.
- The primary agent alone stages, commits, rebases, and pushes.
- Only one release-owning primary session may operate on this shared repository at a
  time. If another session, remote advance, or overlapping writer changes the baseline,
  stop and re-audit rather than racing paper numbers or provenance.
- Custom-agent sandbox settings are defense in depth, not the sole safety boundary:
  parent-session live permission overrides may take precedence. Before each spawn, the
  primary agent records the status/diff baseline and an allowed-write-path list. After
  each result, it compares `git status --short`, `git diff --name-only`, and
  `git diff --cached --name-only` against that baseline. Any unexplained path fails
  closed.

### TPC task and result envelopes

Before spawning a TPC subagent, the primary agent supplies a structured
`TPC_AGENT_TASK_V1` envelope containing at least:

- stable task ID, role, exact finite objective, and mode;
- repository root, baseline HEAD, and current `TPC_HANDOFF.md` content hash;
- exact claim or gate under test and frozen source locks;
- allowed read paths, allowed write paths, and forbidden paths;
- required physical fields, checks, stop conditions, and deliverables.

If any required baseline, claim, or path boundary is missing, the subagent returns
`HANDOFF_INCOMPLETE` instead of guessing. Every subagent returns a
`TPC_AGENT_RESULT_V1` report with the observed baseline and handoff hash, scope, files
read/changed, exact commands and exit codes, source-backed versus inference-only
evidence, physical-object fields, first fatal mismatch, supported claim level, verdict,
remaining gates, and narrowest next action. For source-lock, proof-auditor, and release-
QA roles, `files_changed` must be empty.

For a numbered-paper writer, the envelope is a `TPC_WRITE_GO_V1` specialization and
must additionally contain the exact paper number, declared target-path state, theorem
statement, claim ceiling, normalization/loss ledger, expected file allowlist, required
artifacts/checkers, and explicit invalidation conditions. The primary agent may issue it
only after source lock and independent proof audit agree on the same physical object and
the source-backed theorem pays the active gate. Agent agreement alone is not evidence.

### TPC mathematical gate discipline

For every candidate theorem or transfer, verify separately:

1. literal physical coefficient, including signs, masks, weights, and outer labels;
2. fixed physical `h0`;
3. summation domain and exact prefix index/order;
4. `X`, `N`, `q`, and every parameter range;
5. uniform constants and exceptional-set quantifiers;
6. normalization and natural scale;
7. the complete physical-loss ledger, including the strict `1/400` endpoint.

Required boundaries:

- Keep `L0`, `L1`, and `L2` distinct. Finite algebra, interfaces, certificates, tests,
  and checker PASS do not create arithmetic L2 progress.
- Preserve fixed-phase, fixed-`h0`, named-atom, actual-support, canonical/minimal-
  representation, and exactly-once-cover requirements.
- Never splice different packets, delta families, source locks, theorem branches, or
  normalizations even when exponents or notation match.
- Never force block to equal cumulative, logarithmic to equal natural, averaged or
  metric to equal prescribed phase, finite to equal growing, or model to equal physical.
- Orbit Poisson zero, density-one nonzero frequencies, Parseval, large sieve, or a
  complete-frequency mean does not prove a distinguished auxiliary zero.
- Keep every registered method cell `STOP_SCOPED` unless its exact source-backed reopen
  trigger occurs. Do not rename an exhausted method and present it as new.
- Record an arithmetic advance only when a source-backed theorem pays the declared
  physical loss on the exact object, or directly proves the required physical saving.

### TPC GO, STOP, and numbering

- A selected-packet or finite-interface PASS does not automatically create the next
  numbered paper. Re-read the current handoff trigger and every required downstream
  uniformity, cover, normalization, attachment, selection, tail, and provenance gate.
- If a theorem-backed trigger genuinely changes state, the primary agent may authorize
  one writer for the exact next paper and claim contract.
- If no real theorem trigger exists, update `TPC_HANDOFF.md` with the precise scoped
  stop. Do not create a paper, PDF, placeholder directory, or speculative next number.
- Leave unrelated open parents and global architecture open; a scoped stop is not a
  global nonexistence theorem.

### TPC file ownership and write safety

- A paper writer receives one explicit `papers/tpc-N-*` directory and an expected file
  list. It must not touch any other path unless the primary agent names it explicitly.
- The paper writer may create assigned build/render outputs before it stops. Release QA
  is read-only and must not repair source or create missing QA evidence.
- Do not delete or clean user files or build products. Report generated outputs and let
  the primary agent decide the final expected release set.
- Preserve the `tpc-num-*` naming convention and do not rename unrelated series.
- Before spawning a writer, record all pre-existing tracked/untracked paths. The target
  must be a new, absent directory and must not overlap pre-existing user work. For every
  pre-existing untracked file that could share a write ancestor, record path, size, and
  SHA-256 before the spawn and compare afterward; recurse through untracked directories.
  If that manifest is impractical, prove the write scope is disjoint or do not spawn a
  write-capable agent. A status snapshot alone cannot detect content changes inside an
  already untracked directory.
- Formal expected PDFs may live in the assigned paper directory. Build intermediates and
  page renders go to a unique primary-assigned external scratch directory, preferably
  under `%TEMP%`, never the repository's existing `tmp/`. Report scratch outputs; do not
  delete them implicitly.
- Use `apply_patch` for hand-authored repository edits. Formatting/build tools may make
  mechanical outputs only within the assigned scope.
- Set `PYTHONDONTWRITEBYTECODE=1` and prefer `python -B` so checks do not create new
  `__pycache__` artifacts.

### TPC validation and publication

- Checkers, schemas, manifests, hashes, and mutation tests are trust boundaries, not
  theorem evidence. Validate strict types; in Python, `bool` is a subclass of `int`, so
  use exact type identity when schema equality matters.
- Audit duplicate JSON keys, NaN/nonfinite values, optimized-mode/assert bypass,
  independent-checker separation from the producer, source identity, manifest rebinding,
  vacuous domains, canonical representation, and actual active support.
- Fail closed on any nonzero required checker. Do not rewrite expected artifacts merely
  to make a checker pass.
- A PDF is unfinished until it builds successfully, every page is rendered, and an
  independent release-QA agent visually inspects every rendered page. The primary agent
  or assigned writer prepares build/render outputs before the read-only QA pass; command
  success alone is insufficient.
- Before a numbered release, execute the current provenance cascade and rebuild only the
  releases required by the current handoff.
- Stop all subagents before release synchronization. Fetch and compare the starting
  baseline with current `origin/main`; if upstream touches the handoff, source locks, or
  dependencies, invalidate the old gate and re-audit. Even a disjoint upstream change
  requires rerunning the checks it can affect.
- Stage only the expected files. Before pushing, synchronize again with
  `git pull --rebase origin main`; stop if it is unsafe or introduces relevant evidence
  that changes the mathematical verdict.
- After `git push origin HEAD:main`, verify that `git rev-parse HEAD`,
  `git rev-parse origin/main`, and `git ls-remote origin refs/heads/main` report the same
  hash.

### TPC subagent handoff contract

Every subagent must return a compact, evidence-backed report containing:

- verdict and maximum justified claim level;
- exact object, packet, phase, domain, and normalization;
- first fatal blocker, if any;
- repository or primary-source locators;
- files read, files changed, and generated outputs;
- checks actually run with exit status;
- unresolved gates and the narrowest valid next action.

The primary agent independently reviews these reports. A subagent conclusion is input to
the decision, not authorization to publish.
