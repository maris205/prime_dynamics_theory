# RH-90: Schur-secular sub-quarter certificate

This directory contains the ninetieth RH-layer paper:

> *Schur-Secular Sub-Quarter Contraction Certificates for Rank-One Packet
> Correction*

## Main theorem

For the `(r+1) x (r+1)` enriched compression

    H = [[A,b],[b*,d]],

the rank-one Ritz correction gain is

    Delta = d - lambda_min(H).

For any `delta >= 0` and trial vector `x`, define

    Phi_delta(x)
      = x*(A-(d-delta)I)x - 2 Re(x*b) + delta.

If `Phi_delta(x) <= 0`, then `Delta >= delta`. This follows from one Rayleigh
test vector and requires no matrix inverse, eigengap, or ambient eigensolve.

If the old predictor tail is `C`, the previous memory tail is `E`, and
`delta=C-rho E`, the same inequality certifies corrected contraction by
`rho`.

## Ten-channel audit

With `rho=0.24`:

- one channel is already below target before correction;
- all nine channels needing correction have a strictly negative 256-bit
  Schur trial form;
- the smallest gain/required-gain ratio is above `1.003`;
- direct corrected contraction is below `0.24` in all ten channels;
- the hardest Schur margin is about `2.9e-16` and remains sign-certified;
- only rank-`r` linear solves with `r <= 7` are used.

This removes the floating full-reference packet from the finite contraction
certificate. Uniform control of the Schur trial form remains open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_schur_certificate_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_schur_certificate_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf schur-secular-subquarter-certificate.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
