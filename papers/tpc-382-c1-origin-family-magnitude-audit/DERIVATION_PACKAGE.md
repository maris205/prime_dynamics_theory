# TPC-382 derivation package

## Finite observable

For a locked parent panel `P`, law `ell`, and anchor `Q`, let

`s(P,ell,Q,o) = spectral(A_band(P,ell,Q,o))`.

For a set of locked origins `O`, define

`m(O) = |O|^{-1} sum_o s(P,ell,Q,o)`,
`Delta(O) = (max_o s - min_o s)/m(O)`.

The one-percent rule is the predeclared predicate `Delta(O) <= 0.01`.
For the matched-count cohort, `O` is the six origins from TPC-380 and TPC-381;
for the scale control, `O` is the three TPC-379 origins.  The matched-count
contrast is `(m_2048-m_1024)/m_1024`.

## What is exact

Once the parent rows and hashes are fixed, these are finite arithmetic
transformations of recorded real-valued diagnostics.  The producer writes all
values with 17 significant digits and a canonical JSON encoding.  The
independent checker recomputes minima, maxima, means, spreads, and contrasts
from the parent rows without importing the producer.

## What is not derived

No limit in the origin, count, Q, or shell is taken.  The normalized matrices
remain a modelling choice, and the parent certificates do not constitute a
source-valid prime law.  Therefore this package cannot pay arithmetic power
credit or close Route A, Route B, or the twin-prime endpoint.
