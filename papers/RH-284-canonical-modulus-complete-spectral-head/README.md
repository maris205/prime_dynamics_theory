# RH-284: Canonical modulus-complete spectral head

For an `S2` operator with algebraic eigenvalue sequence `(mu_j)`, define

```text
H_q = {mu_j : |mu_j| > q}
```

with multiplicity.  The head is finite, contains complete conjugate pairs for
a real operator, and satisfies

```text
#H_q <= sum |mu_j|^2 / q^2.
```

It is also the unique smallest spectral submultiset whose complement has
spectral radius at most `q`: every admissible head must contain all roots with
modulus strictly larger than `q`.  Roots exactly on the threshold remain in
the tail under the declared strict convention, removing tie ambiguity.

The corresponding finite genus-one product and complementary canonical
product give an exact `det_2` factorization.  No eigenvectors or Riesz
projectors enter.

This theorem makes the RH-282 head legal and canonical relative to the chosen
threshold.  The numerical value of `q` is a design choice, and canonicality
does not identify this head with the monodromy counterloop.
