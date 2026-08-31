# TPC-318 paper plan

## Research question

Does the true largest eigenvalue of the same literal deleted-diagonal
prime-shell Gram matrix exhibit the finite compression suggested by the
TPC-317 Schatten-4 envelope, and is the leading eigendirection isolated enough
to support an arithmetic interpretation?

## Claim-driven design

1. Freeze the TPC-317 literal matrix, source panels, shell anchors, and kernel
   exponents.
2. Compute the top two eigenvalues with a symmetric subset solver and replay
   the top eigenvalue with a full independent `eigvalsh` path.
3. Propagate a safe `|K|<=160` entry guard and solver spread into finite
   intervals; use Weyl's perturbation inequality only as the finite numerical
   error model.
4. Certify 24 rows and 16 adjacent-scale normalized top-eigenvalue decreases.
5. Record the second-eigenvalue gap and the unnormalized slope as hostile
   controls rather than silently treating normalized decay as arithmetic gain.

## Deliberate non-claims

No uniform `X -> infinity` estimate, prime cancellation, source-independent
normalization theorem, fixed-power credit, Route-B passage, or twin-prime
conclusion is asserted.  A numerical eigensolver output is not presented as an
exact algebraic eigenvalue theorem.

## Planned artifacts

The producer emits a canonical JSON certificate.  The independent checker
rebuilds the matrix with a reverse-order einsum accumulation and checks interval
containment.  The stress suite tests the PSD trace-power chain, Weyl control,
the literal-entry bound, and hostile claim mutations.  The manuscript records
the finite positive result and the near-degeneracy obstruction together.
