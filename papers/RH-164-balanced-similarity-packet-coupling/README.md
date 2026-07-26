# RH-164: Balanced-Similarity Packet Coupling

For the block operator `[[A_P,B],[C,A_Q]]`, conjugation by
`diag(t I_P,I_Q)` changes the directed couplings to `t b` and `c/t`.
RH-164 proves the exact scalar optimum

```text
t_* = sqrt(c/b),       min max(t b,c/t) = sqrt(b c).
```

This converts the RH-161 Neumann rank gate into

```text
max(a,d) sqrt(b c) < 1.
```

The paper also records the price of returning to the original Hilbert norm:
the projector bound is multiplied by `max(t_*,1/t_*)`.  Hence balancing can
rescue rank while producing a poor graph certificate.  This separates a
genuine spectral statement from a conditioning statement.

The Schur product of RH-163 remains the sharper rank test when packet and
complement resolvents are very different.  No physical scale law is proved.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_balance_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf balanced-similarity-packet-coupling.pdf
```
