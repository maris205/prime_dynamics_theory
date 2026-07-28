# RH-246: Block-Power Quotient Envelope Criterion

RH-245 gives the exact quotient traces `tau_n=Tr(C^n)`, but every audited
one-step quotient norm is larger than one.  This paper states the correct
block criterion: if, for one integer `m`, the trace norm of `C^m` is uniformly
bounded and its operator norm is uniformly below one, then the quotient trace
sequence has a geometric envelope.  The theorem also gives an explicit
logarithmic tail bound for the relative `det_2` series.

On the 17 RH-245 endpoints of dimension at most 512, the finite `m=12`
diagnostic has

```text
eta_12 <= 1.3698766308677744e-5
K_12   <= 1.5684781027206807e-5
q_12   = 0.3932995547481413
tail at R=1 <= 1.7991531976413385e-5.
```

The first contractive power is 3--7 across those endpoints.  These constants
are maxima on a 17-point finite subbatch, not uniform small-noise constants;
the all-order envelope remains open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_block_power_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf block-power-quotient-envelope-criterion.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
