# Bridge B — TPC-336 masked signed-Gram response

## Scope

TPC-336 applies the TPC-335 four support masks to one fixed all-plus
deleted-diagonal prime-shell operator with `Q=54`, exponent `1`, and `H=66`.
The finite panel has two origins, three scales, and six rows.

## Certified finite facts

```text
TPC336_MASK_RESPONSE_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC336_FIXED_OPERATOR_REPLAY = NUMERICALLY_CERTIFIED_FINITE_6_ROWS
TPC336_GAIN_ORDERING = NUMERICALLY_CERTIFIED_FINITE_6_OF_6
TPC336_DESTRUCTIVE_OUTPUT_INTERACTION = NUMERICALLY_CERTIFIED_FINITE_6_OF_6
TPC336_TWIN_RESPONSE_DOMINANCE = REFUTED_SCOPED_FINITE_PANEL
TPC336_SELF_TO_FULL_RATIO = [4.8538535937774503, 5.4814134328177246]
TPC336_ARITHMETIC_ADVANCE = NO
TPC336_FIXED_POWER_CREDIT = 0
TPC336_SOURCE_UNIFORM_L2 = OPEN
TPC336_FULL_GATE_B = OPEN
TPC336_TWIN_PRIME_RESULT = NONE
TPC336_STATUS = NUMERICALLY_CERTIFIED_FINITE_MASKED_SIGNED_GRAM_RESPONSE
TPC336_ROUND2_CLUE = RETURN_TO_CONTROL_COVARIANCE_OR_SEEK_UNIFORM_MASKED_OPERATOR_BOUND
```

The output Gram matrix is stored row by row, including all cross-class terms;
the local result is a fail-closed fallback because the official evaluator
files are absent from this checkout.

## Local fallback commands

```bash
python -B papers/tpc-336-masked-signed-gram-response/code/tpc336_masked_signed_gram_response.py --check
python -O -B papers/tpc-336-masked-signed-gram-response/code/tpc336_masked_signed_gram_response.py --check
python -B papers/tpc-336-masked-signed-gram-response/experiments/tpc336_independent_checker.py --check
python -B papers/tpc-336-masked-signed-gram-response/experiments/tpc336_response_stress.py --check
```
