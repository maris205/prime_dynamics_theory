# TPC-319 paper plan

## Title

**Ky Fan cluster masses and the normalization firewall for a literal prime-shell operator**

## Parent and question

TPC-318 directly read the largest eigenvalue of the frozen deleted-diagonal
centered prime-shell Gram, but found small top/second gaps and left the source-count
normalization unpaid.  TPC-319 asks two sharply delimited questions:

1. Does the finite signal live in a small spectral cluster rather than one isolated
   eigenvector?
2. Is the apparent normalized decrease merely the factor-of-two source normalization,
   with the unnormalized cluster mass actually increasing?

The operator, shell rule, source intervals, and kernel exponents are inherited without
change.  No new dynamical-system family is introduced.

## Planned contribution

For (G=A^*A), define the Ky Fan mass

\[
  F_k(G)=\sum_{j=1}^k\lambda_j(G), \qquad
  M_k(G)=F_k(G)/N.
\]

The paper will combine the exact finite Ky Fan variational inequality with a dual
finite audit for (k\in\{1,2,4,8,16\}).  It will report both (F_k) and (M_k),
edge gaps, effective cluster rank, and a finite normalization-flip test.

## Claim discipline

- `PROVED_EXACT`: finite PSD/Ky Fan identities and the algebraic normalization lemma.
- `NUMERICALLY_CERTIFIED_FINITE`: dual shell-order and dual-solver rows, interval
  containment, and strict finite comparisons under the declared binary64 guard.
- `NUMERICAL_OBSERVATION`: cluster-rank ranges and finite trend slopes.
- `OPEN`: any uniform growing law, canonical eigenspace, arithmetic cancellation,
  fixed-power credit, and twin-prime endpoint.

## Planned follow-up

If the normalization flip is universal on this panel, TPC-320 should attack the
source-normalized spectral measure or a scale-invariant quantity; it must not treat
the normalized trend as a power saving.
