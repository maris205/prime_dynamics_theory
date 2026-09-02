# TPC-351 proof and scope package

## Proposition 1: reciprocal shell coefficients

For distinct shell primes `p_0,...,p_(r-1)`, define
`gamma_j=1/p_j-(1/r)sum_k 1/p_k`.  Then the coefficient sum is exactly zero.
For the four declared shells in this project, exact rational evaluation also
checks that every resulting coefficient is nonzero.

**Proof.** Summing the first term gives `(1/r)sum_k1/p_k` exactly `r` times,
which cancels the repeated mean.  The nonvanishing assertion is not needed
for the identity; on the declared finite shell list it is checked exactly by
the producer's rational coefficient routine. ∎

## Proposition 2: incidence identity

At every `t in I`, the producer's accumulator equals
`c_I(t)=sum_j gamma_j 1_(p_j divides t)`.

**Proof.** The accumulator adds exactly the coefficient of every shell prime
dividing `t`; multiply-divisible positions are intentionally retained.  The
coefficients are rational and are evaluated exactly in the anchor. ∎

## Proposition 3: Gram expansion

For every finite defect matrix `D_I`,

```text
||D_I c_I||_2^2
 = sum_(j,k) gamma_j gamma_k
   <D_I h_(p_j,I),D_I h_(p_k,I)>.
```

**Proof.** Substitute Proposition 2, use linearity, and expand the finite
Euclidean inner product. ∎

## Theorem 4: induced-norm lower witness

If `c_I != 0`, then
`||D_I||_(2->2) >= ||D_I c_I||_2/||c_I||_2`.

**Proof.** Normalize `c_I` to a unit vector and insert it into the definition
of the induced Euclidean norm. ∎

## Proposition 5: finite interpretation

The parent comparisons, growth-series values, positivity census, scale floor,
and baseline counts are numerical observations on the locked 192-row panel.
They do not imply a uniform-in-`M` or uniform-in-`Q` bound. ∎

## Scope ceiling

```text
RECIPROCAL_ZERO_SUM_RULE = PROVED_EXACT_FINITE_DECLARED_RATIONAL_RULE
SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
SCALE_REPAIR_AND_PARENT_COMPARISON = NUMERICALLY_CERTIFIED_FINITE
PARENT_IMPROVEMENT = NUMERICALLY_CERTIFIED_FINITE_180_OF_192
UNIFORM_QUARTER_FLOOR = REFUTED_SCOPED
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```
