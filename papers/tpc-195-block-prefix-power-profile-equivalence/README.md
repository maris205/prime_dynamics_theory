# TPC-195: Block and Cumulative Prefix Power Profiles: Exact Constants and the Truncation Tail

## Result

All-scale dyadic block bounds and cumulative prefix bounds transfer in both directions with explicit sigma-dependent constants.  If small blocks are unavailable, the leftover tail is a real loss and cannot be suppressed by notation.

```text
classification = DETERMINISTIC_REDUCTION_L1
verdict = PROVED_BIDIRECTIONAL_POWER_PROFILE_TRANSFER
first_missing = ALL_SCALE_BLOCK_POWER_BOUND_ON_THE_LITERAL_PHYSICAL_SEQUENCE
next_route = APPLY_ONLY_AFTER_PRODUCTION_CROSSWALK
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
python experiments/tpc195_block_prefix_power_profile_equivalence.py
python experiments/tpc195_block_prefix_power_profile_equivalence.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
