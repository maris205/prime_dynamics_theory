# RH-MVP2: Corpus frontier synthesis for conditional prime dynamics

RH-MVP2 is a provenance-preserving synthesis of the numbered RH corpus
`RH-1`--`RH-361`.  It is a survey and status ledger, not a new numbered
theorem paper and not an activation of RH-362.

The synthesis keeps every numbered paper as an atomic source.  It compresses
their logical roles into a small number of phases, records the actual versus
deterministic branch split, and exposes the currently unpaid theorem budget.
The inventory script checks that all 361 numbers occur, records the four
legacy duplicate/alias directory groups (`RH-302`, `RH-303`, `RH-304`, and
`RH-306`), and chooses the non-empty canonical directory for each number.
It also records the 29 established review anchors and their 349-paper union;
the remaining 12 IDs are retained through RH-MVP1 or the adjacent source
papers rather than silently treated as covered by a review.
The audit checks presence and hashes; it does not re-prove 361 papers.

The central current-status statement is:

```text
actual branch:       RH-352--RH-354 (selected/normalized p and Y)
deterministic branch: RH-355--RH-360 (counterloop s only)
bridge:              absent
frontier:            actual_same_clock_unnormalized_head_transport_open
first missing leaf:  D_(4k)(R) -> 0
```

On one source-locked clock,

```text
p = tau-a = q-d,   d = h-s,   q = p+d,   h = s+d.
```

The coefficient identities are exact, but the synthesis makes no physical
operator, root, rank, spectral-submultiset, determinant, von Mangoldt trace,
completed-zeta divisor, or RH claim.  Gates A--E remain false/open.

## Four-volume publication series

The umbrella is accompanied by four provenance-preserving long-form volumes:

```text
Volume I    RH-1--RH-160    RH-MVP1-conditional-prime-dynamics-hilbert-polya-roadmap
Volume II   RH-161--RH-241  RH-VOL2-physical-riesz-cloud-trace-envelope-synthesis
Volume III  RH-242--RH-281  RH-VOL3-deterministic-numerator-anchor-counterloop-synthesis
Volume IV   RH-282--RH-361  RH-VOL4-noisy-head-annulus-signed-completion-synthesis
```

The volumes are thematic syntheses, not four new numbered theorem steps. They
retain the same claim firewall and do not alter the endpoint RH-361.
After the four individual archives verify, an outer series manifest hashes
all four verification records and independently replays their fixed members,
dependency hashes, result hashes, source ranges, semantic PDFs, and Gate
firewalls.

## Reproduction

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python experiments/build_inventory.py
PYTHONDONTWRITEBYTECODE=1 python experiments/build_four_volume_archive.py
PYTHONDONTWRITEBYTECODE=1 python experiments/verify_four_volume_archive.py
PYTHONDONTWRITEBYTECODE=1 python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 python experiments/verify_archive.py
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

`results/corpus_inventory.json` is the machine-readable source index and
`CROSSWALK.md` is its human-readable phase map;
`results/dependency_manifest.json`, `results/summary.json`, and
`results/archive_verification.json` are the local and corpus provenance
records. `results/four_volume_archive_manifest.json` and
`results/four_volume_archive_verification.json` are the outer four-volume
seal and replay record. The original RH papers and all unrelated TPC
files/caches are left untouched.
