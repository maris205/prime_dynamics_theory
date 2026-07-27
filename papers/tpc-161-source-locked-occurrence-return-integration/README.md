# TPC-161: Source-locked occurrence-to-return integration

Paper title:

> *Source-Locked Occurrence-to-Return Integration: Typed H1
> Completion, Almost-Endpoint Mobius Progress, and a Nonduplicating
> Endpoint Ledger*

## Exact result

TPC-161 integrates the frozen TPC-153--160 outputs against the
TPC-151/152 anchors.

The structural state is:

```text
H1.cut_occurrence_shadow = PROVED_L1_STRUCTURAL
current-schema-only canonical lift = STOP_SCOPED
H1.theorem_backed_occurrence_provenance_crosswalk = NOT_TESTABLE
current_verdict = NOT_TESTABLE
```

H1 is an explicit `ANY_CLAUSE` node:

```text
map clause =
  theorem-backed occurrence crosswalk
  AND nine zero defects
  AND independent occurrence-registry totality

scalar clause =
  complete original-scale FUM o(X)
  AND theorem-backed growing-scale ETO disposition
```

The selected map clause has the singleton minimal missing antichain

```text
[H1.theorem_backed_occurrence_provenance_crosswalk]
```

The current-schema stop is not promoted to a global obstruction.

## Arithmetic state

TPC-159 is the strongest arithmetic import:

```text
A159.almost_endpoint_prefix
  = PROVED_L1_ACTUAL_PREFIX_ALMOST_ENDPOINT
```

It advances the actual determinant-two periodic core from good dyadic
blocks to cumulative prefixes outside a sparse dyadic shadow.
TPC-157, TPC-158, and TPC-160 provide positive weight, major-arc
phase, and Abel-return interfaces, respectively. They do not supply
the production literal weight, phase cell, normalization, or atomic
endpoint registries, all of which remain `NOT_TESTABLE`.

Two arithmetic targets are parent-ready and `OPEN`:

- a direct additive-twist theorem on the existing actual core;
- a pointwise theorem at endpoints inside the dyadic bad set.

They are core-level routes, not physical-return results.

## Guardrails

The 53-node typed DAG records evidence, scope, carrier,
normalization, required artifact, and readiness. It computes
clause-wise minimal missing antichains, keeps the nine H1 defects
separate from the occurrence registry, and verifies that H9 has no
direct or transitive arithmetic ancestor.

Endpoint Ledger V3 gives each of six listed charges exactly one owner
and rejects omission from that six-charge contract. The full-synthesis
ledger references its child ledgers without recharging their costs.
This proves nonduplication among the listed charges; it does not claim
that the unknown physical-loss registry is complete. The certified
fixed-\(X\) arithmetic exponent is zero, the physical loss is unknown,
and the `1/400` endpoint is unpaid.

There is no positive fixed-\(X\) L2 result, full physical H3 return,
prime-pair lower bound, or twin-prime theorem.

## Reproduce

```powershell
python experiments/tpc161_source_locked_integration.py
python experiments/tpc161_source_locked_integration.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Generated deterministic artifacts:

```text
experiments/tpc161_occurrence_return_manifest.json
experiments/tpc161_occurrence_return_manifest.schema.json
experiments/tpc161_occurrence_return_audit.json
experiments/tpc161_occurrence_return_audit.schema.json
```

Stable PDF:

`tpc-161-source-locked-occurrence-return-integration.pdf`
