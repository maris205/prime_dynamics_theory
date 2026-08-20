# TPC-214 Paper Plan

## Title

Mobius-Weighted Shared-Frequency Clusters in the Physical Cross-Divisor Gram

## Research question

After TPC-213 identifies common rational-frequency intersections, does the
literal V46 emitter retain independent divisor energies, or do nested divisors
collapse to a smaller reduced-denominator object once the actual
`mu(d) log(d) / d` coefficients and smooth emitter are restored?

## Main claim

For a common reciprocal prime set, common height `H`, and a smooth emitter
profile, the unweighted emitter is dilation-covariant:

```text
B_(k d)(k r) = B_d(r).
```

Consequently, the complete-period physical Gram is exactly diagonal in reduced
frequency denominator clusters.  The coefficient of a denominator `h` is the
Mobius-log tail

```text
C_h = sum_(d in D, h|d) mu(d) log(d) / d.
```

This is an exact structural reduction, not an asymptotic saving theorem.

## Evidence package

1. A finite proof package for dilation covariance and cluster factorization.
2. Exact rational emitter rows for the Schwartz profile
   `psi(t) = (1+t^2)^(-2)`.
3. A nested cancellation fixture `D={5,7,35}`.
4. An adversarial enhancement fixture `D={3,5,7,105}` showing that cluster
   coupling has no universal favorable sign.
5. A four-packet polarization sanity check preserving the coefficients
   `(1, i, -1, -i)/4`.

## Claim ceiling

```text
PROVED_EXACT = DILATION_COVARIANCE_AND_REDUCED_DENOMINATOR_CLUSTER_FACTOR
PROVED_EXACT_FINITE_SIGN = CANCELLATION_AND_ENHANCEMENT_DIRECTIONS
NUMERICAL_OBSERVATION = TWO_FINITE_WEIGHTED_GRAM_RATIOS
REFUTED_SCOPED = UNIVERSAL_CLUSTER_SAVING_SIGN
OPEN = ACTUAL_V46_ASYMPTOTIC_CLUSTER_BOUND_AND_PRIME_SHELL_REASSEMBLY
ARITHMETIC_ADVANCE = NO
```

## Planned sections

1. V46 object and notation.
2. Dilation covariance of the reciprocal emitter.
3. Reduced-denominator cluster theorem.
4. Four-packet linearity and zero-axis scope.
5. Exact finite certificates.
6. Route evaluation, obstruction, and next theorem.
