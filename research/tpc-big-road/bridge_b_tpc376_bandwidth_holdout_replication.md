# Bridge-B — TPC-376 response-blind bandwidth holdout

This is a local fail-closed bridge for TPC-376.  It is repository evidence,
not an official Route-A or Route-B evaluator verdict; the official evaluator
files named by the Session are absent.

## Frozen object

~~~text
schema        = TPC376_BANDWIDTH_HOLDOUT_REPLICATION_V1
grid          = a_j=1010001+401j, 0<=j<41
training      = indices (0,20,40)
holdout       = indices (5,15,30), origins (1012006,1016016,1022031)
panel         = 3 origins x 3 Q anchors, beta=2, all-plus = 9 rows
window        = 2048 points, eight contiguous blocks of length 256
band          = block distance <= 1
normalization = full-window square-energy geometry
caps          = spectral 0.64, Schur 0.83
~~~

The holdout is index-disjoint from the training selection.  The first two
coordinate windows overlap neighboring training windows; no stronger
coordinate-disjoint claim is made.

## Finite result and firewall

~~~text
spectral failure profile by Q = (0,3,3)
total spectral failures      = 6/9
Schur failures                = 0/9
absolute Rayleigh retention  = 0.93760019185559207--0.976941204869197
maximum tail fraction         = 0.062399808144408715
~~~

This is a finite response-blind grid-index replication of the TPC-375
profile.  It does not establish origin/window uniformity, a growing
operator bound, cross-block causality, source-uniform arithmetic L2,
fixed-power credit, Route-B closure, or a twin-prime result.

~~~text
TPC376_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC376_HOLDOUT_REPLAY = NUMERICALLY_CERTIFIED_FINITE_9_ROWS
TPC376_PARENT_Q_PROFILE_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC376_ARITHMETIC_ADVANCE = NO
TPC376_FIXED_POWER_CREDIT = 0
TPC376_FULL_GATE_B = OPEN
TPC376_TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_WINDOW_SCALE_HOLDOUT
~~~

## Reproduction contract

The bridge checks the canonical certificate, all package-file provenance
hashes, PDF identity and clean compile log, then runs producer, independent
replay and mutation stress in both normal and optimized Python modes.  Every
subcheck must return zero, have empty stderr, and emit byte-identical output
across optimization modes.
