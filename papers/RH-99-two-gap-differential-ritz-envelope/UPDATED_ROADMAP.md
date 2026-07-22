# Updated roadmap after RH-99

## Differential result

One invariant projected-cross Ritz update has a clean two-gap derivative
bound. The selected cross-covariance gap controls direction motion; the output
Ritz gap controls the final packet projector.

Adaptive weak-mode quotienting improves the formal derivative constant by up
to roughly ten billion at the five ill-conditioned updates.

## Why the gate is still open

The infinitesimal theorem does not close a finite tube:

- five fine-scale output Ritz gaps are not certifiably positive;
- available constants are astronomically conservative;
- actual quotient displacements lie outside every first-order separation
  radius used in the audit.

The route must therefore choose between:

1. higher-precision/interval spectral gap certification plus nonlinear
   continuation of the projector branch;
2. a nonsmooth gap-aware adaptive rule that avoids near-colliding Ritz
   clusters; or
3. retaining exact hybrid replay as a finite certificate and moving to a
   stopped-clock formulation rather than a uniform differential tube.

## RH-100 review task

The hundred-layer review should compare these alternatives against the full
Stage-A-to-spectral-determinant roadmap, consolidate proved theorems and
negative barriers, and select the next three papers. No Hilbert--Polya
operator, zero identification, or RH proof is asserted.
