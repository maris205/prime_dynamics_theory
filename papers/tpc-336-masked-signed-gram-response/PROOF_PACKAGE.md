# TPC-336 proof and scope package

## Proposition 1 — finite output-Gram expansion

For any finite matrix `C` and vectors `beta_C` with
`beta=sum_C beta_C`,

```text
||C beta||^2 = sum_C ||C beta_C||^2
               + 2 sum_{C<D}<C beta_C,C beta_D>.
```

**Proof.**  Expand the squared Euclidean norm of the finite sum and pair the
two symmetric cross terms. `QED`.

## Proposition 2 — finite response certificate

For the fixed all-plus operator and six declared windows, the output-Gram
expansion is replayed, the gain ordering is identical in all six rows, and
the self-energy sum exceeds the full response energy in all six rows.

**Evidence.**  The producer and an independent reverse-shell implementation
recompute the matrices and masks.  A stress suite rejects five mutations.
The response identity is a finite numerical certificate; its small residual
is explicitly bounded rather than promoted to an exact floating-point claim.

## Scope boundary

The result refutes only the scoped idea that the TPC-335 source-share ordering
can be transferred unchanged through this fixed operator.  It supplies no
uniform operator estimate, arithmetic cancellation theorem, or twin-prime
conclusion.
