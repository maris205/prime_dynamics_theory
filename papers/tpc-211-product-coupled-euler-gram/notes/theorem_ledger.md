# Theorem Ledger

## PROVED

`T211.1` — For active odd primes (p>z), the lifted V46 defects

```text
Delta_S = P_S - B_S,   empty != S subseteq {p_1,...,p_s}
```

obey the exact product cocycle

```text
Delta_(S union T) = P_S Delta_T + B_T Delta_S
                         = B_S Delta_T + P_T Delta_S
```

for disjoint `S,T`, and have zero value at the zero residue and zero mean.

`T211.2` — The nonempty lifted defect family is linearly independent on
(mathbb Z/Mmathbb Z).  The Fourier coefficient at support `T` sees exactly
the divisor supersets `S superset T`; its local coefficient is nonzero because

```text
|Fhat_p(k)| = 1/(p-1),   |Ghat_p(k)| = 1/(p-1)^2
```

for nonzero local frequencies.  Hence the literal product family has full
divisor rank.

`T211.3` — For (ell_p) attached to the active primes,

```text
sum_S mu(d_S) (sum_(p in S) ell_p) Delta_S
 = -sum_p ell_p [ P_p product_(r != p)(1-P_r)
                   - B_p product_(r != p)(1-B_r) ].
```

This is an exact logarithmic Mobius derivative identity.

`T211.4` — In a complete packet with at least two active primes,

```text
sum_S mu(d_S) log(d_S) = 0.
```

Therefore the common endpoint in the product-frozen V43/V46 coefficient
bracket cancels exactly, leaving only the marked-prime derivative atoms.

`T211.5` — Since the defect Gram matrix is positive definite, for every finite
target vector (y_S) there is a common endpoint (w) with

```text
<w, Delta_S> = y_S.
```

Taking `y_S=mu(d_S)` creates a finite shared-endpoint Mobius alignment.

## NUMERICALLY_CERTIFIED

The exact certificate passes for `(5,7)`, `(5,7,11)`, and `(5,7,11,13)`:
25 profile rows, 77,875 CRT coordinates, 9 derivative rows, full rank in all
three cases, nonzero Gram determinants, and coherent-to-diagonal ratios
`3`, `7`, and `15`.

## REFUTED_SCOPED

`T211.R1` — Product coupling, finite profile rank, and a shared endpoint alone
do not imply a universal cross-divisor saving.  The Gram-dual endpoint realizes
the Mobius target on every finite complete packet.

## STOP_SCOPED

`T211.S1` — The common-endpoint alignment is a finite surrogate.  It is not a
counterexample for the actual sequence
(Lambda(u+2)-b_x^{(z)}(u)), whose values, support, interval, and reciprocal
emitter remain constrained.

## OPEN

Control the boundary between the complete divisor derivative packet and the
literal transition set (Y_0<dle U), while retaining the varying reciprocal
occupancy (A_d(r)), the prime shell, the off-diagonal signs, and the exact
zero-axis normalization.

## Status

```text
CLAIM_LEVEL = PROVED_STRUCTURAL_L1_STOP_SCOPED_PHYSICAL_COUPLING
TPC211_ROUTE_ADVANCE = YES
TPC211_ARITHMETIC_ADVANCE = NO
TPC211_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC211_FIXED_ATOM_CREDIT = 0
TPC211_L2 = NONE
```
