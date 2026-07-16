# RH-31: sparse threshold inertia

This paper replaces RH-30's all-column inverse certificate by a fixed
two-factorization inertia certificate.

For the exact stored Grushin matrix G, the shifted Hermitian dilation has
inertia (m,m,0) exactly when s_min(G) > alpha. An exact pairwise Hadamard
congruence stabilizes the diagonal, and independently shifted sparse LU
factors are converted to exact Hermitian L D L* centers. Componentwise
channel enclosures, threshold assembly, sparse-LU backward error, and the
LU-to-LDL* conversion are included in the final Weyl sandwich.

Rigorous exact-target closures:

- sigma = 1e-2, Grushin dimension 4109;
- sigma = 4e-3, Grushin dimension 10255;
- sigma = 2e-3, Grushin dimension 20497.

At the third scale the two total errors are 1.43035e-3 and 1.43152e-3,
both below the selected shift 1.5e-3. The threshold is chosen above
2 / K_*^-, so every certified lifted inverse is strictly below half of the
preceding RH-29 admissible budget.

The result is finite-dimensional and local to three selected stored scales.
It does not prove a full-contour root count, a continuum limit, a
Hilbert--Pólya construction, an identification with zeta zeros, or the
Riemann hypothesis.

## Reproduce

Run the unit and archive tests:

~~~bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
~~~

Fresh factorization runs (the third command is a tens-of-minutes,
roughly 26 GiB calculation on the archived machine):

~~~bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python experiments/run_inertia_pilot.py \
  --sigma 1e-2 --exact-channel-enclosure --threshold-factor 2 \
  --pair-order colamd --bracket-shift 1e-2 --bracket-only \
  --output results/fresh_exact_target_sigma_1e-2.json

PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python experiments/run_inertia_pilot.py \
  --sigma 4e-3 --exact-channel-enclosure --threshold-factor 2 \
  --pair-order colamd --bracket-shifts 5e-4 5.6e-4 --bracket-only \
  --output results/fresh_exact_target_sigma_4e-3.json

PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  python experiments/run_inertia_pilot.py \
  --sigma 2e-3 --exact-channel-enclosure --threshold-factor 2 \
  --pair-order colamd --bracket-shift 1.5e-3 --bracket-only \
  --output results/fresh_exact_target_sigma_2e-3.json
~~~

Rebuild summaries, figures, manuscript, and archive verification:

~~~bash
PYTHONDONTWRITEBYTECODE=1 MPLCONFIGDIR=/tmp/rh31-mpl \
  python experiments/make_summary.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf sparse-threshold-inertia.pdf
PYTHONDONTWRITEBYTECODE=1 python experiments/verify_archives.py
~~~

Principal certificate archives:

- results/exact_target_inertia_sigma_1e-2_op24.json
- results/exact_target_inertia_sigma_4e-3_op24.json
- results/exact_target_inertia_sigma_2e-3.json
- results/threshold_inertia_summary.csv
- results/summary.json
- results/archive_verification.json

The original 32N pilots and failed symmetric middle-scale brackets remain
archived. The 24N derived files record their source SHA-256 hashes.

The formal PDF is sparse-threshold-inertia.pdf.
