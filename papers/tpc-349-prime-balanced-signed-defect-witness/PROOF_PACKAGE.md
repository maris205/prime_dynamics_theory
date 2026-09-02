# TPC-349 proof and scope package

## Proposition 1: exact prime balance

For `r` ordered shell primes and `m=floor(r/2)`, the declared coefficients have
`m` entries equal to `+1`, `m` entries equal to `-1`, and at most one zero.
Therefore `sum_j beta_j=0`.

**Proof.** The first block has indices `0,...,m-1`; the last block has indices
`r-m,...,r-1`.  These blocks are disjoint and have equal cardinality.  The
remaining block has size `r-2m`, which is zero or one. ∎

## Proposition 2: incidence identity

Let `h_(p,I)` be the vector with coordinate `1_(p divides t)` at `t in I`.
Then the producer's vector is exactly

```text
b_I = sum_j beta_j h_(p_j,I).
```

**Proof.** At each coordinate `t`, the right side is the sum of exactly the
coefficients of active shell primes dividing `t`, which is the definition used
by the incidence accumulator. ∎

## Proposition 3: prime-incidence Gram identity

For every finite matrix `D_I`,

```text
||D_I b_I||_2^2
 = sum_(j,k) beta_j beta_k
   <D_I h_(p_j,I),D_I h_(p_k,I)>.
```

**Proof.** Substitute Proposition 2, apply linearity of `D_I`, and expand the
Euclidean inner product.  The sum is finite, so no convergence assumption is
needed. ∎

## Theorem 4: signed-incidence lower witness

If `b_I != 0`, then

```text
||D_I||_(2->2) >= ||D_I b_I||_2 / ||b_I||_2.
```

**Proof.** The vector `b_I/||b_I||_2` is a unit vector.  Insert it into the
definition of the induced Euclidean norm. ∎

## Proposition 5: finite certificate

The locked panel has 192 rows.  All rows have nonzero signed incidence vectors
and positive response.  The producer, reverse-shell checker, and stress suite
certify the row census and the exact anchor.  The finite readout is:

```text
signed/defect ratio       0.39083565842--0.954375010719
signed/ideal ratio        0.0125941959067--0.430061305156
signed/coordinate ratio   0.542800508699--2.04702542827
coordinate baseline wins  136/192 rows are beaten by the signed vector
half-defect census        175/192 rows reach at least one half
```

These are numerical observations on the declared panel.  The fact that the
coordinate baseline is not beaten in every row is retained as
`REFUTED_SCOPED` for a universal balanced-gain statement.

## Claim ceiling

```text
SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
PRIME_BALANCE_AND_GRAM = PROVED_EXACT_FINITE_DECLARED_MODEL
FINITE_SIGNED_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
UNIVERSAL_BALANCED_GAIN = REFUTED_SCOPED
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```
