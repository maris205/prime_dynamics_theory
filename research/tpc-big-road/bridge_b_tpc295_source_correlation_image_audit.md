# Bridge-B — TPC-295 source-correlation image and finite signed feasibility

```text
TPC295_MAXIMUM_CLAIM = PROVED_EXACT_FULL_RANK_IMPLIES_SOURCE_CORRELATION_SURJECTIVITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_MODULAR_FULL_RANK_ATLAS
TPC295_ROUTE_ADVANCE = YES_SCOPED_AMBIENT_SIGN_TARGETS_TO_UNRESTRICTED_FINITE_SOURCE_IMAGE
TPC295_FULL_RANK_IMPLICATION = PROVED_EXACT_FINITE
TPC295_LEAST_NORM_WITNESS_FORMULA = PROVED_EXACT_FINITE
TPC295_MODULAR_FULL_RANK_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_TWO_MODULI
TPC295_UNRESTRICTED_SOURCE_CORRELATION_SURJECTIVITY = NUMERICALLY_CERTIFIED_FINITE_18_OF_18
TPC295_WEIGHTED_MINIMIZER_SOURCE_REALIZABILITY = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_UNRESTRICTED
TPC295_MAXCUT_SOURCE_REALIZABILITY = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_UNRESTRICTED
TPC295_ALL_POSITIVE_SOURCE_REALIZABILITY = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_UNRESTRICTED
TPC295_EDGES = NUMERICALLY_CERTIFIED_FINITE_1380
TPC295_NATIVE_RESTRICTED_PROFILE = OPEN_LITERAL_SOURCE
TPC295_SOURCE_WITNESS_NORM = OPEN
TPC295_GROWING_SOURCE_IMAGE = OPEN
TPC295_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC295_FIXED_POWER_CREDIT = 0
TPC295_FULL_GATE_B = OPEN
TPC295_TWIN_PRIME_RESULT = NONE
TPC295_ROUND2_CLUE = TEST_SOURCE_NORM_COST_AND_RESTRICTED_NATIVE_PROFILE_IMAGE
```

## Interpretation

TPC-294 optimized the exact weighted Gram form in an ambient equal-sign cube.
TPC-295 defines the finite source-correlation map

\[
C=A^{\mathsf T}:\mathbb Q^I\longrightarrow\mathbb Q^S,
\qquad C(h)=(\langle h,g_q\rangle)_{q\in S},
\]

and proves that a nonsingular Gram matrix makes this map surjective, with the
explicit witness `h=A G^{-1} b`.  Two independently replayed modular
determinant calculations certify full rank on all 18 inherited rows.  The
TPC-294 weighted minimizer, its unit-edge max-cut comparison, and the
all-positive target are therefore all attainable in the explicitly broad
finite rational source space on every row.

This is a finite image result, not a native arithmetic-profile theorem.  The
source vector is unrestricted in `Q^I`; no Mobius/comparison parametrization,
uniform witness-norm bound, growing-shell statement, arithmetic `L2` credit,
or twin-prime conclusion is claimed.  The least-norm witness formula makes
the next obstruction quantitative rather than combinatorial.

The Session-named Route-A/Route-B evaluator files are absent from this
checkout.  This bridge therefore records the local proof package, canonical
certificate, independent replay, stress test, and this fail-closed checker;
it does not declare an official evaluator pass.

## Local verification

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-295-source-correlation-image-audit/code/tpc295_source_correlation_image_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-295-source-correlation-image-audit/experiments/tpc295_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-295-source-correlation-image-audit/experiments/tpc295_source_image_stress.py
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_tpc295_source_correlation_image_audit_checker.py --check
```

The checker locks the producer and canonical result hashes, checks the full
paper tree and PDF, and requires normal/optimized producer, independent, and
stress invocations to have empty standard error and byte-identical output.
