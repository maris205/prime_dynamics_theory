# TPC-296 paper plan

## Question

TPC-295 proved that every ambient weighted sign target has an unrestricted
finite source preimage.  Is the least-norm preimage affordable, and does the
frozen native source direction approximate the desired targets?

## Claim spine

1. Prove that `h_b=A G^(-1)b` is the unique least-norm preimage and that a
   source budget `B` is feasible exactly when `b^T G^(-1)b<=B`.
2. Prove the exact source-cost/physical-energy tradeoff
   `(b^T G^(-1)b)(b^T G b)>=(b^T b)^2`.
3. Define the one-ray proxy `span{frozen_beta}` and derive its exact
   least-squares residual formula.
4. Measure all three inherited target families at 70 digits on the 18 rows,
   including conditioning and residual checks.
5. Separate the finite observation “unrestricted cost is cheap” from the
   obstruction “the frozen source ray is geometrically wrong.”
6. Preserve arithmetic `L2`, growing-shell control, Gate B, and the
   twin-prime endpoint as open.

## Claim ceiling

The linear algebra is exact.  The 18-row cost/profile atlas is high-precision
finite numerical evidence.  The `1e-3` budget and one-ray profile are
declared diagnostics, not asymptotic or arithmetic assumptions.
