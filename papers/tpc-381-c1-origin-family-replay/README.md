# TPC-381 — c=1 law-control origin-family replay

**Author:** Liang Wang<br>
**Affiliation:** School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-381 repeats the TPC-380 four-law experiment on a second predeclared
origin family, holding the count at `N=2048` and using eight contiguous
256-point blocks.  The complete 36-row panel again has
the all-plus profile `(0,3,3)` and the three signed-control profiles
`(0,0,0)`, with 6/36 spectral-cap failures and no Schur-cap failures.  This
is finite origin-family persistence evidence and a law-control obstruction; it
is not an origin-uniformity theorem, a scale-uniformity theorem, or a
twin-prime result.

## Frozen protocol

```text
candidate grid = a_j = 1400001 + 401 j, 0 <= j < 41
selected indices = 0,20,40 -> origins 1400001,1408021,1416041
window count = 2048 (eight contiguous blocks of length 256)
band = block distance <= 1 (the inherited c=1 rule)
Q = 512,2048,8192; exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index, mod4_character, half_split
caps = spectral 0.64, Schur 0.83
normalization = one common square-energy geometry for all laws
```

The grid, origins, count, block mask, laws, and complete Cartesian panel are
fixed before any response or metric is read.  The current intervals are
coordinate-disjoint from the declared TPC-376--380 windows by exact integer
endpoint inequalities.

The exact q=8 anchor is the first subinterval `[1400001,1400014)`.  Its shell
is `{11,13}` and exact rational arithmetic verifies positive common geometry
and symmetry for all four laws.  The anchor is an audit object, not a row or
result-selection signal.

The observed band spectral maxima, in law order, are approximately

```text
all_plus           0.66694427563296521
alternating_index  0.0077610039910285299
mod4_character     0.012055505105884349
half_split         0.21613933977437655
```

Across the 36 selected full modes, the absolute band-Rayleigh retention is
`0.0021890151798274436--0.97694644030159705`; the largest absolute tail
fraction is `0.99781098482017305`.

## Claim firewall

```text
TPC381_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC381_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC381_COMMON_GEOMETRY = PROVED_EXACT_FINITE_LAW_INDEPENDENT
TPC381_LAW_FAMILY = PROVED_EXACT_FINITE_PREDECLARED
TPC381_ORIGIN_FAMILY_REPLAY = NUMERICALLY_CERTIFIED_FINITE_36_ROWS
TPC381_ALL_PLUS_FAILURE_PROFILE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC381_SIGNED_CONTROL_SUBCAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC381_RAYLEIGH_TAIL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC381_LAW_UNIFORMITY = OPEN
TPC381_ORIGIN_UNIFORMITY = OPEN
TPC381_WINDOW_SCALE_UNIFORMITY = OPEN
TPC381_CROSS_BLOCK_CAUSALITY = OPEN
TPC381_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC381_GROWING_OPERATOR_BOUND = OPEN
TPC381_SOURCE_UNIFORM_L2 = OPEN
TPC381_ARITHMETIC_ADVANCE = NO
TPC381_FIXED_POWER_CREDIT = 0
TPC381_FULL_GATE_B = OPEN
TPC381_TWIN_PRIME_RESULT = NONE
```

The origin-family replay does not promote the diagnostic signed controls to source
valid arithmetic laws.  No arithmetic power saving, Route-A/Route-B gate
closure, or twin-prime conclusion is claimed.  The official Session-named
evaluator files are absent from this checkout; the local Bridge-B is
fail-closed repository evidence only.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-381-c1-origin-family-replay/code/tpc381_c1_origin_family_replay.py --write
python -B papers/tpc-381-c1-origin-family-replay/code/tpc381_c1_origin_family_replay.py --check
python -O -B papers/tpc-381-c1-origin-family-replay/code/tpc381_c1_origin_family_replay.py --check
python -B papers/tpc-381-c1-origin-family-replay/experiments/tpc381_independent_checker.py --check
python -O -B papers/tpc-381-c1-origin-family-replay/experiments/tpc381_independent_checker.py --check
python -B papers/tpc-381-c1-origin-family-replay/experiments/tpc381_adversarial_certificate_stress.py --check
python -O -B papers/tpc-381-c1-origin-family-replay/experiments/tpc381_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc381_c1_origin_family_replay_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc381_c1_origin_family_replay_checker.py --check
```

The independent checker uses a direct sieve through 20000, reverse-shell
accumulation, independent sign construction, full/band eigensystems, and the
q=8 rational anchor.  The stress suite mutates protocol, result, and claim
fields and requires every mutation to be rejected.

## Route evaluation

The strongest positive result is a complete finite origin-family replay at
count 2048 on a second fresh response-blind panel: the TPC-380 all-plus
high-Q profile and the signed-control separation recur under the same c=1
geometry.  The
strongest obstruction is that the separation remains law-dependent rather
than a common property of the mask.  The reusable structure is a shared
geometry/common-mask origin-family ladder with exact endpoint checks,
reverse-shell replay, and full-mode Rayleigh accounting.

`ROUND2_CLUE = TEST_C1_ORIGIN_FAMILY_MAGNITUDE_AUDIT`.
