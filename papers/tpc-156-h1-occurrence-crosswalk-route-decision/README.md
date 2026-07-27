# TPC-156: H1 occurrence-crosswalk route decision

Paper title:

> *The H1 Occurrence-Crosswalk Route Decision: Canonical Shadows,
> Conservative Completion Obstructions, and Theorem-Backed Witnesses*

## Exact decision

The source-locked production state is:

```text
H1.cut_occurrence_shadow = PROVED_L1_STRUCTURAL
H1.current_artifacts_only_canonical_actual_lift = STOP_DECLARED_ROUTE
H1.theorem_backed_occurrence_provenance_crosswalk = NOT_TESTABLE
H1.map_clause = NOT_TESTABLE
H1.scalar_clause = NOT_TESTABLE
H1.frontier_totalization = NOT_TESTABLE
```

The selected occurrence-augmented route remains open.  The
current-artifacts-only derivation is stopped only in its declared
cell.  The scalar alternative also remains open, but it requires both
a complete original-scale FUM `o(X)` theorem and a theorem-backed ETO
disposition.

## Typed H1 contract

```text
map_clause =
    theorem_backed_occurrence_crosswalk
    AND D_L = D_QD = D_QZ = D_G = D_P = 0
    AND D_DZ = D_GP = D_cover = D_rec = 0
    AND occurrence_registry_complete

scalar_clause =
    complete_FUM_scalar_oX
    AND theorem_backed_ETO_disposition

H1_complete = map_clause OR scalar_clause
```

The frozen finite archive has `ETO=0` and `FUM=2988`; ETO remains a
required growing-scale class.

## Reproduce

Run TPC-153--155 in default mode once, then:

```powershell
python experiments/tpc156_h1_occurrence_decision.py
python experiments/tpc156_h1_occurrence_decision.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Generated artifacts:

```text
experiments/tpc156_h1_occurrence_decision.json
experiments/tpc156_h1_occurrence_audit.json
```

The source-lock policy is `CANONICAL_UTF8_LF_V2`.  Hashes have
integrity semantics only.

## Claim boundary

This paper proves a structural L1 decision and identifies a sharper
missing analytic object.  It does not prove an actual occurrence
lift, a complete physical carrier, positive fixed-X-power L2,
the `1/400` endpoint, a prime-pair lower bound, or the twin-prime
conjecture.
