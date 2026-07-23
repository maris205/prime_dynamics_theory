# RH-110: finite-memory three-mode capacity

This directory contains:

> *Finite-Memory Three-Mode Capacity: A Sharp Enclosure and
> Exterior-to-Fourth-Mode Recovery*

## Main theorem

For `Lambda23=(s2/s1)(s3/s1)`, a recent spectrum `shat` and operator tail
`delta` give

```text
((shat2-delta)+ (shat3-delta)+)/(shat1+delta)^2
    <= Lambda23(K)
    <= ((shat2+delta)(shat3+delta))/(shat1-delta)+^2.
```

Dividing the RH-109 spectral-volume lower bound by this capacity upper
endpoint gives a rigorous fourth-mode lower bound.

## Archived result

- 360 threshold-update records, zero enclosure or implication failures.
- Recovered support counts exactly match direct Weyl counts:
  `113`, `109`, `98` at `1e-8`, `1e-6`, `1e-4`.
- All 78 fine updates pass every threshold.
- Minimum fine recovery efficiency relative to direct Weyl: `0.9982343`.
- Maximum fine relative capacity-interval width: `0.00176065`.

At fixed normalized volume `nu`, capacity has the sharp interval
`nu^(2/3) <= Lambda23 <= 1`; hence an independent physical capacity upper
law is still required for an all-level argument.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_capacity_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_capacity_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf finite-memory-three-mode-capacity.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
