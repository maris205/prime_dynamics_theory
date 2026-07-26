# RH-162: Ambient-Realization Reset--Riesz Gate

RH-162 isolates a type obligation hidden inside physical interface `R`.
The RH-160 reset packets are spectral packets of source-memory Gram matrices,
whereas the RH-80 cloud is a Riesz subspace of a noisy transfer operator.
Equal rank does not identify those ambient spaces.

Let `J:E->H` be an isometry, let `P` reduce a source operator `M`, and put
`P_hat=J P J*`.  If

```text
D  = A J - J M,
D* = A*J - J M*,
```

then the two off-packet couplings satisfy

```text
||(I-P_hat) A P_hat||  <= ||D P||,
||P_hat A (I-P_hat)||  <= ||D* P||.
```

Thus a primal/adjoint ambient realization supplies exactly the two coupling
inputs needed by the later Schur--Riesz certificate.  Without `J`, source
packet data alone imply no coupling bound; a two-dimensional witness proves
this non-identifiability.

The theorem is abstract and exact.  No canonical physical realization `J`
is constructed here, so interface `R` and Gate `A` remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_realization_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf ambient-realization-reset-riesz-gate.pdf
```
