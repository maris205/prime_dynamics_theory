# RH-40: Weighted Riesz projector bridge

This paper replaces gauge-dependent left/right eigenvector tracking by the
intrinsic weighted Riesz term

\[
Q(A;\Gamma)=A\Pi(A;\Gamma)
=\frac{1}{2\pi i}\int_\Gamma z(z-A)^{-1}\,dz.
\]

The main analytic result is a second-order continuum bridge for a simple,
isolated, nonzero Nyström branch:

\[
\|Q_h-Q_h^\circ\|_2=O(h^2).
\]

Here `Q_h` is the finite matrix weighted term and `Q_h^circ` is the midpoint
matrix of the smooth continuum kernel `lambda r(x) ell(y)`. The statement is
independent of signs, phases, scaling, and mode ordering.

## Result boundary

- The weighted-Riesz resolvent perturbation bound is analytic and exact.
- The full smooth folded-Gaussian Perron bridge is unconditional because the
  continuum kernel is strongly positive.
- The negative parity bridge is conditional on a simple isolated continuum
  resonance.
- The adaptive cutoff bridge from RH-39 transfers to the weighted term under
  a uniform Euclidean contour-resolvent bound.
- The Arb ledger is rigorous for the exact stored binary64 factors; it does
  not validate the sparse eigensolver or the binary64 Gaussian construction.
- No zero-noise, zeta-zero, Hilbert--Pólya, or Riemann-hypothesis claim is
  made.

## Exact-stored ledger

At `sigma = 1e-2` and dimensions `2048, 4096, 8192`, 224-bit Arb arithmetic
encloses the second-to-first Frobenius ratios as follows:

| block | rigorous ratio enclosure |
|---|---:|
| `E` | `[0.2498167356411347, 0.2498167356411349]` |
| `C` | `[0.5000282258458135, 0.5000282258458139]` |
| `B` | `[0.5000402199971905, 0.5000402199971907]` |
| `D` | `[0.2500292331599994, 0.2500292331599995]` |

The maximum exact-stored biorthogonality upper is
`2.884875431623001e-15`. Floating diagnostics give a maximum eigen-residual
of `3.516430825983483e-15` and a minimum parity-to-observed-bulk radial gap of
`0.31187762837401034`; these last two numbers are not validated enclosures.

The parity eigenvalue increments have an exact-stored ratio in
`[0.24985683017206403, 0.24985683017206410]`. The two second-order Richardson
extrapolates differ by at most `9.947166793959168e-10`.

## Reproduce

From this directory, with the repository virtual environment available:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_projector_pilot.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_projector_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf weighted-riesz-projector-bridge.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```

The pilot requires the RH-36 and RH-37 snapshots in their repository
locations. The certificate and archive record SHA-256 hashes of every
consumed cross-paper input.

## Layout

- `main.tex`, `references.bib`: manuscript sources.
- `weighted-riesz-projector-bridge.pdf`: publication PDF.
- `src/projector_bridge/`: gauge-invariant low-rank utilities.
- `experiments/run_projector_pilot.py`: floating sparse spectral audit.
- `experiments/build_projector_certificate.py`: 224-bit exact-stored Arb
  ledger.
- `experiments/make_figures.py`: publication figure.
- `experiments/build_archive.py`, `experiments/verify_archive.py`: hashed
  archive construction and replay.
- `results/`: pilot, certificate, manifests, summaries, and verification.
- `tests/`: low-rank identities and archived result gates.
