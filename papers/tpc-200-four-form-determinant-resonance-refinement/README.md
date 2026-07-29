# TPC-200: The Four-Form Determinant Table and Its Unique Positive-Shift Degeneracy

## Result

The Fejer shift produces six pairwise determinants 2, s-squared times h, 2+qh, qh-2, a-squared times h, and 2. For positive h and odd q=as, the only zero is q=1,h=2, where the middle two forms coincide.

```text
classification = ALGEBRAIC_REFINEMENT_L1
verdict = PROVED_UNIQUE_DEGENERACY_Q1_H2
first_missing = NONDEGENERATE_GROWING_FOUR_MOBIUS_CORRELATION_BOUND
next_route = FEJER_NONDEGENERATE_SHIFT_ROUTE
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
python experiments/tpc200_four_form_determinant_resonance_refinement.py
python experiments/tpc200_four_form_determinant_resonance_refinement.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
