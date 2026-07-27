# TPC-133: Executable native entrance

Paper title:

> *An Executable Native Entrance for the TPC-15 Hard Packet:
> Canonical Tuple Enumeration, Symbolic Coefficient DAGs, and
> Scale-Uniform Completeness*

## Result

For fixed nonzero `h0`, rational `0 < delta < 1/2`, a declared compact
support envelope for the fixed smooth weight, and every integer scale
`X`, the paper gives one terminating generator for all candidate native
tuples

```text
(ell,k,d), ell > U, k > V, d | k, d <= V.
```

The generator deliberately uses the certified support envelope. It
does not attempt to decide the exact zero set of an arbitrary smooth
weight. Coefficients are stored as expression trees whose first leaf
is the exact integer value of `-mu(d)`:

```text
integer(-mu(d)) * Lambda(ell) * r_Q(ell*k+h0) * W(ell*k/X).
```

The full `(packet_scope, native_tuple)` pair is the canonical record
identity. The shorter `native_id` is only a label inside one scope.
SHA-256 fields are reproducibility checks and are not treated as
mathematical collision-free identifiers.

The enumeration theorem and divisor opening are L0. Their literal
attachment to the TPC-15 fixed-shift entrance is L1. No downstream
path archive, positive L2 estimate, parity advance, or prime-pair
theorem is claimed.

## Reproduce

Default mode deterministically writes the JSON and JSONL artifacts:

```powershell
python experiments/tpc133_native_entrance.py
```

Read-only verification:

```powershell
python experiments/tpc133_native_entrance.py --check
```

Compile:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```
