# RH-245: Orthogonal-Quotient Superloop Compression

Let `E` be the finite algebraic root space for the selected Perron, parity,
and cloud eigenvalues, `Pi_E` its orthogonal projection, and `Q=I-Pi_E`.
Although `E^perp` need not be invariant, the quotient compression

```text
C = Q A Q |_(E^perp)
```

satisfies, for every determinant-relevant order `n>=2`,

```text
Tr(A^n) - sum_(s in selected spectrum) s^n = Tr(C^n).
```

This is an exact cancellation-preserving regrouping of the RH-242
superloops.  `Pi_E` has norm one and is not the ill-conditioned Riesz
projection.  If `A` has a Hilbert--Schmidt kernel, `C` has a signed/complex
quotient-kernel periodic-loop representation.

An ordered-Schur audit on all 17 archived endpoints of dimension at most 512
has zero rank mismatches.  The maximum trace-partition error is
`3.99e-15`, and the maximum difference from the RH-236 residual archive is
`6.31e-12`.  Orthogonal compression removes cross-block nonnormal mass, but
the quotient one-step norm remains above one at every audited endpoint.

The exact identity does not prove uniform stability of the selected root
spaces, a uniform block-power bound, the deterministic coefficient bridge,
or an all-order envelope.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_orthogonal_quotient_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf orthogonal-quotient-superloop-compression.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
