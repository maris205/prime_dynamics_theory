# TPC-172 / MVP7: Occurrence--phase--atomic route decision

MVP7 dynamically imports TPC-171 and returns:

```text
Verdict = NOT_TESTABLE
FirstMissing = H1.source_backed_local_occurrence_edge_family
```

The result preserves the full seven-node selected-root blocker
antichain and the separate two-node parent-ready pointwise arithmetic
frontier.

The classifier makes two route families disjoint:

- complete `ARCHITECTURE_ROUTE` records can be selected or rerouted;
- `ARITHMETIC_SUBROUTE` records are theorem methods inside an
  architecture and can never trigger architecture rerouting.

The valid-snapshot precedence is:

```text
GO
ARCHITECTURE_INFEASIBLE
REROUTE
STOP_ROUTE
NOT_TESTABLE
ARITHMETIC_FRONTIER
OPEN
```

`INVALID` is the outer validation result. The regression suite reaches
all eight outcomes while keeping synthetic assumed predicates
disjoint from source-locked theorem evidence.

The strongest arithmetic import is an actual-core,
Lebesgue-almost-every-phase, all-prefix packet theorem. It is not a
named physical phase, program-positive L2, or strict `1/400` endpoint.

All four H9 leaves are data registries with `decay_axis=NONE`.
Identifying a literal weight, named phase, deterministic endpoint, or
normalization never creates a decay theorem.

Reproduce:

```powershell
python experiments/tpc172_mvp7_route_audit.py
python experiments/tpc172_mvp7_route_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Hashes are integrity locks only. No prime-pair lower bound or
twin-prime theorem is claimed.
