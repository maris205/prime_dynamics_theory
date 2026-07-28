# TPC-186: The Dyadic Shadow Equals a Local Oscillation Obligation

## Exact result

Every prefix inside a dyadic block is the left block-boundary prefix plus one local consecutive-block increment.  Consequently TPC-159 boundary control closes the full endpoint target exactly when a named-atom local oscillation bound is added.  No averaging or exceptional-endpoint deletion is permitted.

```text
classification = REDUCTION_L1
verdict = LOCAL_OSCILLATION_IS_EXACT_GAP
selected_route = O161.bad_endpoint_pointwise_fixed_atom
smallest_missing = FIXED_ATOM_LOCAL_MAXIMAL_INCREMENT_POWER_SAVING

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
python experiments/tpc186_dyadic_shadow_local_oscillation.py
python experiments/tpc186_dyadic_shadow_local_oscillation.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
