# RH-43: Validated weighted-Riesz parity kernel

This paper turns the isolated negative parity resonance of the
folded-Gaussian Markov operator into a validated, gauge-free continuum
kernel that can be subtracted before later trace and determinant analysis.
The noise width is fixed at sigma = 1/100.

For the circle

\[
c=-0.9865481927458079,\qquad r=0.05,
\]

the intrinsic weighted Riesz term is

\[
Q_-(K;\Gamma)=\frac{1}{2\pi i}\int_\Gamma z(z-K)^{-1}\,dz.
\]

It has rank one and a real smooth Hilbert--Schmidt kernel.  The construction
is intrinsic: it does not depend on a normalization or sign convention for
left and right eigenvectors.

## Main validated results

| result | rigorous value |
|---|---:|
| stored parity-factor error, n = 2048 | 3.650836314181483e-10 |
| stored parity-factor error, n = 4096 | 7.202868434316492e-10 |
| stored parity-factor error, n = 8192 | 1.426439999332510e-9 |
| maximum quarter--half ratio deviation | 3.931292394472319e-4 |
| infinite-complement Schur product | 7.281434256176882e-4 |
| continuum L2 contour resolvent | 112.95503061584434 |
| continuum-kernel L2 construction radius | 2.4271761397945286 |
| kernel midpoint-to-cell-average defect at n = 65536 | 1.7901255123532672e-5 |
| all-grid threshold | n >= 65536 |
| full exact-real matrix resolvent | 267.8125208334001 |
| fixed/adaptive sparse resolvent | 267.81252084743886 |
| full-to-sparse weighted-Riesz difference | 7.275887086007192e-10 |
| full-to-sparse intrinsically deflated difference | 7.277844418892396e-10 |

The archived parity factors at dimensions 2048, 4096, and 8192 are proved
to be genuine spectral weighted terms.  Their two dyadic transitions obey
the actual spectral ratio law

\[
(E,C,B,D)\longrightarrow(1/4,1/2,1/2,1/4).
\]

The analytic smooth-kernel limits are

\[
h^{-2}E_h\to\frac{q_{xx}+q_{yy}}{32},\qquad
h^{-1}C_h\to\frac{q_x}{4},
\]

\[
h^{-1}B_h\to\frac{q_y}{4},\qquad
h^{-2}D_h\to\frac{q_{xy}}{16}.
\]

## Main proof layers

- A two-sided residual correction block-diagonalizes an approximate
  rank-one factor for a nearby matrix and transfers it to the exact
  weighted Riesz term by a contour resolvent identity.
- Componentwise outward bordered-inverse certificates close the stored
  spectral status at all three archived dimensions.
- Arb arithmetic converts the archived algebraic Haar blocks into intervals
  for the actual spectral weighted terms.
- A Schur decomposition against the full infinite-dimensional cell-average
  complement replaces the direct continuum defect by a quadratic
  self-energy term.
- Weighted Schur transport connects the stored 4096 factor to a smooth
  intrinsic continuum kernel.
- Exact-real normalization and Gaussian cutoff bounds transfer the kernel
  to every full, fixed-width, and adaptive sparse matrix from n = 65536.

## Intrinsic deflation

The validated operators are

\[
K_\perp=K-Q_-(K;\Gamma),\qquad
P_{n,\perp}=P_n-Q_-(P_n;\Gamma).
\]

They replace the enclosed negative parity eigenvalue by zero and leave the
remaining spectrum unchanged away from zero.  The adaptive weighted kernel
and deflated family converge at

\[
O\!\left(n^{-2}(\log n)^{-1/4}\right).
\]

## Theorem boundary

- The theorem is at fixed positive noise sigma = 1/100.
- The exact continuum kernel is enclosed in Hilbert--Schmidt norms; the
  displayed heat map is the archived 4096 center, not a pointwise interval
  enclosure.
- The all-dimension theorem concerns exact-real Gaussian formulas.  The
  binary64 theorem concerns only the three archived matrices.
- The Perron weighted term is not yet included, so no validated rank-two
  deflation is claimed.
- Fixed eight-sigma support is uniformly spectrally stable but is not
  claimed to converge to the full kernel in row norm.
- No zero-noise limit, arithmetic trace formula, zeta-zero identification,
  self-adjoint Hilbert--Polya operator, or Riemann-hypothesis conclusion is
  claimed.

## Complete replay

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_multilevel_euclidean_grushin.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_weighted_kernel_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 \
  /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf validated-weighted-riesz-parity-kernel.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
```

The 8192 bordered-inverse replay is the longest step and takes roughly six
minutes on the current server.  The certificate composition, Arb Haar
ledger, figures, tests, and archive verification take seconds.

## Layout

- `main.tex`, `references.bib`: manuscript sources.
- `validated-weighted-riesz-parity-kernel.pdf`: publication PDF.
- `src/weighted_kernel/`: outward factor, weighted-Schur, kernel-envelope,
  and deflation bounds.
- `experiments/run_multilevel_euclidean_grushin.py`: three exact-stored
  Euclidean bordered-inverse certificates.
- `experiments/build_weighted_kernel_certificate.py`: complete factor,
  Haar, continuum-kernel, family, cutoff, and deflation composition.
- `experiments/make_figures.py`: publication figure.
- `experiments/build_archive.py`, `experiments/verify_archive.py`: hashed
  archive construction and theorem-gate verification.
- `results/`: principal certificates, dependency manifest, summary, and
  archive verification.
- `tests/`: analytic identities and archived theorem-gate tests.
