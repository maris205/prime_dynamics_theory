# TPC-337 paper plan

## Research question

Does a finite control orbit remove the output interference exposed by TPC-336,
or does the interaction merely move into a centered covariance term?

## Frozen finite object

- Parent: TPC-336 producer and certificate, both hash-locked.
- Origins: `42001, 44001`; scales: `2048, 4096, 8192`.
- Operator: all-plus deleted-diagonal shell, `Q=54`, exponent `1`, `H=66`.
- Masks: `twin_prime`, `non_twin_prime_shift`, `prime_power_shift`, and
  `zero_support` from the parent source partition.
- Controls: identity, affine `(3,11)`, `(5,17)`, `(7,29)`, and reversal.

For each class `C` and control `j`, set
`y_(C,j)=C P_j beta_C`.  The central object is the four-by-four matrix

```text
K_CD = (1/5) sum_j <y_(C,j)-ybar_C, y_(D,j)-ybar_D>.
```

## Decision rule

If the centered fraction is small and the cross-class covariance signs are
unstable, move to a different control family.  If centered energy dominates,
record the coherent-average obstruction and grow the same orbit to test
whether it is a finite-control artifact.  No finite sign census is promoted
to an arithmetic estimate.

## Deliverable

An exact finite mean/centered covariance identity, a PSD covariance-Gram
certificate, a reverse-shell replay, mutation stress, and a paper with an
explicit claim firewall.
