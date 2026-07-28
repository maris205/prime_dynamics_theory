# TPC-190: Why Parseval Does Not Evaluate a Prescribed Phase Atom

## Exact result

Continuous trigonometric polynomials can have bounded L2 norm and arbitrarily large value at a prescribed point.  The normalized Dirichlet kernels give an explicit witness.  Thus Parseval plus Chebyshev cannot prove the named-atom direct-twist target without additional arithmetic structure.

```text
classification = OBSTRUCTION_L1
verdict = STOP_SCOPED
selected_route = O161.direct_additive_twist_fixed_atom
smallest_missing = POINTWISE_ARITHMETIC_INPUT_BEYOND_PHASE_L2

fixed_atom_decay_obtained = false
named_atom_endpoint_credit = 0
strict_1/400 = UNPAID
```

The result is L0/L1 only. Any `STOP_SCOPED` declaration applies only to the
named method cell and does not stop an O161 pointwise parent or the global
architecture. No program-positive L2, prime-pair lower bound, or twin-prime
theorem is claimed.

## Reproduce

```powershell
python experiments/tpc190_parseval_to_atom_method_barrier.py
python experiments/tpc190_parseval_to_atom_method_barrier.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
