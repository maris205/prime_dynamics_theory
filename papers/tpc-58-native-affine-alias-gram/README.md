# TPC-58: Canonical residual erasure and the native affine Gram

This directory contains the source and final PDF for:

> *Canonical Residual Erasure and the Native Affine Gram at a Fixed
> Shift: Exact Alias Defects, Dark Spaces, and Two-Stage Transfer Gates*

## Core result

TPC-45 has two different Gram forms. The low-sign average resolves a
residual label `s`, while the physical all-minus corner groups all residual
labels inside the same native output coordinate. TPC-58 identifies the
map between them exactly:

```text
(E_mu z)_i = sum_t mu(t) z_(i,t).
```

Its energy defect is the complete signed off-diagonal alias form

```text
||E_mu z||^2 - ||z||^2
  = 2 Re sum_i sum_(t<t') mu(t)mu(t') z_(i,t) conjugate(z_(i,t')).
```

On a fiber with `k_i` active labels, the grouping map has one nonzero
singular value `sqrt(k_i)` and a dark space of dimension `k_i-1`. Hence a
support-only uniform lower bound is impossible whenever two residual
labels share a native output. Möbius signs are a diagonal unitary gauge;
they do not remove the dark space.

## Actual coefficient image

The ambient obstruction does not settle the physical coefficient family.
For a fixed baseline carrier let `z = T zeta` and `E = Ran(T)`. The optimal
coefficient-uniform constant is

```text
alpha_E = inf_(0 != z in E) ||E_mu z||^2 / ||z||^2
        = lambda_min((P_E E_mu^* E_mu P_E)|_E).
```

In finite dimension, `alpha_E > 0` exactly when
`E intersect Ker(E_mu) = {0}`. With `R=T^*T`,
`N=T^*E_mu^*E_mu T`, and `S=Ran(R)`, the exact generalized-Gram form is

```text
alpha_E = lambda_min((R^(dagger/2) N R^(dagger/2))|_S).
```

The restriction to `S` is essential. A kernel direction of `T` is not a
physical generalized eigenvector.

## Two grouping levels

The paper distinguishes

```text
terminal prime p  ->  resolved key (i,s)  ->  native output i.
```

TPC-56/57 study the first arrow. TPC-58 studies the second. Terminal-prime
singleton incidence does not imply residual-label singleton incidence.
The TPC-57 terminal amplitude already contains the physical `mu(s)` gauge,
so its next native operation is an unsigned sum over `s`; multiplying by
`mu(s)` again would be a sign error.

## Exact remaining gates

Writing the canonical high coefficient as

```text
z_H(i,s) = -sum_p b_(i,sp),
h = E_mu z_H = -sum_p v_p,
```

the complete native affine column on the declared direct slice is
`v_0 + h`. Its transfer factors through two independent constants:

```text
||h||^2 >= alpha_H ||z_H||^2,
||v_0+h||^2 >= delta_aff (||v_0||^2+||h||^2).
```

Thus

```text
||v_0+h||^2 >= delta_aff alpha_H ||z_H||^2.
```

The affine pair space is the image of the genuinely coupled map

```text
J_aff(zeta) = (B_0 zeta, E_mu T_H zeta),
```

so both entries use the same coefficient vector. The uniform constants are
assigned only when their corresponding finite-dimensional images are
nonzero. TPC-58 characterizes both gates and gives sharp coupled-map zero
examples, but does not prove either constant has a positive polynomial
lower bound on the endpoint physical packet.

## Endpoint band compatibility

For the fixed endpoint cutoff `y = X^(267/400+eta)` with fixed `eta > 0`,
`p > y` and `pr <= X^(1+o(1))` imply

```text
r <= X^(133/400-eta+o(1)).
```

This very-high face is therefore asymptotically disjoint from the older
`R ~ J = X^(133/400+o(1))` block. The exact interface can be empty on that
old block. A parent-to-compatible-band relocation/occupancy theorem is a
separate upstream gate and its loss is recorded as `lambda_reloc`.

## Claim boundary

The erasure spectrum, dark-space obstruction, compressed Rayleigh
quotient, and generalized-Gram identities are unconditional L0 results.
The coordinate matching on the declared fixed-`h0` carrier is an L1
interface result. No compatible-band occupancy, endpoint terminal
activation, boundary/tail reconnection, parity improvement, or twin-prime
conclusion is claimed.

## Build

Run `pdflatex`, `bibtex`, and two further `pdflatex` passes in this
directory. The archived PDF is
`canonical-residual-erasure-native-affine-gram.pdf`.
