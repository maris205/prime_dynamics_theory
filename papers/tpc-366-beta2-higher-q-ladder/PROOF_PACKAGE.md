# TPC-366 proof and certificate package

## Exact finite statements

1. The candidate list, geometry score, tie-break, and greedy separation rule
   are finite deterministic operations on unsigned weighted geometry.
2. Each weighted block is a rational scalar multiple of the literal masked
   block for the declared integer betas.
3. The geometry diagonal is a finite sum of nonnegative rational squares and
   is positive on all 480 audited rows and on the exact anchor.
4. The normalized matrices are real symmetric finite matrices; Schur and
   Frobenius give the recorded finite envelopes.
5. The `Q=4`, exponent-1, half-open interval `[623372,623385)` anchor with
   shell `{5,7}` is checked by exact rational arithmetic for beta=0 and beta=2.

## Numerical certificate

The producer evaluates 480 rows.  The independent checker rebuilds the
sieve, selection rule, masks, weights, matrices, geometry, envelopes, and
true spectra with reverse shell accumulation and compares every row metric.

The finite result is:

- beta=0: 60 spectral-cap and 60 Schur-cap violations in 240 rows; maximum
  normalized spectrum `1.6419614115857373` and Schur value
  `1.718218622972471`;
- beta=2: zero spectral-cap and zero Schur-cap violations in 240 rows;
  maximum normalized spectrum `0.62448287758976528` and Schur value
  `0.65368278287004711`;
- beta=2 minimum effective shell fraction:
  `0.66944805377549699`;
- beta=2 maximum spectrum minus the TPC-365 value:
  `0.0081509924949620949`.

The adversarial certificate checker rejects 23 mutations of the protocol,
selection, row census, phase counts, and claim firewall while preserving the
baseline digest.  Normal and optimized executions are required to have
empty stderr and byte-identical stdout by local Bridge-B.

These are finite numerical observations.  They do not prove a growing-Q
operator bound, source-uniform arithmetic `L2`, source validity, fixed-power
saving, official evaluator pass, or a twin-prime conclusion.
