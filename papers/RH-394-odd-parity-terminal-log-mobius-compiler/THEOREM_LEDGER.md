# RH-394 theorem ledger

## Fixed quantifiers

- `m,q`, pairwise-distinct integer shifts, phase coefficients, and the terminal
  clock are fixed before `X->infinity`.
- `1<=omega(X)<=X`, `omega(X)->infinity`, and the strict window is
  `X/omega(X)<n<=X`, normalized by `log omega(X)`.
- `mu_0(t)=mu(t)` for integers `t>=1` and is zero for `t<=0`.

## Odd-parity compiler

For `alpha in {0,1,2}^m`, set `O={i:alpha_i=1}` and
`E={i:alpha_i=2}`. The admitted odd-support sizes are exactly zero, two,
and every positive odd integer. Every admitted nonempty odd channel vanishes;
the all-even channels satisfy

```text
T_X(P;omega) -> sum_(r mod q) sum_(alpha in {0,2}^m)
                c_alpha(r) Theta_(q,r)(E(alpha)).
```

The dimension is
`D'_m=2^m+binom(m,2)2^(m-2)+(3^m-1)/2`, with the two-odd term absent
for `m<2`. Thus `D'_3=27` and `D'_4=80` of 81.

## Phase-density and exact-support ledger

For `B_p(E)={a_i mod p^2:i in E}` as a distinct set,
`nu_p=|B_p|`, and `tau_(p,E)(r)=#{b in B_p:b=r mod p}` after
modulo-`p^2` deduplication,

```text
Theta_(q,r)(E)
 =q^-1 prod_(p not|q)(1-nu_p/p^2)
       prod_(p||q)(1-tau_(p,E)(r)/p)
       prod_(p^2|q) 1_(r mod p^2 notin B_p).
```

`Theta_(q,r)(empty)=1/q` and
`sum_(r mod q)Theta_(q,r)(E)=prod_p(1-nu_p/p^2)`.
Finite CRT handles primes through fixed `P`; the union tail is
`O_(m,a)(log omega/P+1)`. The order is `P` fixed, then `X->infinity`,
then `P->infinity`.

Exact support has density

```text
Pi_(q,r)(U)=sum_(W subset [m]\U)(-1)^|W| Theta_(q,r)(U union W).
```

It is nonnegative and has phase mass `sum_U Pi_(q,r)(U)=1/q`.

## Analytic proof ledger

1. Odd support zero is the local finite-CRT and tail calculation.
2. Odd support two is the frozen RH-393 compiler, whose two-form input is
   RH-392 Theorem 2.2.
3. Positive odd support uses Tao--Teräväinen Corollary 1.8 for positive
   exponents in `{1,2}` whose total exponent is odd.
4. In a phase `n=qt+r`, the forms have fixed slope `q`, distinct intercepts,
   and determinants `q(a_i-a_j)!=0`. Remark 1.5 and Theorem A.1 supply the
   affine extension.
5. The bridge uses `1/(qt+r)=1/(qt)+O(t^-2)`, an `O(1)` endpoint error,
   the transformed terminal clock, harmonic-denominator ratio one, and the
   sequential criterion for every admissible clock.

No source in this ledger is used to claim an even correlation of order at
least four.

## Intrinsic table ledger

For disjoint odd/even supports `O,E`, let `c_(O,E)` be the interpolation
coefficient. On Boolean support stratum `S`,

```text
hat h_S(O)=sum_(E subset S\O)c_(O,E),
c_(O,E)=sum_(U subset E)(-1)^(|E|-|U|)hat h_(O union U)(O).
```

Therefore a table is eligible iff the antipodally even part of every stratum
has Fourier degree at most two. The limit is the `Pi`-weighted average of the
stratum sign averages.

For three shifts every one of the 27 monomials is admitted, so all ternary
tables have the exact law. For four shifts the only missing coefficient is

```text
c1111=2^-4 sum_(epsilon in {-1,+1}^4)
       epsilon_1 epsilon_2 epsilon_3 epsilon_4 f(epsilon).
```

A sign table has `c1111=0` exactly when the transformed corner signs split
eight positive and eight negative, giving `binom(16,8)*2^65` tables per phase.
Failure is outside the theorem only.

## Distinguished-current ledger

For `g(x,z)=z*f(x)`, eligibility is equivalent to Fourier degree at most one
for every input-stratum odd part. A linear function with values in
`{-1,0,1}` is exactly

```text
0,  +/-x_i,  or  (+/-x_i+/-x_j)/2.
```

Hence `M_0=2`, `M_1=4`, and for `k>=2`,

```text
M_k=2^(2^(k-1))+2k+4*binom(k,2)*2^(2^(k-2)),
B_d=prod_k M_k^binom(d,k).
```

Every one of the `B_d^q` phase families cancels. In particular,
`B_2=512` and `B_3=36,700,160`.

## Executable role and firewalls

The 658-row certificate is finite regression evidence, not the analytic
proof. Its partition is `81+17+512+8+8+8+8+8+8`; 32 core and 32 result
semantic mutations are rejected. No even odd-support size at least four,
unrestricted `m>=4` table law, growing data, rate, Cesàro, prelimit maximum,
generic graph capacity, operator, trace, zero, RH, or Gate claim is made.
Gates A--E remain false.
