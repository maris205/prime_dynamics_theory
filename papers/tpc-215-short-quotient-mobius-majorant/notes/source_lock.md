# Source Lock

## Literal parent

The source object is Equation (1.5) of
`research/tpc-big-road/bridge_b_transition_native_euler_bdh_compiler.md`:

```text
H = x^(21/32)
Q = x^(1/3)
Y0 = H/(4Q) = x^(31/96+o(1))
U = x^(133/400)
Q-shell = primes q with Q<q<=2Q
divisor band = Y0<d<=U with mu(d)^2=1
coefficient = mu(d)log(d)/d
cutoff = 0<|m|<=dq/H
```

The same source records `d<U<Q<q`, so all inverses modulo `d` are legal.

## Parent theorem

TPC-214 proves, for `h|d`,

```text
B_d((d/h)a)=B_h(a)
```

and the complete-period reduced-denominator factorization.  TPC-215 does not
alter the row, cutoff, smooth profile, coefficient, or period convention.

## Exact exponent ledger

```text
21/32 - 1/3 = 31/96
133/400 + 1/3 - 21/32 = 23/2400
H/(2Q) = 2Y0
Uq_max/H <= 2UQ/H = 2x^(23/2400+o(1))
```

## Scope locks

- The divisor family is the full squarefree V46 transition band, not an
  arbitrary subfamily.  Presence of `d=h` is essential.
- Decimal fixture ratios are observations only.
- The complete-period comparison is not a physical short-window theorem.
- The direct-sum arithmetic energy remains unbounded at the required scale.
- Prime-shell, four-packet, block, and strict `1/400` ledgers remain open.
