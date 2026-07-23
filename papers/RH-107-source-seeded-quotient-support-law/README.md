# RH-107: source-seeded quotient-support law

This directory contains the one-hundred-and-seventh RH-layer paper:

> *Source-Seeded Weak-Mode Support Laws: Coarse-Boundary Quotients and a
> Finite-Extrapolation Barrier*

## Main theorem

For the four-direction adaptive selector,

```text
width < 4  <=>  s4/s1 < tau.
```

If `s4/s1 >= tau` for every update beyond a finite level `k_*`, then the
fine-scale weak-mode support is empty and the total quotient price reduces to
a finite coarse sum. If that coarse sum fits the endpoint allowance, no stop
is needed; otherwise the stopped full-width fallback remains safe.

## Five-scale result

Event counts across `sigma=(0.16,0.08,0.04,0.02,0.01)` are:

```text
tau=1e-8: (4,1,0,0,0)
tau=1e-6: (7,2,2,0,0)
tau=1e-4: (8,8,6,0,0)
```

- 360 selector comparisons all agree with the archived adaptive widths;
- all three observed fine supports are empty;
- minimum fine support margin: `7.364934`;
- 38 local gap certificates are green;
- worst stopped endpoint ratio: `1.006033`.

## Boundary

Finite anchors do not prove eventual support separation. Two infinite
cross-ratio sequences can agree on every audited level and then either stay
above or fall below the cutoff forever. An analytic source-seeded fourth-mode
lower bound remains open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_support_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_support_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf source-seeded-quotient-support-law.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
