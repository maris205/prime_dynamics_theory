# RH-222: Rank-Growing Conjugate Resonance-Cloud Atlas

This paper constructs the first sixteen-scale, two-channel rank-growing cloud
after the fixed-quartic obstruction of RH-219--RH-221.

The frozen target ranks are `4,6,...,34`. Candidate eigenvalues of the
folded Gaussian operators are stripped of the Perron and negative parity
modes, scaled by the inherited Hardy radius `0.85`, partitioned into real
singletons and conjugate pairs, and selected only by complete radial shells.

Across 32 endpoints, actual ranks grow strictly from 4 to 34--35. Shell
completion overshoots by at most one root, discards at most one incomplete
candidate-boundary root, has zero recorded conjugacy error, and retains a
minimum post-cloud radial gap of `7.3991e-5`.

This is a finite physical atlas. The linear rank schedule is a predeclared
stress-test schedule, not a canonical all-level law.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_cloud_atlas.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf rank-growing-conjugate-cloud-atlas.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
