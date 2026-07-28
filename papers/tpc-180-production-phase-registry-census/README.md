# TPC-180: Production phase-registry census

Paper title:

> *A Source-Locked Census for the Production Phase Registry:
> Fixed-\(h_0=2\) Data, Missing Named-Atom Values, and Packet
> Coordinates*

## Exact result

TPC-180 audits the value-bearing phase data in the frozen
TPC-157--172 phase-interface corpus. It proves the scoped result

```text
Verdict = NOT_TESTABLE
ProductionPhaseRegistryConstructed = false
FirstMissing =
  named_physical_atom_id_and_phase_value_source_locator
```

The corpus does source-lock `fixed_h0 = 2` on the actual
determinant-two core. That fact is kept separate from the missing
phase registry. The existing `H9.phase_cell_registry` records only a
typed obligation:

```text
carrier_axis = PHYSICAL_PHASE_REGISTRY
phase_axis   = NAMED_FIXED_ATOM
scale_axis   = DETERMINISTIC_ALL_SCALE
support_axis = ACTUAL_ACTIVE_SUPPORT
decay_axis   = NONE
status       = NOT_TESTABLE
```

The seven explicitly mapped source fields supply no value-bearing
named physical atom, exact phase value modulo one, phase-value source
locator, production packet schedule, or physical-atom-to-packet
coordinate row. This is an explicit mapped-field census, not a generic
scanner for future fields. TPC-170 supplies the packet theorem and the
representative-covariance rule, but not those production data.

TPC-180 therefore constructs a strict registry contract and a
mapped-field missing-value census, not a synthetic phase. The census
is a scoped frozen-corpus statement, not a theorem that a production
phase record cannot exist in an unmapped field or a larger corpus.

## Level boundary

- `L0`: hashes, schema checks, field census, and mutation diagnostics.
- `L1`: the scoped source-interface obstruction for this frozen corpus.
- `L2`: none.

The fixed-\(h_0=2\) data fact is not a cancellation exponent. Every H9
registry has `decay_axis=NONE`.

## Reproduce

```powershell
python experiments/tpc180_phase_registry_census.py
python experiments/tpc180_phase_registry_census.py --check
```

Generated artifacts:

```text
experiments/tpc180_phase_registry_census.json
experiments/tpc180_phase_registry_census_audit.json
schemas/tpc180-phase-registry-census-v1.schema.json
schemas/tpc180-phase-registry-census-audit-v1.schema.json
```

Stable PDF:

```text
tpc-180-production-phase-registry-census.pdf
```

No named-phase estimate, program-positive L2 result, strict `1/400`
gain, prime-pair lower bound, or twin-prime theorem is claimed.
