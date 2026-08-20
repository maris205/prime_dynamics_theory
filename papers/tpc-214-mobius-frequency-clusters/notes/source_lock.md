# Source Lock

## Primary repository sources

- `TPC_HANDOFF.md`, current TPC-213 section and V46 definition.
- `research/tpc-big-road/TPC_ROUTE_MAP.md`, V66 position and next theorem.
- `papers/tpc-213-physical-profile-cross-gram/`, exact common-source Gram.

## Locked physical object

```text
H = x^(21/32)
Q = x^(1/3)
Y0 = x^(31/96)
U = x^(133/400)
B_d(r) = sum_(q,m) psi(Hm/(dq)) 1_(m qbar = r mod d)
c_d = mu(d) log(d)/d
```

The proof uses a common `Q`, common `H`, and the literal V46 cutoff
`0<|m|<=dq/H`.  No source theorem is used to claim an asymptotic saving.

## Modeling choice for the finite certificate

The finite certificate uses `psi(t)=(1+t^2)^(-2)`, which is smooth, even, and
Schwartz.  It is used only to make the finite rows exact rational numbers.
