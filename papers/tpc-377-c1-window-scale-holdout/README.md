# TPC-377 — c=1 window-scale holdout

**Author:** Liang Wang

**Affiliation:** School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-377 keeps the three response-blind origins from TPC-376 and evaluates a
predeclared nested count ladder N=(1024,1536,2048) with the same full-window
normalization, c=1 band, beta-2/all-plus law, and Q=(512,2048,8192). The
complete 27-row panel records the count-by-Q failure table and tests whether
the parent (0,3,3) profile is scale-stable. The precise census is stored
in results/tpc377_certificate.json.

The profile is (0,3,3) at each count: 18 of 27 rows cross the spectral cap,
while 0 of 27 cross the Schur cap. Across all rows, the selected-mode band
Rayleigh retention is 0.93760019185559207--0.98047323365759775 and the
largest tail fraction is 0.062399808144408715. The spectral magnitudes are
not constant across the count ladder, so this is a support replication and
not a magnitude-stability theorem.

The count windows are nested prefixes, not independent samples. The result
is finite and scoped; it does not establish origin/window uniformity,
cross-block causality, a growing operator theorem, source-uniform arithmetic
L2, a power saving, or a twin-prime conclusion.

## Frozen protocol

~~~text
origins       = 1012006, 1016016, 1022031
counts        = 1024, 1536, 2048
blocks        = contiguous blocks of length 256; block counts 4, 6, 8
band          = block distance <= 1
Q             = 512, 2048, 8192
kernel        = exponent 1, height 66
law           = all_plus, beta 2
caps          = spectral 0.64, Schur 0.83
~~~

All parameters and the complete Cartesian panel are fixed before response
metrics are read. Each scale uses its own full-window square-energy
normalization; the band and tail share that scale's normalization.

## Claim firewall

~~~text
TPC377_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC377_NESTED_PREFIX_PROTOCOL = PROVED_EXACT_FINITE
TPC377_COMMON_NORMALIZATION = PROVED_EXACT_FINITE_INHERITED
TPC377_SCALE_LADDER_REPLAY = NUMERICALLY_CERTIFIED_FINITE_27_ROWS
TPC377_C1_PROFILE_STABILITY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC377_PARENT_Q_PROFILE_PERSISTENCE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC377_RAYLEIGH_TAIL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC377_ORIGIN_UNIFORMITY = OPEN
TPC377_WINDOW_SCALE_UNIFORMITY = OPEN
TPC377_CROSS_BLOCK_CAUSALITY = OPEN
TPC377_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC377_GROWING_OPERATOR_BOUND = OPEN
TPC377_SOURCE_UNIFORM_L2 = OPEN
TPC377_ARITHMETIC_ADVANCE = NO
TPC377_FIXED_POWER_CREDIT = 0
TPC377_FULL_GATE_B = OPEN
TPC377_TWIN_PRIME_RESULT = NONE
~~~

The official Session-named Route-A/Route-B evaluator files are absent.
The local Bridge-B is fail-closed repository evidence only.

## Reproduction

~~~bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-377-c1-window-scale-holdout/code/tpc377_c1_window_scale_holdout.py --write
python -B papers/tpc-377-c1-window-scale-holdout/code/tpc377_c1_window_scale_holdout.py --check
python -O -B papers/tpc-377-c1-window-scale-holdout/code/tpc377_c1_window_scale_holdout.py --check
python -B papers/tpc-377-c1-window-scale-holdout/experiments/tpc377_independent_checker.py --check
python -O -B papers/tpc-377-c1-window-scale-holdout/experiments/tpc377_independent_checker.py --check
python -B papers/tpc-377-c1-window-scale-holdout/experiments/tpc377_adversarial_certificate_stress.py --check
python -O -B papers/tpc-377-c1-window-scale-holdout/experiments/tpc377_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc377_c1_window_scale_holdout_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc377_c1_window_scale_holdout_checker.py --check
~~~

ROUND2_CLUE = TEST_C1_SCALE_ORIGIN_CROSSHOLDOUT.
