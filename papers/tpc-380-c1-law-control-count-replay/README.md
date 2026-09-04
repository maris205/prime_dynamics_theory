# TPC-380 — c=1 law-control count replay

**Author:** Liang Wang<br>
**Affiliation:** School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-380 repeats the TPC-379 four-law experiment at the new count
`N=2048`, using eight contiguous 256-point blocks and a fresh
coordinate-disjoint affine origin panel.  The complete 36-row panel again has
the all-plus profile `(0,3,3)` and the three signed-control profiles
`(0,0,0)`, with 6/36 spectral-cap failures and no Schur-cap failures.  This
is finite count-persistence evidence and a law-control obstruction; it is not
a scale-uniformity theorem or a twin-prime result.

## Frozen protocol

```text
candidate grid = a_j = 1300001 + 401 j, 0 <= j < 41
selected indices = 0,20,40 -> origins 1300001,1308021,1316041
window count = 2048 (eight contiguous blocks of length 256)
band = block distance <= 1 (the inherited c=1 rule)
Q = 512,2048,8192; exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index, mod4_character, half_split
caps = spectral 0.64, Schur 0.83
normalization = one common square-energy geometry for all laws
```

The grid, origins, count, block mask, laws, and complete Cartesian panel are
fixed before any response or metric is read.  The current intervals are
coordinate-disjoint from the declared TPC-376--379 windows by exact integer
endpoint inequalities.

The exact q=8 anchor is the subinterval `[1300014,1300027)`.  The first
13-point subinterval at the origin is residue-degenerate for the q=8 shell;
the offset-13 anchor is a deterministic finite positivity repair inside the
already selected window and is not used to select a row or a result.

The observed band spectral maxima, in law order, are approximately

```text
all_plus           0.66694556698889795
alternating_index  0.0077646382652031094
mod4_character     0.012038214320188189
half_split         0.21613429440676551
```

Across the 36 selected full modes, the absolute band-Rayleigh retention is
`0.0021757978771847777--0.97694432793223085`; the largest absolute tail
fraction is `0.99782420212281453`.

## Claim firewall

```text
TPC380_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC380_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC380_COMMON_GEOMETRY = PROVED_EXACT_FINITE_LAW_INDEPENDENT
TPC380_LAW_FAMILY = PROVED_EXACT_FINITE_PREDECLARED
TPC380_COUNT_REPLAY = NUMERICALLY_CERTIFIED_FINITE_36_ROWS
TPC380_ALL_PLUS_FAILURE_PROFILE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC380_SIGNED_CONTROL_SUBCAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC380_RAYLEIGH_TAIL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC380_LAW_UNIFORMITY = OPEN
TPC380_ORIGIN_UNIFORMITY = OPEN
TPC380_WINDOW_SCALE_UNIFORMITY = OPEN
TPC380_CROSS_BLOCK_CAUSALITY = OPEN
TPC380_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC380_GROWING_OPERATOR_BOUND = OPEN
TPC380_SOURCE_UNIFORM_L2 = OPEN
TPC380_ARITHMETIC_ADVANCE = NO
TPC380_FIXED_POWER_CREDIT = 0
TPC380_FULL_GATE_B = OPEN
TPC380_TWIN_PRIME_RESULT = NONE
```

The count replay does not promote the diagnostic signed controls to source
valid arithmetic laws.  No arithmetic power saving, Route-A/Route-B gate
closure, or twin-prime conclusion is claimed.  The official Session-named
evaluator files are absent from this checkout; the local Bridge-B is
fail-closed repository evidence only.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-380-c1-law-control-count-replay/code/tpc380_c1_law_control_count_replay.py --write
python -B papers/tpc-380-c1-law-control-count-replay/code/tpc380_c1_law_control_count_replay.py --check
python -O -B papers/tpc-380-c1-law-control-count-replay/code/tpc380_c1_law_control_count_replay.py --check
python -B papers/tpc-380-c1-law-control-count-replay/experiments/tpc380_independent_checker.py --check
python -O -B papers/tpc-380-c1-law-control-count-replay/experiments/tpc380_independent_checker.py --check
python -B papers/tpc-380-c1-law-control-count-replay/experiments/tpc380_adversarial_certificate_stress.py --check
python -O -B papers/tpc-380-c1-law-control-count-replay/experiments/tpc380_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc380_c1_law_control_count_replay_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc380_c1_law_control_count_replay_checker.py --check
```

The independent checker uses a direct sieve through 20000, reverse-shell
accumulation, independent sign construction, full/band eigensystems, and the
q=8 rational anchor.  The stress suite mutates protocol, result, and claim
fields and requires every mutation to be rejected.

## Route evaluation

The strongest positive result is a complete finite count-2048 replay on a
fresh response-blind origin panel: the TPC-379 all-plus high-Q profile and
the signed-control separation recur under the same c=1 geometry.  The
strongest obstruction is that the separation remains law-dependent rather
than a common property of the mask.  The reusable structure is a shared
geometry/common-mask count ladder with exact endpoint checks, reverse-shell
replay, and full-mode Rayleigh accounting.

`ROUND2_CLUE = TEST_C1_LAW_CONTROL_ORIGIN_FAMILY_REPLAY`.
