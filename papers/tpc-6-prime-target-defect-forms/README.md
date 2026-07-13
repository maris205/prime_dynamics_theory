# TPC-6: Prime-target defect forms

This directory contains the sixth paper in the twin-prime-correlation (`tpc`)
theory branch.

## Rigorous scope

The paper makes the transition from a finite target-roughness kernel to
finite-resolution target von Mangoldt forms and their congruence-layer
operators. It proves:

- an exact divisor and Dirichlet-character expansion for the truncated target
  weight `Lambda_{<=R}(mn+h)`;
- an arithmetic-involution realization of each local congruence layer, whose
  spectrum is contained in `+1/-1`;
- a comparison showing that the old absolutely summable conductor majorant
  cannot be transplanted verbatim after target-prime insertion;
- a classical Bombieri--Vinogradov evaluation of the signed source-divisor
  truncation up to `X^(1/2)/(log X)^B`, whose main term has the full formal
  Hardy--Littlewood pair singular-series constant;
- an exact ledger making the remaining fixed-shift conjecture equivalent to
  cancellation of a complementary large-divisor Moebius--prime tail;
- a periodic-minorant collapse theorem and an exact finite-CRT nullspace
  witness for target primality and Liouville parity.

The large-divisor tail is not estimated. The paper proves no twin-prime lower
bound, no new Bombieri--Vinogradov theorem, and no Type-II breakthrough. The
finite obstruction applies to fixed local resolution only.

## Files

- `main.tex` and `sections/` -- manuscript source
- `references.bib` -- bibliography
- `experiments/` -- exact integer/rational certificate and tests
- `prime-target-defect-forms.pdf` -- compiled manuscript

## Build

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Test

From `experiments/`:

```bash
python exact_defect_certificate.py --output data/exact-certificate.json
python -m unittest -v test_exact_defect_certificate.py
```
