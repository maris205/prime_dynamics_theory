# RH-180: Cyclic-Cloud Riesz-Shell Theorem

For a doubled reduced cycle of length `L`, radius `rho`, and root half-spacing
`s_L=rho sin(pi/L)`, RH-180 gives an explicit conditional Riesz theorem.

If a physical packet block is within `epsilon<delta<s_L`, complement disks
are resolvent-free with bound `d`, and

```text
d ||B|| ||C|| / (delta-epsilon) < 1,
```

then every root circle encloses a Riesz shell of rank exactly two.

The audit contains 192 complex matrices and 1,248 shell contours with zero
rank or certificate failures.  No physical embedding or outward transfer
budget is supplied.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 /root/math/.venv/bin/python experiments/run_cycle_riesz_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf cyclic-cloud-riesz-shell-theorem.pdf
```
