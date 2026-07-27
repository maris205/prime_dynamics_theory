# TPC-143: Frontier occurrence-lift contract

This paper identifies the first object missing after the complete
TPC-136 cut archive.  It is not a single label.  It is a conservative,
row-separated sparse lift from every nonsoft cut path to fully typed
downstream occurrences.  One cut path may split into several
occurrences.

The exact field-descent theorem distinguishes data already determined
by the cut archive from data that require this lift.  The inherited
cut-stage selector is proved:

```text
H1.cut_shift_selector = PROVED_L1
P_h0_cut = identity
```

This is deliberately different from the missing downstream selector:

```text
H1.frontier_occurrence_lift = NOT_TESTABLE
H1.frontier_downstream_shift_selector = NOT_TESTABLE
```

The required domain is `ALL_NONSOFT_CUT_PATHS`, namely both
`ELIGIBLE_TAIL_OPEN` and `FRONTIER_UNMAPPED`.  The committed finite
sample happens to contain 2,988 frontier paths and no eligible-tail
path.  Empty finite sample support is not an asymptotic totality
theorem.

Run the deterministic audit with:

```bash
python experiments/tpc143_frontier_lift_audit.py
python experiments/tpc143_frontier_lift_audit.py --check
```

The script writes and verifies:

- `samples/tpc143_frontier_lift_obligations.jsonl`;
- `experiments/tpc143_frontier_lift_certificate.json`.

It also reruns the TPC-133--136 generators without rewriting their
artifacts.  Logical text is locked as `CANONICAL_UTF8_LF_V2`.  The
older raw hashes that differ only because they were computed on CRLF
bytes are recorded explicitly as `LEGACY_RAW_HASH_STALE`; any
non-EOL semantic or generation mismatch fails closed.

The obligations do not manufacture downstream arithmetic data.  They
record each missing field as `REQUIRED_MISSING`.  Hashes are integrity
checks only; mathematical identity is the exact scope, native tuple,
and path identity.
