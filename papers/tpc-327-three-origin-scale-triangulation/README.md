# TPC-327 — Three-origin triangulation of the finite scale ladder

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

Repeating the frozen TPC-325/TPC-326 four-rung ladder at a third disjoint
origin `20001` gives `32/32` all-plus profile majorization, matches both
earlier four-law censuses, and keeps the three-origin envelope ranges below
the inherited finite controls (`0.001` for TV and `0.005` for energy).

The new contribution is a non-vacuous three-origin triangulation of one
finite operator family, not a source-uniform theorem.

## Frozen protocol

The new nested intervals are

```text
N=320:  [20001,20160]   (160 source integers)
N=640:  [20001,20320]   (320 source integers)
N=1280: [20001,20640]   (640 source integers)
N=2560: [20001,21280]   (1280 source integers)
```

They are disjoint from the earlier `12001` and `16001` ladders and from the
older source panels.  `H=66`, `Q={24,36,54,80}`, exponents `{1,2}`, the
deleted-diagonal centered block, and the four sign laws are locked.  The
producer is provenance-locked to TPC-326, which is in turn locked to the
TPC-325/TPC-324 engine chain.

## Main finite readout

The new-origin all-plus rows have the following envelope readout:

| scale `N` | source count | TV lower envelope | energy upper envelope |
|---:|---:|---:|---:|
| 320 | 160 | 0.2852340552 | 8.901456172 |
| 640 | 320 | 0.2108709647 | 6.864102783 |
| 1280 | 640 | 0.1900525186 | 6.249238483 |
| 2560 | 1280 | 0.1700854483 | 5.998451633 |

The profile census `(signed majorizes / mixed)` is:

```text
all_plus           32 / 0
alternating_index  21 / 11
mod4_character     26 / 6
half_split         23 / 9
```

The corresponding counts exactly match both TPC-325 and TPC-326, including
the energy-side census.

Pooling all three origins gives the following maximum-minus-minimum ranges:

| scale `N` | TV range | energy range |
|---:|---:|---:|
| 320 | 0.0007970083 | 0.0045518412 |
| 640 | 0.0003338713 | 0.0044707079 |
| 1280 | 0.0001938660 | 0.0013977240 |
| 2560 | 0.0000914121 | 0.0006212834 |

Both maxima are below the already frozen controls.  The ranges are strictly
nonzero, so this is not an assertion produced by identical copied values.

At the exact rational anchor `[20001,20016]`, `Q=4`, `s=1`, the direct and
index-alternating energy digests are

```text
direct = 97225bdbd0cb628956b3701748cec3b2eca7b4d559c0d0b42044300f7c26889b
signed = f38ac7229026dcd2ada592c5b245871d3ef1856e4bac21c86010e89766a9f9f7
```

The producer and independent checker recompute the exact rational
numerator/denominator values; the release certificate stores their digests.

## Claim firewall

```text
TPC327_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_THREE_ORIGIN_SCALE_TRIANGULATION
TPC327_THREE_ORIGIN_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_ROWS_3_ORIGINS
TPC327_ALL_PLUS_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_OF_32_NEW_ORIGIN
TPC327_CENSUS_MATCH = NUMERICALLY_CERTIFIED_FINITE_MATCH_TO_BOTH_PARENTS
TPC327_ENVELOPE_TRIANGULATION = NUMERICALLY_CERTIFIED_FINITE_WITHIN_DECLARED_THRESHOLDS
TPC327_ARITHMETIC_ADVANCE = NO
TPC327_FIXED_POWER_CREDIT = 0
TPC327_FULL_GATE_B = OPEN
TPC327_TWIN_PRIME_RESULT = NONE
TPC327_STATUS = NUMERICALLY_CERTIFIED_FINITE_THREE_ORIGIN_SCALE_TRIANGULATION
TPC327_ROUND2_CLUE = TEST_ORIGIN_ENSEMBLE_SCALE_GROWTH_OR_SOURCE_NATIVE_ARITHMETIC_L2
```

The Session-named official Route-A and Route-B evaluator files are absent
from this checkout.  The local Bridge-B checker is a fail-closed fallback and
is not an official evaluator pass.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-327-three-origin-scale-triangulation/code/tpc327_three_origin_scale_triangulation.py --check
python -B papers/tpc-327-three-origin-scale-triangulation/experiments/tpc327_independent_checker.py --check
python -B papers/tpc-327-three-origin-scale-triangulation/experiments/tpc327_three_origin_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc327_three_origin_scale_triangulation_checker.py --check
```

The canonical machine-readable result is
`results/tpc327_certificate.json`; the final manuscript is
`paper/paper.pdf`.
