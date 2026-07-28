# RH-235: Trace powers versus Hilbert--Schmidt mass

The Frobenius route in RH-229 controls a singular-value budget, while the
`det_2` logarithm uses the spectral trace powers

    log det_2(I-zB) = - sum_{n>=2} tr(B^n) z^n/n.

These quantities can be radically different for nonnormal operators.  A
strictly upper-triangular nilpotent shift has Hilbert--Schmidt squared norm
`N-1`, but every trace power and its `det_2` are trivial.

For the RH-222 cloud complements, the maximum extracted second-trace modulus
is only `0.12952`, while the inherited Hilbert--Schmidt squared upper bound
reaches `308.75`; their largest ratio is about `2.36e6`.

Thus RH-229 does not rule out a determinant route.  It rules out one uniform
singular-value estimate.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_trace_hs_separation_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf trace-vs-hilbert-schmidt-separation.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
