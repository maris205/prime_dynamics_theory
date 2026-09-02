# TPC-336 derivation package

Let `beta=sum_C beta_C` be the disjoint TPC-335 mask decomposition and let
`y_C=C beta_C`.  Finite bilinearity gives

```text
||C beta||^2 = ||sum_C y_C||^2
             = sum_C ||y_C||^2 + 2 sum_{C<D}<y_C,y_D>.
```

For each mask define the response gain
`G_C=||C beta_C||^2/||beta_C||^2` when the denominator is nonzero.  The
certificate also records the coordinate diagonal and `O=E-D` for every self
response.  The pairwise Gram entries are retained because component energies
alone cannot determine the full response.

The fixed operator is the all-plus deleted-diagonal prime-shell matrix at
`Q=54`, exponent `1`, height `66`.  All conclusions are finite and tied to
the declared source cutoff.
