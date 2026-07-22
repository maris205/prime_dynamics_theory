# RH-87: Rayleigh injection recursion

This directory contains the eighty-seventh RH-layer paper:

> *Rayleigh Injection Recursions for Dynamic Packet Energy: A Gap-Free
> Rank-Staircase Bootstrap*

## Main theorem

Let

    G_j = X_j*X_j / ||X_j||_HS^2 + eta G_(j-1)

and let `E_(j,r)` be its optimal rank-`r` Ky Fan tail energy. For any
nondecreasing rank staircase `r_j`, the previous optimal packet gives

    E_(j,r_j) <= iota_j + eta E_(j-1,r_(j-1)),

where `iota_j` is the relative energy of the new snapshot left outside the
previous packet. Iteration converts the operator problem into a scalar
convolution of one-step injection energies. No spectral gap appears.

## Five-scale audit

For the RH-86 memory packet with `eta=1/512`:

- the last one-step injection has 192-bit relative norm below `4.95e-4`;
- its captured snapshot energy exceeds `0.99999975`;
- the last injection energy is at most `17.6%` of the preceding injection;
- every binary64 recursion inequality is green;
- the packet available one update earlier still leaves terminal relative
  residual below `1.19e-3`.

The coarse right channel sets the lagged-prediction bound. At the four finer
scales the lagged terminal residual is below `4.1e-6`.

The remaining all-level theorem is now explicit: control the scalar Rayleigh
injection sequence after burn-in.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_injection_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_injection_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf rayleigh-injection-recursion.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
