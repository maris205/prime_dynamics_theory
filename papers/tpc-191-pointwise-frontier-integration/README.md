# TPC-191: Integration of the Two Pointwise Fixed-Atom Audits

## Exact result

The bad-endpoint route reduces exactly to fixed-atom local oscillation; the direct route requires pointwise arithmetic beyond Parseval.  Size-only and uncontrolled metric-to-atom methods are scoped stops, not route stops.  Neither parent is closed and the named-atom endpoint ledger remains at zero.

```text
classification = INTEGRATION_L1
verdict = BOTH_POINTWISE_ROUTES_OPEN_METHODS_SCOPED
selected_route = BOTH_O161_POINTWISE_PARENTS
smallest_missing = LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION

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
python experiments/tpc191_pointwise_frontier_integration.py
python experiments/tpc191_pointwise_frontier_integration.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
