# RH-MVP1: Conditional Prime-Dynamics Hilbert--Polya Roadmap

RH-MVP1 compresses RH-1--RH-160 into a deliberately bold but claim-safe
research architecture. It separates the rigorous dynamical foundation from
five missing macro interfaces:

```text
F (proved foundation)
  -> A (all-level intrinsic determinant)
  -> B (canonical order-sensitive scattering)
  -> C (self-adjoint generator and intrinsic counting)
  -> D (target-independent prime-power trace formula)
  -> E (complete zeta spectral-divisor identity)
```

The current completion debt is `{A,B,C,D,E}`. Gate `A` is the first missing
gate and is itself open: RH-160 supplies a conditional reset-support spine,
but not the typed all-level determinant assembly required by `A`.

## Main result and boundary

The paper proves a short conditional closure theorem. If an entire spectral
determinant of a self-adjoint operator has the same logarithmic derivative as
`Xi(z) = xi(1/2 + iz)` on one nonempty zero-free open set, and one value fixes
the multiplicative constant, then the two entire functions coincide. The
self-adjoint spectral divisor is real, so this identity would imply the
Riemann Hypothesis.

This is an implication, not evidence for its premises. RH-MVP1 does **not**
construct the all-level determinant, scattering completion, self-adjoint
operator, `T log T` counting law, von Mangoldt trace formula, zeta determinant
identity, or a proof of RH. In particular, interface `E` carries major proof
debt and cannot be treated as a routine final step.

## Corpus audit

The machine-readable audit reports:

- RH-1--RH-160 present exactly once;
- 160 README files, 160 TeX sources, and 160 directories with a PDF;
- 131 summary archives and 131 verification archives;
- 1,717 declared publication hashes replayed with zero failures;
- nine attractive shortcuts retained as explicit no-go results.

The audit verifies repository integrity and stated claim boundaries. It does
not independently re-prove every theorem in the 160-paper corpus.

## Reproduction

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_mvp_audit.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf conditional-prime-dynamics-hilbert-polya-roadmap.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```

## Layout

- `main.tex`, `references.bib`: manuscript and bibliography.
- `THEOREM_LEDGER.md`: proved, certified, conditional, and open claims.
- `UPDATED_ROADMAP.md`: post-MVP execution and stopping rules.
- `src/mvp_roadmap/`: tested completion-frontier logic.
- `experiments/build_mvp_audit.py`: 160-paper inventory and macro-gate audit.
- `experiments/make_figures.py`: publication roadmap figure.
- `experiments/build_archive.py`, `experiments/verify_archive.py`: all-corpus
  source/record and local publication hash construction/replay.
- `results/`: audit, dependency manifest, summary, and verification record.
