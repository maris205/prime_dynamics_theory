# Bridge B - TPC-340 Schur/Frobenius hybrid envelope

## Scope

TPC-340 combines the support-restricted Frobenius envelope of TPC-339 with a
global Schur envelope for the same finite symmetric all-plus shell operator.
The source, six windows, four masks, and nine coordinate controls are
parent-locked.  The result is a finite sign-free bound and a branch census;
it is not an arithmetic estimate.

## Certified finite facts

```text
TPC340_HYBRID_BOUND = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC340_HYBRID_REPLAY = NUMERICALLY_CERTIFIED_FINITE_216_RECORDS
TPC340_BOUND_CENSUS = NUMERICALLY CERTIFIED FINITE_0_VIOLATIONS
TPC340_SCHUR_BRANCH_CENSUS = NUMERICALLY_CERTIFIED_FINITE_54_RECORDS
TPC340_FROBENIUS_BRANCH_CENSUS = NUMERICALLY_CERTIFIED_FINITE_162_RECORDS
TPC340_ZERO_SUPPORT_IMPROVEMENT = NUMERICALLY CERTIFIED FINITE FACTOR 1.25 TO 4.70
TPC340_BROAD_TIGHTNESS = REFUTED_SCOPED
TPC340_GLOBAL_OCCUPANCY = [0.010649038161736056,1.0000000000000024]
TPC340_BROAD_OCCUPANCY_MAX = 0.18685503656580477
TPC340_ARITHMETIC_ADVANCE = NO
TPC340_FIXED_POWER_CREDIT = 0
TPC340_SOURCE_UNIFORM_L2 = OPEN
TPC340_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC340_FULL_GATE_B = OPEN
TPC340_TWIN_PRIME_RESULT = NONE
TPC340_STATUS = NUMERICALLY_CERTIFIED_FINITE_SCHUR_FROBENIUS_HYBRID_ENVELOPE
TPC340_ROUND2_CLUE = TEST_NUISANCE_ORTHOGONALIZATION_OR_ADVERSARIAL_HOLDOUT
```

The hybrid is the minimum of two valid upper bounds.  The finite improvement
does not constitute cancellation credit, a lower bound, or a growing result.

## Local fail-closed commands

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-340-schur-frobenius-hybrid-envelope/code/tpc340_schur_frobenius_hybrid_envelope.py --check
python -O -B papers/tpc-340-schur-frobenius-hybrid-envelope/code/tpc340_schur_frobenius_hybrid_envelope.py --check
python -B papers/tpc-340-schur-frobenius-hybrid-envelope/experiments/tpc340_independent_checker.py --check
python -O -B papers/tpc-340-schur-frobenius-hybrid-envelope/experiments/tpc340_independent_checker.py --check
python -B papers/tpc-340-schur-frobenius-hybrid-envelope/experiments/tpc340_hybrid_stress.py --check
python -O -B papers/tpc-340-schur-frobenius-hybrid-envelope/experiments/tpc340_hybrid_stress.py --check
```

The official Session evaluator files are absent.  This local wrapper is
fail-closed and does not claim an official Route-A or Route-B pass.
