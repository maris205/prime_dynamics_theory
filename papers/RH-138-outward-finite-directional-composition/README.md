# RH-138: Outward Finite Directional Composition

This paper joins the RH-137 finite-horizon tail envelope to the directional
normalized base through two outward Loewner residuals:

1. the raw moving-frame tail recurrence;
2. the normalized bridge from `D <= yG` to `D' <= y'G'`.

It also proves the outward base bound

`sqrt((lambda_min(Ghat)-rG)_+ / (lambda_max(Ghat)+rG))`.

On the frozen 80-digit reference assembly, independently rounded 40-decimal
matrices and archived norm radii certify all 330 raw and bridge residuals.
The resulting directional lower is positive on 328 transitions and 28 full
chains; 21 terminal lowers exceed `1e-8`.

Precision is a real gate: fp64 preserves a positive outward base on 320/330
snapshots, decimal-16 on 318, decimal-18 on 324, and decimal-20 on all 330.

Reproduce with:

```bash
/root/math/.venv/bin/python experiments/build_outward_composition_audit.py --smoke
/root/math/.venv/bin/python experiments/build_outward_composition_audit.py
/root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf main.tex
cp main.pdf outward-finite-directional-composition.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
```
