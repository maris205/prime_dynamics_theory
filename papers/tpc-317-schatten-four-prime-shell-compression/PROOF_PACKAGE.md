# TPC-317 proof package

## Proposition 1: finite Gram positivity

For every declared finite row, `G=A^*A` is positive semidefinite.

**Proof.**  For any source vector `z`,
`z^*Gz=z^*A^*Az=||Az||_2^2>=0`.  The matrix is finite because both the
source interval and the prime shell are finite.  ∎

## Proposition 2: Schatten-4 envelope

For every finite source vector `beta`,

```text
||A beta||_2^2 <= sqrt(trace(G^2)) ||beta||_2^2.
```

**Proof.**  Diagonalize the positive semidefinite matrix `G`.  Its eigenvalues
`lambda_i` are nonnegative, and
`lambda_max(G)^2 <= sum_i lambda_i^2=trace(G^2)`.  Since
`||A beta||_2^2=beta^*G beta<=lambda_max(G)||beta||_2^2`, the assertion follows
after taking a square root.  ∎

## Proposition 3: comparison with the Frobenius envelope

```text
sqrt(trace(G^2)) <= trace(G)=||A||_HS^2.
```

**Proof.**  For nonnegative eigenvalues, `sum_i lambda_i^2 <=
(sum_i lambda_i)^2`.  The right-hand trace is the squared Hilbert--Schmidt
norm by definition.  ∎

## Proposition 4: exact finite trace-square identity

If `K_r,t` denotes the literal matrix entry with output index `r=(p,u)`,

```text
trace((A^*A)^2)
 = sum_(t,v) (sum_r K_(r,t) K_(r,v))^2.
```

**Proof.**  The Gram entry is
`G_(t,v)=sum_r K_(r,t)K_(r,v)`.  The matrix is real symmetric, hence
`trace(G^2)=sum_(t,v)G_(t,v)G_(v,t)=sum_(t,v)G_(t,v)^2`.  ∎

## Proposition 5: rationality and exact anchor

Every entry and every finite trace power is rational.  On the declared
`I={17,...,32}`, `p=5`, `s=1` anchor, the producer and the independent stress
replay evaluate `trace(G)` and `trace(G^2)` as exact `Fraction` values and
compare numerator/denominator digests.

**Proof.**  The displayed kernel is a quotient of integers, and finite sums,
products, and squares preserve rationality.  The anchor is a direct finite
enumeration of those operations.  ∎

## Proposition 6: status of the large-panel trend

The 24 large-panel rows and 16 adjacent-scale comparisons are a numerical
certificate under the stated binary64 error model.  It establishes a finite
opposite-trend record: all 16 normalized Schatten-4 comparisons decrease,
while all 16 normalized Frobenius comparisons increase.

This proposition is deliberately not promoted to a theorem about `X ->
infinity`; it is the output of the replayable certificate and its independent
checker.

## Claim ceiling

```text
PROVED_EXACT_FINITE = Gram positivity; Schatten-4 inequality;
                      Schatten-4/Frobenius chain; trace-square identity;
                      rationality of every finite entry and trace power
NUMERICALLY_CERTIFIED_FINITE = exact small anchor; 24 large rows;
                               16 Schatten-4 decreases; 16 Frobenius increases
NUMERICAL_OBSERVATION = the finite compression is interpreted as a scale trend
REFUTED_SCOPED = Frobenius mass is not a sharp spectral proxy on these panels
OPEN = true operator-norm asymptotic; arithmetic cancellation; normalization;
       fixed-power credit; full Gate B; twin-prime endpoint
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```
