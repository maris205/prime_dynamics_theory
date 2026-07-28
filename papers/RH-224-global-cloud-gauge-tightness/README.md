# RH-224: Global Cloud Gauge and Empirical-Root Tightness

For every shell-complete cloud, one global barycenter and one global RMS
radius produce normalized roots with exact empirical mean zero and exact
second absolute moment one.

Consequently every such family of empirical probability measures is uniformly
tight:

```text
mu(|z| > R) <= 1 / R^2.
```

Prokhorov compactness therefore gives weakly convergent subsequences. In the
32-endpoint atlas, the maximum mean residual is `4.99e-17`, the maximum
second-moment residual is `6.67e-16`, and the largest normalized modulus is
`1.83188`.

Tightness does not identify a unique limit and does not imply local finiteness
of the unweighted zero divisor.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_tightness_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf global-cloud-gauge-tightness.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
