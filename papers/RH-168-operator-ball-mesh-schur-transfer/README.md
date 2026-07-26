# RH-168: Operator-Ball Mesh--Schur Transfer

RH-168 combines contour interpolation and matrix uncertainty in one exact
denominator.  If `T` lies within operator norm `eta` of a nominal block
`T_hat`, every contour point is within `h_k` of a sample `z_k`, and
`||(z_k-T_hat)^(-1)|| <= m_k`, then

```text
m_k (h_k + eta) < 1
```

implies

```text
||(z-T)^(-1)|| <= m_k / (1-m_k(h_k+eta)).
```

For a fixed packet projection, the same operator ball enlarges each directed
coupling by at most `eta`.  These formulas produce a robust finite Schur
gate for the unknown exact operator.

A 256-case dense audit has no transfer failure.  The theorem is rigorous,
but the archived audit uses ordinary floating arithmetic; an actual physical
certificate still needs outward operator and inverse balls.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_operator_ball_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf operator-ball-mesh-schur-transfer.pdf
```
