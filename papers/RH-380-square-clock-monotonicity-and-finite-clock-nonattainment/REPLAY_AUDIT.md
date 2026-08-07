# RH-380 replay audit

Status: **PASS**

The final replay used:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf square-clock-monotonicity-and-finite-clock-nonattainment.pdf
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src \
  /root/math/.venv/bin/python experiments/verify_archive.py
```

Pre-archive exact counts:

- 15 tests passed;
- 24 source locks and 24 release-blob identities passed;
- 8 deletion lengths and 24 sampled deletion checks passed;
- 3 direct run-word rows passed;
- 4 exact transition rows passed;
- 9 same-support refinement rows passed;
- 10,152 fine residues passed both density-scaling checks;
- 121,428 generic max-plus comparisons completed without ambiguity;
- 7 lcm/gap bookkeeping rows passed;
- 5 Gate flags remained false.

Archive success criteria are 28 fixed publication members, 24 external
inputs, result/source-lock identity, release-blob identity, semantic-PDF
identity, manifest rebuild identity, and zero verification failures.
