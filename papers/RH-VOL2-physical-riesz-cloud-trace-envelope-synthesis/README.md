# Prime Dynamics Program, Volume II

## Physical Riesz packets, temporal clouds, and the trace-envelope frontier

Volume II synthesizes RH-161--RH-241 as eighty-one atomic sources. RH-161 is
the independent typed packet-to-Riesz assembly; the remaining eighty papers
form eight complete ten-paper phases ending at RH-171, 181, 191, 201, 211,
221, 231, and 241.

The volume records genuine analytic progress: fixed-contour packet-to-Riesz
homotopy and graph bounds, determinant-type adapters for `det_1` and `det_2`,
history/cycle identities, balanced biorthogonal and Feshbach formulas,
source-channel quotient structure, quartet shape and gauge theorems,
rank-growing reciprocal clouds, and projection-free finite `det_2` factors.

The typed Gate-A datum remains conditional on physical interfaces. At the
endpoint, RH-240 proves that a uniform all-order noisy trace envelope would
give the required normal determinant family, but RH-241 certifies only a
finite orders-2--12 ledger. Neither the moving noisy all-order envelope nor
the coefficient anchor is proved.

Finite audits, reset/history packets, synthetic quartets, and local
probability laws are not actual all-level noisy trace theorems. Gates A--E
remain false/open. This volume does not construct a Hilbert--Polya operator,
identify Riemann zeros, prove a von Mangoldt trace, prove completed-zeta
divisor equality, or prove RH.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_volume_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf physical-riesz-cloud-trace-envelope-synthesis.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
