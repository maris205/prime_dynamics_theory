# RH-136: Metric-Balanced Packet Gauges

This paper proves the exact orthogonal minimax identity

`min_O lambda_max(G'^{-1/2} O^T G O G'^{-1/2}) = max_i g_i/g'_i`

for increasingly ordered Gram eigenvalues.  It gives a gauge-independent
contractivity wall for the RH-134 moving-frame recurrence, then balances that
metric endpoint against Euclidean frame forcing with a deterministic
33-candidate interpolation.

Full audit: 183/216 recurrent transitions are orthogonally contractive and
33 are impossible for every orthogonal gauge.  The Euclidean polar gauge
finds 51; the metric-balanced family finds all 183, recovering 132.  Every
reported fixed floor is below `0.002514`.

Reproduce with:

```bash
/root/math/.venv/bin/python experiments/build_metric_balanced_audit.py --smoke
/root/math/.venv/bin/python experiments/build_metric_balanced_audit.py
/root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf main.tex
cp main.pdf metric-balanced-packet-gauge.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
```
