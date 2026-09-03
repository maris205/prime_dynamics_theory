# TPC-368 proof and certificate package

## Exact finite statements

1. The origins `(810001,817061,824121)` are the deterministic output of the
   declared grid indices `(0,20,40)`, with no response or geometry selection.
2. Every weighted block is a rational scalar multiple of the literal masked
   block for beta `0` or `2`.
3. The weighted geometry is a finite sum of nonnegative rational squares.
4. The exact anchor and every replay row have positive geometry; the matrices
   are finite, real, and symmetric.
5. The Schur and Frobenius inequalities give the recorded finite envelopes.

The exact anchor is checked by rational arithmetic on `[810342,810355)` with
shell `{5,7}` for both betas.  Canonical matrix and geometry digests are
stored in the certificate.

## Numerical certificate

The producer evaluates 144 law rows.  The independent checker rebuilds the
prime sieve and every component in reverse shell order, then compares shell,
weights, geometry extrema, raw and normalized metrics, eigenvalue endpoints,
row indices, phase counts, and the exact anchor.  The finite census is:

- beta=0: 18 spectral-cap and 18 Schur-cap violations in 72 rows;
- beta=2: 6 spectral-cap and 0 Schur-cap violations in 72 rows;
- beta=2 maximum normalized spectrum:
  `0.674101905927736`;
- beta=2 maximum normalized Schur value:
  `0.70009251108512549`.

The six beta=2 failures are exactly the three declared origins at count
1024, `Q=2048` and `8192`, exponent one, all-plus law.  The parent TPC-367
maximum is `0.67410738070824539`; the finite replicated maximum is lower by
`5.474780509384658e-06`.  This comparison is descriptive and carries no
asymptotic inference.

The adversarial checker rejects 29 mutations of protocol, origin flags, row
census, phase/audit data, firewall values, and the round clue.  The local
Bridge-B checker additionally requires normal/optimized subprocesses to have
empty stderr and byte-identical stdout.  The official Session evaluator files
are absent, so no official Route-A/Route-B pass is asserted.

## Non-claims

The package proves no growing operator bound, source-valid normalization,
source-uniform arithmetic `L2`, prime-shell reassembly, fixed-power saving,
Route-A/Route-B gate closure, or twin-prime statement.  Arithmetic advance is
`NO` and fixed-power credit is `0`.
