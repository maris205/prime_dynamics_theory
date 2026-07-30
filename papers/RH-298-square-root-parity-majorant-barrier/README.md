# RH-298: Square-root parity majorant barrier

Combining fixed-order Gaussian localization with the exact negative-parity
boundary law gives, for each fixed n,

    (c^H_(sigma,n)-c^H_n)/sqrt(sigma)
      -> (-1)^n n C_* r_H^(-n).

At odd pre-alias orders the counterloop moment is zero, so this is also the
fixed-order leading law in the full-trace constituent e_(sigma,n).

The parity eigenvalue itself is a scalar and can be followed uniformly for
n=O(log(1/sigma)).  If one takes its absolute contribution separately, its
weighted odd-order budget has exponential rate

    b log(R/r_H) - 1/2

on h_sigma=ceil(b log(1/sigma)).  At the RH-292 minimal bridge slope this is

    0.8990081854606016 > 0.

Therefore a proof that separately absolute-majorizes raw trace error and
parity correction cannot close the bridge.  The actual combined error may
still cancel; RH-298 does not prove that E_sigma diverges.

## Reproduction

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
    latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
    cp main.pdf square-root-parity-majorant-barrier.pdf
