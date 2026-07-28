# RH-250: Anchored Head--Analytic Tail Gluing Criterion

RH-240 reduces local determinant convergence to two independent obligations:
a finite coefficient head and a uniformly controlled analytic tail.  This
paper states the exact gluing estimate and audits the current data against it.

For the RH-248 relaxed shell head, even the convex box relaxation has zero
anchored passes at all 32 endpoints.  RH-246 supplies only a finite 17-endpoint
12-block tail diagnostic.  The smallest relaxed head distance is
`0.14649763462315904`, while the finite unit-disk tail bound is
`1.7991531976413385e-05`; the ratio is `8142.588125081018`.  The target
numerator tail is not yet bounded.  Consequently the current batch has zero
complete head/tail certificates.

The result is a precise route stop for this candidate class, not a proof that
no future anchored cloud or tail theorem exists.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_head_tail_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf anchored-head-analytic-tail-gluing-criterion.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
