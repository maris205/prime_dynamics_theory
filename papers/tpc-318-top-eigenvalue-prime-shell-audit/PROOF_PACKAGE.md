# TPC-318 proof and certificate package

## Proposition 1: finite PSD spectrum

For every declared row, `G=A^*A` is positive semidefinite and has real
nonnegative eigenvalues.  This is exact finite linear algebra.

## Proposition 2: top-eigenvalue perturbation bound

For two real symmetric finite matrices `G` and `Ghat`,

```text
|lambda_max(G)-lambda_max(Ghat)| <= ||G-Ghat||_2.
```

This is Weyl's inequality.  In the certificate it is used as a declared finite
error-propagation rule after bounding the matrix perturbation by an entrywise
guard.  The numerical reconstruction and its coverage remain a modeling
choice, so the resulting large-panel label is `NUMERICALLY_CERTIFIED_FINITE`.

## Proposition 3: finite top-eigenvalue readout

The producer computes the largest and second-largest eigenvalues of each
forward and reverse shell Gram matrix with a symmetric subset eigensolver.  A
full `eigvalsh` computation supplies a second scalar readout.  The interval
contains all four top estimates, the residual, the dual-path spread, and the
declared matrix guard.  The independent checker recomputes a reverse-order
Gram with einsum accumulation and verifies containment.

## Proposition 4: finite trend statement

The certificate contains 24 rows and 16 adjacent-scale comparisons.  Every
upper-scale normalized top-eigenvalue interval lies strictly below its paired
lower-scale interval.  This is a finite numerical statement, not an
asymptotic theorem.

## Claim ceiling

```text
PROVED_EXACT_FINITE = PSD spectrum facts and Weyl inequality
NUMERICALLY_CERTIFIED_FINITE = 24 top-eigenvalue rows; 16 strict decreases;
                               dual solver and residual audits; gap census
NUMERICAL_OBSERVATION = normalized top-eigenvalue finite compression
OPEN = unnormalized/growing power law; clustered top eigenspace theorem;
       arithmetic cancellation; normalization; fixed-power credit; Gate B;
       twin-prime endpoint
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```
