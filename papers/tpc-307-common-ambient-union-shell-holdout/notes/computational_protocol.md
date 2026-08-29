# TPC-307 computational protocol

The producer locks the normalized-LF SHA-256 digests of the TPC-305 and
TPC-306 source/result artifacts.  It reconstructs the fixed TPC-302 rows at
`N=512`, `H=58`, `z=5`, and uses `Q=(50,60,70,90)`, exponents `(1,2)`, and
`tau=(.25,.5,.75)`.  Each adjacent pair produces one union shell, one overlap
fit matrix, and two directional exclusive holdouts.

The profile matrix has 17 cutoff columns.  For each directional target the
producer finds the first feasible prefix, chooses the maximum of the two
prefixes, solves the constrained source-budget frontier, and predicts over
the union.  It records three positive source normalizers, budget ratios, MSE
holdout ratios, and a strict `.9/1.1` classification.

The physical matrix is assembled by vectorizing the locked literal deleted-
diagonal formula in float64 and then converting entries to decimal strings for
the `mpmath` solve.  Relative enclosure padding is `1e-5`; therefore the
finite atlas is labelled `NUMERICALLY_REPRODUCED_FINITE`.  The independent
checker imports neither the producer nor its helper functions: it loads the
frozen TPC-268 engine, rebuilds the rows with NumPy, and verifies all printed
case-level values and classes.  The stress suite tests exact small rational
surrogates for the protocol identities.
