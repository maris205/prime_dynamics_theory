# TPC-297 proof package

## Theorem 1 — restricted source projection

Let `A` be any real physical matrix, let `U` be a source-profile matrix, and
write `V=A^T U`.  For every target `b`,

```text
min_c ||A^T U c-b||_2^2 = b^T (I-P_V) b,
```

where `P_V` is the orthogonal projection onto `col(V)`.  If `V` has full
column rank, `P_V=V(V^T V)^(-1)V^T`.

**Proof.** The least-squares normal equations select the orthogonal
projection `P_V b` of `b` onto `col(V)`.  Write
`b=P_V b+(I-P_V)b`; the two summands are orthogonal, so for every `y` in
`col(V)`, Pythagoras gives
`||b-y||^2=||(I-P_V)b||^2+||P_Vb-y||^2`.  Equality is attained at
`y=P_Vb`.  The full-rank formula is the standard inverse form of the
projection. ∎

## Theorem 2 — adding a source profile cannot hurt

If `col(U_1) subseteq col(U_2)`, then
`col(A^T U_1) subseteq col(A^T U_2)`, and hence the optimal residual for
`U_2` is no larger than that for `U_1`.

**Proof.** Linear maps preserve inclusions.  Apply Theorem 1 to the two
nested target subspaces. ∎

## Finite certificate consequence

The producer and independent checker instantiate `U` with the four literal
cutoff profiles `z=3,5,7,11`.  Two modular rank checks give rank 3 on the
three-prime row and rank 4 on all other 17 rows.  At 70 digits, the weighted
target residual is at least `0.6` on those 17 rows, while the all-positive
residual is at most `0.15` on all 18 rows.  These are finite numerical
observations and are not an asymptotic theorem.

## Claim firewall

```text
PROVED_EXACT_FINITE = projection identity; nested-span monotonicity
NUMERICALLY_CERTIFIED_FINITE = exact-rational construction plus 70-digit replay
NUMERICAL_OBSERVATION = finite residual threshold census
OPEN = growing profile dimension, principal angles, source budget growth
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```
