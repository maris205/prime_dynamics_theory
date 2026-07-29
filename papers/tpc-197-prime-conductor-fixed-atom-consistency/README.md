# TPC-197: Prime Conductors versus a Fixed Atom: Recurrence and Period-Corridor Separation

## Result

A fixed nonzero rational atom cannot be represented in lowest terms with infinitely many distinct prime conductors q_X.  The variable q_X branch also lies outside the source-locked polylogarithmic exact-period corridor; the conductor-one branch remains possible but has no occurrence or packet schedule theorem.

```text
classification = CONSISTENCY_BARRIER_L1
verdict = PROVED_NONZERO_FIXED_RATIONAL_ATOM_CANNOT_RECUR_ACROSS_UNBOUNDED_PRIME_CONDUCTORS
first_missing = SOURCE_LOCKED_CONDUCTOR_ONE_OCCURRENCE_PACKET_SCHEDULE_AND_RANGE_ADMISSIBILITY
next_route = FIXED_ATOM_OCCURRENCE_EDGE
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
python experiments/tpc197_prime_conductor_fixed_atom_consistency.py
python experiments/tpc197_prime_conductor_fixed_atom_consistency.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
