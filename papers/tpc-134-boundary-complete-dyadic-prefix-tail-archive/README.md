# TPC-134: Boundary-complete dyadic prefix-tail archive

Paper title:

> *A Boundary-Complete Dyadic Prefix--Tail Path Archive:
> Exact Column Conservation and Fixed-Shift Provenance*

## Result

TPC-134 turns every TPC-133 native atom into an actual finite path
family. It uses an explicit normalized smooth dyadic partition and a
declared integer `D0` policy. Every native divisor record enters
exactly one of

```text
PREFIX: d <= D0
TAIL:   D0 < d <= V.
```

The edge weights are symbolic `psi` expression trees. Their exact sum
is proved from the normalized bump identity, not estimated in floating
point. The executable check verifies the exact finite child-index set
and binds each child to its parent checksum; the symbolic theorem, not
a numerical tolerance, supplies column conservation. For the complete
path matrix,

```text
1^T M_134 = 1^T.
```

The native tuple, fixed `h0`, and unique physical normalization are
preserved on every nonzero path. This yields an exact growing block
identity, but it does not prove that any prefix or tail is small.

The partition identities are L0 and the literal TPC-15-to-block
attachment is L1. No positive L2 estimate, physical cover, parity
advance, or twin-prime theorem is claimed.

## Reproduce

Default deterministic write:

```powershell
python experiments/tpc134_branch_archive.py
```

Read-only check:

```powershell
python experiments/tpc134_branch_archive.py --check
```

Compile:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
