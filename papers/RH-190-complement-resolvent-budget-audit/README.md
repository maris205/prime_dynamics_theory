# RH-190: Complement-Resolvent Budget Audit

RH-190 tests the universal norm-only route to the physical complement
inverse.  With oblique condition `chi` and an orthonormal complement frame,
the sharp elementary bound `||D|| <= chi ||A||` gives a Neumann certificate
only when the contour
minimum modulus exceeds this quantity.

All 126 audited windows fail.  The complement norm bound ranges from
`71.46` to `6.40e5`, while the contour minimum modulus is below `0.719`.
Even replacing the missing complement factor by the optimistic value one
leaves zero Schur successes; the smallest such product is `1.11159`.

This rejects a cheap norm-only certificate.  It does not show that the
actual complement spectrum meets the contour or rule out validated sample
inverses exploiting the physical matrix.

The paper also proves the concrete mesh-and-operator-ball Banach certificate
needed for the next validated inverse calculation.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_complement_budget_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf complement-resolvent-budget-audit.pdf
```
