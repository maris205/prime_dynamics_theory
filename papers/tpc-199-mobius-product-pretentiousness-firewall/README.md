# TPC-199: The Möbius-Pair Sequence Is Not One Multiplicative Function

## Result

The literal sequence c(n)=mu(n)mu(n+2) is not multiplicative: c(3)=c(5)=1 but c(15)=-1.  One-function pretentious theorems therefore cannot be applied to the product merely by renaming it.

```text
classification = METHOD_OBSTRUCTION_L1
verdict = STOP_SCOPED
first_missing = THEOREM_FOR_COUPLED_VALUES_ON_TWO_AFFINE_FORMS
next_route = TWO_FUNCTION_CORRELATION_ROUTE
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
python experiments/tpc199_mobius_product_pretentiousness_firewall.py
python experiments/tpc199_mobius_product_pretentiousness_firewall.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
