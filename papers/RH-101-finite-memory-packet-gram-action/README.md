# RH-101: finite-memory packet Gram action

This directory contains the one-hundred-and-first RH-layer paper:

> *Finite-Memory Packet Actions for Normalized Gram Recursions: Exact
> Matrix-Free Expansion and a Five-Snapshot Frozen Closure*

## Main theorem

For

```text
Q_t = X_t* X_t / ||X_t||_F^2,
G_t = Q_t + eta G_(t-1),   G_(-1)=0,
```

and every packet `V`,

```text
G_t V = sum_(j=0)^(m-1) eta^j X_(t-j)*(X_(t-j)V)/||X_(t-j)||_F^2
        + eta^m G_(t-m)V.
```

The full-history formula is exact and never forms an ambient Gram matrix.  If
the packet has orthonormal rank `r`, dropping the old history gives

```text
||error||_F <= eta^m sqrt(r)/(1-eta).
```

The discarded operator is positive, so the same geometric tail controls
residual energies and Ritz compressions.

## Frozen-prefix result

Across all 120 RH-94 updates with `eta=1/512`:

- full-history state actions match assembled Gram actions within `8.88e-16`;
- every discarded action satisfies its geometric theorem bound;
- depth four passes 9/10 endpoint gates and has worst ratio `1.05492958`;
- depth five is the first tested common depth passing all 10 gates, with worst
  ratio `1.00117186`;
- action agreement near machine precision can still coexist with endpoint
  projector distance `1.75e-4`, so a gap-aware quotient theorem remains
  necessary.

This closes ambient Gram assembly, not state-packet multiplication, uniform
Ritz stability, Stage A, Hilbert--Polya, zero identification, or RH.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_finite_memory_gram_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_finite_memory_gram_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf finite-memory-packet-gram-action.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
