# RH-238: Trace-adaptive shell selection

The fixed rank schedule of RH-222 was geometric rather than determinant
intrinsic.  This paper defines a finite alternative: among shell-complete
candidate prefixes of rank at least four, select the first satisfying

    sum_{n=2}^{12} |tau_n|/n <= epsilon_sigma,
    epsilon_sigma = sigma.

All 32 archived endpoints pass.  The selected ranks range from 5 to 38, the
minimum slack is `4.73e-5`, and the two channels can differ by as many as nine
roots.  Between one and ten prefixes can satisfy the tolerance, so the
"first prefix" rule matters.

The construction is deterministic for the frozen atlas.  It does not prove
that admissible candidates exist at every smaller noise or identify the
deterministic numerator left by the quotient.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_adaptive_shell_selection.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf trace-adaptive-shell-selection.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
