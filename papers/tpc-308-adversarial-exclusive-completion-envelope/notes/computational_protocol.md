# TPC-308 computational protocol

The producer locks the normalized-LF code and result hashes of TPC-307.  It
reuses the TPC-307 common ambient matrix, overlap-only frontier coefficients,
comparison prefix, and aligned native exclusive targets.  For each of the 18
cells (`Q=(50,60,70,90)`, adjacent transitions, exponents `1,2`, tolerances
`.25,.5,.75`) it enumerates all binary flips of each exclusive target up to
radii `0,1,2`.

For a holdout of length `m`, the candidate counts per side are
`sum_{j=0}^{min(r,m)} binom(m,j)`.  The producer records native, minimum, and
maximum MSE intervals for each side, then forms a conservative positive
right-over-left ratio interval.  Strict classes use thresholds `.9` and `1.1`.

The physical construction is inherited from the TPC-307 float64 literal
replay; the parent then converts matrix entries to `mpmath` values for the
frontier.  Relative padding is `1e-5`, so the result is labelled numerical
reproduction.  The standalone checker does not import the TPC-308 producer;
it rebuilds source profiles and physical rows from the frozen TPC-268 engine,
re-solves the frontier with NumPy, enumerates the same finite balls, and checks
the stored values with `2e-3` relative replay slack.

The exact stress suite uses rational predictions and targets to test candidate
counts, extrema, nesting, zero-radius recovery, sign invariance, and the
threshold truth table.  Neither suite supplies a probability model for the
completion labels.
