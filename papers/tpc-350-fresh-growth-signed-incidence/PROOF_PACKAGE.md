# TPC-350 proof and scope package

## Proposition 1: balanced shell coefficients

For a shell of length `r`, the declared coefficient vector has `floor(r/2)`
positive entries, the same number of negative entries, and at most one zero.
Hence its coefficient sum is zero.

**Proof.** The positive indices are `0,...,m-1` and the negative indices are
`r-m,...,r-1`, where `m=floor(r/2)`.  These blocks are disjoint and have equal
cardinality; the remaining block has size `r-2m` in `{0,1}`. ∎

## Proposition 2: incidence identity

At every `t in I`, the producer's accumulator equals
`b_I(t)=sum_j beta_j 1_(p_j divides t)`.

**Proof.** The accumulator adds exactly the coefficient of every shell prime
dividing `t`; multiply-divisible positions are intentionally retained. ∎

## Proposition 3: Gram expansion

For every finite defect matrix `D_I`,

```text
||D_I b_I||_2^2
 = sum_(j,k) beta_j beta_k
   <D_I h_(p_j,I),D_I h_(p_k,I)>.
```

**Proof.** Substitute Proposition 2, use linearity, and expand the finite
Euclidean inner product. ∎

## Theorem 4: induced-norm lower witness

If `b_I != 0`, then
`||D_I||_(2->2) >= ||D_I b_I||_2/||b_I||_2`.

**Proof.** Normalize `b_I` to a unit vector and insert it into the definition
of the induced Euclidean norm. ∎

## Proposition 5: finite interpretation

The growth-series values, positivity census, scale floor, and baseline counts
are numerical observations on the locked 192-row panel.  They do not imply a
uniform-in-`M` or uniform-in-`Q` bound. ∎

## Scope ceiling

```text
SIGNED_INCIDENCE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
FRESH_GROWTH_AND_SCALE_AUDIT = NUMERICALLY_CERTIFIED_FINITE
UNIFORM_QUARTER_FLOOR = REFUTED_SCOPED
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```
