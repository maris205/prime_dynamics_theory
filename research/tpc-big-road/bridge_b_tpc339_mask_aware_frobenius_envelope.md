# Bridge B — TPC-339 mask-aware Frobenius envelope

## Scope

TPC-339 replaces the control-dependent signed covariance heuristic with the
support-restricted Frobenius inequality on six windows, four masks, and the
nine controls inherited from TPC-338.

## Certified finite facts

```text
TPC339_SUPPORT_FROBENIUS_BOUND = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC339_MASKED_CONTROL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_RECORDS
TPC339_BOUND_CENSUS = NUMERICALLY CERTIFIED FINITE_0_VIOLATIONS
TPC339_BROAD_MASK_SLACK = NUMERICALLY CERTIFIED FINITE OCCUPANCY_BELOW_0.2
TPC339_SIGN_FREE_REPLACEMENT = PROVED_FINITE_ONLY
TPC339_SIMPLE_ENVELOPE_TIGHTNESS = REFUTED_SCOPED
TPC339_GLOBAL_OCCUPANCY = [0.0074766258097403735,1.0000000000000024]
TPC339_BROAD_OCCUPANCY_MAX = 0.18685503656580477
TPC339_ARITHMETIC_ADVANCE = NO
TPC339_FIXED_POWER_CREDIT = 0
TPC339_SOURCE_UNIFORM_L2 = OPEN
TPC339_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC339_FULL_GATE_B = OPEN
TPC339_TWIN_PRIME_RESULT = NONE
TPC339_STATUS = NUMERICALLY_CERTIFIED_FINITE_MASK_AWARE_FROBENIUS_ENVELOPE
TPC339_ROUND2_CLUE = TEST_A_SHARPER_MASKED_GRAM_OR_NUISANCE_ORTHOGONALIZATION
```

The inequality is valid for every finite matrix, but the finite occupancy
census shows that its support-only form is loose for broad masks.

## Local fallback commands

```bash
python -B papers/tpc-339-mask-aware-frobenius-envelope/code/tpc339_mask_aware_frobenius_envelope.py --check
python -O -B papers/tpc-339-mask-aware-frobenius-envelope/code/tpc339_mask_aware_frobenius_envelope.py --check
python -B papers/tpc-339-mask-aware-frobenius-envelope/experiments/tpc339_independent_checker.py --check
python -O -B papers/tpc-339-mask-aware-frobenius-envelope/experiments/tpc339_independent_checker.py --check
python -B papers/tpc-339-mask-aware-frobenius-envelope/experiments/tpc339_envelope_stress.py --check
python -O -B papers/tpc-339-mask-aware-frobenius-envelope/experiments/tpc339_envelope_stress.py --check
```

The official Session evaluator files are absent.  The local wrapper is
fail-closed and does not claim an official Route-A or Route-B pass.
