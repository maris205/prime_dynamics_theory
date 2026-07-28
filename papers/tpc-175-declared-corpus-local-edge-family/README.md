# TPC-175: Declared-corpus local edge family

TPC-175 constructs the largest defensible production local occurrence-edge
family from:

- the TPC-173 qualifying source-claim inventory; and
- production witnesses accepted by the TPC-174 source-locked verifier.

The actual imported counts are:

```text
qualifying_claim_count = 0
eligible_carrier_count = 0
family_cardinality = 0
covered_cut_count = 0
unmatched_cut_count = 2988
```

Hence:

```text
status = EMPTY_IN_FROZEN_DECLARED_CORPUS
scope  = FROZEN_CONTIGUOUS_OCCURRENCE_SOURCE_CORRIDOR_TPC133_172
```

The empty family is maximal only in that exact closed-world evidence
universe: every admissible family member must have a TPC-173 qualifying claim,
and there are none. This does **not** prove mathematical nonexistence or
emptiness after an explicit corpus enlargement.

The executable validator locks the complete claim boundary, the coverage and
gluing state, the scoped maximality certificate, and the H1 architecture
state. Mutations separately test every positive claim-boundary field, global
totality, enlarged-corpus nonexistence, and architecture-stop promotion.

The TPC-174 synthetic fixture is excluded. The TPC-153 shadow rows, TPC-164
archive key, TPC-165 formal hypotheses, and actual-core arithmetic statements
cannot be promoted into family members.

TPC-165 gluing is not instantiated: its production local-fibre hypothesis is
nonempty, while the present family is empty. Actual active support and
canonical/minimal representation remain independent `NOT_TESTABLE` roots.

Reproduce:

```powershell
python experiments/tpc175_local_edge_family.py
python experiments/tpc175_local_edge_family.py --check
```

Generated outputs:

- `experiments/tpc175_local_edge_family.json`
- `experiments/tpc175_local_edge_family_audit.json`

No production nonempty local edge family, formal global totality, actual
active support, canonical/minimal actual representation, named fixed phase,
positive fixed-X L2, strict `1/400`, prime-pair lower bound, or twin-prime
theorem is proved.
