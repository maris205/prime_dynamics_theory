# RH-171: Ten-Layer Physical Riesz-Interface Review

RH-171 assembles RH-162--170 into a single conditional closure theorem for
physical interface `R`.

The theorem has four physical leaves:

```text
X_phys : canonical ambient realization of reset packets
D_phys : validated finite block/resolvent/coupling data
K_phys : uniform Schur and directional graph margins
H_phys : shellwise common-coordinate summable transport
```

If all four hold, every fixed reset shell lifts to a same-rank Riesz shell,
the graph maps remain controlled, and the shells form a coherent all-level
atlas.  This is the corrected rank-growing meaning of interface `R`.

All analytic implications behind this theorem are proved in RH-162--170.
None of the four physical leaves is currently proved.  The inclusion-minimal
completion bundle is therefore

```text
{X_phys, D_phys, K_phys, H_phys}.
```

The aggregate audit verifies 3,584 finite matrix cases plus 63 exact
rank-change witnesses with zero recorded failures.  These checks validate
the formulas, not the physical leaves.  The next target is `X_phys`; before
it exists, transfer-space bi-Ritz residuals are not type-defined.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_r_frontier_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf ten-layer-physical-riesz-interface-review.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
