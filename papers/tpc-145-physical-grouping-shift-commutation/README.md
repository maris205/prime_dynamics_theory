# TPC-145: Physical grouping and shift commutation

This paper separates the proved cut-stage selector from the missing
downstream fixed-shift map.  It also gives a pathwise criterion for a
physical grouping map to preserve the prescribed shift.

For an aggregated matrix `G`, the commuting square

```text
P_phys G = G P_src
```

can hold because opposite cross-shift occurrence edges cancel.  On
the row-separated occurrence lift, commutation is equivalent to every
nonzero occurrence edge preserving membership in the prescribed
`h0` slice.

Current statuses:

```text
H1.cut_Ph0 = PROVED_L1
H1.frontier_G_totality = NOT_TESTABLE
H1.frontier_Ph0_downstream_totality = NOT_TESTABLE
```

Run:

```bash
python experiments/tpc145_group_shift_audit.py
python experiments/tpc145_group_shift_audit.py --check
```

Synthetic commuting-square examples are regression tests only.  The
actual manifest contains no fabricated physical occurrence or
downstream stage.  Its strict contract separately records
`P_h0_cut`, `P_h0_downstream`, aggregate commutation, and
row-separated edgewise provenance.
