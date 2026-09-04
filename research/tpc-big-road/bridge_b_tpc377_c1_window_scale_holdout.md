# Bridge-B — TPC-377 c=1 window-scale holdout

This is a local fail-closed bridge for TPC-377. It is repository evidence,
not an official Route-A or Route-B evaluator verdict; the official
Session-named evaluator files are absent.

## Frozen object

~~~text
origins       = 1012006,1016016,1022031
counts        = 1024,1536,2048
blocks        = length 256, counts 4,6,8
band          = block distance <= 1
Q             = 512,2048,8192
kernel        = exponent 1, height 66
law           = all_plus, beta 2
normalization = scale-wise full-window square-energy geometry
caps          = spectral 0.64, Schur 0.83
~~~

The count ladder is fixed before any response is read. At each origin the
three windows are nested prefixes with the same left endpoint. This is a
scale protocol, not an independent-sample claim.

## Finite result and firewall

~~~text
profile by count and Q = (0,3,3), (0,3,3), (0,3,3)
spectral failures      = 18/27
Schur failures         = 0/27
absolute retention     = 0.93760019185559207--0.98047323365759775
maximum tail fraction  = 0.062399808144408715
~~~

The parent high-Q support profile persists on this finite scale ladder, while
the spectral magnitudes vary with count. No growing-window, origin-uniform,
source-uniform arithmetic, or twin-prime conclusion is made.

~~~text
TPC377_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC377_NESTED_PREFIX_PROTOCOL = PROVED_EXACT_FINITE
TPC377_SCALE_LADDER_REPLAY = NUMERICALLY_CERTIFIED_FINITE_27_ROWS
TPC377_C1_PROFILE_STABILITY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC377_PARENT_Q_PROFILE_PERSISTENCE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC377_ARITHMETIC_ADVANCE = NO
TPC377_FIXED_POWER_CREDIT = 0
TPC377_FULL_GATE_B = OPEN
TPC377_TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_C1_SCALE_ORIGIN_CROSSHOLDOUT
~~~

## Reproduction contract

The bridge locks every package source, certificate, proof/route note, paper
source, PDF, compile log, and this bridge description. It then runs the
producer, independent descending-shell replay, and mutation stress in both
normal and optimized Python modes. Every subcheck must return zero, have
empty standard error, and emit byte-identical summary output.
