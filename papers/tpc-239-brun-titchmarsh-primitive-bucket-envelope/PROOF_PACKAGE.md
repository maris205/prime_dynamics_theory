# TPC-239 Proof Package

## Theorem 1: source-backed primitive-bucket envelope

Assume `4Q<H` and `2<=h<=U<Q`. Let `(a,h)=1`, let `R_h(a)` be the number of
prime rows `Q<q<=2Q` whose physical support

```text
S_(h,q)={m q^(-1) mod h:0<|m|<=floor(hq/H)}
```

contains `a`, and put

```text
M_h=floor(2hQ/H),
M_h^x={m:0<|m|<=M_h,(m,h)=1}.
```

Then

```text
R_h(a)
 <= sum_(m in M_h^x)
      [pi(2Q;h,a^(-1)m)-pi(Q;h,a^(-1)m)]
 <= 16 (Q^2/H) (h/phi(h))/log(2Q/h).              (T1)
```

For `h=1`, the row is empty.

### Proof

Fix an actual row `q`. By membership, there is a nonzero multiplier `m` with

```text
|m|<=floor(hq/H)<=floor(2hQ/H)=M_h,
m q^(-1)=a (mod h).
```

Since `q>Q>h`, one has `(q,h)=1`. Multiplying the congruence by `q` gives
`m=aq (mod h)`, whence `(m,h)=1`. Multiplying instead by `a^(-1)` gives

```text
q=a^(-1)m (mod h).
```

Thus every actual row contributes to the displayed AP pair census. TPC-236
internal row injectivity follows from

```text
|m-m'|<=2 floor(hq/H)<=4hQ/H<h;
```

there is no duplicate multiplier inside one `q`-row. We do not require AP rows
for different `m` to be disjoint, so the pair census is a valid upper bound
even if it overcounts across multipliers. Its only support enlargement is the
removal of the `q`-dependent cutoff.

Every class `a^(-1)m mod h` is reduced because both factors are units. The
standard Brun--Titchmarsh inequality therefore gives

```text
pi(2Q;h,a^(-1)m)
 <= 4Q/[phi(h) log(2Q/h)].                         (T2)
```

Moreover,

```text
#M_h^x<=2M_h<=4hQ/H.                               (T3)
```

Bound each shell difference by (T2), sum over `m`, and apply (T3). The product
of the constants `4` and `4` is `16`, proving (T1).

If `h=1`, then `floor(q/H)=0` for every `q<=2Q<H`; hence every physical support
is empty. This proves the separate branch. ∎

## Corollary 2: V59 maximum row

At

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
```

one has

```text
max_(active h<=U,(a,h)=1) R_h(a)
 << x^(1/96) loglog x/log x.                       (T4)
```

### Proof

The `h=1` row is empty. For `2<=h<=U`, Theorem 1 applies. The exact scale gap

```text
Q/U=x^(1/1200)
```

implies

```text
log(2Q/h)>=log(2Q/U)=log 2+(1/1200)log x>>log x.
```

The standard maximal-order estimate gives
`h/phi(h)<<loglog(3h)<<loglog x`. Finally,
`Q^2/H=x^(1/96)`. Substitute these three bounds into (T1). ∎

## Theorem 3: finite-window common-source packet trace

Retain exactly the TPC-237 kernel

```text
K_j(n)
 = sum_(h<=U) sum_((a,h)=1)
     C_h (sum_(q in Q_x) B_(h,q)^(j)(a)) e(na/h)
```

with `M=max_j ||psi_j||_infty`. For
`I_x=(x/2,x] intersect Z` and `N=#I_x`, one has

```text
N^(-1) sum_(n in I_x) sum_(j=1)^J |K_j(n)|^2
 << J M^2 x^(1/48) (log x)^4 loglog x.             (T5)
```

The leading unnormalized fixed-power exponent is `49/48+o(1)`.

### Proof

TPC-237 first applies coordinatewise Cauchy--Schwarz to the prime rows and then
the reduced-frequency large sieve. With a generic primitive-row bound `R_max`,
its exact composition is

```text
sum_(n in I_x) sum_j |K_j(n)|^2
 <= (N-1+U^2) R_max
    sum_(h,a,j,q) |C_h B_(h,q)^(j)(a)|^2.          (T6)
```

Its direct coefficient-energy estimate, unchanged here, is

```text
sum_(h,a,j,q) |C_h B_(h,q)^(j)(a)|^2
 << J M^2 (Q^2/H)(log x)^5.                        (T7)
```

Use Corollary 2 in (T6), then use (T7). Since `N` is comparable to `x` and

```text
U^2/N=x^(-67/200+o(1)),
```

division by `N` gives

```text
J M^2 [x^(1/96)loglog x/log x]
        [x^(1/96)(log x)^5]
 = J M^2 x^(1/48)(log x)^4 loglog x.
```

Multiplication by `N=x^(1+o(1))` changes the leading fixed-power exponent to
`1+1/48=49/48`. ∎

## Exact Fraction ledger

```text
1/3-133/400                  = 1/1200,
2/3-21/32                    = 1/96,
1/96+1/96                    = 1/48,
1+1/48                       = 49/48,
2*(133/400)-1                = -67/200.
```

The producer and independent checker reconstruct these values with Python
`Fraction`; no floating-point exponent arithmetic is accepted.

## Claim boundary

Theorem 3 controls the unsigned trace `sum_j |K_j|^2`. It does not identify an
actual signed four-packet projection. Literal `C_h` remains present, but (T7)
uses `|C_h|^2` and an absolute harmonic majorant. The proof supplies no signed
`C_h` cancellation, arithmetic `L2`, fixed-atom credit, strict `1/400`, full
Gate B, or twin-prime result. The exponent `1/48` is not claimed to be sharp.
