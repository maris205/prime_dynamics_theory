# RH-179: Clock--Cycle--Cloud Calibration

RH-179 proves the exact integer translation

```text
r = ceil(h) + 2,
L = N + 1,
d = h - N,
r - L = ceil(d) + 1.
```

On the seven RH-15 cloud rows, `d` lies between `1.4456` and `2.3376`, so
the formal clock-rank/cycle-length gap is always `3` or `4`.  Only
`sigma=0.01` overlaps the actual RH-151 reset atlas; there the actual rank is
7, the cycle length is 4, and the gap is 3.

The other six ranks are formal clock predictions.  No unique calibration or
asymptotic cloud-degree law is claimed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_clock_cycle_calibration.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf clock-cycle-cloud-degree-calibration.pdf
```
