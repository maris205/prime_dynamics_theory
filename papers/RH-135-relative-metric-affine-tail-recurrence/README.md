# RH-135: Relative-Metric Affine Tail Recurrences

This paper converts the raw RH-134 recurrence into the exact scalar law

`gamma_next^2 <= rho gamma^2 + q`.

It proves sharp formulas for metric amplification and forcing amplification,
plus sharp obstructions showing that tiny raw decay/forcing need not remain
small after normalization by a weak target Gramian.

Audit result: all 330 recurrences pass, but only 51/216 recurrent nonzero-tail
updates admit any subunit `rho`; 165 are metric-blocked.  Every one of the 75
nontrivial feasible updates has optimized fixed floor below `4.7e-6`.

Reproduce with:

```bash
/root/math/.venv/bin/python experiments/build_relative_affine_audit.py --smoke
/root/math/.venv/bin/python experiments/build_relative_affine_audit.py
/root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf main.tex
cp main.pdf relative-metric-affine-tail-recurrence.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
```
