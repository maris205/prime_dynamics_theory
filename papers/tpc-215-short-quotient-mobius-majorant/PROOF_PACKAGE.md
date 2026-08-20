# TPC-215 Proof Package

## Frozen object

```text
D_x = {d in Z : Y0<d<=U, mu(d)^2=1}
c_d = mu(d)log(d)/d
B_d(r) = sum_q sum_(0<|m|<=dq/H)
         psi(Hm/(dq)) 1_(m q^(-1)=r mod d)
C_h = sum_(d in D_x, h|d)c_d
```

The V46 inequalities `d<U<Q<q` make every inverse legal.  TPC-214 supplies
the exact dilation covariance and complete-period cluster factorization.

## Lemma 1: activation floor

If `B_h` is nonzero, one summand has a nonzero integer `m`, so

```text
1 <= |m| <= hq/H
```

for some `q<=q_max`.  Therefore `h>=H/q_max>=H/(2Q)=2Y0`.
As `h` divides a squarefree `d<=U`, it is squarefree and `h<=U`; hence
`h in D_x`.  In particular the `d=h` diagonal term is present.

## Lemma 2: short-quotient normal form

Write `d=hk`.  Squarefreeness gives `(h,k)=1` and
`mu(hk)=mu(h)mu(k)`, whence

```text
C_h = mu(h)/h sum_(Y0/h<k<=U/h, (k,h)=1)
      mu(k)(log h+log k)/k.
```

For active `h`,

```text
k<=U/h<=Uq_max/H<=2UQ/H=2x^(23/2400+o(1)).
```

The exponent identity is exact:

```text
133/400 + 1/3 - 21/32 = 23/2400.
```

## Lemma 3: coefficient comparison

Put

```text
D_h = sum_(d in D_x, h|d)|c_d|^2.
```

Because `d=h` is present,

```text
D_h >= (log h/h)^2.
```

Also

```text
|C_h| <= (log U/h) Harmonic(floor(U/h)).
```

Consequently

```text
|C_h|^2 <= [log U/log h]^2 Harmonic(floor(U/h))^2 D_h.
```

Monotonicity and `h>=H/q_max` give the uniform factor

```text
A_x = [log U/log(H/q_max)]^2
      Harmonic(floor(Uq_max/H))^2.
```

Since `q_max<=2Q` and `UQ/H=x^(23/2400+o(1))`, this is
`O((log x)^2)=x^(o(1))`.

## Lemma 4: exact row decomposition

Define

```text
N_h = sum_(a mod h, gcd(a,h)=1)|B_h(a)|^2.
```

Every residue `r mod d` has one reduced fraction `r/d=a/h`; TPC-214
dilation covariance gives `B_d(r)=B_h(a)`.  The disjoint partition by reduced
denominator therefore yields

```text
sum_(r mod d)|B_d(r)|^2 = sum_(h|d)N_h.
```

The source-locked additive zero row is absent because `q_max<H`.

## Theorem: complete-period no-power-loss majorant

TPC-214 and Lemmas 3--4 give

```text
E_cluster/L = sum_h N_h|C_h|^2
 <= A_x sum_h N_hD_h
  = A_x sum_d |c_d|^2 sum_(r mod d)|B_d(r)|^2
  = A_x E_direct/L.
```

Thus `E_cluster<=x^(o(1))E_direct`, with the explicit
`O((log x)^2)` factor above.

## Obstruction

If `U/2<h<=U`, any distinct multiple of `h` is at least `2h>U`.  Therefore
the full band contains only `d=h` above that reduced denominator:

```text
C_h=c_h,  D_h=|c_h|^2.
```

The coefficient-level ratio is exactly one on every active top-shell row.
This refutes only a uniform rowwise cluster-algebra power saving.  It does not
refute a global saving that uses arithmetic row norms, finite-window
orthogonality, or prime-shell coupling.

## Trust boundary

The theorem is a deterministic structural `L1` comparison.  It supplies no
bound for `E_direct`, no physical finite-window off-frequency Gram estimate,
no prime-shell or four-packet reassembly, no arithmetic `L2`, and no
twin-prime theorem.
