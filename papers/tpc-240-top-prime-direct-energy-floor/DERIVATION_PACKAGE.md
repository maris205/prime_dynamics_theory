# Derivation Package

## Frozen object

Let

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
P_top={p prime:U/2<p<=U}, Q_x={q prime:Q<q<=2Q}.
```

Fix one real `psi in C_c^infty(R)` independently of `x`, with
`0<=psi<=1`, support in `[-1,1]`, and `int psi=1`.  Put

```text
kappa_psi=int psi(t)^2 dt,
M_(p,q)=floor(pq/H),
B_(p,q)^psi(a)
 = sum_(0<|m|<=M_(p,q)) psi(Hm/(pq)) 1_(m q^(-1)=a mod p),
C_p=-log(p)/p.
```

The main object is q-split:

```text
D_top^psi=sum_p |C_p|^2 sum_q sum_((a,p)=1)|B_(p,q)^psi(a)|^2.
```

## Scale ledger

```text
U/Q=x^(-1/1200),
H/(4Q)=x^(31/96)/4,
UQ/(2H)=x^(23/2400)/2,
H/(UQ)=x^(-23/2400),
Q^2/H=x^(1/96),
log(U)/log(Q)=399/400.
```

Thus, eventually, `p<q`, `4Q<H`, and every top-shell row has lattice depth
`pq/H >= UQ/(2H) -> infinity`.

## Row compiler

For `M=floor(pq/H)`,

```text
2M <= 2pq/H <= 4pQ/H < p.
```

If two signed integers collide after multiplication by `q^(-1) mod p`, then
`p` divides their difference, while the nonzero difference has absolute value
less than `p`.  Hence the map is injective.  Each occupied residue is nonzero,
so the primitive restriction loses nothing and

```text
sum_((a,p)=1)|B_(p,q)^psi(a)|^2
 = sum_(0<|m|<=M)|psi(Hm/(pq))|^2.
```

## Endpoint-safe lattice asymptotic

Set `f=psi^2` and `T=pq/H`.  Since `f` is smooth, compactly supported in
`[-1,1]`, and vanishes at the support endpoints, the unit-mesh Riemann estimate
after the rescaling `t=m/T` gives

```text
sum_(m in Z) f(m/T)=T int f+O_psi(1).
```

The support makes the restriction `|m|<=floor(T)` exact.  Omitting `m=0`
subtracts `f(0)`, which remains inside `O_psi(1)`.  Therefore

```text
sum_((a,p)=1)|B_(p,q)^psi(a)|^2
 = kappa_psi pq/H+O_psi(1).
```

The constant depends on the fixed profile; no uniformity over the entire
profile class is asserted.

## Aggregation and error

Substitution yields

```text
D_top^psi
 = (kappa_psi/H)
     [sum_(U/2<p<=U) (log p)^2/p]
     [sum_(Q<q<=2Q) q]
   + O_psi(P sum_(U/2<p<=U)(log p)^2/p^2),
```

where `P=#Q_x`.  Since `p>U/2` and `P<=Q^(-1)sum_q q`, the error-to-main
ratio is `O_psi(H/(UQ))=O_psi(x^(-23/2400))` after the positive weighted-PNT
main terms are inserted.

Partial summation and the prime number theorem give

```text
sum_(Q<q<=2Q) q=(3/2+o(1))Q^2/log Q,
sum_(U/2<p<=U)(log p)^2/p=(log 2+o(1))log U.
```

Consequently

```text
D_top^psi
 = [(3/2)*(399/400)*kappa_psi*log 2+o_psi(1)]Q^2/H
 = [1197*kappa_psi*log 2/800+o_psi(1)]Q^2/H.
```

Finally, `2/3-21/32=1/96`.

## Optional finite-window transfer

Because `psi>=0`, q-collapsing can only increase the residue-row squared norm:

```text
sum_a |sum_q B_(p,q)^psi(a)|^2
 >= sum_q sum_a |B_(p,q)^psi(a)|^2.
```

For `z_(p,a)=C_p sum_q B_(p,q)^psi(a)`, the TPC-238 normalized lower frame
therefore gives, on `N~x` consecutive integers,

```text
N^(-1)E_I(z) >= (1/2-o(1))D_top^psi.
```

This is only an `x^(1/96)` lower bound.  It does not measure collision excess
and does not establish `x^(1/48)` sharpness.
