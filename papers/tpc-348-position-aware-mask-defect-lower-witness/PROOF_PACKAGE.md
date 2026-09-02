# TPC-348 proof and scope package

## Proposition 1: two-sided mask defect

For every finite interval `I`, shell prime `p`, and finite kernel matrix `K_p`,

```text
R_I(P_p K_p P_p-K_p)E_I
 = R_I((P_p-I)K_pP_p+K_p(P_p-I))E_I.
```

**Proof.** Expand the right-hand side:
`P K P-K P+K P-K=P K P-K`.  The restriction and extension are then applied
to both sides.  ∎

## Proposition 2: position-aware coordinate formula

For `t in I`, write `e_t` for the corresponding unit coordinate vector.  If
`p divides t`, then `P_p e_t=0` and

```text
R_I((P_p-I)K_pP_p+K_p(P_p-I))E_I e_t = -R_I K_p e_t.
```

If `p does not divide t`, then `(P_p-I)e_t=0` and the same expression is

```text
R_I(P_p-I)K_p e_t.
```

Multiplying by `e_p` and summing over the shell proves

```text
D_I e_t = -sum_(p|t)e_p R_I K_p e_t
          +sum_(p not|t)e_p R_I(P_p-I)K_p e_t.
```

This is an exact identity; it does not assert that the summands have a common
sign.

## Proposition 3: coordinate lower bound

For any finite matrix `D` and any coordinate `e_t`,

```text
||D||_(2->2) >= ||D e_t||_2.
```

Consequently, for
`J_I={t in I: p divides t for at least one active shell prime p}`,

```text
||D_I||_(2->2) >= max_(t in J_I)||D_I e_t||_2 = W_I(D).
```

**Proof.** Each `e_t` is a unit vector in the supremum defining the induced
Euclidean norm.  Taking a maximum over a subset preserves the inequality.  ∎

## Proposition 4: finite certificate

The frozen two-origin, three-count, four-anchor, two-exponent, four-law grid
contains `192` rows.  The producer and reverse-shell checker independently
reconstruct every matrix.  All `192` rows have a nonempty mask-hit set, a
strictly positive selected witness column, and a verified two-sided projection
formula.  The largest formula discrepancy is
`2.0872192863e-14` in the floating-point replay.

The best mask-hit coordinate witness satisfies

```text
0.453958762219 <= W_I(D)/||D_I|| <= 0.897148966365
```

on the declared rows, while

```text
0.0183057714619 <= W_I(D)/||T_I|| <= 0.336311065586.
```

These are finite numerical observations, not growing lower bounds.

## Exact anchor

For `I={1,...,6}`, `Q=4`, exponent `1`, and all-plus signs, the shell is
`{5,7}`, the hit set is `{5}`, and the selected fifth column has exact squared
norm

```text
1264004832717663389653333 / 162252681195863096059456.
```

## Claim ceiling

```text
COORDINATE_LOWER_WITNESS = PROVED_EXACT_FINITE_LINEAR_ALGEBRA
MASK_HIT_SELECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL
POSITION_FORMULA = PROVED_EXACT_FINITE_DECLARED_MODEL
FINITE_POSITION_AUDIT = NUMERICALLY_CERTIFIED_FINITE_192_ROWS
POSITIVE_WITNESS_CENSUS = NUMERICALLY_CERTIFIED_FINITE_192_OF_192
MASK_DISCARD_SHORTCUT = REFUTED_SCOPED
SOURCE_UNIFORM_ARITHMETIC_L2 = OPEN
UNIFORM_MASKED_OPERATOR_BOUND = OPEN
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```
