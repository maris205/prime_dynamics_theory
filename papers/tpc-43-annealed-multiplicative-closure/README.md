# TPC-43: Annealed multiplicative closure

This directory contains the manuscript

> **Annealed Multiplicative Closure at the Four-Mobius Gate:
> Prime-Sign Orthogonality, Product-Fiber Rigidity, and the Deterministic
> Walsh Corner**.

TPC-42 left a coefficient-specific four-Mobius Hilbert-energy gate. This
paper tests that gate with one globally consistent Rademacher
multiplicative field

```text
F_epsilon(n) = mu(n)^2 product_(p|n) epsilon_p.
```

The same prime signs act at every source and target occurrence. This is
not independent row noise, and the all-minus environment is exactly the
Mobius function.

## Main results

- For every nonzero atom, the source divisor and affine target fuse into
  the squarefree Walsh label

  ```text
  s = d n / gcd(d,n)^2.
  ```

  At fixed orbit time and alias, each label has at most `X^o(1)` physical
  rows. The proof reconstructs a row from `g | (h+kM)` and
  `d | s g^2`, so the multiplicity is bounded by divisor functions.

- Walsh orthogonality and fiberwise Cauchy-Schwarz give the full annealed
  trace estimate

  ```text
  E Z_tr <= rho_X D_tr << X^o(1) Q^2 J K_B,
  rho_X = X^o(1).
  ```

  The same argument closes the actual minimal folded bank. All inherited
  masks, source weights, orbit coordinates, and aliases are retained.

- At the equality alias `k=0`, the labels

  ```text
  u_(alpha,j) = d_alpha (ell_alpha d_alpha j + h)
  ```

  are injective for fixed `j`, because `D_0=o(J)`. Consequently the
  complete left-plus-right Hilbert energy is exactly diagonal in
  expectation:

  ```text
  E Z_0 = D_0.
  ```

- Fixed Bonami-Beckner moments give

  ```text
  P(Z_0 > K_B D_0) <= X^(-q/400+o_q(1))
  ```

  for every fixed integer `q`. With one global prime-sign field, equality
  and trace closure hold almost surely eventually along any one fixed,
  prescribed dyadic packet sequence. No uniformity over all packet
  sequences is claimed.

- The physical all-minus corner has the exact deterministic expansion

  ```text
  ||T_0^L||^2 + ||T_0^R||^2
    = D_0 + sum_(kappa>1) mu(kappa) C(kappa).
  ```

  Here `kappa` is the squarefree symmetric-difference kernel of two fused
  row labels. Thus each literal four-Mobius row interaction is compressed
  to one Mobius value. Averaging only primes up to `z` gives an exact
  filtration that retains precisely the kernels with least prime factor
  greater than `z`.

- A one-corner Walsh extremizer has annealed energy `R` but all-minus
  energy `R^2`, and vanishes at every other corner. Therefore an annealed
  theorem cannot by itself select the physical Mobius environment.

## What advances beyond TPC-42

The complete random-multiplicative terminal geometry is now closed. The
remaining deterministic problem is no longer an unspecified collection
of four-Mobius row correlations: it is the explicit one-sided kernel
sum

```text
sum_(kappa>1) mu(kappa) C(kappa)
  <= X^o(1) K_B Q^2 J.
```

This identifies three concrete next routes: rough-kernel descent,
coefficient spectral flatness, or arithmetic de-randomization of the
all-minus prime phase.

## Exact certificate

Run from this directory:

```text
python experiments/tpc43_certificate.py
python -O experiments/tpc43_certificate.py
```

Both commands produce byte-identical canonical JSON. The frozen run
passes `43,877` exact checks.

Certificate digest:

```text
d7d2b07107a6da1bd242ef9dbd8c02de7daea24dfdfbf9b5f31178cacf834d01
```

JSON SHA-256:

```text
f46e5b5ef49cc5f12f92ba0f702938a3fa2367b30c694e01f93fd14d30bd628a
```

## Build

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Claim boundary

TPC-43 does **not** prove the deterministic all-minus kernel bound, a
fixed-shift Chowla estimate, four-Mobius cancellation, a parity breach, a
Hardy-Littlewood prime-pair asymptotic, or infinitely many twin primes.
The random field generally fails the special convolution identity
`mu * 1 = delta_1`; this is a randomized terminal-interface theorem, not
a randomized prime proof.
