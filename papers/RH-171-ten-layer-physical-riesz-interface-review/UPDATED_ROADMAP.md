# Roadmap after RH-171

## Current coordinate inside Gate A

```text
S reset seed (conditional)
  -> R = X_phys AND D_phys AND K_phys AND H_phys   [current wall]
  -> Q cloud coefficient/pole ledger              [open]
  -> U Schatten complement limit                   [open]
  -> Z canonicity/normalization                     [open]
  -> T directed marked-trace limit                  [open]
  -> macro Gate A
```

## Recommended next target

Construct or reject `X_phys` before spending heavily on contour numerics:

1. specify the source-memory space and transfer/determinant space at each
   physical scale;
2. define a target-independent normalized map `J_j`;
3. bound its Gram/polar correction and commutator;
4. derive primal and adjoint transfer defects on each proposed shell;
5. test compatibility under scale embeddings.

If no canonical `J_j` survives, the reset-packet branch into the RH-80 cloud
is rejected, while other Riesz-cloud constructions remain possible.  If it
does survive, RH-167--168 provide the exact finite contour-validation
pipeline and `D_phys` becomes the next wall.

Gates B--E remain untouched at the macro level.
