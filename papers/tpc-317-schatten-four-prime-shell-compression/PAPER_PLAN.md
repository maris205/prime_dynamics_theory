# TPC-317 paper plan

## Research question

Can the loose finite Frobenius envelope from TPC-316 be replaced by the next
trace-power (Schatten-4) envelope for the same literal deleted-diagonal
prime-shell operator, and does that replacement behave differently across
growing finite source panels?

## Claims to establish

1. Keep the TPC-316 matrix and its prime-shell, mask, and deleted-diagonal
   conventions unchanged.
2. Prove the finite positive-semidefinite Gram chain
   `lambda_max(G) <= sqrt(trace(G^2)) <= trace(G)`.
3. Derive the normalized Schatten-4 `L2` envelope for every finite source
   vector.
4. Anchor the trace and trace-square calculations with an exact rational
   one-prime panel.
5. Rebuild the large panels `X=640,1280,2560` in forward and reverse shell
   order, with a conservative binary64 error budget and extended-precision
   scalar reduction.
6. Certify 16 strict Schatten-4 decreases against 16 strict Frobenius
   increases, and record the result as finite compression rather than an
   asymptotic saving.

## Deliberate non-claims

No true operator-norm asymptotic, arithmetic cancellation theorem, canonical
normalization, fixed-power credit, Route-B passage, or twin-prime conclusion
is asserted.  The large-panel numbers are numerical certificates under the
declared finite error model; only the small trace-power anchor is exact
rational arithmetic.

## Planned artifacts

The producer emits a canonical JSON certificate.  The independent checker
rebuilds the matrix without importing the producer, verifies the exact small
panel and all large-panel intervals, and checks the two opposite finite
trends.  The stress suite attacks the trace-power inequality, deletion gate,
accumulation order, and claim firewall.
