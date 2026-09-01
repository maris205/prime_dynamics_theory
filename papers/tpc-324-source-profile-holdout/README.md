# TPC-324 — A source-location holdout for signed prime-shell profiles

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

The all-plus signed spectral-profile majorization observed in TPC-323
survives two frozen source-location holdouts that are disjoint from the
training union: 48/48 rows majorize, with 24/24 on each holdout panel.
The three alternative sign laws reproduce the same finite census as the
parent panel (34/14, 42/6, and 36/12 majorizing/mixed).  This is a genuine
finite replication across residue environments, not an asymptotic theorem.

## What is new

TPC-323 used source intervals
`[321,640]`, `[641,1280]`, and `[1281,2560]`.  TPC-324 freezes two new
panels before recomputation:

```text
continuation = [2561,2880], [2881,3520], [3521,4800]
gap_offset   = [5001,5320], [6001,6640], [8001,9280]
```

The source cardinalities remain `320, 640, 1280`; `H=66`, the four prime
shell anchors `Q={24,36,54,80}`, the exponents `s={1,2}`, and the four
predeclared sign laws are unchanged.  Thus the intervention is source
location only.  The two panels are disjoint from each other and from the
TPC-323 source union.

The exact conditional covariance lemma is also recorded: a translation
divisible by every prime in a fixed shell leaves differences, congruence
classes, and deleted divisibility masks unchanged.  The selected gap offset
is not such a common multiple, so the observed replication is not explained
by that lemma.

## Claim firewall

```text
TPC324_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SOURCE_LOCATION_HOLDOUT_REPLICATION
TPC324_SOURCE_LOCATION_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_48_ROWS_2_PANELS
TPC324_ALL_PLUS_PROFILE_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_48_OF_48
TPC324_PER_PANEL_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_24_OF_24_EACH
TPC324_ALTERNATIVE_PROFILE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_48_ROWS
TPC324_TRANSLATION_COVARIANCE = PROVED_EXACT_FINITE_CONDITIONAL
TPC324_ARITHMETIC_ADVANCE = NO
TPC324_FIXED_POWER_CREDIT = 0
TPC324_FULL_GATE_B = OPEN
TPC324_TWIN_PRIME_RESULT = NONE
TPC324_STATUS = NUMERICALLY_CERTIFIED_FINITE_SOURCE_LOCATION_HOLDOUT_REPLICATION
TPC324_ROUND2_CLUE = TEST_HOLDOUT_SCALE_LADDER_OR_SOURCE_NATIVE_ARITHMETIC_L2
```

“Replication” here means an exactly specified finite recomputation with
independent replay.  It does not mean an external physical experiment,
uniform-in-(X) theorem, canonical Möbius sign law, or arithmetic
cancellation estimate.  The Session-named `propose.md` and official
Route-A/Route-B evaluator files are absent from this checkout, so the local
Bridge-B record is fail-closed and is not an official evaluator pass.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-324-source-profile-holdout/code/tpc324_source_profile_holdout.py --write
python -B papers/tpc-324-source-profile-holdout/code/tpc324_source_profile_holdout.py --check
python -O -B papers/tpc-324-source-profile-holdout/code/tpc324_source_profile_holdout.py --check
python -B papers/tpc-324-source-profile-holdout/experiments/tpc324_independent_checker.py --check
python -O -B papers/tpc-324-source-profile-holdout/experiments/tpc324_independent_checker.py --check
python -B papers/tpc-324-source-profile-holdout/experiments/tpc324_holdout_stress.py --check
python -O -B papers/tpc-324-source-profile-holdout/experiments/tpc324_holdout_stress.py --check
```

The machine-readable result is
`results/tpc324_certificate.json`; the manuscript is `paper/paper.pdf`.
The local Bridge-B record and checker are in
`research/tpc-big-road/bridge_b_tpc324_source_profile_holdout.md` and
`research/tpc-big-road/tpc_bridge_b_tpc324_source_profile_holdout_checker.py`.

## Package contents

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable package.
The next question is whether this replicated profile law survives a new
scale ladder or can be connected to a source-native arithmetic (L^2) bound.
