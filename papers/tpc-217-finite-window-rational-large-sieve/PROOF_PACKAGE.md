# Proof Package

## Claim

Let

```text
H=x^(21/32), Q=x^(1/3), Y0=H/(4Q), U=x^(133/400),
Q_x={q prime: Q<q<=2Q},
D_x={d: Y0<d<=U, mu(d)^2=1},
c_d=mu(d)log(d)/d.
```

For a bounded profile `psi`, define

```text
B_d(r)=sum_(q in Q_x) sum_(0<|m|<=floor(dq/H))
        psi(Hm/(dq)) 1_(m q^(-1)=r mod d).
```

Let `I_x=(x/2,x] intersect Z`, `N=|I_x|`, and

```text
K(n)=sum_(d in D_x)c_d sum_(r mod d)B_d(r)e(nr/d).
```

Then, for sufficiently large `x`,

```text
sum_(n in I_x)|K(n)|^2
  <<_psi (N+U^2) x^(11/32)(log x)^5,
```

and therefore

```text
N^(-1) sum_(n in I_x)|K(n)|^2
  <<_psi x^(11/32)(log x)^5.
```

The unnormalized exponent is `43/32+o(1)` because `N asymp x` and
`U^2/x=x^(-67/200)`.

## Status

`PROVABLE AS STATED` for the complete common-source cluster kernel `K`.  The
claim is a structural finite-window theorem and is not the final arithmetic
Gate-B estimate.

## Assumptions

- `M_psi=sup_t|psi(t)|<infinity`.
- `x` is sufficiently large that `4Q<H`, `U<Q`, and `Q>=1`.
- The source divisor family is the full squarefree band `D_x`.
- The standard additive large-sieve inequality is available for consecutive
  integer intervals and frequencies separated modulo one by `delta`.
- TPC-215's exact cluster-to-direct majorant and TPC-216's direct-sum envelope
  are used as established upstream lemmas.

## Notation

For `h|d`, define

```text
C_h=sum_(d in D_x,h|d)c_d,
N_h=sum_(a mod h,(a,h)=1)|B_h(a)|^2.
```

The `h=1` term is interpreted with `a=0`; it vanishes because `q_max<H`.

## Proof Strategy

The proof has four independent parts: exact regrouping, rational-frequency
spacing, the finite-interval additive large sieve, and the inherited coefficient
energy majorant.  No cancellation is inferred from the signs of `mu` or from
the prime shell.

## Dependency Map

1. The source exponents imply `4Q<H` and `U<Q`.
2. These inequalities give the exact dilation identity for the literal integer
   cutoff and eliminate the additive zero axis.
3. Reduced fractions with denominators at most `U` have circular spacing at
   least `U^(-2)`.
4. The additive large sieve bounds the physical interval by `(N+U^2)` times
   the reduced-frequency coefficient energy.
5. TPC-215 bounds that coefficient energy by `O((log x)^2)E_direct/L`.
6. TPC-216 bounds `E_direct/L` by
   `O_psi((Q^3/H)(log U)^3)`.

## Proof

### Step 1: Source inequalities and units

The displayed exponents give

```text
H/(4Q)=x^(31/96)/4 -> infinity,
U/Q=x^(-1/1200) -> 0.
```

Thus, for sufficiently large `x`, `4Q<H` and `U<Q`.  Every shell prime is a
unit modulo every `d in D_x`.

### Step 2: Exact reduced-frequency regrouping

For a residue `r mod d`, let `g=(r,d)`, `h=d/g`, and `a=r/g`.  If `r=0`, use
the convention `h=1,a=0`; otherwise `(a,h)=1`.  Then `r/d=a/h` in lowest
terms.  The integer cutoff is compatible with divisibility: if `h|d` and
`d=kh`, the congruence

```text
m q^(-1) = k a mod k h
```

forces `m=kn`, and the cutoff and profile argument become exactly

```text
|n|<=floor(hq/H),   Hm/(dq)=Hn/(hq).
```

Therefore

```text
B_d(k a)=B_h(a).
```

Regrouping the finite divisor sum by reduced fractions gives the exact identity

```text
K(n)=sum_(h<=U) sum_(a mod h,(a,h)=1)
        C_h B_h(a)e(na/h).
```

The `h=1` row is zero because `q<H` implies `floor(q/H)=0`, so no nonzero
integer atom can occupy the zero residue.

### Step 3: Reduced-fraction spacing

Let `a/h` and `a'/h'` be distinct reduced frequencies with `h,h'<=U`.
Their difference is a nonzero rational with denominator dividing `hh'`, so its
absolute value is at least `1/(hh')`.  If the relevant distance is across the
unit boundary, `1-|a/h-a'/h'|` has the same denominator property.  Hence the
circular separation satisfies

```text
||a/h-a'/h'||_R >= U^(-2).
```

### Step 4: Additive large sieve on the physical interval

Use the standard additive large-sieve inequality: if frequencies are separated
modulo one by at least `delta`, then for any consecutive interval of `N`
integers,

```text
sum_(n in I)|sum_j z_j e(n alpha_j)|^2
  <= (N-1+delta^(-1))sum_j|z_j|^2.
```

Apply it to the exact expansion in Step 2 with `delta=U^(-2)` and
`z_(h,a)=C_hB_h(a)`.  This gives

```text
sum_(n in I_x)|K(n)|^2
  <= (N+U^2) S_cluster,
S_cluster=sum_(h,a)|C_hB_h(a)|^2.
```

### Step 5: Coefficient-energy majorant

TPC-215 supplies the exact row-norm divisor decomposition and the coefficient
majorant

```text
S_cluster <= A_x E_direct/L,
A_x=O((log x)^2).
```

The estimate uses the diagonal anchor `d=h` and the short quotient bound; it
does not use cancellation in `mu(k)`.

### Step 6: Insert the TPC-216 direct envelope

TPC-216 gives

```text
E_direct/L
  <= C_psi (Q^3/H)(log U)^3
  = O_psi(x^(11/32)(log x)^3).
```

Combining Steps 4--6 yields

```text
sum_(n in I_x)|K(n)|^2
  <<_psi (N+U^2)x^(11/32)(log x)^5.
```

Because `U^2/x=x^(-67/200)` and `N asymp x`, division by `N` gives the
normalized claim.

Therefore the finite-window attachment is proved. `QED`.

## Corrections or Missing Assumptions

The theorem is deliberately stated for the common-source cluster kernel.  It
does not identify this kernel with the final signed Gate-B scalar after every
prime-shell, four-packet, zero/nonunit, and Euler correction has been returned.

## Open Risks

- The standard large sieve controls the finite-window Gram at the spacing scale;
  it does not exploit additional arithmetic cancellation.
- The inherited `O((log x)^2)` coefficient majorant may be too coarse for a
  strict endpoint theorem, even though it preserves the current power exponent.
- Prime-shell/four-packet reassembly and arithmetic `L2` remain open.
