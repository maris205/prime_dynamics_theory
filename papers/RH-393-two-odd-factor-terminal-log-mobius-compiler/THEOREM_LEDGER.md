# RH-393 theorem ledger

## Fixed quantifiers

- `m,q`, pairwise-distinct integer shifts, phase coefficients, and the clock
  are fixed before `X->infinity`.
- `1<=omega(X)<=X`, `omega(X)->infinity`, and the window is
  `X/omega(X)<n<=X`, normalized by `log omega(X)`.
- The Möbius extension is `mu_0(t)=mu(t)` for `t>=1` and zero for `t<=0`.

## Compiler

For `alpha in {0,1,2}^m`, set `O={i:alpha_i=1}` and
`E={i:alpha_i=2}`. The theorem admits exactly `|O|<=2`. Channels with
`|O|=1,2` vanish; channels with `O=empty` converge to
`Theta_(q,r)(E)`. Hence

```text
T_X(P;omega) -> sum_(r mod q) sum_(alpha in {0,2}^m)
                c_alpha(r) Theta_(q,r)(E(alpha)).
```

The monomial count is
`D_m=2^m+m*2^(m-1)+binom(m,2)*2^(m-2)`. In dimension three it is 26 of
27, with `z1*z2*z3` as the unique excluded monomial.

## Phase-density ledger

For `B_p(E)={a_i mod p^2:i in E}` as a distinct set,
`nu_p=|B_p|`, and `tau_(p,E)(r)=#{b in B_p:b=r mod p}`,

```text
Theta_(q,r)(E)
 =q^-1 prod_(p not|q)(1-nu_p/p^2)
       prod_(p||q)(1-tau_(p,E)(r)/p)
       prod_(p^2|q) 1_(r mod p^2 notin B_p).
```

Modulo-`p^2` deduplication precedes modulo-`p` collision counting.
`Theta_(q,r)(empty)=1/q` and
`sum_(r mod q)Theta_(q,r)(E)=kappa_E`.

Finite CRT handles primes up to fixed `P`. The square-divisor union tail is
`O_(m,a)(log omega/P+1)`; the prefix error is
`O_(m,a)(N/P+sqrt(N))`.

## Odd-channel proof ledger

1. For `|O|=1`, freeze all even square masks at `P`; the remaining mask is
   fixed periodic, and RH-392 equation (19) plus terminal Abel cancellation
   applies.
2. For `|O|=2`, the forms `n-a_i,n-a_j` have nonzero determinant
   `a_i-a_j`; RH-392 Theorem 2.2 applies after the same finite mask.
3. The replacement error is bounded by `||rho||_infinity` times the tail.
4. The only permitted limit order is fixed `P`, then `X->infinity`, then
   `P->infinity`. Finite phase and monomial sums are taken afterward.

## Signed cube and 192 tables

For `f:T^3->R`,

```text
c111(f)=2^-3 sum_(epsilon in {-1,+1}^3)
        epsilon_1 epsilon_2 epsilon_3 f(epsilon).
```

The interpolant is admitted iff `c111=0`. For `g(x,y,z)=z*f(x,y)`, this is
the alternating four-corner condition `c11(f)=0`. There are six eligible
corner patterns and five free noncorner values, hence `6*2^5=192` tables.

## Squarefree landscape

- If `m<=3`, `kappa_A>=C_m=prod_p(1-m/p^2)>0`, with equality iff every
  nonzero pairwise difference is squarefree.
- If `m>=4`, `kappa_A=0` iff some `A mod p^2` covers all `p^2` residues;
  zero is attained by a modulo-four cover.
- For fixed `m>=2`, `sup_A kappa_A=6/pi^2` and is not attained. The family
  `A_(m,y)={jQ_y:0<=j<m}`, `Q_y=prod_(p<=y)p^2`, approaches it.
- A phase density may vanish even when the global density is positive.

## Executable role and firewalls

The 576-row artifact is finite regression evidence, not the CRT or analytic
proof. Its row partition is `512+27+8+12+9+8`; 32 semantic mutations are
rejected. No odd support at least three, growing data, rate, ordinary Cesàro,
pre-limit maximum, generic multishift capacity, operator, trace, or zero claim
is made. Gates A--E remain false.
