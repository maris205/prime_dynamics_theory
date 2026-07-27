# RH-195: Source--Observation Riesz Channels

For an isolated simple base eigenvalue with Riesz projector `P_lambda`, the
physical source and observation select the matrix states

```text
X_lambda = P_lambda S,
Y_lambda = P_lambda^* O^*.
```

They are exact right/left eigenstates of Frobenius left multiplication and
their pairing is the scalar transfer residue

```text
<Y_lambda, X_lambda>_F = tr(O P_lambda S).
```

Different spectral channels are cross-orthogonal in this oblique pairing.
If every selected residue is nonzero, residue normalization gives exact
biorthogonal channel coordinates.  A 160-case complex nonnormal audit checks
projector resolution, residue diagonality, transfer partial fractions, and
biorthogonality with zero failures.

The theorem identifies the correct rank-one meaning of a packet root: one
source--observation channel inside an `m`-dimensional ambient eigenspace.  It
does not provide interval projectors or a uniform residue lower bound.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_riesz_channel_identity_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf source-observation-riesz-channels.pdf
```
