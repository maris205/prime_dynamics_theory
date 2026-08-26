# TPC-261 derivation package

All exponents below are on the common V59 clock.  The notation is deliberately
an endpoint ledger: it records what a theorem would have to pay, without
pretending that an unpaid lane has already been estimated.

## 1. Baseline and target

The current unnormalized baseline is

```text
E0 = 5/3 = 2000/1200.
```

The target endpoint retained by the Route-B ledger is

```text
E* = 1997/1200.
```

Therefore the exact required power saving is

```text
Delta* = E0-E* = 3/1200 = 1/400.
```

The identity is an exponent identity, not an arithmetic estimate.

## 2. Lane-wise compiler

Let `T_l(x)` be a finite collection of reassembly lanes.  Suppose that for
every `epsilon>0`

```text
|T_l(x)| <= C_(l,epsilon) x^(E0-delta_l+lambda_l+epsilon),
```

where `delta_l` is a proved lane saving and `lambda_l` is a proved loss from
normalization, boundary leakage, or reassembly.  Define

```text
sigma_l = delta_l-lambda_l,
sigma = min_l sigma_l.
```

For a fixed finite lane set, if `sigma>Delta*`, choose
`epsilon < (sigma-Delta*)/2`.  Summing the finitely many bounds gives

```text
sum_l |T_l(x)| = o(x^E*).
```

At `sigma=Delta*`, the same hypotheses give only a power-level borderline
bound (with an arbitrarily small epsilon); they do not by themselves give a
strict little-oh statement at the target.  If `sigma<Delta*`, the ledger does
not close.

## 3. Logarithmic savings do not buy a fixed power

For every fixed `M` and every fixed `delta>0`,

```text
x^delta/(log x)^M -> infinity.
```

Consequently an estimate of the form `x^E0/(log x)^M` cannot be rewritten as
`x^(E0-delta+epsilon)` with `epsilon<delta`.  It has zero fixed-power credit in
this compiler.  This is why TPC-258/259 `o(1)` or arbitrary fixed logarithmic
suppression cannot be entered as payment for the `1/400` endpoint gap.

## 4. Scaled TPC-260 witness

Let `z` and `w` be orthonormal, with `z` the source-frozen null direction and
`w` the scaling/residual direction.  Put `a(x)=x^(E0/2)=x^(5/6)` and define

```text
V_j^+(x) = a(x) w,
V_j^-(x) = (-1)^j a(x) w,       0<=j<=3.
```

Both families have identical packet norms `a(x)`, identical packet diagonal,
zero Haar/null projections, and total packet energy `4x^E0`.  But

```text
||sum_j V_j^+(x)||^2 = 16x^E0,
||sum_j V_j^-(x)||^2 = 0.
```

Thus the current marginal/null interface permits a full residual at baseline
scale.  For every `delta>0`, the plus family violates any universal claim that
those data alone force `O(x^(E0-delta))`.  The witness is synthetic and finite
dimensional; it is not identified with a growing prime shell.

## 5. Minimum sufficient literal theorem

The smallest missing statement that would activate the endpoint compiler is a
common-clock estimate for the literal four-packet mode-zero output, or an
equivalent signed cross-Gram estimate, with effective saving strictly larger
than `1/400` after every boundary, mask, deleted-diagonal, and normalization
loss.  A local `1/48` boundary gap is numerically larger than `1/400`, but it is
not global credit until a transfer theorem attaches it to the same literal
whole object.
