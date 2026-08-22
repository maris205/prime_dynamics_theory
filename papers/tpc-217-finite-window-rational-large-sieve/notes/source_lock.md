# Source Lock

## Literal parent

TPC-217 uses the TPC-216/TPC-215 V46 object without changing its scales:

```text
H=x^(21/32), Q=x^(1/3), Y0=H/(4Q), U=x^(133/400)
Q<q<=2Q, Y0<d<=U, mu(d)^2=1, c_d=mu(d)log(d)/d.
```

The reciprocal emitter remains

```text
B_d(r)=sum_(q,m) psi(Hm/(dq)) 1_(m q^(-1)=r mod d),
0<|m|<=floor(dq/H).
```

## Physical interval

```text
I_x=(x/2,x] intersect Z, N=|I_x|.
```

The common-source kernel is

```text
K(n)=sum_d c_d sum_(r mod d)B_d(r)e(nr/d).
```

## Exact inherited interfaces

- TPC-214: `B_d((d/h)a)=B_h(a)` and complete-period reduced-frequency
  regrouping.
- TPC-215: `S_cluster<=A_x E_direct/L` with `A_x=O((log x)^2)`.
- TPC-216: `E_direct/L<<_psi(Q^3/H)(log U)^3`.

## New input

The only new analytic input is the standard additive large-sieve inequality for
frequencies separated modulo one by `delta`:

```text
sum_(n in I)|sum_j z_j e(n alpha_j)|^2
 <= (N-1+delta^(-1))sum_j|z_j|^2.
```

The reduced fractions of denominator at most `U` have `delta>=U^(-2)`.

## Exponent ledger

```text
Q^3/H = x^(11/32)
U^2/x = x^(-67/200)
N ~ x
cluster majorant = O((log x)^2)
direct envelope = O(x^(11/32)(log x)^3)
finite-window normalized envelope = O(x^(11/32)(log x)^5)
finite-window unnormalized exponent = 43/32
```

## Claim boundary

The new result controls the finite-window off-frequency Gram for the common
source cluster kernel.  It does not claim prime cancellation, Möbius
cancellation, arithmetic `L2`, full Gate B, or the twin-prime endpoint.
