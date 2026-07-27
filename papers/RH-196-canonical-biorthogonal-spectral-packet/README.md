# RH-196: Canonical Biorthogonal Spectral Packet

The source--observation Riesz channels of RH-195 determine exact right and
left invariant spaces.  Applying the cross-Gram SVD to these spaces gives a
balanced packet with

```text
W^* V = I,
L_A V = V K,
L_A^* W = W K^*,
sigma(K) = {selected physical eigenvalues}.
```

Both directed residuals vanish exactly.  The balanced frames attain the
smallest possible norm product `1/sigma_min` among biorthogonal coordinates
on the same two channel spaces.  The packet determinant and every power
trace are the exact finite spectral determinant and trace of the selected
source-observable modes.

A 140-case complex nonnormal audit records zero failures.  The construction
is canonical relative to the chosen physical spectral contours, source, and
observation; selecting those contours intrinsically and transporting them
across levels remain open.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_canonical_packet_identity_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf canonical-biorthogonal-spectral-packet.pdf
```
