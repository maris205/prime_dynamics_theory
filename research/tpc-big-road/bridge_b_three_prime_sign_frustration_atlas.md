# Bridge-B note: TPC-292 three-prime sign frustration atlas

TPC-292 is the next structural bridge after the TPC-291 pairwise Schur
cancellation atlas.  It keeps the literal source, physical deleted-diagonal
operator, interval, and prime-shell family fixed, and asks whether three
pairwise cancellation preferences can be realized by one coefficient-sign
assignment.

For nonzero cross terms on a triangle, the exact parity rule is
`a_i*a_j*sign(G_ij)=-1` on all edges if and only if
`sign(G_12 G_13 G_23)=-1`.  The product `+1` case is sign-frustrated.  The
three-vector projection residual is the exact Schur quotient
`det(G_ijk)/(G_ii det(G_(j,k)))`.

The exact-rational finite replay covers all 5,727 unordered triples in the
18-row TPC-291 grid.  It finds 5,718 sign-frustrated triples and 9
anti-alignable triples; all 5,727 normalized Gram volumes are positive.  The
late `(512,58,90,5,2)` row contributes 680 `+++` triangles, so its strong
near-dependence remains sign-frustrated rather than becoming a common
all-pair cancellation direction.

```text
TPC292_MAXIMUM_CLAIM = PROVED_EXACT_TRIANGLE_SIGN_PARITY_AND_THREE_VECTOR_SCHUR_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGN_FRUSTRATION_ATLAS
TPC292_ROUTE_ADVANCE = YES_SCOPED_PAIRWISE_TO_THREE_PRIME_COMPATIBILITY_OBSTRUCTION
TPC292_TRIANGLE_SIGN_PARITY = PROVED_EXACT_CONDITIONAL
TPC292_THREE_VECTOR_SCHUR_IDENTITY = PROVED_EXACT_FINITE
TPC292_NORMALIZED_VOLUME = PROVED_EXACT_FROM_GRAM_PSD
TPC292_TRIANGLE_ATLAS = NUMERICALLY_CERTIFIED_FINITE_5727_TRIPLES
TPC292_SIGN_FRUSTRATION = NUMERICALLY_CERTIFIED_FINITE_5718_OF_5727
TPC292_ANTI_ALIGNABLE = NUMERICALLY_CERTIFIED_FINITE_9_OF_5727
TPC292_GROWING_TRIANGLE_COMPATIBILITY = OPEN
TPC292_SOURCE_NATIVE_L2 = OPEN_LITERAL_SOURCE
TPC292_FIXED_POWER_CREDIT = 0
TPC292_FULL_GATE_B = OPEN
TPC292_TWIN_PRIME_RESULT = NONE
TPC292_STATUS = PROVED_EXACT_TRIANGLE_SIGN_PARITY_AND_THREE_VECTOR_SCHUR_IDENTITY_PLUS_NUMERICALLY_CERTIFIED_FINITE_SIGN_FRUSTRATION_ATLAS
TPC292_ROUND2_CLUE = TEST_SIGNED_GRAPH_MAXCUT_AND_MULTI_PRIME_RAYLEIGH_COMPATIBILITY
```

The nine anti-alignable cases are finite crossover exceptions, not an
asymptotic shell theorem.  The next route question is whether a whole signed
prime graph has a useful frustration index, and whether any surviving sign
pattern lies in the coefficient image of the literal source.  Arithmetic
`L2`, fixed-power credit, full Gate B, and the twin-prime endpoint remain
open.  The Session-named evaluator files are absent from this checkout; the
project proof package, canonical certificate, independent replay, stress
test, and Bridge-B checker are the local fail-closed validation package.
