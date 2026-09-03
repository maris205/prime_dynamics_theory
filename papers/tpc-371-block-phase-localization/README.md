# TPC-371 — Block-local phase localization of the count-2048 audit

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-371 partitions each of the three inherited count-2048 windows into eight
fixed 256-point blocks and recomputes the complete finite panel.  All 288
beta=2 block-local rows pass both working caps, with maximum normalized
spectral value `0.5536333251967529`, whereas the beta=0 control has 72
spectral and 72 Schur violations.  Since TPC-370 has six beta=2 failures for
the full-window-normalized object, the hypothesis that those failures are
already visible in one independently normalized short block is
`REFUTED_SCOPED`.

This result localizes the next question to cross-block structure, but does
not by itself prove cross-block causality: changing the domain changes the
square-energy normalization.

## Protocol

The origins `(1010001,1018021,1026041)` are inherited from the fixed grid
`1010001+401j` at indices `(0,20,40)`.  Each interval of 2048 integers is
partitioned before replay into blocks

```text
[origin + 256*b, origin + 256*b + 255],  b = 0,...,7.
```

The shell anchors are `Q={512,2048,8192}`, exponent is `1`, the four laws are
`all_plus`, `alternating_index`, `mod4_character`, and `half_split`, and beta
is `{0,2}`.  The full Cartesian product has
`3*8*3*1*4*2 = 576` rows.  No block, origin, law, or shell is selected from a
response, source vector, or geometry score.

The inherited exact anchor is `[1010346,1010359)` at `Q=4`, exponent `1`,
shell `{5,7}`.  It is checked exactly and is not used to choose a main-panel
row.

## Finite census

| beta | rows | spectral-cap violations | Schur-cap violations | maximum spectral |
|---:|---:|---:|---:|---:|
| 0 | 288 | 72 | 72 | 1.4642797645332997 |
| 2 | 288 | 0 | 0 | 0.5536333251967529 |

For beta=2, the maximum by shell is:

| Q | rows | spectral failures | maximum spectral |
|---:|---:|---:|---:|
| 512 | 96 | 0 | 0.54979749502051356 |
| 2048 | 96 | 0 | 0.55258383785942589 |
| 8192 | 96 | 0 | 0.5536333251967529 |

The beta=0 failures are concentrated in the all-plus control phase.  The
parent TPC-370 finite object has six beta=2 high-Q/all-plus failures at the
same three origins, so the local audit separates local cap behavior from the
full-window behavior without claiming an asymptotic mechanism.

## Claim firewall

```text
TPC371_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND
TPC371_BLOCK_PARTITION = PROVED_EXACT_FINITE_PREDECLARED
TPC371_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC371_BLOCK_LOCAL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_576_ROWS
TPC371_BETA2_BLOCK_PHASE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC371_BETA2_LOCAL_FAILURE = REFUTED_SCOPED
TPC371_CROSS_BLOCK_COHERENCE = OPEN
TPC371_ORIGIN_UNIFORMITY = OPEN
TPC371_WINDOW_UNIFORMITY = OPEN
TPC371_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC371_GROWING_OPERATOR_BOUND = OPEN
TPC371_SOURCE_UNIFORM_L2 = OPEN
TPC371_ARITHMETIC_ADVANCE = NO
TPC371_FIXED_POWER_CREDIT = 0
TPC371_FULL_GATE_B = OPEN
TPC371_TWIN_PRIME_RESULT = NONE
```

`REFUTED_SCOPED` refers only to the finite hypothesis “a beta=2 parent failure
must already occur in one independently normalized 256-point block.”  It does
not refute beta=2 behavior for other partitions or normalizations, and it does
not prove a cross-block theorem.

## Auditable package

The project contains `PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`,
`PROOF_PACKAGE.md`, `notes/`, `code/`, `experiments/`, `results/`, and
`paper/`.  The canonical certificate is
`results/tpc371_certificate.json`; the manuscript is `paper/paper.pdf`.

The producer accumulates shell terms in increasing order.  The independent
checker uses its own prime sieve and descending shell order, recomputes all
576 rows, and checks the inherited exact anchor.  The adversarial checker
mutates the protocol, partition, row census, phase counts, anchor, firewall,
and clue.  Local Bridge-B additionally checks normal/optimized replay,
empty stderr, and byte-identical stdout.

## Reproduce

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-371-block-phase-localization/code/tpc371_block_phase_localization.py --write
python -B papers/tpc-371-block-phase-localization/code/tpc371_block_phase_localization.py --check
python -O -B papers/tpc-371-block-phase-localization/code/tpc371_block_phase_localization.py --check
python -B papers/tpc-371-block-phase-localization/experiments/tpc371_independent_checker.py --check
python -O -B papers/tpc-371-block-phase-localization/experiments/tpc371_independent_checker.py --check
python -B papers/tpc-371-block-phase-localization/experiments/tpc371_adversarial_certificate_stress.py --check
python -O -B papers/tpc-371-block-phase-localization/experiments/tpc371_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc371_block_phase_localization_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc371_block_phase_localization_checker.py --check
```

The official Session Route-A/Route-B evaluator files are not present in this
checkout; the local bridge is fail-closed repository evidence only.

## Route decision

The local block audit removes the simplest localization hypothesis while
preserving the parent full-window obstruction.  The next minimal experiment
must keep the full-window normalization and split its matrix into a fixed
block-diagonal part and an off-block part.

```text
ROUND2_CLUE = TEST_OFF_BLOCK_COHERENCE_DECOMPOSITION
```
