# RH-45: Bulk two-step trace norm and determinant

This paper closes the trace-ideal gap for the intrinsic Perron/parity-deflated
folded-Gaussian operator at fixed noise `sigma = 1/100`.

Define

\[
B=K-Q_+-Q_-,
\]

where `Q_+` and `Q_-` are the validated weighted Riesz terms from RH-44.
For the full exact-real midpoint family and the adaptive Gaussian-cutoff
family, lifted to `L2([0,1])`, the paper proves

\[
\|B_n-B\|_{HS}=O(n^{-1}).
\]

The trace-ideal product rule then gives

\[
\|B_n^2-B^2\|_1
\le
\|B_n-B\|_{HS}(\|B_n\|_{HS}+\|B\|_{HS})
=O(n^{-1}).
\]

Consequently every fixed even bulk trace converges, and

\[
\det(I-wB_n^2)\longrightarrow\det(I-wB^2)
\]

locally uniformly in the entire `w`-plane.

The two-step determinant is exactly the symmetric completion of the
regularized one-step determinant:

\[
\det_2(I-zB)\det_2(I+zB)=\det(I-z^2B^2).
\]

## Main validated results

| result | rigorous value |
|---|---:|
| continuum bulk Hilbert--Schmidt upper | 15.418003788081082 |
| continuum bulk-square trace-norm upper | 237.71484080928263 |
| full bulk HS error at `n = 65536` | 0.12813829228640602 |
| adaptive bulk HS error at `n = 65536` | 0.12813829359745443 |
| full bulk-square trace-norm error at `n = 65536` | 3.967692773690177 |
| full bulk HS error at `n = 2^30` | 3.785070933298939e-6 |
| full bulk-square trace-norm error at `n = 2^30` | 1.1671649030227931e-4 |
| determinant disk error, `n = 2^30`, `|w| <= 1e-2` | 3.682918268863141e-4 |

The rigorous first-order rate comes from the piecewise-constant
continuum-to-Galerkin lift. Midpoint quadrature, exact row normalization,
and adaptive cutoff are second order or smaller.

## Floating stored determinant pilot

The archived 2048, 4096, and 8192 matrices use an eight-sigma cutoff. At
these dimensions this is exactly the adaptive schedule

\[
L_n=\max(8,2\sqrt{\log n}).
\]

A sparse LU plus a rank-two matrix determinant lemma gives:

| dimension | `det(I - 1e-2 B_n^2)` |
|---:|---:|
| 2048 | 1.0079758611904712 |
| 4096 | 1.0079757565175829 |
| 8192 | 1.0079757303660912 |

Across five `w` values, the mean ratio of the 4096-to-8192 difference to
the 2048-to-4096 difference is `0.2493`. This is a floating diagnostic,
not a validated convergence rate and not part of the theorem.

## Proof and certificate layers

- Cellwise Poincare--Wirtinger bounds give the continuum-to-Galerkin
  Hilbert--Schmidt error.
- Midpoint Peano-kernel and exact row-scaling bounds remain valid in
  Frobenius/Hilbert--Schmidt norm.
- The adaptive cutoff certificate is explicitly a Frobenius-square ledger.
- Weighted Schur transport controls the continuum-to-Galerkin Perron and
  parity terms.
- Each difference of two rank-one weighted terms has rank at most two, so
  its Hilbert--Schmidt norm is at most `sqrt(2)` times its operator norm.
- Products of Hilbert--Schmidt operators are trace class.
- Standard trace-ideal determinant continuity gives local uniform
  convergence on every compact `w`-disk.

## Theorem boundary

- The theorem is at fixed positive noise `sigma = 1/100`.
- The fixed eight-sigma family is spectrally stable, but continuum
  Hilbert--Schmidt or trace-norm convergence is not claimed for that fixed
  support family.
- The stored sparse-LU determinant values are binary64 diagnostics, not
  outward enclosures.
- The result does not prove a zero-noise determinant limit.
- No arithmetic trace formula, prime-power identity, zeta-zero
  identification, self-adjoint Hilbert--Polya operator, `T log T` counting
  law, or Riemann-hypothesis conclusion is made.

## Complete replay

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_trace_norm_certificate.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_stored_determinant_pilot.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 \
  /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf bulk-two-step-trace-norm-determinant.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
```

The rigorous certificate, tests, figures, and archive steps take seconds.
The full stored determinant pilot takes about four minutes on the reference
server because the 8192 level requires ten sparse LU factorizations.

## Layout

- `main.tex`, `references.bib`: manuscript sources.
- `bulk-two-step-trace-norm-determinant.pdf`: publication PDF.
- `src/bulk_trace/`: trace-ideal bounds and floating determinant lemma.
- `experiments/build_trace_norm_certificate.py`: rigorous HS, trace-norm,
  trace, and determinant ledgers.
- `experiments/run_stored_determinant_pilot.py`: floating 2048--8192 sparse
  determinant diagnostic.
- `experiments/make_figures.py`: publication figure.
- `experiments/build_archive.py`, `experiments/verify_archive.py`: hashed
  archive construction and theorem-gate verification.
- `tests/`: analytic identities and archived theorem-gate tests.
- `results/`: rigorous certificate, floating pilot, summary, dependency
  manifest, and archive verification.
