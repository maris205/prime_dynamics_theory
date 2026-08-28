# TPC-296 derivation package

## 1. Source-correlation map

Let `A in Q^(n x m)` have the physical prime-shell vectors as columns and
let `G=A^T A`.  TPC-295 certifies `G` nonsingular on every inherited row.
For a coefficient target `b`, define

```text
C(h)=A^T h,
S(b)=min { ||h||_2^2 : C(h)=b }.
```

## 2. Least-norm witness

The explicit preimage is

```text
h_b = A G^(-1)b.
```

Every other preimage is `h_b+v` with `v in ker(A^T)`.  Since `h_b` belongs
to `col(A)=ker(A^T)^perp`, Pythagoras gives

```text
||h_b+v||_2^2 = ||h_b||_2^2 + ||v||_2^2.
```

Therefore

```text
S(b)=||h_b||_2^2=b^T G^(-1)b.
```

It follows immediately that the unrestricted source budget `||h||^2<=B`
can realize `b` if and only if `S(b)<=B`.

## 3. Source-energy tradeoff

The physical coefficient energy is

```text
E(b)=||A b||_2^2=b^T G b.
```

Apply Cauchy--Schwarz to `G^(1/2)b` and `G^(-1/2)b`:

```text
(b^T b)^2 <= (b^T G b)(b^T G^(-1)b) = E(b) S(b).
```

For a sign target, `b^T b=m`, so the normalized product is at least one.

## 4. One-ray profile proxy

Let `beta` be the frozen source vector and set `v=A^T beta`.  The enlarged
one-dimensional profile proxy is `{alpha v:alpha in R}`.  The best normalized
target residual is

```text
r_ray(b)^2
 = min_alpha ||alpha v-b||_2^2 / ||b||_2^2
 = 1 - (v^T b)^2 / ((v^T v)(b^T b)).
```

The certificate reports RMS normalization by `sqrt(m)`, which is identical
for sign targets because `||b||_2^2=m`.

## 5. Diagnostic normalizations

The finite source-cost ratio is

```text
tau(b)=S(b)/||beta||_2^2.
```

The threshold `tau<1e-3` is a declared finite diagnostic.  No argument in
this project turns that threshold into a growing-shell exponent or an
arithmetic `L2` estimate.

## 6. Numerical protocol

The producer reconstructs exact rational physical columns in target-first
order, converts them to 70-digit arithmetic, and solves the Gram systems.
The independent checker accumulates columns source-first without importing
the producer.  Both verify correlation residuals and the identity
`||h_b||^2=b^T G^(-1)b`; exact small-matrix stress fixtures attack rank,
budget, tradeoff, and one-ray formulas.
