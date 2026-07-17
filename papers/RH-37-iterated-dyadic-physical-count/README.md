# RH-37: iterated dyadic physical count

This paper proves a second rigorous dyadic refinement of the stored physical
contour count at fixed Gaussian width `sigma = 1e-2`:

\[
\boxed{N_\Gamma(A_{2048})=N_\Gamma(A_{4096})=N_\Gamma(A_{8192})=1}.
\]

The statement concerns three exact stored binary64
Perron/parity-extracted physical two-step matrices. It is not a continuum,
all-dimensions, zero-noise, zeta-zero, Hilbert--Pólya, or RH theorem.

## Main certified bounds

For the second split `4096 -> 8192`, rank-96 proof centers plus
componentwise outward residuals give

\[
\|E_2\|_2\le4.9703504366\times10^{-5},
\]

\[
\|C_2\|_2\le5.6612430489\times10^{-3},\qquad
\|B_2\|_2\le6.8617517173\times10^{-3},
\]

\[
\|D_2\|_2\le3.2633698567\times10^{-5}.
\]

Hence

\[
\sup_{z\in\Gamma}\|\Delta_2(z)\|_2
\le1.5296171141\times10^{-4},
\]

and the admissible `A4096` resolvent threshold is `6537.583757`.

The new theoretical step is a hierarchical block-inverse estimate. If
`M0` bounds the `A2048` resolvent and `M0 * epsilon1 < 1`, then

\[
\|(z-A_{4096})^{-1}\|_2
\le d_1+
\sqrt{1+(d_1\|C_1\|)^2}
\sqrt{1+(d_1\|B_1\|)^2}
\frac{M_0}{1-M_0\varepsilon_1}.
\]

A tightened atlas combines 170 inherited rigorous centers with 13 new
centers. Its exact 324-leaf rational partition certifies

\[
\max M_0\varepsilon_1=0.7474271469,
\]

\[
\max\|(z-A_{4096})^{-1}\|_2\le4843.8191045,
\]

and therefore

\[
\max\|(z-A_{4096})^{-1}\|_2\,\varepsilon_2
=0.7409188600<1.
\]

The four second-level blocks are respectively about one quarter, one half,
one half, and one quarter of their first-level certified bounds. These are
finite-scale certified ratios, not an asymptotic theorem.

## Fast verification

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 python experiments/build_final_certificate.py
PYTHONDONTWRITEBYTECODE=1 python experiments/build_archive.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf iterated-dyadic-physical-count.pdf
PYTHONDONTWRITEBYTECODE=1 python experiments/verify_archive.py
```

## Rebuild the second dyadic block certificate

The committed snapshot is split into one exact fine-object archive and four
rank-96 center archives so that every file remains below GitHub's single-file
limit.

```bash
OPENBLAS_NUM_THREADS=32 OMP_NUM_THREADS=32 \
PYTHONDONTWRITEBYTECODE=1 python \
  experiments/run_second_dyadic_block_certificate.py --chunk-size 128
```

## Rebuild the propagated atlas

The 13 additional `A2048` center workspaces are intentionally ignored after a
compact combined archive is built. To regenerate them from an unresolved
audit:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
PYTHONDONTWRITEBYTECODE=1 python \
  experiments/run_additional_coarse_resolvent_batch.py \
  --snapshot ../RH-36-nested-grid-physical-count/results/nested_grid_snapshot_sigma_1e-02.npz \
  --block-certificate ../RH-36-nested-grid-physical-count/results/nested_block_certificate_sigma_1e-02.json \
  --target-file results/propagated_resolvent_atlas.json \
  --workers 8 --chunk-size 256

PYTHONDONTWRITEBYTECODE=1 python \
  experiments/audit_propagated_resolvent_atlas.py \
  --first-product-limit 0.75 \
  --second-block-certificate results/second_dyadic_block_certificate_sigma_1e-02.json \
  --max-extra-refinement 14
```

The formal manuscript is `iterated-dyadic-physical-count.pdf`.
