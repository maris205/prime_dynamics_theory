# TPC-274 proof package

## Theorem 1: projected Frobenius output envelope

Let `A` be the finite literal V59 operator, `P_3` an orthogonal projection,
and `beta` any finite coefficient vector.  Then

```text
||(I-P_3) A beta||_2^2
 <= ||(I-P_3)A||_F^2 ||beta||_2^2.
```

### Proof

Set `B=(I-P_3)A`.  For each row `i`, Cauchy--Schwarz gives

```text
|sum_j B_(i,j) beta_j|^2
 <= (sum_j |B_(i,j)|^2)(sum_j |beta_j|^2).
```

Summing over `i` gives the displayed inequality.  The argument is valid over
the reals or complexes and does not use a probabilistic model.

## Theorem 2: conservative margin ordering

If `W_perp>0`, `G_perp>0`, and
`G_F=||(I-P_3)A||_F^2||beta||_2^2`, then

```text
m_F^2 := |C_perp|^2/(W_perp G_F) <= |C_perp|^2/(W_perp G_perp) = m^2.
```

### Proof

Theorem 1 gives `G_perp<=G_F`; division by the positive quantity
`W_perp G_F G_perp` preserves the inequality.

## Theorem 3: registered finite certificate

For the six TPC-269 growing-cutoff scale rows

```text
(N,H,Q)=(64,15,4),(96,20,5),(128,24,5),
        (192,32,6),(256,38,6),(384,50,7)
```

and exponents `s=1,2`, exact rational matrix construction and parent outward
interval transfer certify:

- 12/12 rows have `G_F/G_perp > 50`;
- 12/12 rows have `m_F^2 < 1/64`, so the envelope-derived margin is below
  `1/8`;
- all 12 rows have positive source/output residual lanes and phase intervals
  separated from zero (11 negative-real, 1 positive-real, no crossing).

These are finite numerical certificates.  The first two bullets say that the
norm-only envelope is insufficient to establish a quarter-sector margin on
these rows; they do not say that the actual margin is small.

## Claim ceiling

```text
PROVED_EXACT_FINITE_INEQUALITY = projected Frobenius envelope
NUMERICALLY_CERTIFIED_FINITE = 12-row gap and envelope-margin audit
INSUFFICIENT_SCOPED = cancellation-free output route on the registered rows
OPEN_ASYMPTOTIC = source-level output bound and signed reassembly
FIXED_POWER_CREDIT = 0
ARITHMETIC_L2 = NONE
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```
