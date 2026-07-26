# RH-166: Bi-Ritz Directional Riesz Graph

RH-166 turns the two Schur couplings into computable frame residuals.  For an
orthonormal packet frame `V` and `H=V* A V`, define

```text
R_right = A V - V H,
R_left  = A*V - V H*.
```

Then `||R_right||=||QAP||=c` and
`||R_left||=||PAQ||=b`.  Under `kappa=a d b c<1`, the paper proves separate
primal and dual graph-slope bounds.  The primal Riesz range is controlled by
the right residual `c`; the dual range is controlled by the left residual
`b`.  A large residual in one direction need not destroy the other graph.

This is sharper than using only the global norm `||Pi-P||` and makes the
physical data request explicit.  The archived reset atlas does not yet
supply transfer-space bi-Ritz residuals, so interface `R` remains open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_bi_ritz_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf bi-ritz-directional-riesz-graph.pdf
```
