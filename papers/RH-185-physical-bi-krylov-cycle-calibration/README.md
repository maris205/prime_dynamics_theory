# RH-185: Physical Bi-Krylov Cycle Calibration

RH-185 applies the balanced cross-Gram construction to physical source and
observation histories over 126 windows.

Findings:

- no length-three window passes the two-sided `0.10` residual gate;
- at `sigma=0.01, L=4`, 12/38 windows pass (5 left, 7 right);
- the best residual pair is `(0.02332, 0.02498)`;
- accepted phase-grid errors are about `0.095--0.099` and radial errors are
  a few hundredths;
- oblique condition numbers remain large, roughly `194--960` in the accepted
  late windows and up to `4.33e5` overall.

This is a local floating candidate, not a physical Riesz shell or an
all-scale calibration theorem.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /root/math/.venv/bin/python experiments/run_bi_krylov_calibration.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf physical-bi-krylov-cycle-calibration.pdf
```
