# TPC-339 paper plan

## Research question

After TPC-338 rejected a canonical covariance sign, can a sign-free support
bound control every masked response, and how much slack does it leave?

## Frozen design

- Parent: TPC-338 producer and certificate, both hash-locked.
- Six parent windows, all-plus `Q=54`, exponent `1`, `H=66`.
- Nine TPC-338 controls and four source masks.

For a finite matrix `A` and a vector supported on `S`, use the elementary
mask-aware envelope

```text
F(S)^2 = ||A[:,S]||_F^2 = sum_(t in S) sum_u |A(u,t)|^2,
||A x||^2 <= F(S)^2 ||x||^2.
```

The certificate audits the bound on all `6*9*4=216` records and reports the
occupancy `response_gain/F(S)^2`.

## Decision rule

If the envelope is violated, repair the matrix/source implementation before
proceeding.  If it is valid but broad masks have occupancy below `0.2`, treat
the factor-five tightness target as refuted in this panel and test a sharper
Schur/Gram or nuisance-orthogonal construction.  Prime-power singleton
records are retained rather than used to represent broad support.
