# TPC-367 proof and certificate package

## Exact finite statements

1. The origin list `(620001,626141,632281)` is the deterministic output of the
   declared grid indices `(0,20,40)`, with no response or geometry selection.
2. Each weighted block is a rational scalar multiple of the literal masked
   block for beta `0` or `2`.
3. The weighted geometry is a finite sum of nonnegative rational squares.
4. On the exact anchor and every replay row, the computed geometry is
   positive; the resulting matrices are finite, real, and symmetric.
5. The Schur and Frobenius inequalities give the recorded finite envelopes.

The exact anchor is checked by rational arithmetic on `[620362,620375)` with
shell `{5,7}`, exponent one, for both betas.  Its matrix and geometry digests
are stored in the canonical certificate.

## Numerical certificate

The producer evaluates 288 law rows.  The independent checker rebuilds the
prime sieve and every component in reverse shell order, compares shell,
weights, geometry extrema, raw/normalized metrics, eigenvalue endpoints, and
row indices, and independently recomputes the exact anchor.  The finite
census is:

- beta=0: 36 spectral-cap and 36 Schur-cap violations in 144 rows;
- beta=2: 6 spectral-cap and 0 Schur-cap violations in 144 rows;
- beta=2 maximum normalized spectrum:
  `0.67410738070824539`;
- beta=2 maximum normalized Schur value:
  `0.70009945776422788`.

The six beta=2 spectral violations are exactly the count-1024,
`Q in {2048,8192}`, all-plus rows across the three origins.  This is the
scoped obstruction recorded as `REFUTED_SCOPED`.

The adversarial checker rejects 28 mutations of protocol, origin flags, row
census, phase counts, audit fields, and claim-firewall values.  Local
Bridge-B additionally requires normal/optimized subprocesses to have empty
stderr and byte-identical stdout.  The official Session evaluator files are
not present, so no official Route-A/Route-B pass is asserted.

## Non-claims

The package does not prove a growing operator bound, source-valid
normalization, source-uniform arithmetic `L2`, shell reassembly, a fixed
power saving, or any twin-prime statement.  It assigns zero fixed-power
credit and leaves the full Route-B gate open.
