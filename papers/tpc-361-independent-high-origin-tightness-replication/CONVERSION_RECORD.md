# TPC-361 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `7108301b3ef40963062dc0f61271c53d83077a043c102af3e31f1d4c11818d7a`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `8389ee6f17d7d6ca927554e23bff048e13d19bb23178a7ab1a89aba18ed306f9`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `37de2b01e7dfc6c77c4ac03ca11b3fc48f0066dd51bd391e0c77a3f1ffece81f`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [notes/route_evaluation.md](notes/route_evaluation.md), [experiments/protocol.md](experiments/protocol.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 39 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator` | 54 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen selection and replay` | 86 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 113 | 2 | `HEADING_TEXT_MATCH` |
| `Independent audit and exact anchor` | 164 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route decision` | 180 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 209 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `33` before writing and `33` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `e39c7b49404e9a3d7969c6f6b837f21c5b263f00fab1bd340b97d4c81c994cd9`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 58–63 | `f8797497f668f47bc3a56fad52b71277bfbd033a737b84872466f06e994d1b4a` |
| D02 | equation | 66–71 | `a2c0653ad4aa3f9c4b4e0f84d5e6c181fd9defe4ff31b4c90ff6f331e26f360e` |
| D03 | equation | 77–82 | `ff0b62b94b9ded8c5f28196afcd839cc9ba330a5abfe6d81f9bda26d544af395` |
| D04 | equation* | 89–91 | `910b514b4fb32eb0f32bf27837fc3da73abdc8961d66dcaa978cf861e22a9946` |
| D05 | \[...\] | 97–99 | `6b83a0e80e83f20b730bdcec8d1e113e2bcad628019026e3bee45f5dd268959b` |
| D06 | \[...\] | 137–139 | `5164e358c94265fa8e55595192354eae4b33623e320109521dbf2c99a5881a43` |
| D07 | \[...\] | 143–147 | `42d98a5c32f0251603cb3db9581caa1312f9acde037437b095e0d48f0974dc6a` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{Independent High-Origin Replication of a Finite\`
- TeX line 23: `We independently replicate a finite tightness audit for a normalized`
- TeX line 34: `flats over 54 adjacent transitions.  These are finite, reproducible`
- TeX line 41: `The preceding finite studies found a normalized cap and measurable slack in`
- TeX line 45: `signed matrix or eigenvalue is evaluated.  Thus the experiment tests finite`
- TeX line 46: `transfer and implementation stability, not an asymptotic conjecture.`
- TeX line 50: `fail-closed finite evidence only.  In particular, no source response is`
- TeX line 51: `queried, no arithmetic reassembly is attempted, and no fixed-power credit is`
- TeX line 54: `\section{Finite operator}`
- TeX line 76: `For every finite real matrix $T$ we use the exact inequalities`
- TeX line 83: `Ratios to these envelopes are descriptive finite quantities, not proposed`
- TeX line 150: `slack statement is restricted to the declared finite matrices.`
- TeX line 154: `not win.  This is evidence that all-plus is a useful finite stress law, while`
- TeX line 161: `also blocks the tempting inference from a finite cap to a growing-origin`
- TeX line 182: `The finite envelope inequalities in \eqref{eq:envelopes} are proved exactly`
- TeX line 183: `for finite matrices.  The finite selection and its response independence are`
- TeX line 186: `this finite protocol.`
- TeX line 189: `TPC361_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND`
- TeX line 190: `TPC361_HIGH_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS`
- TeX line 191: `TPC361_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE`
- TeX line 192: `TPC361_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE`
- TeX line 193: `TPC361_TIGHTNESS_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 194: `TPC361_LAW_UNIFORM_SHORT_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 196: `TPC361_GROWING_OPERATOR_BOUND = OPEN`
- TeX line 197: `TPC361_SOURCE_UNIFORM_L2 = OPEN`
- TeX line 200: `TPC361_FULL_GATE_B = OPEN`
- TeX line 206: `finite obstruction/replication checkpoint, not progress through the missing`
- TeX line 211: `The independent high-origin panel reproduces the finite normalized cap and`
- TeX line 213: `matter for route planning: sign-law variation remains finite but nonzero,`
- TeX line 216: `source-uniform arithmetic $L^2$ statement, a growing masked-operator bound,`
- TeX line 217: `Route-B reassembly, and the twin-prime endpoint remain open.`
- TeX line 222: `\texttt{TPC361\_FULL\_GATE\_B=OPEN}.`

## Conversion limitations

- No PROOF_PACKAGE.md is present; no proof-package review is claimed.

- Link relocation: `#tab:summary` → `main.tex#L122` (existing project target or original TeX label line).
- Link relocation: `#eq:envelopes` → `main.tex#L81` (existing project target or original TeX label line).
