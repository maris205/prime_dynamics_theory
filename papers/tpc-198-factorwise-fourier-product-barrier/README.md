# TPC-198: A Sharp Black-Box Barrier from Factorwise Fourier Bounds to a Product Twist

## Result

Rudin--Shapiro coefficients give two factors with uniform square-root Fourier bounds whose modulated pointwise product has a full linear resonance at a prescribed atom.  This stops only the factorwise-single-Fourier black-box implication.

```text
classification = METHOD_OBSTRUCTION_L1
verdict = STOP_SCOPED
first_missing = ARITHMETIC_TWO_FACTOR_COUPLING_THEOREM
next_route = TWO_MOBIUS_PRODUCT_FOURIER_ROUTE
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
python experiments/tpc198_factorwise_fourier_product_barrier.py
python experiments/tpc198_factorwise_fourier_product_barrier.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
