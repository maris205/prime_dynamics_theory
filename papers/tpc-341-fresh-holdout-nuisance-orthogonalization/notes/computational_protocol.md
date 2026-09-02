# TPC-341 computational protocol

The producer uses the parent-locked all-plus `Q=54`, exponent-1, `H=66`
operator and nine coordinate bijections.  It audits the three disjoint rows

```text
(origin, scale) = (48097,1024), (48609,1024), (49217,1024)
```

The corresponding intervals are `[48097,48608]`, `[48609,49120]`, and
`[49217,49728]`; every shifted argument is below `50,000`.  For each row it
records four masks times nine controls, then computes an all-control nuisance
projection and nine leave-one-control-out projections.  NumPy SVD is used
only to obtain the finite column-space basis; the rank rule is recorded in the
certificate.  Normal and optimized Python replays, an independent reverse
engine, and mutation stress are required.
