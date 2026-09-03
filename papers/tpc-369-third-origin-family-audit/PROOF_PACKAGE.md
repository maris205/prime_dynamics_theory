# TPC-369 proof and certificate package

## Exact finite statements

1. The origins `(1010001,1018021,1026041)` are the deterministic output of
   grid indices `(0,20,40)` in `1010001+401j`, with no signed response or
   geometry ranking.
2. Each weighted block is a rational scalar multiple of the literal masked
   block for beta `0` or `2`.
3. The weighted geometry is a finite sum of nonnegative rational squares.
4. The initially proposed exact anchor has a zero geometry row for both
   betas; the first-valid scan rule selects `[1010346,1010359)`, where exact
   geometry is positive and the matrices are symmetric.
5. The Schur and Frobenius inequalities give the recorded finite envelopes.

The exact anchor uses shell `{5,7}` at `Q=4` and exponent one.  Its canonical
matrix and geometry digests are stored in the certificate, along with the
initial-anchor obstruction and offset four repair.

## Numerical certificate

The producer evaluates 144 law rows.  The independent checker rebuilds the
prime sieve and all components in reverse shell order, then compares shells,
weights, geometry extrema, raw and normalized metrics, eigenvalue endpoints,
row indices, phase counts, the parent-pattern comparison, and the exact
anchor repair fields.  The finite census is:

- beta=0: 18 spectral-cap and 18 Schur-cap violations in 72 rows;
- beta=2: 6 spectral-cap and 0 Schur-cap violations in 72 rows;
- beta=2 maximum normalized spectrum:
  `0.67410489800609708`;
- beta=2 maximum normalized Schur value:
  `0.7000873870755715`.

The six beta=2 keys agree with the parent six-key template.  The maximum is
`2.9920783610748458e-06` above the TPC-368 maximum
`0.674101905927736`; this is a finite comparison only.

The adversarial checker rejects 30 mutations, including an anchor-repair
mutation.  The local Bridge-B checker additionally requires normal/optimized
subprocesses to have empty stderr and byte-identical stdout.  Official
Route-A/Route-B evaluator files are absent, so no official pass is asserted.

## Non-claims

No growing operator bound, source-valid normalization, source-uniform
arithmetic `L2`, prime-shell reassembly, fixed-power saving, Route-A/Route-B
gate closure, or twin-prime statement is proved.  Arithmetic advance is `NO`
and fixed-power credit is `0`.
