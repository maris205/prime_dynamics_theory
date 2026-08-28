# Bridge-B — TPC-294 magnitude-weighted signed Rayleigh atlas

```text
TPC294_MAXIMUM_CLAIM = PROVED_EXACT_TRACE_NORMALIZED_SIGNED_QUADRATIC_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_GLOBAL_SIGN_ATLAS
TPC294_ROUTE_ADVANCE = YES_SCOPED_FINITE_SIGN_LAYER_TO_MAGNITUDE_WEIGHTED_RAYLEIGH_LAYER
TPC294_TRACE_NORMALIZED_IDENTITY = PROVED_EXACT_FINITE
TPC294_GLOBAL_SIGN_ENUMERATION = PROVED_EXACT_FINITE
TPC294_GRAM_NONNEGATIVITY = PROVED_EXACT_FINITE
TPC294_WEIGHTED_RAYLEIGH_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_ROWS
TPC294_EQUAL_SIGNED_CONTRACTION = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_BELOW_ONE
TPC294_ALL_POSITIVE_AMPLIFICATION = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_ONE
TPC294_MAXCUT_CANDIDATE_CONTRACTION = NUMERICALLY_CERTIFIED_FINITE_18_OF_18_BELOW_ONE
TPC294_WEIGHTED_VS_MAXCUT = NUMERICALLY_CERTIFIED_FINITE_DIFFERENT_18_OF_18
TPC294_EDGES = NUMERICALLY_CERTIFIED_FINITE_1380
TPC294_OPTIMUM_LE_QUARTER = NUMERICALLY_CERTIFIED_FINITE_13_OF_18
TPC294_OPTIMUM_LE_TENTH = NUMERICALLY_CERTIFIED_FINITE_8_OF_18
TPC294_SOURCE_NATIVE_COEFFICIENT_IMAGE = OPEN_LITERAL_SOURCE
TPC294_GROWING_WEIGHTED_THEOREM = OPEN
TPC294_ARITHMETIC_L2 = OPEN_LITERAL_SOURCE
TPC294_FIXED_POWER_CREDIT = 0
TPC294_FULL_GATE_B = OPEN
TPC294_TWIN_PRIME_RESULT = NONE
TPC294_ROUND2_CLUE = TEST_SOURCE_IMAGE_OF_WEIGHTED_OPTIMAL_SIGN_PATTERNS_AND_DIFFUSE_SIGNED_WEIGHTS
```

## Interpretation

TPC-293 optimized a unit-weight signed complete graph.  TPC-294 restores the
exact Gram magnitudes and exhaustively minimizes

\[
R(a)=a^{\mathsf T}Ga/\operatorname{tr}(G)
\]

over equal coefficient signs on the 18 inherited frozen rows.  The finite
weighted optimum is below one in every row, but it is a different object from
the max-cut witness in every row.  The strongest displayed minimum is
`0.0496374497659` at `(N,H,Q,z,s)=(512,58,90,5,2)`; the exceptional crossover
row has max-cut quotient `0.988974603760` and weighted optimum
`0.519059163428`.

This is a finite/source-unconstrained structural advance.  The certificate
does not establish that the sign vector is in the native source image, does
not provide a growing-shell estimate, and pays no arithmetic or twin-prime
credit.  The Session-named Route-A/Route-B evaluator files are absent from
the checkout; the local Bridge-B checker is fail-closed and makes no official
evaluator claim.

## Local verification

```bash
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/code/tpc294_magnitude_weighted_signed_rayleigh_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/experiments/tpc294_independent_checker.py
PYTHONDONTWRITEBYTECODE=1 python -B papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas/experiments/tpc294_magnitude_weighted_stress.py
PYTHONDONTWRITEBYTECODE=1 python -B research/tpc-big-road/tpc_bridge_b_magnitude_weighted_signed_rayleigh_atlas_checker.py --check
```

The checker locks the producer and canonical result hashes, checks the
project tree and PDF, and runs normal/optimized producer, independent, and
stress invocations with empty stderr and byte-identical stdout.
