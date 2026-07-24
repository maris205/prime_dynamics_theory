# RH-141: Gap-Stable Spectral Packet Enclosure

This paper turns an operator-norm snapshot ball into a top-spectral-packet
certificate.  If the approximate rank-`r` gap is `g` and the snapshot radius
is `eps`, the sharp no-crossing gate is `g > 2 eps`.  Under that gate,

`||P-P_hat|| <= eps / (g-eps)`.

Canonical polar alignment converts the projector ball into a frame ball;
individual eigenvectors are deliberately not claimed stable inside a cluster.

Applied to RH-140, the universal Arb-derived balls certify four of ten
rank-four anchor packets.  Six are gap walls for the available information.
The non-certified quadratic SVD diagnostic would certify all ten, although
the coarsest right channel has only a `1.0213` crossing margin.  This sharply
identifies interval validation of quadratic SVD cancellation as the next
source-interface problem.

Reproduce with:

```bash
/root/math/.venv/bin/python experiments/build_packet_audit.py --smoke
/root/math/.venv/bin/python experiments/build_packet_audit.py
/root/math/.venv/bin/python experiments/make_figures.py
/root/math/.venv/bin/python -m pytest -q
latexmk -pdf main.tex
cp main.pdf gap-stable-spectral-packet-enclosure.pdf
/root/math/.venv/bin/python experiments/build_archive.py
/root/math/.venv/bin/python experiments/verify_archive.py
```

