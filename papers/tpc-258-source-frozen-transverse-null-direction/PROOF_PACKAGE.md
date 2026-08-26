# TPC-258 proof package

## Theorem (source-frozen transverse diagonal cancellation)

Let `x` tend to infinity through real values.  Retain the literal V59 object,
operator, and four-block frame from TPC-257.  Put

```text
L1=log(3456/3125), L2=log(884736/823543), LT=(L1^2+L2^2)^(1/2),
z_null=(L2 z1-L1 z2)/LT.
```

Then `z_null` is source-only, unit, and lies in `z0`-perp.  Moreover,

```text
<z_null,A_x beta>=o(x^(7/6)/log^3(x)).                 (P258.1)
```

The claim is `PROVED_SOURCE_BACKED`; it is a cancellation theorem for one
finite projection, not an upper estimate for the full output.

## 1. Exact frame input

TPC-257's four consecutive blocks have normalized contrasts `z0,z1,z2` with

```text
<zi,zj>=delta_ij,
TV(zi)=2/rho_i=O(x^(-1/2)).
```

The source construction is independent of the coefficient.  Since the two
constants `L1,L2` are positive, `LT>0`, and direct expansion gives

```text
||z_null||^2=(L2^2||z1||^2+L1^2||z2||^2)/LT^2=1.
```

Disjoint support gives `<z1,z2>=0`; TPC-257 also gives both vectors
orthogonal to `z0`, hence `<z_null,z0>=0`.

## 2. Inherited scalar asymptotics

The TPC-257 theorem, applied to the two descendant vectors, states

```text
<z1,A_x beta>=-(9/2*kappa1+o(1))S_x,
<z2,A_x beta>=-(9/2*kappa2+o(1))S_x,
S_x=x^(7/6)/log^3(x),
```

with `kappa1=L1/2` and `kappa2=L2/2`.  Its proof retains the exact
TPC-255 bounded-variation identity

```text
<z,A_x beta>=-B_Q<z,beta>+R_unit(z)+R_boundary(z),
```

and proves `B_Q=(9/2+o(1))x^(2/3)/log x`, beta curvature of order
`sqrt(x)/log^2 x`, and `R_boundary=O_(psi,epsilon)(x^(55/48+epsilon))`.

## 3. Cancellation proof

By linearity of the Hilbert-space inner product in the second slot and real
linearity of the displayed coefficients,

```text
<z_null,A_x beta>
 = [L2<z1,A_x beta>-L1<z2,A_x beta>]/LT.
```

Substitute the inherited asymptotics:

```text
L2*(-9/2)*(L1/2)-L1*(-9/2)*(L2/2)=0.
```

The remaining two `o(S_x)` terms are still `o(S_x)` after multiplication by
the fixed constants `L1/LT,L2/LT`.  This proves (P258.1).  The boundary terms
are already included in the `o(S_x)` remainder because

```text
x^(55/48+epsilon) / S_x
 = x^(-1/48+epsilon) log^3(x) -> 0
```

for any fixed `epsilon<1/48`.  No cancellation of a boundary term is assumed.

## 4. Conditional rate refinement

Suppose, in addition, that the two inherited scalar formulas are available
with the explicit remainder

```text
<zi,A_x beta>=-(9/2*kappa_i)S_x
 +O_(psi,epsilon)(S_x/log x+x^(55/48+epsilon)).       (P258.2)
```

Then the same exact linear combination proves

```text
|<z_null,A_x beta>|
 <<_(psi,epsilon) S_x/log x+x^(55/48+epsilon).        (P258.3)
```

This is labelled `CONDITIONAL_THEOREM` in the certificate because the
released TPC-257 interface freezes an `o(1)` coefficient in its headline
theorem.  The conditional line is not used to claim a fixed power.

## 5. Adversarial rate firewall

Consider formal scalar errors `e1(x)=1/sqrt(log x)` and `e2(x)=0` in place of
the two `o(1)` terms.  They satisfy `e_i(x)->0`, but the null combination is
`(L2/LT)e1(x)S_x`, which is not `O(S_x x^(-delta))` for any `delta>0`.
This finite symbolic adversary is a quantifier control, not a literal V59
counterexample.  It proves only that the `o(1)` theorem cannot be silently
upgraded to a power saving.

## 6. Claim firewall

```text
TPC258_MAXIMUM_CLAIM = PROVED_SOURCE_BACKED_TRANSVERSE_DIAGONAL_NULL_CANCELLATION_FOR_LITERAL_V59_ADJOINT
TPC258_NULL_DIRECTION = PROVED_SOURCE_FROZEN_UNIT_VECTOR
TPC258_LEADING_DIAGONAL_CANCELLATION = PROVED_SOURCE_BACKED
TPC258_RATE_REFINEMENT = CONDITIONAL_THEOREM_LOG_ONE_OVER_X
TPC258_FIXED_POWER_SAVING = NONE
TPC258_L2 = NONE
TPC258_FULL_GATE_B = OPEN
TPC258_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC258_FIXED_ATOM_CREDIT = 0
TPC258_TWIN_PRIME_RESULT = NONE
```

The separately named Session Route-A/Route-B evaluator files are absent from
this checkout.  The local proof package, theorem ledger, bridge checker, and
`AGENTS.md` are the available fail-closed authorities.
