# TPC-54: Sharp energy selection

This directory contains the source and final PDF for:

> *Sharp Energy Selection Before Residual Grouping: Capacity Saturation,
> Cofactor Occupancy, and the Exact Coverage Threshold*

## Core result

The paper turns the carrier-energy coverage subgate left by TPC-53 into a
sharp finite-atom theorem. If a compatible source cell has structural mass
`delta`, bounded coefficients fill a normalized fraction `kappa` of the
total available capacity, and `sigma` is the actual-coefficient-weighted
carrier-energy fraction on the cell, then

```text
sigma >= (1 - (1-delta)/kappa)_+.
```

The inequality and its zero threshold are sharp. An exact odds identity and
a sharp transport law separately track row density, fixed source shapes,
the sampled carrier, coefficient magnitude, and cofactor occupancy. In odds
coordinates these factors multiply, so their worst-case polynomial costs
add exactly.

The paper also proves that phase information cannot repair a pre-terminal
magnitude deficit, and that positive atomic coverage need not survive a
two-atom collision in one full post-prime output fiber. The residual value
`s=d(m)r` is only one coordinate of that fiber. Thus selection must be
completed before grouping unless a new coherence estimate is supplied.

## Claim boundary

This is an L0/L1 carrier-coverage theorem on a declared fixed-`h0` sampled
slice. It does not prove the missing coefficient floor or capacity
saturation for the full inherited packet, cofactor balance, grouping
stability, a parity breakthrough, or a twin-prime result.

## Build

Run `pdflatex`, `bibtex`, and two further `pdflatex` passes in this directory.
