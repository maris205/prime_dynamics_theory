# TPC-166: refined H1 crosswalk frontier decision

Paper title:

> *Refining the H1 Crosswalk Frontier: Three Independent Production
> Roots after Archive Separation and Formal Gluing*

## Decision

TPC-162 remains historically frozen at:

```text
H1.theorem_backed_occurrence_provenance_crosswalk
```

TPC-166 does not rewrite that pointer.  It refines the object into a
dependency DAG whose minimal `NOT_TESTABLE` root antichain is exactly:

```text
H1.source_backed_local_occurrence_edge_family
H1.actual_active_support_certificate
H1.canonical_minimal_representation_certificate
```

The selected first-child pointer is the local edge family because it
is the next source-producing constructible object.  That selection
does not erase the other two independent roots.

## Scope guard

The three-root antichain belongs **only** to the historical monolithic
crosswalk sub-DAG.  It is not the minimal blocker antichain of the
complete H1 contract.

The full occurrence-augmented H1 map clause still requires:

```text
monolithic crosswalk
+ nine zero-defect conditions
+ independent occurrence-registry totality
```

The alternative scalar+ETO clause remains independently
`NOT_TESTABLE` and requires both the complete FUM `o(X)` estimate and
a theorem-backed ETO disposition.  A later full-H1 integration must
restore these external nodes around the refined crosswalk sub-DAG.

## Descendants

```text
local edge family
    -> overlap bijection/cocycle
    -> glued formal occurrence totality

formal totality + active support + canonical/minimality
    -> production occurrence witness
    -> historical monolithic H1 crosswalk
```

TPC-164's archived separation key and TPC-165's formal gluing theorem
are already `PROVED`; they are supporting prerequisites, not missing
roots.

## Current production status

```text
theorem-backed local occurrence edges     0
current verdict                           NOT_TESTABLE
selected route stopped                    false
actual-carrier impossibility              false
```

## Reproduce

```powershell
python experiments/tpc166_refined_frontier.py
python experiments/tpc166_refined_frontier.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Generated artifacts:

```text
experiments/tpc166_refined_h1_frontier.json
experiments/tpc166_refined_h1_frontier_audit.json
samples/tpc166_refined_frontier_excerpt.json
```

Stable archival PDF:

```text
tpc-166-refined-h1-crosswalk-frontier-decision.pdf
```

## Claim boundary

This is an L0/L1 frontier refinement.  It proves no production local
occurrence family, actual active support, canonical/minimal actual
representation, completed production crosswalk, positive fixed-`X`
L2, prime-pair lower bound, or twin-prime theorem.  In particular,
the displayed three roots are not claimed to be the complete H1
minimal blocker set.
