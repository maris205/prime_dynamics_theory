# TPC-364 proof package

## Exact finite statements

1. The displayed weighted block is a finite rational multiple of the literal
   masked block for every integer beta in the declared menu.
2. The weighted geometry diagonal is a finite sum of nonnegative squares and
   is positive on all 960 audited rows.
3. The resulting normalized matrices are real symmetric finite matrices.
4. Schur's row-sum inequality and the Frobenius inequality give the two
   finite envelopes recorded by the producer and independently reconstructed
   by the reverse-shell checker.
5. The `Q=4`, exponent-1, interval `[313060,313073]` anchor is evaluated with
   exact rational arithmetic for every beta; symmetry and positivity are
   checked by exact equality and sign tests.

## Numerical certificate

The forward producer evaluates 960 rows.  The independent checker rebuilds
the sieve, masks, weights, matrices, geometry, envelopes, and true spectra
with reverse prime accumulation and compares all recorded metrics.  The
stress checker rejects 18 mutations of the protocol, row census, phase
counts, and claim firewall.  Normal and optimized executions are required to
have empty stderr and byte-identical stdout by the local Bridge-B checker.

The finite phase result is:

- beta `-2,-1,0,1,2` have respectively `63,36,30,30,0` spectral-cap
  violations over 192 rows each;
- beta=2 has maximum normalized spectrum `0.61628753962786131` and maximum
  normalized Schur value `0.64531400360759594`;
- beta=2 has effective shell fraction at least `0.66938300094026681`.

These are finite numerical observations, not uniform or asymptotic claims.
