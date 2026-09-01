# TPC-326 paper plan

## Question

Is the TPC-325 finite scale-ladder readout tied to the residue environment at
origin `12001`, or does it replicate at a second source origin?

## Design

Freeze the TPC-325 ladder and repeat it at origin `16001`, disjoint from every
earlier source panel.  Keep shell anchors, height, exponents, kernel, and sign
menu identical.  Compare full row labels, energy census, and all-plus envelope
values to the parent certificate.

## Release-bearing results

1. New 32-row all-plus profile-majorization certificate.
2. Exact parent-census match for all four sign-law classes and energy sides.
3. Finite cross-origin envelope agreement under thresholds TV `<0.001` and
   energy upper envelope `<0.005`.
4. Independent reverse/einsum replay, residue perturbation stress, and exact
   rational anchor at the new origin.

## Failure policy

Any census mismatch, threshold failure, source overlap, unresolved row, or
normal/optimized disagreement converts the proposed replication into an
obstruction and prevents a positive release marker.
