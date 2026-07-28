# TPC-184: A Literal Contract for the Bad-Endpoint Pointwise Fixed-Atom Target

## Exact result

The bad-endpoint target is frozen as a q/T-normalized cumulative actual-core sum at the prescribed atom, uniformly over every prefix endpoint and deterministic scale.  TPC-159 supplies only the complement of its dyadic shadow; TPC-169 supplies all prefixes only in phase L2.  Neither matches the contract.

```text
classification = CONTRACT_L0_L1
verdict = TARGET_WELL_TYPED_OPEN
selected_route = O161.bad_endpoint_pointwise_fixed_atom
smallest_missing = POINTWISE_NAMED_ATOM_CONTROL_INSIDE_TPC159_DYADIC_SHADOW

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
python experiments/tpc184_bad_endpoint_literal_target_contract.py
python experiments/tpc184_bad_endpoint_literal_target_contract.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
