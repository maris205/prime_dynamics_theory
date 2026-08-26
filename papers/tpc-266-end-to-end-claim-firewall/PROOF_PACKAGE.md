# TPC-266 proof package

All powers below are interpreted with an arbitrarily small positive
`epsilon`, and all evidence labels are literal type labels rather than
informal descriptions.

## Definition — the typed endpoint compiler

Let

```text
Delta* = E0-E* = 1/400.
```

For a center descriptor `L_c` and a radius descriptor `L_r`, define
`pay(L)=true` exactly when `L` is of type `POWER` or `SIGNED_PHASE` and its
effective saving `delta-lambda` is strictly larger than `Delta*`.  A
`FIXED_LOG`, `MISSING`, or `DELETED` descriptor is not paid.  The compiler
returns `CLOSED_CONDITIONAL` precisely when both descriptors are paid and the
residual-retained flag is true.

## Theorem 1 — sound composition

Suppose the residual scalar has the form

```text
T_x = c_x+z_x,       |z_x| <= R_x,
```

and the residual is retained.  Assume

```text
|c_x| <= C_c(epsilon) x^(E0-delta_c+lambda_c+epsilon),
R_x    <= C_r(epsilon) x^(E0-delta_r+lambda_r+epsilon).
```

with

```text
delta_c-lambda_c > Delta*,
delta_r-lambda_r > Delta*.
```

Then `T_x=o(x^E*)`.

### Proof

The triangle inequality gives

```text
|T_x| <= |c_x|+|z_x| <= |c_x|+R_x.
```

Let `eta` be half the smaller of the two strict gaps above.  Choose
`epsilon<eta`.  Each displayed lane is then `O(x^(E*-eta))`, after reducing
the exponent by `Delta*`; their sum is `O(x^(E*-eta))`, hence `o(x^E*)`.
This is exactly the decision made by the compiler. `(square)`

## Theorem 2 — typed non-promotion

Under the compiler interface, a `FIXED_LOG` lane cannot be paid as a positive
fixed-power lane.  In particular, for every fixed `M` and every `delta>0`,

```text
x^E0/(log x)^M is not O(x^(E0-delta)).
```

### Proof

The ratio is `x^delta/(log x)^M`, which tends to infinity.  Thus the type
transition `FIXED_LOG -> POWER(delta)` is unsound. `(square)`

## Theorem 3 — residual-retention firewall

If only the projected center is retained and the Schur radius is deleted,
the resulting scalar certificate is not sound.  Indeed, for any `R>0` the
admissible disk contains the aligned point `z=R c/|c|` when `c!=0` (and any
point of modulus `R` when `c=0`), so

```text
sup_{|z|<=R}|c+z| = |c|+R.
```

The deleted-residual output `|c|` can therefore differ from the admissible
endpoint by the full radius `R`. `(square)`

## Theorem 4 — exact failure classification

Relative to the declared interface, the compiler's six-state matrix is
minimal:

1. two strict paid lanes close conditionally by Theorem 1;
2. a fixed-log center has no legal power payment by Theorem 2;
3. a missing radius has no bound for the second summand;
4. equality `sigma=Delta*` is only power-level borderline;
5. `sigma<Delta*` leaves an endpoint at or above the target scale;
6. residual deletion is rejected by Theorem 3.

### Proof

Items 1, 2, and 6 are Theorems 1--3.  For item 4, the lane exponent is
exactly `E*+epsilon`, so the interface has no strict margin.  For item 5,
write `sigma=Delta*-ho` with `rho>0`; the lane exponent is
`E*+rho+epsilon`, which is not a target-saving exponent.  Item 3 is the
definition of a missing hypothesis.  Each conclusion is attained by the
exact rational fixtures in the certificate, so no matrix row can be silently
relabelled as `CLOSED_CONDITIONAL`. `(square)`

## Corollary — end-to-end route status

The TPC-263 -> TPC-264 -> TPC-265 chain has a valid structural type path, but
its actual current labels are

```text
center   = FIXED_LOG,
residual = SCHUR_SET with radius OPEN,
endpoint = RADIAL_ENVELOPE,
```

Consequently the chain is correctly classified as open for the literal V59
endpoint.  A future literal radius or signed-phase theorem must enter as a
new paid lane with effective saving strictly greater than `1/400`.

## Scope firewall

```text
PROVED = typed compiler soundness; fixed-log non-promotion; residual-retention
         firewall; exact six-state failure classification
NUMERICALLY_CERTIFIED = exact rational endpoint fixtures and mutation matrix
CONDITIONAL_THEOREM = the target bound under two strict paid-lane hypotheses
OPEN = literal V59 radius/phase, arithmetic L2, full Gate B, twin-prime theorem
REFUTED_SCOPED = fixed-log-to-power promotion and residual deletion
MODELING_CHOICE = finite hostile fixtures; no literal growing-shell counterexample
```
