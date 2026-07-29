# TPC-196: Rational Atoms after Residue Splitting: Determinant Inflation and the DFT Ledger

## Result

A rational twist of conductor R splits into R residue-class sums. On each class the two affine slopes have gcd exactly R and the determinant becomes 2R.  One Fourier mode is one DFT coordinate, not control of every residue sum.

```text
classification = ALGEBRAIC_REDUCTION_L1
verdict = PROVED_RESIDUE_SPLIT_WITH_DETERMINANT_2R
first_missing = UNIFORM_ALL_RESIDUE_CLASS_CANCELLATION_OR_DIRECT_MODE_THEOREM
next_route = RATIONAL_ATOM_THEOREM_SCREEN
TPC193_DECLARED_CANDIDATE_MECHANISM_CORPUS_V1 = STOP_SCOPED
bad_endpoint_O161_parent = OPEN
direct_twist_O161_parent = OPEN
global_architecture = OPEN
fixed_atom_decay_obtained = false
named_atom_endpoint_credit = 0
strict_1/400 = UNPAID
```

This is an L0/L1 artifact. It claims no program-positive L2 result,
prime-pair lower bound, or twin-prime theorem.


## Reproduce

```powershell
python experiments/tpc196_rational_atom_residue_determinant_ledger.py
python experiments/tpc196_rational_atom_residue_determinant_ledger.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
