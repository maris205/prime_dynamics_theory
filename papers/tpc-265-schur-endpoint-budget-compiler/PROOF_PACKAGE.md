# TPC-265 proof package

All inner products use the conjugate-linear-first-slot convention.  The
endpoint constants are

```text
E0=5/3,  E*=1997/1200,  Delta*=1/400.
```

## Theorem 1 — sharp Schur reassembly envelope

For `c in C` and `R>=0`, define the disk `D(c,R)={c+z: |z|<=R}`.  Then

```text
sup_{y in D(c,R)} |y| = |c|+R,
inf_{y in D(c,R)} |y| = max(|c|-R,0).
```

If the residual set is the circle `{c+z:|z|=R}`, the supremum is still
`|c|+R` and the infimum is `||c|-R|`.

### Proof

For every admissible `z`, the triangle inequality gives
`|c+z|<=|c|+|z|<=|c|+R`.  If `c != 0`, choose
`z=R c/|c|`; if `c=0`, choose any `|z|=R`.  Equality follows.  The reverse
triangle inequality gives `|c+z|>=||c|-|z||`; choosing `z` opposite to `c`
when `|c|>=R`, and choosing `z=-c` when `|c|<R`, attains the disk lower edge.
On the circle the upper aligned point remains available, while the lower
calculation is forced to use `|z|=R`, giving `||c|-R|`. `(square)`

## Theorem 2 — Schur-derived endpoint compiler

Let `c_x` be a projected center and let the admissible residual set be a disk
of radius `R_x`.  Suppose that for every sufficiently small `epsilon>0`,

```text
|c_x| <= C_c(epsilon) x^(E0-delta_c+lambda_c+epsilon),
R_x    <= C_r(epsilon) x^(E0-delta_r+lambda_r+epsilon).
```

If

```text
delta_c-lambda_c > Delta*  and  delta_r-lambda_r > Delta*,
```

then every admissible full scalar is `o(x^E*)`.  If either effective saving is
equal to `Delta*`, the corresponding lane is power-level borderline; if either
is below `Delta*`, these hypotheses alone do not close the target.

### Proof

Theorem 1 gives the exact worst-case envelope `|c_x|+R_x`.  Choose epsilon
smaller than half the minimum of the two strict margins.  Each lane is then
`O(x^(E*-eta))` for some `eta>0`, and their sum is `o(x^E*)`.  Equality and
subcritical cases follow by direct exponent comparison. `(square)`

## Theorem 3 — logarithmic control has zero power credit

For fixed `M` and `delta>0`,

```text
x^E0/(log x)^M is not O(x^(E0-delta)).
```

Thus a fixed-log estimate for either the center or radius cannot be entered as
a positive fixed-power saving in Theorem 2.

### Proof

The ratio is `x^delta/(log x)^M`, which tends to infinity after taking
logarithms. `(square)`

## Corollary — exact next-input specification

After TPC-263's rank-three logarithmic channel, a full endpoint proof needs a
new literal theorem paying the center lane and the Schur radius lane, or a
signed phase theorem that replaces the disk envelope.  A norm-only Schur bound
does not supply cancellation credit.

## Scope firewall

```text
PROVED = exact disk/circle radial envelope and two-lane exponent compiler
NUMERICALLY_CERTIFIED = rational/Gaussian endpoint fixtures and mutations
CONDITIONAL_THEOREM = power-saving hypotheses in Theorem 2
OPEN = literal V59 residual radius, signed residual phase, arithmetic L2,
       full Gate B, twin-prime theorem
REFUTED_SCOPED = automatic cancellation credit from the Schur disk
MODELING_CHOICE = finite endpoint fixtures; no literal growing-shell model
```
