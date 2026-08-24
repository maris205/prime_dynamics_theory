# Proof Package

## Claim

For the exact frozen object in `DERIVATION_PACKAGE.md`, let
`kappa_psi=int_{-1}^1 psi(t)^2 dt`.  Then `1/2<=kappa_psi<=1` and, for every
fixed admissible profile,

```text
D_top^psi
 = [1197*kappa_psi*log(2)/800+o_psi(1)]Q^2/H
 = x^(1/96+o_psi(1)).
```

Equivalently, for every fixed admissible `psi` and every `epsilon>0`, there is
`x_0(psi,epsilon)` such that the relative asymptotic holds for all
`x>=x_0(psi,epsilon)`.  No class-uniform threshold is claimed.

## Status

`PROVABLE AS STATED`

## Assumptions

- `H=x^(21/32)`, `Q=x^(1/3)`, and `U=x^(133/400)`.
- `psi` is fixed, real, smooth, compactly supported in `[-1,1]`, satisfies
  `0<=psi<=1`, and has integral one.
- `p` and `q` range over primes in `(U/2,U]` and `(Q,2Q]`, respectively.
- The main energy is q-split and unsigned exactly as defined; no q-collapse or
  signed four-packet projection is substituted.

## Notation

- `M_(p,q)=floor(pq/H)` and `T_(p,q)=pq/H`.
- `B_(p,q)^psi(a)` is the fixed-`q` residue row.
- `C_p=-log(p)/p`.
- `P=# {q prime:Q<q<=2Q}`.

## Proof Strategy

First compile each signed integer row injectively into primitive residues.
Then replace its exact squared norm by an endpoint-safe lattice Riemann sum.
Finally factor the top-prime and q-shell averages and evaluate both by weighted
forms of the prime number theorem.

## Dependency Map

1. The exact row identity uses `U<Q` and `4Q<H`.
2. The row asymptotic uses the exact row identity, fixed-profile smoothness,
   and the growing depth `UQ/(2H)`.
3. The aggregate asymptotic uses the row asymptotic and two weighted PNT
   formulas.
4. The leading constant uses `log U/log Q=399/400`.
5. The exponent uses `Q^2/H=x^(1/96)`.

## Proof

### Step 1: profile norm bounds

Cauchy--Schwarz on an interval of length two gives

```text
1=(int psi)^2 <= 2 int psi^2=2 kappa_psi.
```

Thus `kappa_psi>=1/2`.  Since `0<=psi<=1`, pointwise
`psi^2<=psi`; integration gives `kappa_psi<=1`.

### Step 2: exact primitive row identity

The scale difference is `U/Q=x^(-1/1200)`, so eventually `p<q` and `q` is a
unit modulo `p`.  Also `4Q/H -> 0`.  For `M=floor(pq/H)`,

```text
2M <= 2pq/H <= 4pQ/H < p.
```

Suppose distinct admissible signed integers `m_1,m_2` have the same residue
after multiplication by `q^(-1) mod p`.  Then `p` divides `m_1-m_2`, while
`0<|m_1-m_2|<=2M<p`, a contradiction.  Moreover `0<|m|<=M<p`, so an occupied
residue cannot be zero modulo `p`.  The map is therefore injective into the
primitive residues, and squaring the row introduces no cross term:

```text
sum_((a,p)=1)|B_(p,q)^psi(a)|^2
 = sum_(0<|m|<=M)|psi(Hm/(pq))|^2.                 (1)
```

### Step 3: uniform fixed-profile lattice estimate

Set `f=psi^2` and `T=pq/H`.  For a continuously differentiable compactly
supported function, comparison on each interval `[m/T,(m+1)/T]` bounds the
difference between the mesh sum `T^(-1)sum_m f(m/T)` and `int f` by
`T^(-1)int |f'|`.  Hence

```text
sum_(m in Z)f(m/T)=T int f+O_psi(1).               (2)
```

Because `f` vanishes outside `[-1,1]` and at both endpoints, restricting (2)
to `|m|<=floor(T)` is exact.  Removing `m=0` changes the sum by `f(0)`, also
`O_psi(1)`.  Combining with (1),

```text
sum_((a,p)=1)|B_(p,q)^psi(a)|^2
 = kappa_psi pq/H+O_psi(1).                        (3)
```

The estimate is uniform over the top p-shell and q-shell for the fixed
profile because

```text
T>=UQ/(2H)=x^(23/2400)/2 -> infinity.
```

The implied constant contains fixed norms of `psi`, so this argument does not
produce an `x_0` uniform over all admissible profiles.

### Step 4: aggregate the row error

Since `|C_p|^2=(log p)^2/p^2`, summing (3) gives

```text
D_top^psi
 = (kappa_psi/H) A_U S_Q
   +O_psi(P E_U),                                  (4)
A_U=sum_(U/2<p<=U)(log p)^2/p,
S_Q=sum_(Q<q<=2Q)q,
E_U=sum_(U/2<p<=U)(log p)^2/p^2.
```

On the top shell, `E_U<=(2/U)A_U`; also `P<=S_Q/Q`.  Relative to the positive
main product in (4), the accumulated row error is therefore

```text
O_psi(H P E_U/(A_U S_Q))
 =O_psi(H/(UQ))=O_psi(x^(-23/2400)).               (5)
```

### Step 5: evaluate the weighted prime sums

Partial summation from the prime number theorem gives

```text
S_Q=(3/2+o(1))Q^2/log Q,                           (6)
A_U=(log(2)+o(1))log U.                            (7)
```

For (6), the main integral is `int_Q^(2Q) t/log(t) dt`; its leading dyadic
increment is `(3/2)Q^2/log Q`.  For (7), the main integral is
`int_(U/2)^U log(t)/t dt=log(2)log U-(log(2))^2/2`.

Substituting (6)--(7) into (4), and using (5), yields

```text
D_top^psi
 = [(3/2) kappa_psi log(2) log(U)/log(Q)+o_psi(1)]Q^2/H.
```

Since `log U/log Q=(133/400)/(1/3)=399/400`, the leading rational multiplier is
`(3/2)(399/400)=1197/800`.

### Step 6: exponent and obstruction

The final power is

```text
Q^2/H=x^(2/3-21/32)=x^(1/96).
```

The leading constant is strictly positive because `kappa_psi>=1/2`.  Thus the
exact q-split unsigned direct energy is not `o(Q^2/H)`.  In particular, no
estimate `D_top^psi<<x^(-delta)Q^2/H` with fixed `delta>0` can hold for this
object.  This completes the proof.  QED.

## Corrections or Missing Assumptions

None.  The theorem survived the independent source/proof audit unchanged after
replacing an earlier inadmissible plateau model by the literal fixed profile
and its factor `kappa_psi`.

## Open Risks

- The theorem is profilewise, not uniform over the entire profile class.
- The theorem evaluates q-split direct energy, not q-collapsed collision energy.
- Squaring `C_p` erases its sign; no signed cancellation is present.
- No statement reaches arithmetic `L2`, strict `1/400`, full Gate B, or the
  twin-prime conclusion.
