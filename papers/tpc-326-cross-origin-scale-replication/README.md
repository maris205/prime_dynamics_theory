# TPC-326 — Cross-origin replication of the source-scale ladder

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

Repeating the TPC-325 four-rung scale ladder at a second disjoint source origin
`16001` reproduces its finite profile census and strict envelope trends:
all-plus majorization holds on `32/32` new rows, the alternative-law census
matches the parent (`21/11`, `26/6`, `23/9`), and the new all-plus TV/energy
envelopes stay within declared finite agreement thresholds of the parent.

## Frozen protocol

The new origin is `16001`; the nested intervals are

```text
N=320:  [16001,16160]   (160 source integers)
N=640:  [16001,16320]   (320 source integers)
N=1280: [16001,16640]   (640 source integers)
N=2560: [16001,17280]   (1280 source integers)
```

The source panels are disjoint from TPC-323, TPC-324, and the TPC-325 origin
`12001` ladder.  `H=66`, `Q={24,36,54,80}`, exponents `{1,2}`, the literal
deleted-diagonal centered blocks, and the four predeclared sign laws are
unchanged.  The producer is locked to the released TPC-325 producer, which in
turn locks the TPC-324 literal engine.

## Claim firewall

```text
TPC326_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_CROSS_ORIGIN_SCALE_LADDER_REPLICATION
TPC326_CROSS_ORIGIN_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_ROWS_2_ORIGINS
TPC326_ALL_PLUS_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_32_OF_32
TPC326_CENSUS_MATCH = NUMERICALLY_CERTIFIED_FINITE_PARENT_MATCH
TPC326_ENVELOPE_AGREEMENT = NUMERICALLY_CERTIFIED_FINITE_WITHIN_DECLARED_THRESHOLDS
TPC326_ARITHMETIC_ADVANCE = NO
TPC326_FIXED_POWER_CREDIT = 0
TPC326_FULL_GATE_B = OPEN
TPC326_TWIN_PRIME_RESULT = NONE
TPC326_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_ORIGIN_SCALE_LADDER_REPLICATION
TPC326_ROUND2_CLUE = TEST_CROSS_ORIGIN_SCALE_LADDER_OR_SOURCE_NATIVE_ARITHMETIC_L2
```

This is an adversarial finite replication, not a uniform-in-source theorem or
an asymptotic scale limit.  It does not introduce a canonical Möbius or von
Mangoldt sign, source-native arithmetic `L2` cancellation, a power saving, or
a twin-prime conclusion.  The Session-named official evaluator files are
absent from this checkout; local Bridge-B is fail-closed and is not an
official Route-A/Route-B pass.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-326-cross-origin-scale-replication/code/tpc326_cross_origin_scale_replication.py --write
python -B papers/tpc-326-cross-origin-scale-replication/code/tpc326_cross_origin_scale_replication.py --check
python -O -B papers/tpc-326-cross-origin-scale-replication/code/tpc326_cross_origin_scale_replication.py --check
python -B papers/tpc-326-cross-origin-scale-replication/experiments/tpc326_independent_checker.py --check
python -O -B papers/tpc-326-cross-origin-scale-replication/experiments/tpc326_independent_checker.py --check
python -B papers/tpc-326-cross-origin-scale-replication/experiments/tpc326_cross_origin_stress.py --check
python -O -B papers/tpc-326-cross-origin-scale-replication/experiments/tpc326_cross_origin_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc326_cross_origin_scale_replication_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc326_cross_origin_scale_replication_checker.py --check
```

The canonical result is `results/tpc326_certificate.json`; the final PDF is
`paper/paper.pdf`.
