# TPC-373 paper plan

## Question

TPC-372 showed that the beta=2 full-window excess is not reproduced by the
fixed block-diagonal component or by the off-block component in isolation.
The next smallest common-normalization question is whether the extremal
eigenmode itself has a reproducible block-distance profile.  This paper
audits that profile on the complete inherited 18-row panel.

## Frozen protocol

The origins, count-2048 window, eight contiguous 256-point blocks, shell
anchors `Q={512,2048,8192}`, exponent one, all-plus law, and beta values
`{0,2}` are inherited unchanged from TPC-372.  All 18 rows are materialized
before any eigenmode or layer contribution is inspected.

For each full-window normalized symmetric matrix `T`, compute its full
eigendecomposition.  Select the eigenvector for the largest absolute
eigenvalue; an exact absolute-value tie is resolved in favor of the minimum
eigenvalue.  For `d=0,...,7`, retain entries whose two block indices have
absolute difference `d`, and record the selected vector's Rayleigh term on
that layer.  The masks and the selection rule are fixed independently of
the observed profile.

## Decision rule

If one or more block distances carry a stable finite concentration across
the declared rows, record it as scoped profile evidence and test the most
natural layerwise extension next.  If the profile is diffuse or changes
with origin/`Q`, record that as an obstruction to a low-dimensional
cross-block reduction.  Either outcome remains finite; no decay law or
causal attribution is promoted without a uniform theorem.

## Claim boundary

The intended contribution is a response-blind, common-normalization,
finite eigenmode decomposition with numerical replay.  It cannot establish
cross-block causality, origin/window uniformity, a growing-operator bound,
arithmetic `L2`, fixed-power credit, Route-A/Route-B closure, or a twin-prime
theorem.  Official evaluator files named by the Session are absent; the
local Bridge-B remains fail-closed repository evidence only.
