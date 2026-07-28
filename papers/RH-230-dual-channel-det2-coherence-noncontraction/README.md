# RH-230: Dual-Channel det2 Coherence without Cross-Scale Contraction

Selected-cloud regularized determinants are compared branch-free through
their principal logarithms on a 256-point grid in `|z|<=1`.

All sixteen left/right comparisons pass the predeclared `0.02` gate; the
maximum difference is `0.017855`. In contrast, 30 adjacent-scale differences
range from `0.04213` to `0.18366`, and neither channel contracts strictly
over the last four transitions.

Thus dual-channel coherence survives at the determinant level, but a
small-noise Cauchy family is not supported by the selected factors alone.
Unresolved-tail and moving-cloud renormalization remain necessary.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_det2_coherence_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf dual-channel-det2-coherence-noncontraction.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
