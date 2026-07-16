# RH-30: sparse two-step Grushin inverse

This paper gives an exact sparse two-step Grushin linearization for the
RH-29 lifted complement shift and closes the selected stored-model resolvent
gate at two scales.

Main rigorous results:

- at `sigma = 1e-2`, `||A_tilde^{-1}||_2 < 108.745`, versus the RH-29
  admissible budget `9497.415`;
- at `sigma = 4e-3`, `||A_tilde^{-1}||_2 < 151.491`, versus the RH-29
  admissible budget `34053.573`;
- the corresponding original selected-arc bounds are `576.695` and
  `746.234`.

The proof treats every archived binary64 factor as exact stored input. Sparse
LU only generates an approximate inverse. The exact lifted target is then
reevaluated with componentwise outward radii, and a Frobenius--Neumann theorem
turns the residual into an inverse upper bound.

The result is deliberately limited to two selected arcs. It does not prove a
full-contour root count, a continuum limit, a Hilbert--Pólya construction, or
anything about the Riemann hypothesis.

## Reproduce

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider

PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python experiments/run_stored_inverse_certificate.py \
  --sigma 1e-2 --chunk-size 256

PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python experiments/run_stored_inverse_certificate.py \
  --sigma 4e-3 --chunk-size 256

MPLCONFIGDIR=/tmp/rh30-mpl python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf sparse-two-step-grushin-inverse.pdf
python experiments/verify_archives.py
```

Principal archives:

- `results/stored_inverse_certificate_sigma_1e-2.json`
- `results/stored_inverse_certificate_sigma_4e-3.json`
- `results/stored_inverse_certificate_sigma_1e-2_chunk128.json`
- `results/stored_certificate_summary.csv`
- `results/sparse_lu_scale_summary.csv`
- `results/summary.json`
- `results/archive_verification.json`

The formal manuscript PDF is generated as
`sparse-two-step-grushin-inverse.pdf`.
