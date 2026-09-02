# TPC-338 paper plan

## Research question

Does the TPC-337 covariance dominance survive when the same affine control
orbit is enlarged, and are its signed class interactions canonical?

## Frozen design

- Parent: TPC-337 producer and certificate, both hash-locked.
- Source/operator: exactly the six TPC-337 windows and its all-plus
  `Q=54`, exponent-1, `H=66` matrix.
- Five-control ensemble: TPC-337's identity, three affine controls, and
  reversal.
- Nine-control ensemble: the five controls plus affine `(9,1)`, `(11,13)`,
  `(13,17)`, and `(17,19)`.

For both nested ensembles record the class covariance Gram matrix and its
eigenvalues normalized by trace.  Compare the two ledgers row by row.

## Decision rule

If centered dominance disappears, treat TPC-337 as a small-ensemble artifact.
If dominance persists but a selected covariance sign changes, reject a
canonical signed-covariance heuristic and move to a sign-free operator bound.
If both persist, test a fresh source location before promoting stability.

## Deliverable

An exact nested mean/centered identity, a finite spectral comparison, an
independent reverse-shell replay, and a paper separating stable energy facts
from control-family-dependent signs.
