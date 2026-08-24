# TPC-239 Derivation Package

## 1. Frozen common-source kernel

Retain the exact TPC-237 scales and coefficients:

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
Q_x={q prime:Q<q<=2Q},
D_x={d:H/(4Q)<d<=U, mu(d)^2=1},
C_h=sum_(d in D_x,h|d) mu(d)log(d)/d.
```

For `M=max_j ||psi_j||_infty`, define

```text
B_(h,q)^(j)(a)
 = sum_(0<|m|<=floor(hq/H))
     psi_j(Hm/(hq)) 1_(m q^(-1)=a mod h),

K_j(n)
 = sum_(h<=U) sum_(a mod h,(a,h)=1)
     C_h (sum_(q in Q_x) B_(h,q)^(j)(a)) e(na/h).
```

The `q` weight, packet profiles, literal `C_h`, and primitive frequency index
are unchanged.

## 2. Primitive residue to reduced prime AP

Assume `2<=h<=U<Q` and fix `(a,h)=1`. Let `R_h(a)` count shell-prime rows
whose physical support contains `a`. Put

```text
M_h=floor(2hQ/H),
M_h^x={m:0<|m|<=M_h,(m,h)=1}.
```

If a physical row indexed by `q` contains `a`, then some nonzero `m` satisfies

```text
|m|<=floor(hq/H)<=M_h,
m q^(-1)=a (mod h).
```

Because `q>Q>h`, the prime `q` is a unit modulo `h`. Hence

```text
(m,h)=(aq,h)=1,
q=a^(-1)m (mod h).
```

Thus every actual row enters one of the reduced AP rows indexed by
`m in M_h^x`. Dropping only the `q`-dependent cutoff yields

```text
R_h(a)
 <= sum_(m in M_h^x)
      [pi(2Q;h,a^(-1)m)-pi(Q;h,a^(-1)m)].       (2.1)
```

TPC-236 internal row injectivity ensures that one physical `q`-row has no
hidden duplicate multiplier. Equation (2.1) is deliberately a sum of pair
counts: no disjointness across `m` is needed, and the sum is allowed to
overcount while also ignoring the physical cutoff.

## 3. The factor-16 envelope

For every reduced class `b mod h`, the standard Brun--Titchmarsh estimate gives

```text
pi(2Q;h,b) <= 4Q/[phi(h) log(2Q/h)].             (3.1)
```

The shell difference in (2.1) is at most the left side of (3.1). Also,

```text
#M_h^x <= 2M_h <= 4hQ/H.                         (3.2)
```

Multiplying (3.1) and (3.2) proves

```text
R_h(a)
 <= 16 (Q^2/H) (h/phi(h))/log(2Q/h).             (3.3)
```

The constant `16` is not an unspecified implied constant: it is `4*4` from
the displayed two estimates.

For `h=1`, the physical cutoff is `floor(q/H)=0` for every `q<=2Q<H`, so the
row is empty. No logarithmic AP expression is needed in that branch.

## 4. V59 row scale

The exact gap between the shell and modulus scales is

```text
Q/U=x^(1/3-133/400)=x^(1/1200).
```

For `h<=U`,

```text
log(2Q/h) >= log(2Q/U)
            = log 2 + (1/1200)log x
            >> log x,
h/phi(h) << loglog(3h) << loglog x.
```

Since

```text
Q^2/H=x^(2/3-21/32)=x^(1/96),
```

equation (3.3) gives

```text
max_(active h<=U,(a,h)=1) R_h(a)
 << x^(1/96) loglog x/log x.                     (4.1)
```

## 5. Exact substitution into TPC-237

TPC-237 proves, before the reduced-frequency large sieve,

```text
sum_(n in I) sum_j |K_j(n)|^2
 <= (N-1+U^2) R_max
    sum_(h,a,j,q) |C_h B_(h,q)^(j)(a)|^2,         (5.1)
```

and independently

```text
sum_(h,a,j,q) |C_h B_(h,q)^(j)(a)|^2
 << J M^2 (Q^2/H)(log x)^5.                       (5.2)
```

Insert (4.1) for `R_max` in (5.1), retain (5.2), and take
`I=I_x=(x/2,x] intersect Z`, `N=#I_x`. Since

```text
U^2/N=x^(2*(133/400)-1+o(1))=x^(-67/200+o(1)),
```

the normalized result is

```text
N^(-1) sum_(n in I_x) sum_(j=1)^J |K_j(n)|^2
 << J M^2 x^(1/48) (log x)^4 loglog x.            (5.3)
```

The exact fixed-power ledger is

```text
row density:          1/96,
direct energy:        1/96,
normalized trace:     1/96+1/96=1/48,
unnormalized trace:   1+1/48=49/48.
```

## 6. Comparison with TPC-237

TPC-237 had `x^(1/48)(log x)^5`. Equation (5.3) has
`x^(1/48)(log x)^4 loglog x`. The ratio of old to new losses is

```text
log x/loglog x.
```

This is genuine logarithmic progress. The fixed-power exponent is unchanged,
so it is not a fixed-power saving.

## 7. Finite fixture boundary

The certificate uses `(Q,H,h)=(101,8830,82)`, for which `M_h=1`. It enumerates
the 20 shell primes and all 40 primitive buckets. The buckets `a=3` and `a=79`
each have actual row multiplicity three. Every bucket satisfies the finite
numerical ordering

```text
actual R_h(a) <= AP census <= factor-16 real RHS.
```

This enumeration tests implementations and mutations only. It is not evidence
for the uniform Brun--Titchmarsh theorem or the asymptotic packet estimate.
