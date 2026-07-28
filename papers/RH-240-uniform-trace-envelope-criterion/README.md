# RH-240: Uniform trace-envelope criterion

Let `tau_n(sigma)` be the cloud-extracted complement traces.  If constants
`M` and `q` satisfy

    |tau_n(sigma)| <= M q^n,  n>=2,

uniformly in `sigma`, then on every disk `Rq<1`,

    |log R_sigma(z)| <= M (Rq)^2 / (2(1-Rq)).

Hence the relative regularized determinants form a locally bounded, zero-free
normal family on that disk.

For the observed orders 2--12, unit-amplitude rates are `0.35989` globally
and `0.14377` on the fine endpoints.  If those same envelopes held for all
higher orders, the corresponding unit-disk log bounds would be `0.10117` and
`0.01207`.  They are conditional extrapolations: order thirteen is the first
uncontrolled coefficient.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_trace_envelope_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf uniform-trace-envelope-criterion.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
