# Bridge B — TPC-337 control covariance of masked responses

## Scope

TPC-337 takes the four TPC-336 source masks and applies five predeclared
coordinate bijections before the fixed all-plus deleted-diagonal shell matrix
(`Q=54`, exponent `1`, `H=66`).  The panel has two origins and three scales,
for six windows and twenty-four class-level decompositions.

## Certified finite facts

```text
TPC337_MEAN_CENTERED_OUTPUT_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC337_COVARIANCE_GRAM_PSD = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC337_MASKED_CONTROL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_ROWS_5_CONTROLS
TPC337_FULL_CENTERED_COVARIANCE_DOMINANCE = NUMERICALLY_CERTIFIED_FINITE_6_OF_6
TPC337_TWIN_BACKGROUND_COVARIANCE_SIGN = NUMERICALLY_CERTIFIED_FINITE_POSITIVE_6_OF_6
TPC337_ZERO_BACKGROUND_COVARIANCE_SIGN = NUMERICALLY_CERTIFIED_FINITE_NEGATIVE_6_OF_6
TPC337_SOURCE_SHARE_TRANSFER = REFUTED_SCOPED
TPC337_FULL_COHERENT_FRACTION = [0.14470178324009286,0.21496774521290674]
TPC337_FULL_CENTERED_FRACTION = [0.78503225478709315,0.85529821675990692]
TPC337_ARITHMETIC_ADVANCE = NO
TPC337_FIXED_POWER_CREDIT = 0
TPC337_SOURCE_UNIFORM_L2 = OPEN
TPC337_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC337_FULL_GATE_B = OPEN
TPC337_TWIN_PRIME_RESULT = NONE
TPC337_STATUS = NUMERICALLY_CERTIFIED_FINITE_CONTROL_COVARIANCE_MASKED_RESPONSE
TPC337_ROUND2_CLUE = GROW_THE_CONTROL_ORBIT_AND_TEST_COVARIANCE_SPECTRUM_STABILITY
```

The covariance matrix is a Gram matrix of centered output vectors.  The
negative selected entries are therefore anti-alignment observations, not a
failure of positive semidefiniteness.  The exact rational anchor records the
pair identity with average, coherent, and centered cross terms `0`, `1/2`, and
`-1/2`.

## Local fallback commands

```bash
python -B papers/tpc-337-control-covariance-masked-response/code/tpc337_control_covariance_masked_response.py --check
python -O -B papers/tpc-337-control-covariance-masked-response/code/tpc337_control_covariance_masked_response.py --check
python -B papers/tpc-337-control-covariance-masked-response/experiments/tpc337_independent_checker.py --check
python -O -B papers/tpc-337-control-covariance-masked-response/experiments/tpc337_independent_checker.py --check
python -B papers/tpc-337-control-covariance-masked-response/experiments/tpc337_covariance_stress.py --check
python -O -B papers/tpc-337-control-covariance-masked-response/experiments/tpc337_covariance_stress.py --check
```

The official Session-named evaluator files are absent from this checkout.  A
local Bridge-B wrapper is consequently fail-closed and does not claim an
official Route-A or Route-B pass.
