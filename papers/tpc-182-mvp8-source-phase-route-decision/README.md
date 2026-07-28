# TPC-182 / MVP8: Source-phase route decision

MVP8 dynamically imports the actual TPC-175--181 artifacts. It fails closed
unless the declared-corpus structural result, the phase-registry census, and
the metric-to-fixed-atom selector result retain their exact scopes.

## Decision

The structural batch returns:

```text
qualifying local actual-occurrence edges       0
covered production cuts                         0
unmatched production cuts                    2988
declared-corpus extraction cell       STOP_SCOPED
global occurrence architecture       NOT_TESTABLE
actual active support                NOT_TESTABLE
canonical/minimal representation     NOT_TESTABLE
```

The phase batch returns:

```text
fixed h0                                      2
named physical atom                           absent
production packet-coordinate rows             0
H9 phase registry                    NOT_TESTABLE
uncontrolled metric-to-atom          STOP_SCOPED
source-backed metric selector        NOT_TESTABLE
two O161 pointwise targets           OPEN_PARENT_READY
```

Therefore:

```text
Verdict = NOT_TESTABLE
FirstMissing = H1.source_backed_local_occurrence_edge_family
```

The seven-node structural/physical blocker antichain is unchanged. The
TPC-170 powers `X^(-delta)`, `delta<1/4`, retain the quantifier
`LEBESGUE_AE_FIXED_PHASE`; Endpoint Ledger V5 does not charge them as
named-fixed-atom power.

## Dynamic route meaning

Two cells are now stopped in exact scopes:

- extraction from the frozen continuous TPC-133--172 theorem corpus;
- uncontrolled promotion from a metric almost-every-phase result to a
  prescribed singleton atom.

Neither scoped stop proves architecture infeasibility. A new explicit source
corpus or theorem can reopen the structural extraction, and a source-locked
named atom plus schedule-specific exceptional-set avoidance can reopen the
metric bridge. Independently, the two O161 pointwise fixed-atom routes remain
open.

## Reproduce

After generating TPC-173--181 in order:

```powershell
python experiments/tpc182_mvp8_route_audit.py
python experiments/tpc182_mvp8_route_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Generated artifacts:

- `experiments/tpc182_mvp8_snapshot.json`
- `experiments/tpc182_mvp8_route_audit.json`

Stable archival PDF:

`tpc-182-mvp8-source-phase-route-decision.pdf`

## Claim boundary

This batch adds L0 contracts/diagnostics and L1 scoped obstructions. It adds no
production local occurrence family, actual active-support certificate,
canonical physical representative, named fixed-atom theorem, program-positive
L2 result, strict `1/400`, prime-pair lower bound, or twin-prime theorem.
