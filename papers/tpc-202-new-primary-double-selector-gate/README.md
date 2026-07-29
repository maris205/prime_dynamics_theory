# TPC-202: A New Primary-Source Audit: Two Averaged Selectors Still Do Not Select One Physical Packet

## Result

Menon's 2026 Theorems 1.4 and 1.5 sharpen an origin-averaged single-Liouville Fourier bound and a shift-averaged Liouville correlation bound.  Their combination does not select the prescribed affine relation and deterministic packet simultaneously.

```text
classification = PRIMARY_SOURCE_AUDIT_L1
verdict = SCREENED_NON_DIRECT_ZERO_ELIGIBLE
first_missing = THEOREM_SELECTING_PRESCRIBED_ORIGIN_SHIFT_RELATION_AND_PACKET
next_route = NEW_PRIMARY_FIXED_PACKET_SELECTOR_SEARCH
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
python experiments/tpc202_new_primary_double_selector_gate.py
python experiments/tpc202_new_primary_double_selector_gate.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
