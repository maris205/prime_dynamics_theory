# Theorem Ledger

## PROVED

`T213.1` — For a finite support `U`, the residue aggregation operator
`C_d f(a)=sum_{u congruent a (mod d)} f(u)` is the exact common-source map for
all divisor profiles.

`T213.2` — If `R_d=C_d(v-b_d)`, then the bilinear emitter pairing satisfies

```text
sum_d sum_r A_d(r) Rhat_d(r)
 = sum_u v(u) K(u) - sum_d sum_u b_d(u) K_d(u),
K=sum_d K_d,
K_d(u)=sum_r A_d(r)e_d(ru).
```

`T213.3` — On a complete period `L` divisible by `lcm(d,e)`,

```text
(C_d C_e^*)(a,b) = (L/lcm(d,e)) 1_(a == b mod gcd(d,e)).
```

`T213.4` — On one complete period `L=lcm(d,e)`,

```text
sum_(u mod L) K_d(u) conjugate(K_e(u))
 = L sum_(r/d == s/e mod 1) A_d(r) conjugate(A_e(s)).
```

`T213.5` — The finite unit-weight fixture has cross-Gram values `560` for
`(5,35)`, `770` for `(7,35)`, and zero for `(5,7)`.  The joint residue lift
on `{0,...,34}` has rank `35` and codomain dependency dimension `12`.

## NUMERICALLY_CERTIFIED

The producer and independent checker reproduce `47` Euler profile coordinates,
three lift identities, three emitter rows, and three cross-Gram cases.  All
reported values are exact integers or rational strings; the label refers to a
finite certificate, not floating-point or asymptotic evidence.

## MODELING_CHOICE

The finite emitter takes unit reciprocal weights (`psi=1`) and omits the
irrational `log(d)` scalar so that the geometric Gram is exact over integers.
The literal V46 smooth emitter and logarithmic prefactors are retained in the
theorem statement as symbolic inputs but are not estimated by the certificate.

## REFUTED_SCOPED

`T213.R1` — Replacing the common-source physical profile family by an orthogonal
direct sum is not an identity for the V46 operator.  The exact pullback has
off-diagonal cross-divisor terms whenever emitter frequency sets intersect.

This is not a refutation of a future coupled cancellation theorem.

## OPEN

Bound the joint pullback kernel in the actual range
`Y0<d<=U`, with smooth `psi`, the `mu(d) log(d)/d` coefficients, the four-packet
signs, zero-axis normalization, and prime-shell reassembly.  A finite cross-Gram
identity does not pay the strict `1/400` endpoint.

## Status

```text
CLAIM_LEVEL = PROVED_STRUCTURAL_L1_CROSS_DIVISOR_COUPLING
TPC213_ROUTE_ADVANCE = YES
TPC213_ARITHMETIC_ADVANCE = NO
TPC213_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC213_FIXED_ATOM_CREDIT = 0
TPC213_L2 = NONE
```
