# TPC-371 proof and certificate package

## Exact statements

1. The three origins are inherited deterministic points of the fixed grid
   `1010001+401j` at indices `(0,20,40)`; response, source, and geometry
   scores are not consulted.
2. Each count-2048 interval is partitioned into the eight deterministic
   intervals `[a+256b,a+256b+255]`.
3. For every declared block and beta, the weighted geometry is a finite sum
   of nonnegative rational squares.  The exact inherited anchor
   `[1010346,1010359)` is positive and symmetric for both betas.
4. Every recorded block matrix is finite and symmetric, so the Schur and
   Frobenius quantities are valid finite upper envelopes for its spectral
   norm.

These statements are exact finite facts; they do not identify the block-local
object with the full-window-normalized object.

## Numerical certification

The producer evaluates all 576 Cartesian-product rows.  The independent
checker rebuilds primes with its own sieve, accumulates shell terms in reverse
order, recomputes exact-anchor digests, and compares every shell, weight,
geometry, raw metric, normalized metric, eigenvalue endpoint, row index, and
phase count.  The certificate also records the parent TPC-370 full-window
failure keys as provenance, rather than treating them as block-local results.

The certified census is:

* beta `2`: `288/288` block-local rows below the spectral cap `0.64` and the
  Schur cap `0.83`; maximum spectral value `0.5536333251967529`;
* beta `0`: `72` spectral and `72` Schur violations among `288` control rows;
* all 24 declared origin/block locations are represented, and beta=2 has no
  block-local failure key.

The adversarial suite rejects 36 mutations spanning the header, origin
protocol, block partition, row census, digest, phase counts, exact-anchor
inheritance, firewall, and routing clue.  The local Bridge-B additionally
requires normal and optimized subprocesses to have empty stderr and
byte-identical stdout.

## Interpretation boundary

The finite result refutes only the scoped hypothesis that the TPC-370
full-window beta=2 failure is already visible in a single independently
normalized 256-point block.  It does not prove that cross-block coherence is
the causal mechanism, because changing the domain also changes the geometry
normalization.  Cross-block decomposition is the next declared experiment.

No arithmetic `L2`, fixed-power credit, source-uniform theorem, asymptotic
statement, prime-shell reassembly, official Route-A/Route-B pass, or
twin-prime conclusion is claimed.
