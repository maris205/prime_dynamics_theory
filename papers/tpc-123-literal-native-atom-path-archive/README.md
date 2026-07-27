# TPC-123: Literal native-atom path archive

Paper title:

> *Literal Native-Atom Path Archives for the TPC-15 Hard Packet:
> Local-to-Global Conservation, Metadata Intertwining, and
> First-Failure Certificates*

## Core result

Every exact branch operation is represented by a sparse stage matrix
`T_j`. Its columns are incoming records and its rows are outgoing
records. The complete leaf matrix is

```text
M = T_s ... T_1.
```

If every stage is coefficientwise conservative,

```text
1^T T_j = 1^T,
```

then

```text
1^T M = 1^T.
```

The path-expanded archive records the complete intermediate path and
the product of its edge multipliers. It therefore distinguishes exact
coefficientwise conservation from a scalar coincidence on one
coefficient vector.

The paper also proves the exact defect identity

```text
1_s^T M - 1_0^T
  = sum_j (1_j^T T_j - 1_(j-1)^T) T_(j-1) ... T_1.
```

This localizes a failure once the actual stage tables are present. A
separate metadata intertwining condition retains the native key,
fixed `h0`, one physical normalization, determinant-fiber fields and
ordered zero-mode fields.

## Current verdict

The finite theorem and exact rational model pass. The machine
certificate labels this result as a finite regression only; its
`route_verdict` remains separate. The existing repository snapshot
does not yet provide every actual branch table,
boundary rule and collision rule needed to instantiate the complete
growing TPC-15 archive:

```text
LITERAL ARCHIVE VERDICT = NOT_TESTABLE_FROM_CURRENT_ARTIFACTS
```

This is not a claim that H8 is false. The canonical path archive is a
strong sufficient proof language, not the only possible exact proof.

## Claim level

- Matrix/path identities and counterexamples: L0.
- Attachment of the schema to the TPC-15 native keys: L1 interface.
- No complete growing archive, soft `o(X)` theorem, fixed-`h0` L2
  saving, parity breakthrough, prime-pair theorem or twin-prime
  theorem.

## Reproduce

```powershell
python experiments/tpc123_path_archive_audit.py --check
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Archival PDF:

`tpc-123-literal-native-atom-path-archive.pdf`

SHA-256:

`59b222202d78038ae58a5048b2171bda4b26cd52c75e4daa8ccb39cee88ea406`
