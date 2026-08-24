# TPC-234 proof package

## Theorem

Let `H` be a Hilbert space and let `(u_q)` be unit vectors in the direct coordinate
space `ell^2(X;H)`.  Assume each coordinate `x` belongs to the supports of at most two
rows.  For

\[
Tc=\sum_q c_q u_q,
\qquad G=T^*T,
\]

one has

\[
0\le G\le2I,
\qquad \sigma(G)\subset[0,2],
\qquad \|G-I\|\le1.
\]

The constant `2` is sharp in the abstract multiplicity-two class.  In the TPC-232
dilated clock the hypothesis holds for every `L<Q/4`, so the bound is depth-uniform.

## Proof

For finitely supported coefficients `c`, at each coordinate `x` there are at most two
nonzero vectors `c_qu_q(x)`.  The Hilbert-space parallelogram inequality gives

\[
\left\|\sum_{q:x\in\operatorname{supp}u_q}c_qu_q(x)\right\|^2
\le2\sum_{q:x\in\operatorname{supp}u_q}|c_q|^2\|u_q(x)\|^2.
\]

Summing over coordinates and exchanging the finite sums,

\[
\|Tc\|^2
\le2\sum_q|c_q|^2\sum_x\|u_q(x)\|^2
=2\sum_q|c_q|^2.
\]

Thus `G=T*T<=2I`; positivity is automatic.  Since every row is unit, the diagonal of
`G` is one.  Therefore `K=G-I` is self-adjoint and `-I<=K<=I`, which proves
`||K||<=1` and the spectral statement.

For sharpness, take two copies of the same unit vector supported at one coordinate.
With coefficients `(1,1)`, the output energy is `4` and the coefficient energy is `2`.
Hence no smaller universal constant is possible under multiplicity two alone.  ∎

## Literal non-saving block

At `Q=39,L=7`, the clock is `1092`.  The positive primitive multipliers in both rows
`67` and `71` are `(1,5,11)`.  Their six-point supports intersect exactly at

```text
277: multipliers (-5,11),
815: multipliers (5,-11).
```

Uniform unit rows therefore have inner product `1/3`.  Symmetric and antisymmetric
coefficients yield exact normalized energies `4/3` and `2/3`.  This proves that the
Bessel theorem is a conditioning result only; normalized geometry can amplify or save.

## Source boundary

The transform `v_q -> v_q/||v_q||` changes row coefficients.  Until the actual V59
source-to-row crosswalk is written, it is a modeling transform rather than a licensed
arithmetic operation.
