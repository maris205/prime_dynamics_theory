# Theorem Ledger

## PROVED

`T212.1` — For a squarefree prime set and selected nonempty subset family
`A`, the endpoint coefficient of the `mu(d) log(d)` packet is

```text
sum_(S in A) mu(d_S) log(d_S)
 = sum_p eta_p(A) log(p),
eta_p(A) = sum_(S in A, p in S) (-1)^|S|.
```

The full Boolean packet has zero incidence for at least two active primes.

`T212.2` — For arbitrary finite profiles and a common endpoint, the selected
packet equals the complete packet minus the missing-subset packet, separately
in every `log(p)` coefficient.  The cut boundary is therefore an exact
operator term, not a notational remainder.

`T212.3` — For the reciprocal map `(q,m) -> m q^{-1} mod d`, the squared
occupancy norm is exactly the number of ordered pairs satisfying
`d | m1*q2-m2*q1`.

`T212.4` — In the natural direct sum of residue spaces over a finite divisor
family, the emitter Gram is diagonal with entries `||A_d||_2^2`.  If all rows
are nonzero, its rank is the number of divisors.

`T212.5` — Any finite family of nonzero emitter rows admits a residual family
whose emitter contributions have the same prescribed sign and magnitude.
For the unit-weight fixture, the coherent-to-diagonal ratio is exactly the
number of divisor blocks.

## NUMERICALLY_CERTIFIED

The exact certificate passes four boundary cuts covering 5,810 CRT/profile
coordinates and three emitter families covering nine divisor rows.  It checks
the `t=35`, `5<d<=35` endpoint leak, all boundary decompositions, every
reciprocal collision identity, direct-sum rank, and alignment ratios `2`, `4`,
and `3`.

## MODELING_CHOICE

The emitter fixture sets the finite reciprocal test weight to `psi=1`.  This
keeps the collision algebra exact and isolates the occupancy map.  It is not a
source-backed replacement for the smooth physical `psi`.

## REFUTED_SCOPED

`T212.R1` — A divisor cut and reciprocal occupancy map, without a theorem
relating the literal residual profiles across divisors, do not imply a
universal cross-divisor saving.

## OPEN

Control the literal physical boundary after `A_d(r)` is paired with the
coupled profile family, retaining the prime shell, smooth weights, four-packet
signs, zero-axis normalization, and block reassembly.

## Status

```text
CLAIM_LEVEL = PROVED_STRUCTURAL_L1_STOP_SCOPED_BOUNDARY_EMITTER
TPC212_ROUTE_ADVANCE = YES
TPC212_ARITHMETIC_ADVANCE = NO
TPC212_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID
TPC212_FIXED_ATOM_CREDIT = 0
TPC212_L2 = NONE
```
