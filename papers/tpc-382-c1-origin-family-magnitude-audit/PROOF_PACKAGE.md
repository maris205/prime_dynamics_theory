# TPC-382 proof package

## Proposition (finite locked aggregation)

Given the three parent certificate byte strings named by the embedded SHA-256
locks, the TPC-382 producer and independent checker compute the same 12
same-count cells, 12 scale-control cells, and 12 matched-count contrasts.
Each cell statistic is the stated finite minimum/maximum/mean transform of its
listed values.

## Verification status

The proposition is checked by canonical JSON, parent source/certificate hashes,
complete row-key censuses, recomputed arithmetic, and normal/optimized
replay.  The adversarial checker mutates 25 semantic fields and requires every
mutation to be rejected.

## Boundary

This is a finite certificate-level proposition.  It is not a proof of origin
uniformity, scale uniformity, a source-valid normalization, an arithmetic
estimate, a growing operator bound, or any twin-prime assertion.
