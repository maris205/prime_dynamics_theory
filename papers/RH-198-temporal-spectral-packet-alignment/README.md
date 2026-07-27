# RH-198: Temporal--Spectral Packet Alignment

The accepted temporal windows approach the exact canonical four-mode packet
as their start moves later.  All four right/left subspace-gap sequences have
negative fitted log slopes, their final values are their minima, and their
descriptive per-step ratios lie between about `0.830` and `0.850` with
`R^2 >= 0.899`.  Root errors decay faster, with per-step ratios about
`0.695--0.739`.

The paper proves the exact graph-coordinate formula
`tan(theta_max)=||G||` and gives a conditional Krylov convergence mechanism:
a radial spectral gap plus a uniformly invertible selected-mode Vandermonde
block forces graph decay.  The physical audit establishes only a finite
signal; it does not prove those uniform hypotheses or an asymptotic rate.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_packet_alignment_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf temporal-spectral-packet-alignment.pdf
```
