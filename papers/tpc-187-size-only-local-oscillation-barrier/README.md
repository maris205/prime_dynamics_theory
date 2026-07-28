# TPC-187: A Sharp Barrier for Size-Only Control of Local Oscillation

## Exact result

The triangle inequality gives only block length after q/T normalization.  A constant-sign synthetic sequence attains that bound, so boundedness and support size alone cannot yield any fixed-X power saving.  This stops only the size-only local oscillation method.

```text
classification = OBSTRUCTION_L1
verdict = STOP_SCOPED
selected_route = O161.bad_endpoint_pointwise_fixed_atom
smallest_missing = ARITHMETIC_CANCELLATION_INPUT_FOR_LOCAL_INCREMENTS

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
python experiments/tpc187_size_only_local_oscillation_barrier.py
python experiments/tpc187_size_only_local_oscillation_barrier.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
