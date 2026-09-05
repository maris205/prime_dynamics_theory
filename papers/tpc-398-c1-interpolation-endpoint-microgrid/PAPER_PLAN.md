# TPC-398 paper plan

## Research question

Does the finite endpoint transition reported by TPC-397 remain stable under a
finer, predeclared coefficient grid on a fresh coordinate-disjoint c=1 family,
and do origin stability and parent-relative transfer identify the same crossing?

## Locked design

Use the affine candidate family `a_j=6800001+401j`, `0 <= j < 41`, and select
indices `(0,8,16,24,32,40)`. The first three origins are calibration and the
last three are holdout. Keep `N=1024`, `Q=8192`, `fixed_c3`, beta two,
exponent one, height 66, and all four existing normalizations fixed before
readout.

Construct the exact finite matrices

```text
M_lambda = (1-lambda) M_all_plus + lambda M_alternating_index
lambda in {7/8, 15/16, 31/32, 1}
```

The parent interface is TPC-397's hash-locked `blend_3_4` and `blend_1`
all-origin means. For each current coefficient use the exact segment
coordinate `t=(lambda-3/4)/(1/4)` and compare cohort means with
`(1-t) parent(3/4)+t parent(1)`. Parent means and holdout roles are frozen
before current responses are read.

## Claim classes and decision rule

`PROVED_EXACT_FINITE` covers the parent hashes, grid arithmetic, interval
disjointness, role assignment, exact rational interpolation identities, and
the declared definitions. `NUMERICALLY_CERTIFIED_FINITE` covers the 96 finite
rows and aggregate counters after independent reverse-order replay.

Keep the one-percent origin-spread and three-percent parent/transfer caps
unchanged. Report each coefficient separately. No result can promote an
asymptotic threshold, a source-valid law, arithmetic `L2`, Route A/B, or a
twin-prime conclusion.

The observed result leads naturally to a second fresh-family replication of
the same microgrid. That continuation is a test of transferability, not a
threshold theorem.

## Required artifacts

README, derivation/proof packages, producer and independent checker, mutation
stress, canonical certificate, claim/route/protocol/theorem notes, Bridge-B
checker/note, and byte-identical compiled PDFs.
