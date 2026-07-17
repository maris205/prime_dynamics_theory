# RH-36: certified nested-grid physical count

This paper proves the first rigorous adjacent-dimension continuation of the
stored physical contour count established in RH-35.

At fixed Gaussian width `sigma = 1e-2`, let

\[
A_{2048}=U_{2048}^2,\qquad A_{4096}=U_{4096}^2
\]

be the exact stored binary64 Perron/parity-extracted physical two-step
matrices. The fine grid is split by exact dyadic replication and alternating
detail coordinates. In those coordinates,

\[
T^{-1}A_{4096}T=
\begin{pmatrix}
A_{\rm cc}&B_{\rm cd}\\
C_{\rm dc}&D_{\rm dd}
\end{pmatrix}.
\]

Rank-96 stored proof centers plus componentwise residuals certify

\[
\|A_{\rm cc}-A_{2048}\|_2
\le 1.9887717655\times10^{-4},
\]

\[
\|C_{\rm dc}\|_2\le1.1321437876\times10^{-2},\qquad
\|B_{\rm cd}\|_2\le1.3722641667\times10^{-2},
\]

\[
\|D_{\rm dd}\|_2\le1.3052207679\times10^{-4}.
\]

The detail spectrum lies outside the counting disk, and the complete
coarse consistency plus Schur self-energy obeys

\[
\sup_{z\in\Gamma}\|\Delta(z)\|_2
\le 6.1195331541\times10^{-4}.
\]

A direct physical resolvent atlas uses 170 rigorous centers and an exact
314-leaf rational partition. Its worst continuation product is

\[
0.8993497429<1.
\]

The RH-36 coarse snapshot replays the RH-35 exact packet defect and 949-leaf
transfer ledger bitwise. Therefore

\[
\boxed{N_\Gamma(A_{2048})=N_\Gamma(A_{4096})=1}.
\]

This is a theorem for two exact finite stored matrices at one fixed noise
scale. It does not prove a continuum limit, an arbitrary-dimension induction,
a zero-noise limit, a zeta-zero identification, a Hilbert--Pólya
construction, or the Riemann hypothesis.

## Fast verification

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 python experiments/build_archive.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf nested-grid-physical-count.pdf
PYTHONDONTWRITEBYTECODE=1 python experiments/verify_archive.py
```

## Rebuild the stored block certificate

The committed 35 MiB snapshot contains both exact sparse targets and the four
rank-96 proof centers:

```bash
OPENBLAS_NUM_THREADS=32 OMP_NUM_THREADS=32 \
PYTHONDONTWRITEBYTECODE=1 python \
  experiments/run_nested_block_certificate.py --chunk-size 128
```

## Rebuild the physical resolvent atlas

Per-center workspaces are resumable and ignored by Git. Start from a rational
64-center grid:

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
PYTHONDONTWRITEBYTECODE=1 python \
  experiments/run_physical_resolvent_batch.py \
  --initial-grid 64 --workers 8 --chunk-size 256
```

Audit the current centers and generate unresolved midpoint targets:

```bash
PYTHONDONTWRITEBYTECODE=1 python \
  experiments/audit_physical_resolvent_atlas.py \
  --base-arcs 64 --max-extra-refinement 12 --product-limit 0.9
```

Feed `results/physical_resolvent_atlas.json` back through
`run_physical_resolvent_batch.py --target-file ...` until the audit reports no
unresolved component.

The formal manuscript is `nested-grid-physical-count.pdf`.
