# TPC-136: Complete native cut archive

Paper title:

> *A Complete Native Cut Archive at the First Unsupported Carrier:
> Exact Reconnection, Totality Defects, and an H1 Subgate Certificate*

## Result

TPC-136 composes the actual TPC-133--135 artifacts. Every TPC-134
path appears exactly once as one of:

```text
ELIGIBLE_PREFIX_SOFT
ELIGIBLE_TAIL_OPEN
FRONTIER_UNMAPPED
```

No frontier path is deleted or called soft. The resulting growing cut
archive is coefficientwise conservative and preserves the native
tuple, fixed `h0`, and one physical normalization. It gives

```text
B = eligible_prefix_soft + eligible_tail_open + frontier_unmapped
```

exactly. The published TPC-17 theorem supplies the soft label only in
its valid eligible scope.

The paper then audits four separate partial maps: determinant fibers,
zero-mode ordering, physical grouping, and downstream fixed-shift
selection. The current artifacts do not make any of these maps total
on all nonsoft cut paths. Each map has a separate theorem-source
status and an inherited fixed-`h0` contract; all four source statuses,
including the downstream fixed-`h0` selector source, remain
`NOT_TESTABLE`.

At row-separated matrix level, path-totality is equivalent to
`(I-P_Dom) M_ret = 0`: different omitted rows cannot cancel each
other. Only the weaker aggregated scalar check
`1^T (I-P_Dom) M_ret = 0` can pass by cancellation, so it is not used
as a provenance certificate.

Hence:

```text
H1.native_cut     = PROVED_L1
H1.actual_carrier = NOT_TESTABLE
```

This split prevents a change of terminal scope from being mistaken for
closure of the original MVP3 H1 node. There is no new positive L2
estimate, parity advance, or twin-prime theorem.

## Reproduce

Default deterministic write:

```powershell
python experiments/tpc136_cut_archive.py
```

Read-only check:

```powershell
python experiments/tpc136_cut_archive.py --check
```

Compile:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
