# TPC-365 proof and certificate package

## Exact finite statements

1. The candidate list, score, tie-break, and greedy separation rule are
   finite deterministic operations on unsigned weighted square geometry.
2. The weighted block is a rational scalar multiple of the literal masked
   block for each declared beta.
3. The weighted geometry diagonal is a finite sum of nonnegative squares and
   is positive on all 384 audited rows and on the exact anchor.
4. The normalized matrices are real symmetric finite matrices.  Schur's
   row-sum inequality and the Frobenius inequality provide the two recorded
   finite envelopes.
5. The `Q=4`, exponent-1, half-open interval `[413372,413385)` anchor with
   shell `{5,7}` is checked by exact rational arithmetic for beta=0 and beta=2.

## Numerical certificate

The forward producer evaluates 384 rows.  The independent checker rebuilds
the sieve, response-blind selection, masks, weights, matrices, geometry,
envelopes, and true spectra with reverse shell accumulation.  It compares
all row metrics, selection output, phase census, and exact anchors.

The finite result is:

- beta=0: 30 spectral-cap violations in 192 rows, maximum spectrum
  `1.6398827540264729`;
- beta=2: 0 spectral-cap violations in 192 rows, maximum spectrum
  `0.61633188509480319`;
- beta=2 maximum Schur value: `0.64544840644076373`;
- beta=2 minimum effective shell fraction:
  `0.66938300094026681`;
- holdout minus TPC-364 beta=2 maximum: `4.4345466941875245e-05`.

The adversarial certificate checker rejects 19 mutations of the protocol,
selection, row census, phase counts, and claim firewall while preserving the
baseline digest.  Normal and optimized executions are required to have
empty stderr and byte-identical stdout by the local Bridge-B checker.

These statements are finite numerical observations.  They do not provide a
growing-`Q` operator bound, source-uniform `L2` estimate, arithmetic
reassembly, fixed-power credit, or twin-prime conclusion.
