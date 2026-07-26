# RH-170: Rank-Growing Riesz Shell Atlas

RH-170 proves a necessary route correction.  If two finite-rank idempotents
have different ranks, then

```text
||P-Q|| >= 1.
```

Therefore the full moving-cloud Riesz projections cannot converge in
operator norm while their cloud degree grows.  The fixed-rank theorem of
RH-169 must be applied shell by shell.

For disjoint Riesz contours, if every fixed shell has summable transported
projector defects, its projection converges in norm.  The limiting shell
projections remain mutually annihilating, and every finite partial cloud is
an idempotent with the expected rank.  No bounded infinite sum is asserted.

This is a positive shellwise construction plus a negative global-norm
result.  It sharpens the meaning of physical interface `R`; it does not prove
the required physical shell estimates.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_shell_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf rank-growing-riesz-shell-atlas.pdf
```
