# TPC-237 derivation package

## 1. Frozen primitive-frequency kernel

Let

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
Q_x={q prime:Q<q<=2Q},
D_x={d:H/(4Q)<d<=U, mu(d)^2=1},
C_h=sum_(d in D_x,h|d) mu(d)log(d)/d.
```

For fixed packet profiles `psi_j`, with `M=max_j ||psi_j||_infty`, define

```text
B_(h,q)^(j)(a)
 = sum_(0<|m|<=floor(hq/H))
     psi_j(Hm/(hq)) 1_(m q^(-1)=a mod h),

K_j(n)
 = sum_(h<=U) sum_(a mod h,(a,h)=1)
     C_h (sum_(q in Q_x) B_(h,q)^(j)(a)) e(na/h).
```

The `q` weight is one.  There is no packet-dependent transform, row-dependent
normalization, or replacement of `C_h`.  The frequency index is primitive.

## 2. Collision compression before the large sieve

TPC-236 bounds the number of physical rows meeting a residue `a mod h` by

```text
R_h(a) <= 4Q^2/H + 4hQ/(gH),  g=gcd(a,h).
```

The kernel keeps only primitive residues, hence `g=1`.  Since `h<=U`,

```text
R_h(a) <= 4Q^2/H + 4UQ/H =: R_*.
```

For every `(h,a,j)`, coordinatewise Cauchy gives

```text
|sum_q B_(h,q)^(j)(a)|^2
 <= R_* sum_q |B_(h,q)^(j)(a)|^2.
```

Multiplication by literal `|C_h|^2` and summation preserve the inequality.  This
is where the former coarse `P=#Q_x` collapse is replaced by physical incidence.

## 3. Direct coefficient energy

For fixed `(h,q,j)`, `4Q<H` makes the multiplier map injective, so

```text
sum_((a,h)=1) |B_(h,q)^(j)(a)|^2 <= 2M^2 hq/H.
```

Only rows with `h>=H/(2Q)` can be active.  On these rows,

```text
|C_h| << (log x)^2/h,
sum_h h|C_h|^2 << (log x)^5.
```

Using `#Q_x<=2Q` and `q<=2Q` yields

```text
sum_(h,a,j,q) |C_h B_(h,q)^(j)(a)|^2
 << J M^2 (Q^2/H)(log x)^5.
```

## 4. Finite-window attachment

Distinct primitive fractions `a/h` with `h<=U` have circular spacing at least
`U^(-2)`.  The additive large sieve on a consecutive interval `I` of `N`
integers gives

```text
sum_(n in I) sum_j |K_j(n)|^2
 <= (N-1+U^2) R_*
    sum_(h,a,j,q) |C_h B_(h,q)^(j)(a)|^2.
```

Thus

```text
N^(-1) sum_(n in I) sum_j |K_j(n)|^2
 << JM^2(1+U^2/N)
    [(Q^2/H)^2 + (UQ/H)(Q^2/H)](log x)^5.
```

## 5. Exact exponent ledger

```text
Q^2/H                     = x^(1/96),
UQ/H                      = x^(23/2400),
(Q^2/H)^2                 = x^(1/48),
(UQ/H)(Q^2/H)             = x^(1/50),
U^2/x                     = x^(-67/200),
x * x^(1/48)              = x^(49/48).
```

The normalized main exponent is `1/48`; the leading unnormalized exponent is
`49/48+o(1)`.

## 6. Finite reproduction fixture

The exact floor fixture

```text
(Q,H,U,h)=(101,8830,99,82)
```

satisfies `H=floor(Q^(63/32))`, `U=floor(Q^(399/400))`, and `h` is squarefree.
The source band contains `d=82`, so the rational marked-divisor reproduction weight
is `C_82^(rat)=mu(82)/82=1/82`.  The shell primes `109,137,191` all have support
`{3,79}`.  The constant packet has coherent-to-direct ratio `3`; adding the signed
multiplier packet gives packet-trace ratio `5/3`.  Over one complete `82`-point
window, the normalized trace is exactly `5/1681`.  This finite calculation reproduces
the algebra only; replacing `log d` by `1` is not an asymptotic source substitution.
