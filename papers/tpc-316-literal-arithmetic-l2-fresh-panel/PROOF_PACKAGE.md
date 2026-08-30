# TPC-316 proof package

## Proposition 1: literal finite matrix

For each declared `(X,Q,s)`, the matrix `A_(Q,s,X)` is a finite rational
matrix with `N_X` columns and `N_X |S_Q|` rows.

**Proof.**  The height, difference, divisibility indicators, congruence
indicator, and centered factor in the displayed definition are rational.
There are finitely many `p,u,t`, and the diagonal or divisible endpoint rows
are exactly zero.  ∎

## Proposition 2: finite Frobenius `L2` interface

For every vector `beta`,

```text
||A beta||_2^2 <= ||A||_HS^2 ||beta||_2^2.
```

**Proof.**  For each output row `r`, Cauchy--Schwarz gives
`|sum_t A_(r,t) beta_t|^2 <= (sum_t |A_(r,t)|^2)(sum_t |beta_t|^2)`.
Summing over `r` proves the assertion.  Dividing by the positive source
cardinality gives the normalized form in the derivation package.  ∎

## Proposition 3: exact difference/residue identity

Let `delta=u-t` be nonzero.  The endpoint pairs with that difference are
parameterized by `t in J_delta`.  When `p|delta`, both endpoints have the same
residue and only residue zero is forbidden; when `p` does not divide `delta`,
the zero and `-delta` residues are distinct and both are forbidden.  The
centered square is respectively `(p-2)^2/(p-1)^2` and `1/(p-1)^2`.

Multiplying the number of admissible pairs by the common squared kernel factor
and summing over `delta` and `p` gives the formula in the derivation package.
Every step is an equality over the rationals.  ∎

## Proposition 4: coordinate lower witnesses

For every source coordinate `t`,

```text
||A_(Q,s,X)||_(2->2)^2 >= ||A_(Q,s,X)e_t||_2^2.
```

**Proof.**  The coordinate vector has unit Euclidean norm, so this is the
definition of the induced operator norm.  The certificate evaluates the
right-hand side directly from the matrix entries.  ∎

## Proposition 5: finite certificate result

The producer and independent checker evaluate 16 rows (two scales, four
shell anchors, two exponents) and five columns per row.  They agree on every
exact rational digest.  The normalized Hilbert--Schmidt mass at `1280` is
strictly larger than at `640` for all eight matched rows.  On the fresh panel
the exact Frobenius-to-best-probe ratios are all greater than `517`.

This is a finite, same-engine certificate.  It does not imply that the true
operator norm grows, nor does it refute a future cancellation theorem.  It
only refutes, on the declared two-panel scope, the use of this normalized
Frobenius envelope as evidence for a decaying power.  ∎

## Claim ceiling

```text
PROVED_EXACT_FINITE_LITERAL_OPERATOR = YES
PROVED_EXACT_FINITE_FROBENIUS_INTERFACE = YES
PROVED_EXACT_FINITE_DIFFERENCE_COUNT = YES
NUMERICALLY_CERTIFIED_FINITE_TWO_SCALE_RISE = 8_OF_8
NUMERICALLY_CERTIFIED_FINITE_PROBE_GAP = 16_OF_16
GROWING_ARITHMETIC_L2 = OPEN
TRUE_OPERATOR_NORM_DECAY = OPEN
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```
