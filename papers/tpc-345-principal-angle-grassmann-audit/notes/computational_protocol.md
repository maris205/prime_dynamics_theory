# TPC-345 computational protocol

The producer locks TPC-340 as the source/operator parent, TPC-341 and TPC-342
as the two panel certificates, and TPC-344 as the immediate route parent.
Each of six rows uses length 512, scale 1024, all-plus `Q=54`, exponent one,
and `H=66`.  Nine fixed bijective controls act on four declared source masks.

For raw weighting, row blocks are stacked directly.  For equal-row weighting,
each target and all nuisance columns in a row are divided by that target's
positive `L2` norm.  SVD rank uses
`max(matrix.shape)*eps*sigma_max`.  The producer records two main geometry
audits, 18 leave-one-control-out audits, four cross-panel target projections,
and a deterministic upper-triangular shear invariance test.

The reverse-shell checker uses the separately hash-locked TPC-340 independent
engine and compares all 216 record labels and energies plus every geometry
metric.  The stress suite makes nine in-memory certificate mutations and
requires rejection after resealing.
