# TPC-90: Primitive affine local-obstruction split

This paper separates the local squarefree support of a primitive
fixed-determinant affine Mobius pair from its unresolved Liouville
sign correlation.

For

```text
L1(r) = d + s r,
L2(r) = u + a r,
s u - a d = h0 != 0,
gcd(d,s) = gcd(u,a) = 1,
```

the exact determinant identities are

```text
gcd(a,s) | h0,
gcd(L1(r),L2(r)) | h0.
```

Thus every simultaneous value prime divides the prescribed fixed
determinant.

## Exact local root count

For a prime `p` and `k >= 1`, let `nu[p,k]` be the number of
residues modulo `p^k` on which `p^k | L1(r)` or
`p^k | L2(r)`. Put

```text
eps1 = 1_(p does not divide s),
eps2 = 1_(p does not divide a).
```

Then

```text
nu[p,k] = eps1 + eps2 - eps1 eps2 1_(p^k | h0).
```

Consequences:

- common roots modulo `p^k` occur exactly when both slopes are units
  modulo `p` and `p^k | h0`;
- a collision modulo `p` requires `p | h0`;
- a collision modulo `p^2` requires `p^2 | h0`;
- a prime dividing exactly one slope deletes one local root and may
  move with the growing coefficients;
- a prime dividing both slopes must divide `h0`, and neither form has
  a root modulo that prime.

If one slope is zero, primitivity forces that affine form to be the
constant `1` or `-1`. The exact root formula still holds and reduces
to the one-form count; the paper does not describe the infinitely
many primes dividing the integer zero as a finite exceptional set.

## Squarefree support

The simultaneous squarefree factor is

```text
Qsf(r) = mu^2(|L1(r)|) mu^2(|L2(r)|).
```

Its local product is

```text
S_sf(L1,L2) = product_p (1 - nu[p,2]/p^2)
            >= product_p (1 - 2/p^2)
            > 0.
```

For every fixed primitive pair, this product is the natural density
of values for which both forms are squarefree. The paper proves this
directly.

For squarefree `q1,q2`, the system

```text
q1^2 | L1(r),
q2^2 | L2(r)
```

is soluble exactly when

```text
gcd(q1,s) = gcd(q2,a) = 1,
gcd(q1,q2)^2 | h0.
```

When soluble, it is one residue class modulo
`lcm(q1^2,q2^2)`.

## Exact parity split

On an interval where both forms are positive,

```text
mu(L1(r)) mu(L2(r))
  = Qsf(r) lambda(L1(r)) lambda(L2(r)).
```

The first factor is the completely classified squarefree/local
support. The second factor is the still-hard Liouville parity
correlation.

The unresolved literal target keeps:

- the growing physical slopes and intercepts;
- the same prescribed nonzero `h0`;
- the actual interval origins and all relevant prefixes;
- all masks and weights;
- both polarizations and every outer key;
- the complete global post-aggregation normalization.

Fixed-form logarithmic correlation theorems and averaged-shift
theorems do not automatically supply this growing fixed-`h0`
ordinary weighted estimate.

## Proof levels and ledgers

- **L0:** determinant algebra, exact root counts, CRT compatibility,
  the Euler product, fixed-form squarefree density, and the
  `mu = mu^2 lambda` split.
- **L1:** verification that these are the literal physical
  coefficients and that content masks, origins, weights, prefixes,
  polarizations, and outer reassembly are complete.
- **L2:** uniform cancellation for the actual growing fixed-`h0`
  weighted Liouville correlation. This is not proved.

The determinant compatibility condition

```text
lambda_D <= 2 eta_Z
```

and the independent physical-loss rule

```text
Lambda_phys < 1/400
```

remain separate. The positive squarefree local factor is not a
signed cancellation gain.

The paper does not specialize `h0` to `2`, breach the parity barrier,
prove a prime-pair lower bound, or prove the twin-prime conjecture.

## Build

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

```text
primitive-affine-local-obstruction-split.pdf
```
