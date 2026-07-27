# TPC-155: theorem-backed occurrence witness verifier

Companion code and manuscript for:

> *A Theorem-Backed Occurrence Witness Contract: Exact Verification
> without Provenance Promotion*

## Result

TPC-155 specifies `OccurrenceWitnessV1` and proves the soundness of a
finite verifier for a supplied occurrence bundle. A valid bundle is
row-separated, covers both `ELIGIBLE_TAIL_OPEN` (ETO) and
`FRONTIER_UNMAPPED` (FUM), conserves every cut column exactly, and
records canonical-parent, stage, multiplier, native, fixed-shift,
normalization, support, determinant quotient (`QD`), zero-mode
quotient (`QZ`), physical grouping (`G`) and downstream selector
(`P_h0`) provenance.

Physical cover, reconnection and occurrence-registry evidence are
separate exports. Passing one cannot silently fill either of the
others.

The V1 cover export is explicitly row-disjoint. Shared physical atoms
would require a later theorem-backed joint-token/no-double-charge
extension; they are not silently deduplicated.

The committed positive fixture is **synthetic L0 only**. It contains
one ETO cut and one FUM cut, including a genuine one-to-many column,
and exists solely to demonstrate that the contract and verifier are
non-vacuous.

The current production declaration remains:

```text
partial_shadow_status = PROVED_L1_STRUCTURAL
production_witness_present = false
current_production_actual_witness_status = NOT_TESTABLE
H1.frontier_occurrence_lift = NOT_TESTABLE
physical_cover_status = NOT_TESTABLE
reconnection_status = NOT_TESTABLE
occurrence_registry_status = NOT_TESTABLE
```

Thus TPC-155 proves a verification theorem, not the existence or
truth of a production occurrence lift.

## Deterministic artifacts

The standard-library script writes:

- `experiments/tpc155_occurrence_witness.schema.json`;
- `samples/tpc155_synthetic_occurrence_witness.json`;
- `samples/tpc155_synthetic_physical_cover.json`;
- `samples/tpc155_synthetic_reconnection.json`;
- `samples/tpc155_synthetic_occurrence_registry.json`;
- `samples/tpc155_production_witness_status.json`; and
- `experiments/tpc155_occurrence_witness_audit.json`.

All upstream locks use `CANONICAL_UTF8_LF_V2`. Hashes are
integrity/provenance controls, never arithmetic evidence.
The source chain includes the TPC-153 canonical partial shadow and the
TPC-154 current-schema completion-fiber obstruction. The former is not
an actual lift, and the latter stops only current-artifacts-only
canonical recovery.

Run:

```bash
python experiments/tpc155_occurrence_witness_verifier.py
python experiments/tpc155_occurrence_witness_verifier.py --check
```

An external four-file bundle can be checked without writing:

```bash
python experiments/tpc155_occurrence_witness_verifier.py \
  --witness witness.json \
  --cover physical_cover.json \
  --reconnection reconnection.json \
  --registry occurrence_registry.json
```

Add `--production` only for a source-locked candidate intended to
cover the exact current TPC-143 nonsoft cut domain. The verifier checks
the supplied source hashes and internal equations; it does not prove
the imported theorems.

## Claim boundary

No production occurrence lift, full active-support carrier, complete
four-map route, fixed-\(X\)-power saving, \(1/400\) endpoint,
\(B_{h_0,\delta}(X)=o(X)\), prime-pair lower bound or twin-prime
theorem is established.
