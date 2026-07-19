# RH-44: Validated rank-two peripheral complement

This paper completes the intrinsic Perron-plus-parity subtraction for the
folded-Gaussian Markov operator at fixed noise sigma = 1/100.

The two validated contours are

\[
\Gamma_+=\{|z-1|=0.05\},\qquad
\Gamma_-=\{|z+0.9865481927458079|=0.05\}.
\]

Each contains one algebraically simple eigenvalue. Their weighted Riesz
terms form the gauge-free rank-two kernel

\[
q_{\mathrm{per}}(x,y)=\pi(y)+q_-(x,y),
\]

where `pi` is the normalized stationary density and `q_-` is the validated
negative-parity kernel from RH-43.

## Main validated results

| result | rigorous value |
|---|---:|
| stored Perron-factor error, n = 2048 | 2.160071359188073e-10 |
| stored Perron-factor error, n = 4096 | 4.216696298600817e-10 |
| stored Perron-factor error, n = 8192 | 8.337810516512359e-10 |
| continuum Perron resolvent upper | 81.30575843422578 |
| Perron-kernel operator construction radius | 1.0350408593793905 |
| Perron-kernel L2 construction radius | 1.4637688209446382 |
| rank-two-kernel L2 construction radius | 3.8909449607391675 |
| maximum actual rank-two Haar target deviation | 6.059251560736612e-4 |
| all-grid threshold | n >= 65536 |
| union-contour sparse resolvent upper | 267.81252084743886 |
| full-to-sparse rank-two weighted difference | 9.269128034310783e-10 |
| full-to-sparse intrinsic bulk difference | 9.271085367195988e-10 |

The Perron kernel has the exact form

\[
q_+(x,y)=\pi(y),\qquad K^*\pi=\pi,\qquad \int_0^1\pi=1.
\]

It is independent of the source variable, so all source and mixed
derivatives vanish. The actual stored rank-two Haar ratios are rigorously
enclosed near

\[
(E,C,B,D)=(1/4,1/2,1/2,1/4).
\]

## Intrinsic bulk algebra

Define

\[
B=K-Q_+-Q_-.
\]

Then the Perron and negative-parity eigenvalues are replaced by zero while
the remaining spectrum is unchanged away from zero. For every `m >= 1`,

\[
B^m=K^m-Q_+-\lambda_-^{m-1}Q_-,
\]

\[
\operatorname{tr}(B^m)=\operatorname{tr}(K^m)-1-\lambda_-^m,
\]

and

\[
\det(I-zK)=(1-z)(1-z\lambda_-)\det(I-zB).
\]

These are structural operator identities. They do not identify the bulk
determinant with an arithmetic zeta function.

## Proof and certificate layers

- Strong positivity gives the exact Perron eigenvalue, stationary density,
  and rank-one projector formula.
- Componentwise outward bordered-inverse certificates close the stored
  Perron circles at dimensions 2048, 4096, and 8192.
- Two-sided residual correction proves that every stored Perron factor is
  the true weighted Riesz term of its exact stored matrix.
- Hilbert--Galerkin and infinite-complement Schur steps transfer the Perron
  circle to the continuum with an explicit Euclidean resolvent.
- The RH-43 parity kernel and the Perron kernel have disjoint spectral
  supports, so their weighted terms annihilate one another.
- Arb arithmetic corrects the archived rank-two Haar ledger from algebraic
  factors to actual spectral terms.
- Exact-real normalization and Gaussian cutoff bounds transfer both contours
  and the rank-two deflation to every n >= 65536.

## Theorem boundary

- The theorem is at fixed positive noise sigma = 1/100.
- Continuum kernels are enclosed in Hilbert--Schmidt norms; the displayed
  heat map is an archived center, not a pointwise interval enclosure.
- The all-dimension theorem concerns exact-real Gaussian formulas. Binary64
  claims concern only the six archived Perron/parity factors.
- Fixed eight-sigma support is uniformly stable but is not claimed to
  converge to the full kernel in row norm.
- The trace and determinant identities are structural, not an arithmetic
  trace formula or prime-power identity.
- No zero-noise limit, zeta-zero identification, self-adjoint Hilbert--Polya
  operator, T log T counting law, or Riemann-hypothesis conclusion is made.

## Complete replay

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_multilevel_perron_grushin.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_rank_two_certificate.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 \
  /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf validated-rank-two-peripheral-complement.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
```

The 8192 bordered inverse takes roughly six minutes on the current server.
The composition, Arb Haar ledger, tests, figures, and archive verification
take seconds.

## Layout

- `main.tex`, `references.bib`: manuscript sources.
- `validated-rank-two-peripheral-complement.pdf`: publication PDF.
- `src/rank_two_complement/`: specialized Perron-kernel and rank-two bounds.
- `experiments/run_multilevel_perron_grushin.py`: three exact-stored Perron
  bordered-inverse certificates.
- `experiments/build_rank_two_certificate.py`: Perron contour, factor,
  rank-two Haar, kernel, full/sparse, cutoff, and bulk composition.
- `experiments/make_figures.py`: publication figure.
- `experiments/build_archive.py`, `experiments/verify_archive.py`: hashed
  archive construction and theorem-gate verification.
- `results/`: theorem ledgers, dependency manifest, summary, and archive
  verification.
- `tests/`: analytic identities and archived theorem-gate tests.
