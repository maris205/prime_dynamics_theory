# Proof Package

## Claim

For a finite physical support `U`, a divisor family `D`, residue lifts `C_d`,
finite emitter rows `A_d`, and profile corrections `b_d`, the V46-style sum
has an exact common-source pullback.  On a complete period, the residue-lift
cross block is a gcd compatibility matrix and the Hermitian pullback Gram is a
frequency-intersection sum.

## Status

`PROVABLE AS STATED` for the finite operator identities.  No asymptotic V46
estimate is asserted.

## Assumptions

- `U` is a finite set of integers.
- `d,e` are positive moduli and all emitter rows are finite functions on their
  residue classes.
- `C_d f(a)=sum_{u in U, u == a mod d} f(u)`.
- `F_d g(r)=sum_(a mod d) g(a) exp(2*pi*i*r*a/d)`.
- `K_d(u)=sum_(r mod d) A_d(r) exp(2*pi*i*r*u/d)`.
- `R_d=C_d(v-b_d)` for a common source sequence `v` and a divisor-dependent
  correction `b_d`.

## Notation

Write `L=lcm(d,e)` and `g=gcd(d,e)`.  For a complete period, take
`U={0,...,L-1}`.  The bilinear pairing is
`B_d(A,R)=sum_(r mod d) A_d(r) F_d R(r)`; no conjugation is needed for the
V46 scalar identity.  The Gram calculation below uses the Hermitian pairing.

## Proof Strategy

Expand the residue aggregation first, then interchange the finite sums.  For
the lift cross block, count simultaneous congruences using the Chinese
remainder theorem.  For the emitter Gram, expand both Fourier pullbacks and
apply finite geometric-series orthogonality on one lcm period.

## Dependency Map

1. The pullback identity uses only the definitions of `C_d`, `F_d`, `R_d`, and
   `K_d`.
2. The lift identity uses the solvability criterion for two congruences modulo
   `d` and `e`, followed by the number of solutions in a complete lcm period.
3. The Gram identity uses the finite geometric sum
   `sum_(u=0)^(L-1) exp(2*pi*i*alpha*u)=L` when `alpha` is an integer and zero
   otherwise.

## Proof

### Step 1: Common-source pullback

For one divisor `d`, expand the definitions:

```text
sum_r A_d(r) F_d R_d(r)
 = sum_r A_d(r) sum_a R_d(a) exp(2*pi*i*r*a/d)
 = sum_r A_d(r) sum_a sum_(u in U, u == a mod d)
       (v(u)-b_d(u)) exp(2*pi*i*r*a/d).
```

For every term in the inner sum, `a == u (mod d)`, so the exponential equals
`exp(2*pi*i*r*u/d)`.  Interchanging the finite sums gives

```text
sum_r A_d(r) F_d R_d(r)
 = sum_(u in U) (v(u)-b_d(u)) K_d(u).
```

Summing over `d` and defining `K(u)=sum_d K_d(u)` yields

```text
sum_d sum_r A_d(r) F_d R_d(r)
 = sum_u v(u) K(u) - sum_d sum_u b_d(u) K_d(u).
```

The second term is retained; it is the exact affine profile correction and is
not absorbed into the common source term.

### Step 2: Residue-lift cross block

Let `U={0,...,L-1}`.  The `(a,b)` entry of `C_d C_e^*` is the number of
integers `u` in this period satisfying

```text
u == a (mod d),   u == b (mod e).
```

The Chinese remainder theorem says that this system is solvable exactly when
`a == b (mod g)`.  When solvable, all solutions form one residue class modulo
`L`; hence exactly one solution occurs in `{0,...,L-1}`.  Therefore

```text
(C_d C_e^*)(a,b) = 1_(a == b mod g).
```

If the support contains `M` complete lcm periods, the count is multiplied by
`M`.  This proves the gcd/lcm lift identity.

### Step 3: Pullback Gram

For the same complete period, expand

```text
K_d(u) conjugate(K_e(u))
 = sum_(r mod d) sum_(s mod e) A_d(r) conjugate(A_e(s))
   exp(2*pi*i*(r/d-s/e)*u).
```

Summing over `u=0,...,L-1` gives a finite geometric series.  The ratio is one
exactly when `r/d-s/e` is an integer, and otherwise the ratio is a nontrivial
`L`-th root of unity because `L(r/d-s/e)` is an integer.  Consequently the
sum is `L` in the first case and zero in the second.  Interchanging the finite
sums proves

```text
sum_(u mod L) K_d(u) conjugate(K_e(u))
 = L sum_(r/d == s/e mod 1) A_d(r) conjugate(A_e(s)).
```

### Step 4: Scope conclusion

The preceding identities show that the literal common-source operator has a
joint pullback kernel and can have off-diagonal divisor Gram entries.  They do
not bound the resulting kernel in the V46 asymptotic range.  Therefore the
finite structural conclusion is valid, while a physical fixed-power saving
remains an open theorem.

Therefore the claim follows. ∎

## Corrections or Missing Assumptions

No correction is needed for the finite statements.  A complete lcm period is
required only for the simplified gcd and frequency-orthogonality formulas; on
an arbitrary finite interval the exact Gram is instead weighted by the finite
exponential sum over that interval.

## Open Risks

- The finite unit-weight fixture does not model the smooth `psi` exactly.
- The `log(d)` prefactors and four-packet signs may change the sign of a
  shared-frequency cluster.
- No part of this proof supplies the V46 AP--BDH estimate, Gate B, or arithmetic
  `L2` credit.
