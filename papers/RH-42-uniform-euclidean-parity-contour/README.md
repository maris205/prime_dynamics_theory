# RH-42: Uniform Euclidean parity contour

This paper closes the dimension-uniform Euclidean contour condition left by
the RH-40 weighted-Riesz bridge.

At the exact first band-merging parameter

\[
u_{\mathrm c}^3-2u_{\mathrm c}^2+2u_{\mathrm c}-2=0
\]

and fixed noise width sigma = 1/100, let K be the exactly normalized
folded-Gaussian Markov operator on L2([0,1]). For

\[
c=-0.9865481927458079,\qquad r=0.05,
\]

the circle |z-c|=r lies in the resolvent set of K, contains exactly one
eigenvalue counted algebraically, and satisfies

\[
\sup_{|z-c|=r}\|(z-K)^{-1}\|_{L^2\to L^2}
\le 266.6496824500989.
\]

The enclosed eigenvalue is real, negative, and algebraically simple.

For every integer n >= 131072, the exact-real continuum-normalized midpoint
matrix, the discretely normalized full Markov matrix, the fixed eight-sigma
sparse matrix, and the adaptive sparse matrix all have exactly one
eigenvalue inside the same circle. Their uniform Euclidean resolvent uppers
are 837.124, 838.211, and 838.211, respectively.

## Certificate chain

| gate | rigorous upper/product |
|---|---:|
| exact-stored Euclidean Grushin residual | 1.1805165238523326e-10 |
| exact-stored contour resolvent | 84.0073245249997 |
| stored to exact midpoint product | 0.0008866273425013429 |
| midpoint to Hilbert Galerkin product | 0.06823949740334896 |
| maximum dyadic Schur product | 0.14911367300796002 |
| Galerkin to continuum product | 0.5767224275624271 |
| continuum to all-grid midpoint product | 0.6814692507211605 |
| discrete-normalization product | 0.0012966148099273645 |
| cutoff product | 1.6281695877396865e-10 |

## Main proof layers

- Exact stored 1- and infinity-norm residual ledgers are converted to
  Euclidean bounds by the geometric-mean operator inequality.
- A 224-bit Arb Frobenius calculation bridges the stored 4096 matrix to the
  exact continuum-normalized midpoint matrix.
- Closed Gaussian target moments reduce every Hilbert-Schmidt derivative
  validation to a one-dimensional Arb integral.
- A midpoint-average Peano kernel gives a genuinely second-order Euclidean
  midpoint-to-Galerkin defect.
- Orthogonal cell averages and four Haar-Schur steps transfer the count to
  dimension 65536 and then to the continuum L2 operator.
- Direct continuum, row-normalization, and cutoff perturbations give one
  uniform Euclidean theorem for every n >= 131072.

The fixed eight-sigma window already preserves the spectral count uniformly
in Euclidean norm. The adaptive schedule

\[
L_n=\max\{8,2\sqrt{\log n}\}
\]

additionally restores the weighted-Riesz cutoff rate
O(n^-2 (log n)^-1/4).

## Result boundary

- The theorem is at the fixed positive noise width sigma = 1/100.
- The all-dimension theorem concerns exact-real Gaussian matrix formulas.
  It does not certify every future binary64 transcendental evaluation.
- Fixed width is spectrally stable in Euclidean norm, but its row-norm defect
  floor remains; no full-kernel row-norm convergence is claimed for it.
- No zero-noise limit, zeta-zero identification, self-adjoint
  Hilbert--Polya operator, T log T law, trace formula, or
  Riemann-hypothesis conclusion is claimed.

## Reproduce

From this directory:

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_euclidean_grushin_certificate.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_euclidean_midpoint_bridge.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_hilbert_envelope_certificate.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_uniform_euclidean_certificate.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/estimate_hilbert_constants.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf uniform-euclidean-parity-contour.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
~~~

The exact-stored Grushin replay is the longest step, typically about one
minute on the current server. The 224-bit midpoint bridge takes roughly half
a minute; the closed-target Hilbert envelope takes only a few seconds.

## Layout

- `main.tex`, `references.bib`: manuscript sources.
- `uniform-euclidean-parity-contour.pdf`: publication PDF.
- `src/euclidean_contour/`: Euclidean Grushin, Hilbert-Galerkin, Peano,
  normalization, and cutoff bounds.
- `experiments/run_euclidean_grushin_certificate.py`: exact-stored bordered
  inverse certificate.
- `experiments/build_euclidean_midpoint_bridge.py`: 224-bit Frobenius bridge.
- `experiments/build_hilbert_envelope_certificate.py`: closed-target
  Hilbert-Schmidt derivative envelope.
- `experiments/build_uniform_euclidean_certificate.py`: complete theorem
  composition.
- `experiments/estimate_hilbert_constants.py`: non-rigorous floating pilot.
- `experiments/make_figures.py`: publication figure.
- `experiments/build_archive.py`, `experiments/verify_archive.py`: hashed
  archive construction and verification.
- `results/`: theorem ledgers, pilot, dependency manifest, summary, and
  archive verification.
- `tests/`: analytic identities and archived gate checks.
