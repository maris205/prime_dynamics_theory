# Bridge-B — TPC-296 least-norm source budget and native-ray obstruction

```text
TPC296_MAXIMUM_CLAIM = PROVED_EXACT_LEAST_NORM_SOURCE_BUDGET_AND_SOURCE_ENERGY_TRADEOFF_PLUS_NUMERICALLY_CERTIFIED_FINITE_COST_PROFILE_ATLAS
TPC296_ROUTE_ADVANCE = YES_SCOPED_SOURCE_IMAGE_TO_LEAST_NORM_BUDGET_AND_PROFILE_GEOMETRY
TPC296_LEAST_NORM_IDENTITY = PROVED_EXACT_FINITE
TPC296_BUDGET_FEASIBILITY_CRITERION = PROVED_EXACT_FINITE
TPC296_SOURCE_ENERGY_TRADEOFF = PROVED_EXACT_FINITE
TPC296_COST_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_ROWS_HIGH_PRECISION_REPLAY
TPC296_UNRESTRICTED_BUDGET_TEST = NUMERICAL_OBSERVATION_FINITE_18_OF_18_BELOW_1E_MINUS_3
TPC296_ONE_RAY_PROFILE_OBSTRUCTION = NUMERICAL_OBSERVATION_FINITE_18_OF_18_RMS_AT_LEAST_0_9
TPC296_NATIVE_RESTRICTED_PROFILE = OPEN_LITERAL_SOURCE
TPC296_GROWING_SOURCE_BUDGET = OPEN
TPC296_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC296_FIXED_POWER_CREDIT = 0
TPC296_FULL_GATE_B = OPEN
TPC296_TWIN_PRIME_RESULT = NONE
TPC296_ROUND2_CLUE = TEST_RESTRICTED_PROFILE_DIMENSION_AND_GROWING_SOURCE_BUDGET
```

## Interpretation

TPC-295 removed the finite unrestricted image obstruction: when the physical
columns form a full-rank matrix `A`, every finite target `b` is attained by a
rational source vector.  TPC-296 quantifies the cheapest such witness.  With
`G=A^T A`, the exact least-norm solution of `A^T h=b` is

\[
 h_b=A G^{-1}b,\qquad
 S_A(b)=\min_{A^T h=b}\|h\|_2^2=b^T G^{-1}b.
\]

The same finite linear algebra gives the iff budget test
`S_A(b) <= B` and the exact source/physical-energy tradeoff
`S_A(b)(b^TGb) >= (b^Tb)^2`.  A separate one-ray projection measures the
distance from a target to `span{A^T beta}`.

On the inherited 18-row, 1,380-edge grid, a 70-digit source-first replay
certifies that the weighted minimizer, unit-edge max-cut target, and
all-positive target all have unrestricted cost ratio below the declared
`1e-3` threshold on every row.  At the same time, every weighted minimizer
and every max-cut target has one-ray RMS at least `0.9` on all 18 rows, while
the all-positive target is close to the ray in the declared finite proxy.
This separates two issues that TPC-295 left conflated: ambient source norm is
not the finite bottleneck, but the dimension and geometry of the admissible
native profile may be.

The budget threshold and frozen-beta ray are explicit modeling choices.  They
are finite diagnostics, not arithmetic Gate-B hypotheses, and earn no power
credit.  No growing-shell source-budget estimate, literal Mobius/comparison
profile image theorem, arithmetic `L2` estimate, twin-prime conclusion, or
official Session evaluator pass is claimed.  The Session-named evaluator
files are absent from this checkout; the local proof package, canonical
certificate, independent replay, stress suite, PDF audit, and this
fail-closed Bridge-B checker are the available validation path.

## Local verification

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-296-source-norm-budget-interface/code/tpc296_source_norm_budget_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-296-source-norm-budget-interface/experiments/tpc296_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-296-source-norm-budget-interface/experiments/tpc296_budget_stress.py
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_tpc296_source_norm_budget_interface_checker.py --check
```

The checker locks the producer and canonical-result hashes, checks the full
paper tree and PDF, and requires normal/optimized producer, independent, and
stress invocations to have empty standard error and byte-identical output.
