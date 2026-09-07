# TPC-363 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `efdf0cebde51e40cee1c296e8993fdc533a6508cb69306c270f24ceb35c8feae`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `9b1f149654d5995bf0dea81e19f5c939100ddbca60debaa322f3a3c846049eca`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `3d0f2dc054991ec4f82fefb6d66d9c202e49b8895b87c7ba7ded2451638e5fa1`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [notes/route_evaluation.md](notes/route_evaluation.md), [experiments/protocol.md](experiments/protocol.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 35 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator` | 51 | 1 | `HEADING_TEXT_MATCH` |
| `Localization audit` | 81 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 106 | 2 | `HEADING_TEXT_MATCH` |
| `Checks and exact anchor` | 166 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route decision` | 183 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 209 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `55` before writing and `55` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `78e8fa54a3c2279da9b7d33256786288f30fba40f2e65af267e4c6195e75cad2`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 55–60 | `b0a28707730955a18c77823c0cdaae78ac7e40cb5264725fc1baf4dabf92a1a3` |
| D02 | equation | 64–70 | `ee24a120dd5f2a66c1ec1d6d0b5e018f188f8b0f9beb316227973fa35897616e` |
| D03 | equation | 74–79 | `bb57f66b7af183da8f7aa62bc477af1d0a56527fb55de8c048ea26e1597c11f5` |
| D04 | \[...\] | 87–89 | `f6e44996db75d2339e7986b47668769d85891e8696b5e1dac7b6fb4336175ce8` |
| D05 | \[...\] | 94–96 | `bc360bfd50f89fef578991d331a56ce971df98d4ec96b1a8d1d2d8f7d4a73def` |
| D06 | \[...\] | 132–134 | `fa1aeb0e6752dcbd21d11ec908443768138d4c5469fb147cf94899ffbcba553f` |
| D07 | \[...\] | 136–138 | `941c23ec8831f0f08722f6c6c964d7786594641e1b0dcffd8dc6c3fd0bf264bd` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 21: `TPC-362 found that a finite normalized spectral cap, valid on the inherited`
- TeX line 31: `set.  This is a finite, scoped bulk obstruction; it is not an asymptotic`
- TeX line 37: `The preceding shell-scale audit kept a normalized finite cap below $0.64$ at`
- TeX line 42: `violation survives targeted deletions, the finite evidence instead points to`
- TeX line 45: `We answer only this finite diagnostic question.  The Session-named official`
- TeX line 51: `\section{Finite operator}`
- TeX line 72: `character, and a half-shell split.  For every finite real matrix $T$ we use`
- TeX line 97: `This is a descriptive finite test, not a claim that a data-selected`
- TeX line 114: `\caption{Finite spectral and deletion audit by shell anchor.}`
- TeX line 130: `zero failures in this finite panel.  The smallest restricted value among the`
- TeX line 163: `0.55114876369112986.  These are finite descriptive indicators of a spread`
- TeX line 164: `eigenvector, not a theorem of asymptotic delocalization.`
- TeX line 180: `in the certificate.  This exact sanity anchor does not enlarge the`
- TeX line 186: `TPC363_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS`
- TeX line 187: `TPC363_FINITE_ENVELOPE_INEQUALITIES = PROVED_EXACT_FINITE`
- TeX line 188: `TPC363_FIRST_Q128_FAILURE = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 189: `TPC363_BULK_PERSISTENCE = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 191: `TPC363_EIGENVECTOR_DELOCALIZATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 192: `TPC363_RENORMALIZED_REPAIR = OPEN`
- TeX line 193: `TPC363_GROWING_OPERATOR_BOUND = OPEN`
- TeX line 194: `TPC363_SOURCE_UNIFORM_L2 = OPEN`
- TeX line 197: `TPC363_FULL_GATE_B = OPEN`
- TeX line 201: `The strongest finite conclusion is that two natural five-percent leverage`
- TeX line 204: `from the same matrix, the panel is finite, and no universal renormalization`
- TeX line 206: `holdout, while the growing operator bound, source-uniform arithmetic $L^2$,`
- TeX line 207: `Route-B reassembly, and the twin-prime endpoint remain open.`
- TeX line 211: `TPC-363 converts the first shell-scale cap failure into a more precise finite`
- TeX line 212: `obstruction.  It is not a one-row spike under either declared deletion rule;`
- TeX line 220: `\texttt{TPC363\_FULL\_GATE\_B=OPEN}.`

## Conversion limitations

- No PROOF_PACKAGE.md is present; no proof-package review is claimed.

- Link relocation: `#tab:q` → `main.tex#L115` (existing project target or original TeX label line).
