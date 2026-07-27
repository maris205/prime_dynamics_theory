# RH-191: Ten-Layer Biorthogonal Frontier Review

RH-191 reviews RH-182--RH-190.  The simplest orthogonal temporal-clock branch
fails at all 126 audited anchors, including after optimal phase/scalar wrap.
A balanced source/observation construction then yields an exact
biorthogonal algebra and a local `sigma=0.01, L=4` candidate: 12 of 38 local
windows pass the predeclared two-sided residual gate.

That candidate is poorly transverse.  Coarse conditioning and singular-value
clipping both fail, but a directional coupling product survives in eight
windows.  The exact oblique Feshbach determinant identity is proved; the
universal norm-only complement bound fails everywhere.  The next genuine
frontier is therefore a validated contour inverse for the physical
complement block.

The corrected orthonormal-coordinate audit uses `||D|| <= chi ||A||`; even
this sharper bound has zero successes.  Any later Riesz count must retain the
identity `N_A=N_K+N_D` until the complement count is separately shown to
vanish.

The aggregate machine ledger records 2,960 finite items and zero formula or
identity failures.  This is a reproducibility count, not evidence for an
all-level theorem.  Gate A and Gates B--E remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_biorthogonal_frontier_review.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf ten-layer-biorthogonal-frontier-review.pdf
```
