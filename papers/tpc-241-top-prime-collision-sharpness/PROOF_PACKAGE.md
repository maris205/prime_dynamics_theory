# TPC-241 proof package

## Theorem object

Let

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
I_x=(x/2,x] intersect Z, N=#I_x.
```

The literal source coefficient is

```text
D_x={d:H/(4Q)<d<=U, mu(d)^2=1},
C_h=sum_(d in D_x,h|d)mu(d)log(d)/d.
```

Fix a real `psi in C_c^infinity(R)`, independently of `x`, with
`0<=psi<=1`, support in `[-1,1]`, and integral one.  For primitive residues,

```text
B_(h,q)^psi(a)
 =sum_(0<|m|<=floor(hq/H))
   psi(Hm/(hq)) 1_(m q^(-1)=a mod h),

K_psi(n)=sum_(h<=U)sum_((a,h)=1)
 C_h(sum_(Q<q<=2Q)B_(h,q)^psi(a))e(na/h).
```

For top primes `U/2<p<=U`, eventually `p>H/(4Q)`, and the only active
multiple of `p` not exceeding `U` is `d=p`.  Thus
`C_p=mu(p)log(p)/p=-log(p)/p`.  Define

```text
B_p^psi(a)=sum_(Q<q<=2Q)B_(p,q)^psi(a),
S_p=sum_((a,p)=1)B_p^psi(a),
E_top^psi=sum_(U/2<p<=U)|C_p|^2
            sum_((a,p)=1)|B_p^psi(a)|^2.
```

## Lemma 1: primitive support

Eventually `p<q`, `4Q<H`, and
`2floor(pq/H)<p`.  Every active nonzero multiplier therefore satisfies
`0<|m|<p`; because `p` is prime, its residue after multiplication by
`q^(-1)` is primitive.  Summing over all primitive residues counts every
active multiplier exactly once inside each fixed q-row.

## Lemma 2: uniform row mass

For `T=pq/H`, the fixed-profile Riemann estimate is

```text
sum_(0<|m|<=floor(T))psi(m/T)=T+O_psi(1).
```

The integral over both signs is already one.  The omitted `m=0` and endpoint
rounding are absorbed by `O_psi(1)`.  Since
`T>=(1/2)x^(23/2400)`, this estimate is uniform on the top p- and q-shells.
Hence

```text
S_p=(p/H)sum_(Q<q<=2Q)q+O_psi(pi(2Q)-pi(Q))
   =(3/2+o_psi(1))pQ^2/(H log Q),
```

uniformly for `U/2<p<=U`.  The relative lattice error is
`O_psi(H/(pQ))=O_psi(x^(-23/2400))`.

## Lemma 3: post-collapse residue Cauchy

There are exactly `p-1` primitive residues modulo `p`.  Therefore

```text
sum_((a,p)=1)|B_p^psi(a)|^2 >= |S_p|^2/(p-1).
```

The placement is essential: q labels have already been collapsed.  Applying
Cauchy separately to each q-row would recover only the TPC-240 direct floor.

## Theorem 1: top-prime coefficient liminf

Multiply Lemma 3 by `|C_p|^2=(log p)^2/p^2`, sum over top primes, and use

```text
sum_(U/2<p<=U)(log p)^2/p=(log(2)+o(1))log U.
```

Then

```text
E_top^psi
 >=(9log(2)/4+o_psi(1))(Q^4/H^2)log U/(log Q)^2.
```

The exact exponent and constant ledger is

```text
Q^4/H^2=x^(1/48),
log U/log Q=399/400,
1/log Q=3/log x,
(9/4)(399/400)3=10773/1600.
```

Thus

```text
liminf_(x->infinity)[(log x)/x^(1/48)]E_top^psi
 >=10773log(2)/1600.
```

## Theorem 2: legal finite-window transfer

Apply the TPC-238 lower frame first to the complete primitive-frequency
coefficient vector defining `K_psi`:

```text
N^(-1)sum_(n in I_x)|K_psi(n)|^2
 >=[1/2-pi^2U^4/(6N^2)]_+
   sum_(h,a)|C_h sum_q B_(h,q)^psi(a)|^2.
```

Only after this inequality is established may the nonnegative coefficient norm
be restricted to the top-prime terms.  No physical-window cross term is
deleted.  Since `U^4/N^2=x^(-67/100+o(1))`,

```text
liminf_(x->infinity)[(log x)/x^(1/48)]
 [N^(-1)sum_(n in I_x)|K_psi(n)|^2]
 >=10773log(2)/3200.
```

## Corollary: fixed-power sharpness

Fix `delta>0` and real `A`.  If an eventual upper estimate at scale
`x^(1/48-delta)(log x)^A` held, division by the proved lower scale would force
`x^delta/(log x)^(A+1)` to remain bounded.  It tends to infinity.  Hence every
such estimate is false for every fixed admissible profile.

## Scope

The result concerns the exact unsigned common-profile kernel.  It does not use
the sign of `C_p` after the absolute square, does not project through the four
literal polarized packets, and proves no arithmetic `L2`, strict `1/400`, or
twin-prime result.
