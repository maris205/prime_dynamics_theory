# TPC-378 — c=1 scale–origin cross-holdout

**Author:** Liang Wang<br>
**Affiliation:** School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-378 takes the inherited finite `c=1`, beta-2, all-plus prime-shell band
and evaluates it on a new, coordinate-disjoint affine origin grid.  The
origins `(1100001,1108021,1116041)` are fixed as grid indices `(0,20,40)`
before any response is read; the endpoint counts are `N=1024,2048`, and the
Q anchors are `512,2048,8192`.  The complete 18-row panel has profile
`(0,3,3)` at both counts: 12 spectral-cap violations and zero Schur-cap
violations.  The exact data and all row metrics are in
`results/tpc378_certificate.json`.

The selected full-mode absolute-Rayleigh retention is
`0.93759972206138864--0.98046528117382914`; the largest tail fraction is
`0.062400277938610291`.  This is a finite cross-holdout transfer of a support
profile, not an origin-uniformity, scale-uniformity, or asymptotic theorem.

## Frozen protocol

```text
candidate grid = a_j = 1100001 + 401 j, 0 <= j < 41
selected indices = 0,20,40  -> origins 1100001,1108021,1116041
counts         = 1024,2048 (nested prefixes; blocks 4,8)
block length   = 256
band           = block distance <= 1 (inherited c=1)
Q              = 512,2048,8192
kernel         = exponent 1, height 66
law            = all_plus, beta 2
caps           = spectral 0.64, Schur 0.83
normalization  = each scale's full-window square-energy geometry
```

The current six intervals are disjoint from the largest declared TPC-376 and
TPC-377 intervals by exact integer endpoint inequalities.  The two counts at
each new origin share a left endpoint, but their separately normalized
matrices are not asserted to be restrictions of one growing operator.

## Claim firewall

```text
TPC378_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC378_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC378_COMMON_BAND_RULE = PROVED_EXACT_FINITE_INHERITED
TPC378_SCALE_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_18_ROWS
TPC378_C1_PROFILE_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC378_PARENT_PROFILE_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC378_RAYLEIGH_TAIL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC378_ORIGIN_UNIFORMITY = OPEN
TPC378_WINDOW_SCALE_UNIFORMITY = OPEN
TPC378_SPECTRAL_MAGNITUDE_UNIFORMITY = OPEN
TPC378_CROSS_BLOCK_CAUSALITY = OPEN
TPC378_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC378_GROWING_OPERATOR_BOUND = OPEN
TPC378_SOURCE_UNIFORM_L2 = OPEN
TPC378_ARITHMETIC_ADVANCE = NO
TPC378_FIXED_POWER_CREDIT = 0
TPC378_FULL_GATE_B = OPEN
TPC378_TWIN_PRIME_RESULT = NONE
```

No arithmetic power saving, Route-B reassembly, or twin-prime conclusion is
claimed.  The official Session-named Route-A/Route-B evaluator files are not
present in this checkout; the local Bridge-B is fail-closed repository
evidence only.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-378-c1-scale-origin-crossholdout/code/tpc378_c1_scale_origin_crossholdout.py --write
python -B papers/tpc-378-c1-scale-origin-crossholdout/code/tpc378_c1_scale_origin_crossholdout.py --check
python -O -B papers/tpc-378-c1-scale-origin-crossholdout/code/tpc378_c1_scale_origin_crossholdout.py --check
python -B papers/tpc-378-c1-scale-origin-crossholdout/experiments/tpc378_independent_checker.py --check
python -O -B papers/tpc-378-c1-scale-origin-crossholdout/experiments/tpc378_independent_checker.py --check
python -B papers/tpc-378-c1-scale-origin-crossholdout/experiments/tpc378_adversarial_certificate_stress.py --check
python -O -B papers/tpc-378-c1-scale-origin-crossholdout/experiments/tpc378_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc378_c1_scale_origin_crossholdout_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc378_c1_scale_origin_crossholdout_checker.py --check
```

## Route evaluation

The strongest positive result is a finite response-blind profile transfer to
three fresh coordinate-disjoint origins at both endpoint scales.  The main
obstruction is that the profile is only a cap census: high-Q spectral
magnitudes move with count and origin, and the normalization remains
scale-specific.  The open theorem is a uniform cross-origin/cross-scale
operator statement with a source-valid normalization.  The reusable object is
the response-blind affine-grid selection plus exact interval-disjointness,
common c=1 mask, and full-mode band/tail Rayleigh audit.

`ROUND2_CLUE = TEST_C1_CROSSHOLDOUT_LAW_CONTROL`.
