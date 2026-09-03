# TPC-370 proof and certificate package

## Exact finite statements

1. The origins `(1010001,1018021,1026041)` are the deterministic output of
   grid indices `(0,20,40)` in `1010001+401j`; no signed response or geometry
   ranking is consulted.
2. Each weighted block is a rational scalar multiple of the literal masked
   block for beta `0` or `2`.
3. The weighted geometry is a finite sum of nonnegative rational squares.
4. The inherited exact anchor `[1010346,1010359)` has positive exact geometry
   and symmetric exact matrices for both betas.
5. The Schur and Frobenius inequalities give the recorded finite envelopes.

The exact anchor's canonical matrix and geometry digests are stored in the
certificate. Its provenance is locked to the TPC-369 certificate and code.

## Numerical certificate

The producer evaluates 72 law rows. The independent checker rebuilds the
prime sieve and all components in reverse shell order, then compares shells,
weights, geometry extrema, raw and normalized metrics, eigenvalue endpoints,
row indices, phase counts, failure keys, the parent-signature comparison, and
the inherited exact-anchor fields. The finite census is:

- beta=0: 9 spectral-cap and 9 Schur-cap violations in 36 rows;
- beta=2: 6 spectral-cap and 0 Schur-cap violations in 36 rows;
- beta=2 maximum normalized spectrum:
  `0.71099989528234753`;
- beta=2 maximum normalized Schur value:
  `0.72908109638522522`.

The six beta=2 failure keys are the all-plus rows at each origin and
`Q=2048,8192`. Their origin/Q/law signature agrees with TPC-369 after the
count coordinate is removed. The maximum is larger than the TPC-369 value by
`0.036894997276250452`; this is a finite comparison, not a convergence claim.

The adversarial checker rejects 32 mutations, including count, row, parent
signature, inherited-anchor, firewall, and clue mutations. The local
Bridge-B checker additionally requires normal/optimized subprocesses to have
empty stderr and byte-identical stdout. Official Route-A/Route-B evaluator
files are absent, so no official pass is asserted.

## Non-claims

No growing operator bound, source-valid normalization, source-uniform
arithmetic `L2`, prime-shell reassembly, fixed-power saving, Route-A/Route-B
gate closure, asymptotic repair, or twin-prime statement is proved.
Arithmetic advance is `NO` and fixed-power credit is `0`.
