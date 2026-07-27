# RH-184: Balanced Biorthogonal Temporal Realization

RH-184 gives a canonical finite realization for two transverse temporal
subspaces. If `H=Q_L^* Q_R=U Sigma V^*`, the balanced frames are

```text
V_R = Q_R V Sigma^{-1/2}
W_L = Q_L U Sigma^{-1/2}
```

They satisfy `W_L^* V_R=I`. Their norm product and the oblique projector norm
are exactly `1/sigma_min(H)`, which is optimal among all biorthogonal frames
on the same subspaces. Compressed spectra are gauge-covariant.

The 120-case complex audit has zero failures. Physical cross-angle and
residual bounds remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_biorthogonal_identity_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf balanced-biorthogonal-temporal-realization.pdf
```
