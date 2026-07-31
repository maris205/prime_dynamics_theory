# RH multi-agent research protocol

This repository uses a sequential research pipeline with one project lead and
at most three concurrent subagents.  The repository is the sole source of
truth; old chat text is context only.

## Primary agent: RH project lead

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

## Three concurrent subagent stations

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
modify publication state unless the primary agent explicitly assigns a
single mechanical repair.

## Pipeline

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

## Mandatory verdicts and stops

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

## RH claim firewall

Finite tables are reproduction checks, never asymptotic evidence.  Synthetic
matrices, graded families, scalar repairs, and abstract ledgers are not actual
noisy operators.  Local probability laws are not trace observations without
an identification theorem.  Conditional criteria remain inactive until all
their hypotheses are proved on one common clock.

Gates A--E remain false/open unless a paper proves the exact gate definition
in `RH_HANDOFF.md`.  Never imply that the repository has constructed a
Hilbert--Polya operator, identified Riemann zeros, proved a von Mangoldt trace
formula, proved completed-zeta divisor equality, or proved RH.

## Repository and release discipline

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
  before every push.

More specific instructions in a nested `AGENTS.md` override this file only
for that subtree.  Dynamic mathematics, completed endpoints, open hypotheses,
and the next route remain in `RH_HANDOFF.md`; this file contains durable
workflow policy only.
