# Final QA and preservation receipt

Date: 2026-09-09. This is a scoped research handoff, not a publication release.

## Required startup regression

After all nine delegated agents closed and the handoff prefix was updated,
both read-only wrapper invocations exited 0:

```sh
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_tpc418_c1_shell_parity_envelope_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -O -B research/tpc-big-road/tpc_bridge_b_tpc418_c1_shell_parity_envelope_checker.py --check
```

Both returned exactly:

```text
TPC418_BRIDGE_CHECK=PASS fixtures=3 sigma=PASS independent=PASS stress=PASS paper_artifacts=PASS strict_firewall=PASS
```

Each wrapper checks source/artifact hashes and invokes the producer, independent
checker and stress checker in normal and optimized modes. Together these
two top-level and twelve child executions cover the eight distinct command/
mode forms in the current TPC418 startup suite.

The earlier [independent startup audit](agent-reports/physical-loop-startup-regression.md)
records the important inherited limitations: the independent checker reuses
TPC417's large rows; some standalone stress-schema coverage is not exercised
by the wrapper; and PDF checks are hash/presence checks, not a fresh visual
or semantic PDF review. PASS is not arithmetic evidence.

## New research diagnostics and navigation

The [current diagnostic receipt](DIAGNOSTIC_RECEIPT_ROUND4.md) contains the
complete byte-identical normal/optimized outputs. Both exited 0; the checker
writes no files and uses explicit guards, not Python assertions.
Its SHA-256 at final verification is:

```text
6c25eaf5b20d2a23842cce3d211f47f7f517bd56ebdf7440754aec54d3d3a800
```

The diagnostics distinguish rational finite identities, floating-point matrix
tests, exact one-scale prerequisite inequalities, and the actual uniform
proofs. No diagnostic Gaussian, arbitrary random lane, nonpositive numerical
cutoff, or one-scale test is promoted to the physical asymptotic conclusion.

The initial naive link check exited 1. It confused TeX function notation with
Markdown, mishandled surrounding target whitespace, and found one genuine
path typo in an immutable raw report. The revised navigation check excludes
code/math, trims targets, and explicitly retains the single corrected raw
exception described in [SOURCE_LINK_ERRATA.md](SOURCE_LINK_ERRATA.md).
The earlier corrected run checked 195 local targets with no unresolved
missing destination. Final navigation verification additionally includes
this receipt, the completed review, and only the new handoff prefix.
The final run exited 0: 330 local targets checked, no unresolved missing
destination, and the one explicit immutable-raw erratum retained. State
checks confirmed four completed rounds, all agents closed, 15 full reports,
eight raw independent reviews, no pending cycle work, and publication GO false.

## Worktree and old-body preservation

Start and finish HEAD and local origin/main remained:

```text
ab23455ba941e5a14ded27d49de0e874aee811ac
```

This is the local tracking reference fetched at startup, not a claim of a
second final remote synchronization. Existing dirty work prevented safe
rebase; no staging, commit, push, auto-stash, reset, cleanup or deletion ran.

The initial worktree had 10 tracked dirty paths, 631 untracked paths, and an
empty index. Before this receipt was added, the final comparison had the same
10 tracked dirty paths and empty index, 663 untracked paths, no removed status
entry, and 32 new paths all confined to the two new root review files and this
new research directory. Adding this receipt makes 33 scoped new files in all
and 664 untracked paths. Final checks verify those counts.
The final post-write status check confirmed exactly 10 tracked dirty,
664 untracked, 33 authorized additions, no removed entry, no unexplained
addition, and an empty index.

The only pre-existing file intentionally edited in this cycle was
TPC_HANDOFF.md, by adding the new top entry. Reconstructing its original
header and complete older body gives the exact starting digest:

```text
36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
```

After the prefix insertion its digest is:

```text
234aa1533a7ade0775cd91d4e9d6f79ad80eca0c28fb662a547a1bdc4bd5d2d4
```

AGENTS.md, the route map and the candidate ledger retain their starting hashes.
The initial source controls matched before the handoff update. A tracked-file
existence check and exact HEAD diff confirm that both published TPC417/418
trees and the TPC418 startup wrapper remain unchanged. The final tracked
whitespace check exited 0. No recursive content-hash audit of all unrelated
pre-existing untracked files is claimed; the write scopes and executed
read-only checks left them untouched.

## Claim ceiling

All four proof-review rounds reached positive scoped assessments, and all
15 complete task/review reports are preserved verbatim. No necessary proof
fix remains. Exact source/ordinary-norm results, real and complex growing-rank
obstructions, and the boundary support estimate are proved in their stated
scopes. Literal signed interior cancellation, Gate A, Gate B, and publication
novelty/readiness remain open. No new numbered paper or release was created.
