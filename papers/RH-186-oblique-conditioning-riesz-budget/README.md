# RH-186: Oblique Conditioning Riesz Budget

RH-186 proves that the balanced packet's intrinsic coordinate condition is
`chi=1/sigma_min(Q_L^*Q_R)` and audits the sufficient gate
`chi*max(epsilon_R,epsilon_L)<1`.

Although RH-185 has 12 raw residual successes, the minimum amplified residual
is `10.253`; none of 126 windows passes the conditioning-aware gate. The
condition number ranges from `48.2` to `4.33e5`.

This rejects a coarse maximum-norm budget, not a sharp directional Schur
product or an exact contour resolvent.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_oblique_conditioning_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf oblique-conditioning-riesz-budget.pdf
```
