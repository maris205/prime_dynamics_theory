# RH-199: Source-Channel Determinant and Trace Factorization

The canonical packet carries two distinct ledgers:

- unweighted spectral data `tr(K^q)=sum lambda_j^q` and
  `det(zI-K)=prod(z-lambda_j)`;
- residue-weighted physical moments
  `<c,K^q b>=sum r_j lambda_j^q`.

The transfer function is encoded by the exact rank-one determinant ratio

```text
det(zI-(K+b c^*)) / det(zI-K) = 1 - c^*(zI-K)^(-1)b.
```

A 240-case nonnormal audit verifies the determinant lemma, weighted moments,
and Newton traces with zero failures.  In the physical late windows, the
temporal determinant error is below `1e-4` and the maximum relative
power-trace error through order eight is below `8e-4`.

These are finite source-channel traces, not von Mangoldt prime-power traces
and not a zeta spectral determinant.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_channel_determinant_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf source-channel-determinant-trace-factorization.pdf
```
