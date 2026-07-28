# RH-247: Separate-Absolute Majorant Barrier

The grouped quotient trace is small because physical and atomic sectors
cancel.  If absolute values are taken before that cancellation, the Perron
atomic sector alone forces

```text
U_n >= |p_sigma|^n = r_H^(-n),   r_H=0.85.
```

Therefore this cancellation-blind majorant cannot have a subunit geometric
rate.  On all 352 archived endpoint/order cases (32 endpoints, orders 2--12),
the trace-sector separate majorant has root rates `1.253165378203787` through
`3.5568338003788416`, all above one.  Its ratio to the signed residual ranges
from `42.68449383956666` to `7.802289221403802e15`.

The audit uses the smaller quantity formed from absolute full traces and
absolute atomic/cloud power sums.  A physical periodic-loop absolute
integral is at least as large, so it cannot repair this barrier.  The result
rules out only cancellation-blind absolute majorants; signed quotient loops
and grouped complex cancellations remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_absolute_majorant_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf separate-absolute-majorant-barrier.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
