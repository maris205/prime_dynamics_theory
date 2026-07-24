# RH-139: Ten-Layer Controlled-Viability Review

This paper reviews RH-130--RH-139 and proves a revised eventual-support
theorem.  The old requirement that every transition have a subunit affine
coefficient is replaced by the weaker controlled-viability condition

`limsup y_n < 1`.

Together with a positive normalized-base liminf, this gives

`liminf B_n >= (1-sqrt(y_bar))^4 a_* > 0`.

Both the strict tail gap and the positive base liminf are sharp within the
directional candidate architecture.  The exact-matrix frontier is therefore
these two packets; source exact/interval enclosure is added for a validated
model route, and all-level outward radii are additionally needed when
assemblies are independent.

The archive review checks all nine upstream summaries and verification
records, with zero archive or forbidden-claim failures.

Reproduce with:

```bash
/root/math/.venv/bin/python experiments/build_ten_layer_review.py --smoke
/root/math/.venv/bin/python experiments/build_ten_layer_review.py
/root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf main.tex
cp main.pdf ten-layer-controlled-viability-review.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
```
