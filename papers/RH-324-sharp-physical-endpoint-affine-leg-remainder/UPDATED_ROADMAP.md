# Roadmap after RH-324

RH-324 proves an actual finite-noise theorem for the endpoint-to-repelling
first leg.  The exact folded row, state boundary, and row normalizer differ
from the exact curved Gaussian by exponentially small tails.  Removing the
quadratic displacement costs a sharp positive multiple of `sigma` in the
joint `L1` norm.

The phase-matched local scale is compatible with the first-alias target:
`sigma = o(R^(-2k))` on the natural clock.  This does not authorize direct
iteration, because the number of channels grows and the relevant lifted
operator norms and phase bookkeeping have not been combined.

RH-325 should formulate and prove a moving-order Duhamel composition
criterion.  It must distinguish:

1. retained-coordinate joint `L1` errors from marginalized errors;
2. phase-matched local kernels from phase transport between cycle points;
3. sums of Markov contractions from weighted trace contributions;
4. ordinary affine legs from the unresolved second physical critical leg;
5. a conditional composition criterion from an actual full-cycle theorem.

Parity, neighboring-shell cancellation, and their joint matching equation
remain assigned to RH-326--RH-328.  Gates A--E remain false/open.
