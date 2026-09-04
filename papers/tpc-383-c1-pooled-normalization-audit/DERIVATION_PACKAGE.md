# TPC-383 derivation package

Let `M_{o,Q,ell}` be the finite raw law matrix and `g_{o,Q}(i)` its common
square-energy geometry.  The two audited matrices are

`A^loc_{ij}=M_{ij}/sqrt(g(i)g(j))`,
`A^pool_{ij}=M_{ij}/G_Q`,

where `G_Q` is the arithmetic mean of all `g_{o,Q}(i)` over the three fixed
origins and all coordinates.  The same block-distance-one mask is applied to
both matrices.  The reported observable is the largest absolute eigenvalue of
the masked matrix.

For each law/Q/normalization cell, the origin spread is
`(max s-min s)/mean s`.  All constants, origins, laws, and the one-percent
predicate are fixed before the matrix metrics are read.

The finite exact component is the common geometry and law-independent pooled
scalar construction.  The spectral values are numerical finite outputs,
recomputed by an independent reverse-shell implementation.  Neither
normalization is identified with a source-valid arithmetic law, and no limit
or power credit is inferred.
