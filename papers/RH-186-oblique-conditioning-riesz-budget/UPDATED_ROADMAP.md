# Roadmap after RH-186

The maximum-residual oblique gate fails. Two possible repairs remain:

1. regularize the small cross-Gram singular values while paying an explicit
   duality defect;
2. avoid the maximum norm and use the invariant product of the two directed
   couplings.

RH-187 should settle the first option exactly. If it fails, RH-188 should
audit the product-form Schur branch.
