# TPC-183: The Two Pointwise Fixed-Atom Parents: A Source-Locked Interface Comparison

## Exact result

The two O161 parents have the same six-axis target signature, but different literal normalizations (q/T versus q/N).  After explicitly locking the common summand, specialization N=T proves direct twist implies the bad-endpoint target.  The reverse implication is not established. The narrower bad-endpoint parent is selected first.

```text
classification = ROUTE_DECISION_L1
verdict = PROVED_L1_INTERFACE_ONE_WAY_IMPLICATION
selected_route = O161.bad_endpoint_pointwise_fixed_atom
smallest_missing = UNIFORM_NAMED_ATOM_BAD_ENDPOINT_PREFIX_POWER_SAVING

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
python experiments/tpc183_pointwise_parent_interface_comparison.py
python experiments/tpc183_pointwise_parent_interface_comparison.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
