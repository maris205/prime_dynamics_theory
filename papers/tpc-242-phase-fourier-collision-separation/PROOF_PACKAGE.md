# TPC-242 proof package

## 1. Convention and objects

Let `H` be a complex Hilbert space with inner product conjugate-linear in the
first slot and linear in the second. For `X,Y in H`, put

```text
E_j = ||X+i^j Y||^2,                         0<=j<=3,
F_k = (1/4) sum_(j=0)^3 i^(k j) E_j,         0<=k<=3.
```

Write

```text
S = ||X||^2+||Y||^2,
c = <Y,X>.
```

Then `<X,Y>=conjugate(c)`.

## 2. Complete `C_4` phase spectrum

### Theorem 2.1

For every `X,Y`,

```text
F_0 = ||X||^2+||Y||^2,
F_1 = <Y,X>,
F_2 = 0,
F_3 = <X,Y>.
```

### Proof

Conjugate-linearity in the first slot gives

```text
E_j
 = <X+i^jY, X+i^jY>
 = ||X||^2+||Y||^2+i^j<X,Y>+i^(-j)<Y,X>
 = S+i^j conjugate(c)+i^(-j)c.
```

For every integer `m`,

```text
(1/4) sum_(j=0)^3 i^(m j) = 1 if 4 divides m, and 0 otherwise.
```

Substitution into the definition of `F_k` yields

```text
F_k = S 1_(k=0)+conjugate(c) 1_(k=3)+c 1_(k=1),
```

for `k=0,1,2,3`. This is the asserted spectrum. In particular the literal
`i^j` convention selects `<Y,X>`; the `(-i)^j` convention would reverse the
selected orientation. ∎

### Corollary 2.2 (phase-independent additive terms)

If a scalar `A` is added to every phase energy, so `E'_j=E_j+A`, then

```text
F'_0-F_0=A,
F'_1-F_1=F'_2-F_2=F'_3-F_3=0.
```

Indeed, the increment is `A` times the `C_4` character sum. Thus a genuinely
phase-independent additive scalar contributes only to the trivial mode and
exactly zero to `F_1`. The hypothesis is an equality in all four phase-labelled
energies; it cannot be inferred from an unrelated unsigned norm estimate.

## 3. Exact feasible set at fixed total energy

### Theorem 3.1

Fix a nonzero complex Hilbert space and `S>=0`. Over all pairs `X,Y` with
`||X||^2+||Y||^2=S`, the possible values of `F_1=<Y,X>` form exactly

```text
{z in C : |z|<=S/2}.
```

This includes `S=0`, for which the set is `{0}`.

### Proof

Cauchy--Schwarz and the arithmetic--geometric mean inequality give

```text
|F_1| = |<Y,X>|
      <= ||X|| ||Y||
      <= (||X||^2+||Y||^2)/2
      = S/2.
```

For the reverse inclusion, first suppose `S>0` and let `rho=|z|<=S/2`. Put

```text
D=sqrt(S^2-4rho^2),
a=(S+D)/2,
b=(S-D)/2.
```

Then `a>0`, `a+b=S`, and `ab=rho^2`. Choose a unit vector `e` and set

```text
X=sqrt(a)e,
Y=(conjugate(z)/sqrt(a))e.
```

Direct calculation gives

```text
||X||^2=a,
||Y||^2=|z|^2/a=b,
<Y,X>=z.
```

If `S=0`, nonnegativity of the squared norms forces `X=Y=0`. Both inclusions
are proved. ∎

## 4. Exact defect identity

### Theorem 4.1

With `S=F_0` and `F_1=<Y,X>`,

```text
S^2-4|F_1|^2
 = (||X||^2-||Y||^2)^2
   +4(||X||^2||Y||^2-|<Y,X>|^2).
```

### Proof

Put `a=||X||^2` and `b=||Y||^2`. Then

```text
(a+b)^2-4|<Y,X>|^2
 = (a-b)^2+4ab-4|<Y,X>|^2,
```

which is the stated identity. Both terms on the right are nonnegative: the
first is a square, and the second is four times the determinant of the
two-vector Gram matrix. ∎

### Equality characterization

The boundary equality `|F_1|=S/2` holds exactly when

```text
||X||=||Y||
```

and the Gram determinant vanishes. Equivalently, the norms are balanced and
`X,Y` are linearly dependent (with the zero case included). The two summands
therefore separate norm imbalance from angular decorrelation.

## 5. Source-typed corollary for TPC-241

The V59 source uses the literal packets `beta+i^j w` and the literal multiplier
`i^j`, so its scalar projector has the orientation `F_1=x conjugate(y)=<y,x>`.
TPC-241 proves an unsigned floor for a standalone fixed common-profile kernel.
Its proof does not establish any of

```text
K_psi = T beta,
K_psi = T w,
E_top^psi = F_0,
the TPC-241 floor = one common additive term in all four V59 energies.
```

Consequently TPC-241 supplies zero direct quantitative implication for the
literal V59 coefficient `F_1`: no lower bound, upper bound, nonvanishing,
phase, sign, or power saving transfers from that result alone. This is a
source-type non-transfer statement. It does not prove that the physical
top-prime mode is zero or annihilated. A phase-by-phase physical attachment
theorem remains necessary.

## 6. Claim ceiling

The maximum status is

```text
PROVED_STRUCTURAL_L1_PHASE_FOURIER_NO_TRANSFER.
```

There is no arithmetic asymptotic estimate, signed `C_h` theorem, arithmetic
`L2`, fixed-atom credit, strict `1/400` payment, full Gate-B closure, or
twin-prime result.
