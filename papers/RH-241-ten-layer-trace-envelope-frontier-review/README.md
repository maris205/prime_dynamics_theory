# RH-241: Ten-layer trace-envelope frontier review

RH-232--RH-240 decide the moving-cloud complement fork left open by RH-231.
The direct Riesz projector is numerically too ill-conditioned for a uniform
argument, but the regularized determinant admits an exact projection-free
spectral factor.  Nonnormal Hilbert--Schmidt growth is then separated from
the much smaller trace powers that actually generate `det_2`.

The batch contains 7,280 finite ledger items and zero identity failures.
Orders 2--12 support a subunit trace envelope, dual channels are coherent,
and a trace-adaptive shell selector succeeds at all 32 endpoints.  The route
still stops at the all-order tail and at coefficient identification.

Current route coordinate:

```text
projection_free_relative_det2_open_uniform_trace_envelope
```

No Gate A closure, Hilbert--Polya operator, zeta-divisor identification, or RH
conclusion is asserted.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_trace_envelope_review.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf ten-layer-trace-envelope-frontier-review.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_batch_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_batch_archive.py
```
