# Bridge-B note: TPC-293 signed shell max-cut atlas

TPC-293 is the direct shell-level continuation of TPC-292.  It keeps the
literal source, physical deleted-diagonal operator, interval, kernel, and
prime-shell family fixed, and replaces the triangle question by a signed
complete-graph objective.  An edge is favorable when
`a_i*a_j*sign(G_ij)=-1`.

The exact all-positive benchmark is `floor(m^2/4)`, and the finite frustration
index is the complement of the signed max-cut value.  On the inherited
18-row grid the certificate covers 1,380 edges and 5,727 triangles.  Seventeen
rows are all-positive and attain the benchmark.  The only exception is the
`(256,38,27,5,1)` crossover row, where three negative edges produce a finite
`+3` sign-only gain (15 rather than 12 favorable edges).

```text
TPC293_MAXIMUM_CLAIM = PROVED_EXACT_ALL_POSITIVE_MAXCUT_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGNED_SHELL_FRUSTRATION_ATLAS
TPC293_ROUTE_ADVANCE = YES_SCOPED_THREE_PRIME_TO_WHOLE_SHELL_SIGNED_GRAPH
TPC293_ALL_POSITIVE_MAXCUT = PROVED_EXACT_CONDITIONAL
TPC293_SIGNED_OBJECTIVE = PROVED_EXACT_FINITE
TPC293_SWITCHING_INVARIANCE = PROVED_EXACT_FINITE
TPC293_SIGNED_MAXCUT_ATLAS = NUMERICALLY_CERTIFIED_FINITE_18_ROWS
TPC293_EDGE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_1380_EDGES
TPC293_MAX_FAVORABLE = NUMERICALLY_CERTIFIED_FINITE_744
TPC293_MINIMUM_UNSATISFIED = NUMERICALLY_CERTIFIED_FINITE_636
TPC293_EXCEPTIONAL_GAIN = NUMERICALLY_CERTIFIED_FINITE_PLUS_3_EDGES_ONE_ROW
TPC293_GROWING_SIGNED_GRAPH = OPEN
TPC293_MAGNITUDE_WEIGHTED_RAYLEIGH = OPEN
TPC293_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE
TPC293_FIXED_POWER_CREDIT = 0
TPC293_FULL_GATE_B = OPEN
TPC293_TWIN_PRIME_RESULT = NONE
TPC293_STATUS = PROVED_EXACT_ALL_POSITIVE_MAXCUT_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGNED_SHELL_FRUSTRATION_ATLAS
TPC293_ROUND2_CLUE = TEST_MAGNITUDE_WEIGHTED_SIGNED_RAYLEIGH_AND_SOURCE_IMAGE
```

The `+3` is an unweighted sign diagnostic, not physical cancellation credit.
The growing-shell theorem, magnitude-weighted objective, source-restricted
coefficient image, arithmetic `L2`, full Gate B, and the twin-prime endpoint
remain open.  The Session-named Route-A/Route-B evaluator files are absent
from this checkout; the project proof package, canonical certificate,
independent replay, stress test, and this Bridge-B checker are the local
fail-closed validation package.
