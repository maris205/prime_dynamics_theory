# Roadmap after RH-131

## Next: changing supports

Construct a canonical partial isometry between source and target supports.
Use principal vectors/polar decomposition, record the dimension mismatch,
and isolate the target component not reached by transport.

## Then: natural packet gauge

Derive the support map from the actual memory/packet update rather than an
after-the-fact exact-Gram optimizer.  Compare its angle loss with the optimal
principal-angle bound.

## Then: affine forcing

Represent newly born target-tail range as an explicit positive forcing
operator.  Normalize it into the RH-123 coefficient `q_n` and test whether
the finite packet enters a contractive affine regime.

## Boundary

Support restriction is rigorous, but it cannot be promoted to a full-space
inequality without exact kernel compatibility.  Rank-`r` pseudovolume is not
a rank-four Stage A certificate when `r<4`.
