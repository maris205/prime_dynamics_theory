# TPC-384 paper plan

## Research question

Does the finite origin-spread behavior observed under one block bandwidth
survive a predeclared bandwidth sweep, and does the answer depend on the
normalization convention?

## Design

Use a fresh affine coordinate panel with three response-blind origins, four
128-point blocks, four fixed block-distance cutoffs, four fixed sign laws, and
three shell anchors. Compute the raw matrices once per origin and Q, then apply
the same geometry with local-diagonal or pooled-scalar normalization. The
complete Cartesian panel is fixed before any metric is inspected.

## Claim-bearing outputs

1. Exact finite protocol and coordinate-disjointness proof.
2. 288-row producer certificate and 96-cell origin-spread phase diagram.
3. Independent reverse-shell replay with a distinct accumulation order.
4. A finite calibration comparison and a scoped all-plus high-Q bandwidth phase.
5. Exact q=8 rational anchor, mutation firewall, and local fail-closed Bridge-B.

## Anticipated boundary

The sweep can test finite stability and calibration sensitivity only. It cannot
choose an arithmetic law, prove monotonicity in `c`, establish a growing
operator norm, certify source-valid normalization, or advance Route A/B toward
the twin-prime endpoint.

## Next decision rule

If a fresh origin holdout preserves the phase, audit finite origin transfer at
the selected bandwidths. If it fails, record the failure as a bandwidth/origin
obstruction. Do not promote any finite profile to an asymptotic theorem.
