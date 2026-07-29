# TPC-203: MVP10 after Per-Packet Formula Completion and the Fixed-Atom Subgate Audit

## Result

MVP10 imports TPC-194--202 fail-closed.  The per-packet direct formula is complete, but the production crosswalk and named-atom power theorem are absent.  Both O161 pointwise parents and the global architecture remain open; fixed-atom endpoint credit is zero.

```text
classification = MVP10_INTEGRATION
verdict = NOT_TESTABLE
global_first_missing = H1.source_backed_local_occurrence_edge_family
selected_pointwise_first_missing = LITERAL_FIXED_ATOM_ARITHMETIC_CANCELLATION
direct_production_first_missing = SOURCE_LOCKED_PRODUCTION_PACKET_PREFIX_CROSSWALK
next_route = SEARCH_FOR_NAMED_PACKET_CROSSWALK_OR_GENUINE_FIXED_ATOM_THEOREM
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

## Exact reopen triggers

- `DIRECT`: formula-complete production target plus a theorem-backed natural
  `q/N` fixed-atom positive-power mechanism preserving all six axes and all losses.
- `METRIC`: source-locked named atom, exact packet schedule, and a
  schedule-specific exceptional-limsup avoidance theorem.
- `BAD_ENDPOINT`: literal fixed-atom local-increment cancellation theorem.
- `STRUCTURAL`: theorem-backed local-occurrence edge.
- `DECLARED_CORPUS`: genuinely new primary theorem corpus, while TPC-193 V1
  remains `STOP_SCOPED`.


## Reproduce

```powershell
python experiments/tpc203_mvp10_direct_pointwise_route_decision.py
python experiments/tpc203_mvp10_direct_pointwise_route_decision.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
