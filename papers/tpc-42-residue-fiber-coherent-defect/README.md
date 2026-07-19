# TPC-42: Residue-fiber coherent defect

This directory contains the manuscript

> **Residue-Fiber Orthogonality at the Triple-Prime Mobius Gate:
> Canonical Hilbert Defects, Coherent Synthesis, and Exact Convolution
> Counterterms**.

The paper proves that the natural Hilbert-valued residue-class
vectorization is already exactly diagonal for the physical terminal
coefficient field. The remaining arithmetic gate is coherent synthesis
between distinct CRT residues. It also proves that the natural localized
Dirichlet-convolution boundary is an exact counterterm, not a small error,
on the physical product window.

## Main results

- For fixed alias `k`, terminal vectors at distinct products in the same
  residue class modulo `M` are orthogonal. Therefore

  ```text
  sum_a ||V_(k,a)||^2 = D_k
  ```

  exactly, where `D_k` is the actual atomic diagonal including the target
  Mobius square. These packet identities sum over every residue modulo
  `M`, including nonunits; the TPC-41 scalar theorem controls only the
  unit-residue sector unless a separate regular pruning is justified.

- For the minimal folded bank,

  ```text
  E_same = sum_(s,a) ||W_(s,a)||^2,
  E_fold = sum_s ||sum_a W_(s,a)||^2,
  F      = sum_s sum_(a!=b) <W_(s,a), W_(s,b)>.
  ```

  Thus TPC-41 already closes the residue-packed vector variance; the
  unresolved operation is coherent synthesis across distinct residues.

- The canonical Moore-Penrose decomposition is

  ```text
  T_G = (T_G P_w^dagger) P_w + T_G (I-Pi_w).
  ```

  A coefficient-blind scalar-to-Hilbert lift exists exactly when the
  directional defect vanishes. For pairwise orthogonal fibers of size
  `rho`, only `1/rho` of the coefficient energy lies in the common scalar
  mode.

- The uniform diagonal-normalized equality-column route would improve
  the coherent quotient from the universal row scale `Q` to the
  sufficient benchmark `K_B`; the endpoint-scale gap is

  ```text
  Q/K_B = X^o(1) J^2.
  ```

- Each TPC-36 projective layer reduces exactly to a restricted
  orbit-slope Bessel form. This is the next coefficient-specific target,
  not an arbitrary Hilbert-valued KMT extension.

- For the localized convolution cell

  ```text
  A   = lambda_L * mu_D * u_J,
  B_D = lambda_L * (mu-mu_D) * 1,
  B_J = lambda_L * mu_D * (1-u_J),
  ```

  one has `A+B_D+B_J=lambda_L`. On the physical product window,
  `B_D+B_J=-A` pointwise. The completed shifted-prime term cancels against
  the source-complement term rather than bounding the local cell.

- For the natural unmasked hard cell,

  ```text
  X/log X << ||A||_2^2 << X^(1+o(1)),
  A(n) Lambda(n) = 0.
  ```

  This is a deterministic obstruction to a small-boundary approximation,
  not a lower bound for the signed physical terminal output.

## Exact certificate

Run from this directory:

```text
python experiments/tpc42_certificate.py
python -O experiments/tpc42_certificate.py
```

The two commands produce byte-identical canonical JSON. The frozen run
passes `178,226` exact checks.

Certificate digest:

```text
c2860f5d7c679224a5ff4edd417cb956a3cb49e3c7addc434e23dd7b4b8c50bf
```

## Build

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Claim boundary

TPC-42 does **not** prove the orbit-slope Bessel target, the physical
four-Mobius estimate, a fixed-shift Chowla theorem, a parity breach, a
Hardy-Littlewood prime-pair asymptotic, or infinitely many twin primes.
