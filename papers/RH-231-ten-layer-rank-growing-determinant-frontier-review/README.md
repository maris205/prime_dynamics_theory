# RH-231: Ten-Layer Rank-Growing Determinant Frontier Review

RH-222--RH-230 replace the fixed quartet by shell-complete clouds of ranks
4--35, prove global empirical tightness, and then show why raw or normalized
resonances cannot themselves be determinant zeros. The reciprocal variable
reconnects the atlas to RH-7's rigorous fixed-noise `det_2`.

Resolved omitted shells are controlled on the unit disk and all dual-channel
determinant comparisons pass. The route still fails at the full complement:
the only whole-matrix Frobenius certificate grows roughly as
`sigma^{-1.03}`, reciprocal local counts do not stabilize, and selected
determinants do not contract across scales.

Current route coordinate:

```text
rank_growing_reciprocal_cloud_open_uniform_complement_ideal_limit
```

The aggregate ledger contains 9,870 finite cases and zero identity failures.
Gates A--E remain open. No Hilbert--Polya, zeta-divisor, or RH conclusion is
asserted.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_determinant_frontier_review.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf ten-layer-rank-growing-determinant-frontier-review.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_batch_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_batch_archive.py
```
