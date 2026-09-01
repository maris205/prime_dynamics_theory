# TPC-325 — A source-scale ladder for signed prime-shell profiles

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

On one fresh fixed-origin nested ladder with source counts
`160, 320, 640, 1280`, the all-plus signed normalized profile majorizes the
direct profile on all `32/32` finite rows.  Its outward lower TV envelope and
outward upper energy envelope both decrease strictly across the four rungs.
The result is a finite scale audit, not an asymptotic law.

## Why this is a new project

TPC-324 changed source location while preserving source cardinality.  TPC-325
freezes a new source origin `12001` and changes only the nested cardinality:

```text
N=320:  [12001,12160]   (160 source integers)
N=640:  [12001,12320]   (320 source integers)
N=1280: [12001,12640]   (640 source integers)
N=2560: [12001,13280]   (1280 source integers)
```

Every rung uses `H=66`, `Q={24,36,54,80}`, exponents `{1,2}`, the same four
predeclared sign laws, and the literal deleted-diagonal centered prime-shell
blocks.  The engine itself is provenance-locked to TPC-324; the scale protocol,
expectations, independent replay, and certificate are new here.

## Claim firewall

```text
TPC325_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SOURCE_SCALE_LADDER_AUDIT
TPC325_SCALE_LADDER = NUMERICALLY_CERTIFIED_FINITE_32_ROWS_4_SCALES
TPC325_ALL_PLUS_SCALE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
TPC325_ALL_PLUS_PROFILE_MAJORISATION = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
TPC325_TV_ENVELOPE = NUMERICAL_OBSERVATION_STRICTLY_DESCENDING_4_SCALES
TPC325_ENERGY_ENVELOPE = NUMERICAL_OBSERVATION_STRICTLY_DESCENDING_4_SCALES
TPC325_ARITHMETIC_ADVANCE = NO
TPC325_FIXED_POWER_CREDIT = 0
TPC325_FULL_GATE_B = OPEN
TPC325_TWIN_PRIME_RESULT = NONE
TPC325_STATUS = NUMERICALLY_CERTIFIED_FINITE_SOURCE_SCALE_LADDER_AUDIT
TPC325_ROUND2_CLUE = TEST_SCALE_LADDER_SOURCE_REPLICATION_OR_SOURCE_NATIVE_ARITHMETIC_L2
```

The strict ladder trends are numerical observations on a predeclared finite
panel.  They do not prove a limit, a uniform-in-source estimate, a canonical
Möbius/von Mangoldt sign, source-native arithmetic `L2` cancellation, a power
saving, or a twin-prime conclusion.  The Session-named `propose.md` and
official Route-A/Route-B evaluator files are absent from this checkout; the
local Bridge-B record is therefore fail-closed and is not an official pass.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-325-scale-ladder-profile/code/tpc325_scale_ladder_profile.py --write
python -B papers/tpc-325-scale-ladder-profile/code/tpc325_scale_ladder_profile.py --check
python -O -B papers/tpc-325-scale-ladder-profile/code/tpc325_scale_ladder_profile.py --check
python -B papers/tpc-325-scale-ladder-profile/experiments/tpc325_independent_checker.py --check
python -O -B papers/tpc-325-scale-ladder-profile/experiments/tpc325_independent_checker.py --check
python -B papers/tpc-325-scale-ladder-profile/experiments/tpc325_scale_stress.py --check
python -O -B papers/tpc-325-scale-ladder-profile/experiments/tpc325_scale_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc325_scale_ladder_profile_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc325_scale_ladder_profile_checker.py --check
```

The machine-readable result is `results/tpc325_certificate.json`; the final
manuscript is `paper/paper.pdf`.

## Package contents

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable package.
