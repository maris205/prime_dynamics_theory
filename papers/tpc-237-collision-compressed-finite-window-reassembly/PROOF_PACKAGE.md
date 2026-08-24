# TPC-237 proof package

## Theorem: collision-compressed finite-window packet trace

Let `I` be a consecutive interval of `N` integers.  For the frozen primitive-frequency
kernel in `DERIVATION_PACKAGE.md`, assume `x` is sufficiently large, `J` is fixed,
and `M=max_j ||psi_j||_infty`.  Put

```text
R_* = 4Q^2/H + 4UQ/H.
```

Then

```text
sum_(n in I) sum_(j=1)^J |K_j(n)|^2
 <= (N-1+U^2) R_*
    sum_(h<=U) sum_((a,h)=1) sum_j sum_(q in Q_x)
      |C_h B_(h,q)^(j)(a)|^2.                         (T1)
```

Moreover,

```text
sum_(h,a,j,q) |C_h B_(h,q)^(j)(a)|^2
 << JM^2 (Q^2/H)(log x)^5.                            (T2)
```

For `I=I_x=(x/2,x] intersect Z`, this proves

```text
N^(-1) sum_(n in I_x) sum_j |K_j(n)|^2
 << JM^2 [x^(1/48)+x^(1/50)](log x)^5
 << JM^2 x^(1/48)(log x)^5.                           (T3)
```

The leading unnormalized exponent is `49/48+o(1)`.

## Proof

### Step 1: primitive-coordinate collision Bessel

TPC-236 proves for each residue `a mod h`

```text
R_h(a) <= 4Q^2/H + 4hQ/(gH),  g=(a,h).
```

Every frequency in `K_j` is primitive, so `g=1`.  Restricting the TPC-236 support
incidence matrix to primitive coordinates can only decrease row support.  Therefore
`R_h(a)<=R_*` for `h<=U`.  At one coordinate, Cauchy--Schwarz gives

```text
|sum_q B_(h,q)^(j)(a)|^2
 <= R_h(a) sum_q |B_(h,q)^(j)(a)|^2.
```

Multiply by `|C_h|^2` and sum in `h,a,j`.  No sign, profile value, packet label, or
`q` weight is changed.

### Step 2: reduced-frequency large sieve

Distinct primitive pairs `(h,a)` represent distinct points `a/h` modulo one.  If two
such frequencies differ, their circular distance is at least `1/(hh')>=U^(-2)`.
The additive large sieve, applied separately for each packet and then summed over
`j`, gives

```text
sum_(n in I) sum_j |K_j(n)|^2
 <= (N-1+U^2)
    sum_(h,a,j) |C_h sum_q B_(h,q)^(j)(a)|^2.
```

Combining this with Step 1 proves `(T1)`.  Passing unreduced residues to this step
would create duplicate frequencies and invalidate the argument.

### Step 3: direct coefficient energy

For fixed `h,q,j`, internal row injectivity and the profile bound imply

```text
sum_((a,h)=1)|B_(h,q)^(j)(a)|^2
 <= 2M^2 hq/H.
```

An active row has `h>=H/(2Q)`.  Writing `d=hk` in the literal definition of `C_h`
and using absolute values only,

```text
|C_h| <= (log U)/h sum_(k<=U/h) 1/k << (log x)^2/h.
```

Consequently

```text
sum_(active h) h|C_h|^2 << (log x)^5.
```

Since every shell prime obeys `q<=2Q` and `#Q_x<=2Q`, summing the fixed-row estimate
proves `(T2)`.

### Step 4: exponent arithmetic

The exact rational identities are

```text
2/3-21/32 = 1/96,
133/400+1/3-21/32 = 23/2400,
2*(1/96) = 1/48,
1/96+23/2400 = 1/50,
2*(133/400)-1 = -67/200.
```

Because `N` is comparable to `x` on `I_x`, `(T1)` and `(T2)` give `(T3)`.

## Claim boundary

The proof controls the unsigned quantity `sum_j |K_j|^2`.  It does not identify that
trace with the literal signed four-packet Gate-B scalar.  Literal `C_h` is retained in
the kernel, but the proof uses `|C_h|^2` and an absolute harmonic majorant.  Hence
signed `C_h` cancellation, arithmetic `L2`, fixed-atom credit, strict `1/400`, full
Gate B, and the twin-prime endpoint remain open.  Sequential upper bounds also do not
prove simultaneous saturation or sharpness of exponent `1/48`.
