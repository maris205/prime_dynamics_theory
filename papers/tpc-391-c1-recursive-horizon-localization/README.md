# TPC-391 — Localizing a Recursive Horizon Obstruction

Author: Liang Wang
Affiliation: School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-391 is a fresh-family finite audit following TPC-390.  It freezes the
TPC-390 slope interface and adds the intermediate horizons
N=1152,1280,1408 before the fixed terminal holdout N=1536.  The parent
forecast stays inside the 3% cap at the first three horizons in all 32
cells, then has 23/32 passing cells at 1536; exactly 9 cells cross for the
first time at 1536.  The same-family local control passes 32/32 at every
horizon.  The result is a finite localization of a proxy obstruction, not an
arithmetic or twin-prime theorem.

## Frozen protocol

~~~text
schema = TPC391_C1_RECURSIVE_HORIZON_LOCALIZATION_V1
candidate grid = a_j = 3400001 + 401 j, 0 <= j < 41
selected indices = 0,10,20,30,40
origins = 3400001,3404011,3408021,3412031,3416041
calibration origins = first three
holdout origins = last two
calibration counts = 1024,1152,1280,1408
holdout count = 1536
block length = 128
band modes = fixed_c3, full_relative
Q = 2048,8192
kernel exponent = 1; beta = 2; height = 66
laws = all_plus, alternating_index, mod4_character, half_split
normalizations = local_diagonal, pooled_train_scalar
transfer error cap = 0.03; spectral cap = 0.64; Schur cap = 0.83
~~~

The selection and holdout roles are fixed before current-family responses are
read.  The TPC-390 parent certificate is locked by normalized SHA-256:

~~~text
parent schema = TPC390_C1_RECURSIVE_SLOPE_COMPOSITION_V1
parent producer SHA-256 = ec9cc88a9b05a7561fc0f8fee41352c6639d3990ae593e1affc91a079ad7e144
parent certificate SHA-256 = 870c92db4c697a1a822554256019657e1c3c27ab78f9e76a41b4ade5911d34d0
parent slopes refit on current family = false
~~~

The intermediate lengths are calibration-only.  The terminal 1536 readout
uses the two origins whose holdout role was declared in advance.

## Forecast and localization

For each cell, S_N is the mean band spectral diagnostic over the relevant
origins.  Let alpha_P be the frozen parent slope and let

~~~text
alpha_L = log(S_1280 / S_1024) / log(1280 / 1024).
~~~

For every N in {1152,1280,1408,1536}, direct parent and local forecasts are
anchored at S_1024:

~~~text
P_N = S_1024 * (N/1024)^alpha_P
L_N = S_1024 * (N/1024)^alpha_L
~~~

For N >= 1280, the parent forecast is also evaluated by first forecasting
1024 -> 1280 and then 1280 -> N.  The direct/staged identity is recorded
exactly.  The first horizon with absolute parent error above 0.03 is stored
per cell; no failing cell or horizon is removed after readout.

## Finite findings

~~~text
rows = 448; cells = 32
parent pass by horizon (1152,1280,1408,1536) = 32/32,32/32,32/32,23/32
local pass by horizon (1152,1280,1408,1536) = 32/32,32/32,32/32,32/32
recursive pass by horizon (1280,1408,1536) = 32/32,32/32,23/32
first parent crossing = 9 at 1536; 0 at every earlier horizon
parent max error = 0.0097231600284870545, 0.019799860658296864,
                   0.029171461379271735, 0.051733528427127862
local max error = 0.0013662092272366255, 2.22e-16,
                  0.0026116447189823422, 0.016641234963871265
recursive composition max residual = 4.4408920985006262e-16
stable cells = 24/32,24/32,24/32,24/32,30/32
spectral failures / Schur failures = 112/448, 0/448
~~~

The terminal parent failures are therefore horizon-localized on this finite
panel.  The local control does not cross the transfer cap.  This supports a
scoped obstruction statement about the frozen interface, while leaving the
source-valid normalization, origin/count uniformity, growing operator bound,
and arithmetic L2 questions open.

## Claim firewall

~~~text
TPC391_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC391_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC391_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC391_HORIZON_PANEL = NUMERICALLY_CERTIFIED_FINITE_448_ROWS
TPC391_PARENT_HORIZON_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC391_LOCAL_CONTROL = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC391_HORIZON_TRAJECTORY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC391_RECURSIVE_COMPOSITION = PROVED_EXACT_FINITE_NUMERICAL_IDENTITY
TPC391_ORIGIN_UNIFORMITY = OPEN
TPC391_COUNT_UNIFORMITY = OPEN
TPC391_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC391_GROWING_OPERATOR_BOUND = OPEN
TPC391_SOURCE_UNIFORM_L2 = OPEN
TPC391_ARITHMETIC_ADVANCE = NO
TPC391_FIXED_POWER_CREDIT = 0
TPC391_FULL_GATE_B = OPEN
TPC391_TWIN_PRIME_RESULT = NONE
~~~

The official Session propose.md, Route-A evaluator, and Route-B evaluator are
absent from this checkout.  The local checker is fail-closed repository
evidence only; it cannot declare an official Route-A or Route-B pass.

## Reproduction

~~~bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-391-c1-recursive-horizon-localization/code/tpc391_recursive_horizon_localization.py --check
python -O -B papers/tpc-391-c1-recursive-horizon-localization/code/tpc391_recursive_horizon_localization.py --check
python -B papers/tpc-391-c1-recursive-horizon-localization/experiments/tpc391_independent_checker.py --check
python -O -B papers/tpc-391-c1-recursive-horizon-localization/experiments/tpc391_independent_checker.py --check
python -B papers/tpc-391-c1-recursive-horizon-localization/experiments/tpc391_adversarial_certificate_stress.py --check
python -O -B papers/tpc-391-c1-recursive-horizon-localization/experiments/tpc391_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc391_c1_recursive_horizon_localization_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc391_c1_recursive_horizon_localization_checker.py --check
~~~

The release requires paper/main.pdf and paper/paper.pdf to be byte-identical
copies.
