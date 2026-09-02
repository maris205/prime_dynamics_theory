# Bridge B — TPC-338 growing-control covariance spectrum

## Scope

TPC-338 keeps the TPC-337 source and fixed all-plus operator, and compares its
five-control orbit with a nine-control orbit on the same six windows.  The
additional controls are four explicitly declared odd affine bijections.

## Certified finite facts

```text
TPC338_NESTED_COVARIANCE_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC338_COVARIANCE_GRAM_PSD = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC338_ENERGY_DOMINANCE_STABILITY = NUMERICALLY_CERTIFIED_FINITE_6_OF_6
TPC338_NORMALIZED_SPECTRUM_STABILITY = NUMERICALLY_CERTIFIED_FINITE_6_ROWS
TPC338_TWIN_ZERO_SIGN_STABILITY = REFUTED_SCOPED
TPC338_TWIN_ZERO_SIGN_REVERSAL = NUMERICALLY_CERTIFIED_FINITE_6_OF_6_NESTED_COMPARISON
TPC338_TWIN_BACKGROUND_SIGN = NUMERICALLY_CERTIFIED_FINITE_POSITIVE_6_OF_6_BOTH_ENSEMBLES
TPC338_BACKGROUND_ZERO_SIGN = NUMERICALLY_CERTIFIED_FINITE_NEGATIVE_6_OF_6_BOTH_ENSEMBLES
TPC338_NINE_CENTERED_FRACTION = [0.87718018381890517,0.89726357864346618]
TPC338_NORMALIZED_SPECTRUM_L1 = [0.026439631324708706,0.044059181229585159]
TPC338_ARITHMETIC_ADVANCE = NO
TPC338_FIXED_POWER_CREDIT = 0
TPC338_SOURCE_UNIFORM_L2 = OPEN
TPC338_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC338_FULL_GATE_B = OPEN
TPC338_TWIN_PRIME_RESULT = NONE
TPC338_STATUS = NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_COVARIANCE_SPECTRUM
TPC338_ROUND2_CLUE = REPLACE_SIGN_HEURISTICS_BY_A_UNIFORM_MASKED_OPERATOR_ENVELOPE
```

The five-control twin--zero covariance is negative in all six rows, while the
nine-control value is positive in all six.  This is a scoped counterexample to
ensemble-invariant signed interaction, not a claim about all control sets.

## Local fallback commands

```bash
python -B papers/tpc-338-growing-control-covariance-spectrum/code/tpc338_growing_control_covariance_spectrum.py --check
python -O -B papers/tpc-338-growing-control-covariance-spectrum/code/tpc338_growing_control_covariance_spectrum.py --check
python -B papers/tpc-338-growing-control-covariance-spectrum/experiments/tpc338_independent_checker.py --check
python -O -B papers/tpc-338-growing-control-covariance-spectrum/experiments/tpc338_independent_checker.py --check
python -B papers/tpc-338-growing-control-covariance-spectrum/experiments/tpc338_spectrum_stress.py --check
python -O -B papers/tpc-338-growing-control-covariance-spectrum/experiments/tpc338_spectrum_stress.py --check
```

The official Session-named evaluator files are absent.  The local wrapper is
fail-closed and does not claim an official Route-A or Route-B pass.
