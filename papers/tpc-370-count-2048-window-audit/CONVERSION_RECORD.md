# TPC-370 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `91bc8448959f5c04b938f8d3b241e1b505bd9b57d0850005cf2a7606e01107cf`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `244c0e45e34fbe1f8745e02b65c9a258ef5641221691162d0fa74b8abf1d42eb`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8f2528551b0a3a8db1f3b73e40db99be477a6369aa2e996ba70b40c06d6e2fcb`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 36 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator and frozen protocol` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `Inherited exact anchor` | 91 | 2 | `HEADING_TEXT_MATCH` |
| `Complete count-2048 audit` | 101 | 2 | `HEADING_TEXT_MATCH` |
| `Independent and hostile verification` | 147 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route decision` | 163 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 195 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `45` before writing and `45` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `9dab2cc455e1e0f91e2f6a85b5a4f32ad477d8f81619b796171628207e68383d`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 53–58 | `c1f0bbb0c9cea23f88b23971864c031c25d6c1cfdfc63a885eb90e6f1f621ba0` |
| D02 | equation | 60–67 | `326b50f08060dfba4bedd267e67fc6e5acf576e6e9808f33896f7e293c0b4abd` |
| D03 | equation | 69–74 | `b813279c718a97fd560d492d88e7d2f408c7c0ea15cb1b38c881edab88a72bf0` |
| D04 | equation | 77–82 | `bb57f66b7af183da8f7aa62bc477af1d0a56527fb55de8c048ea26e1597c11f5` |
| D05 | equation* | 125–128 | `fd4842bb9fcc6af78b9b86693b604c720709b80ceb3ca101302c69f47452ce32` |
| D06 | equation* | 135–139 | `61696b4af2648032f62d1d3a2aa8a9af9029e274fe2624bfbf19ae728940adc0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{A Count-2048 Audit of a Persistent Finite Prime-Shell Failure Signature}`
- TeX line 21: `We perform the next predeclared finite-window audit after a third-origin`
- TeX line 32: `finite numerical certificate and obstruction analysis, not an asymptotic`
- TeX line 46: `all statements below are restricted to the declared finite panel; no source`
- TeX line 49: `\section{Finite operator and frozen protocol}`
- TeX line 68: `When $G_\beta(u)>0$, the normalized finite matrix is`
- TeX line 75: `Every summand of $G_\beta$ is a rational square.  For a finite real symmetric`
- TeX line 94: `the half-open interval $[1010346,1010359)$ at $Q=4$, exponent one, and shell`
- TeX line 98: `count-2048 responses.  It is a finite witness for well-defined normalization,`
- TeX line 105: `separate finite envelopes.`
- TeX line 141: `$0.67410489800609708$, so the finite difference is`
- TeX line 143: `but does not support a constant-level extrapolation.  The beta=0 control has`
- TeX line 161: `not present, this is repository-level finite evidence only.`
- TeX line 166: `TPC370_ORIGIN_FAMILY_PROTOCOL = PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND`
- TeX line 167: `TPC370_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE`
- TeX line 168: `TPC370_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_72_ROWS`
- TeX line 169: `TPC370_COUNT_2048_WINDOW = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 170: `TPC370_BETA2_PHASE_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 171: `TPC370_BETA2_PARENT_SIGNATURE = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 172: `TPC370_ORIGIN_UNIFORMITY = OPEN`
- TeX line 173: `TPC370_WINDOW_UNIFORMITY = OPEN`
- TeX line 174: `TPC370_BETA2_ASYMPTOTIC_REPAIR = OPEN`
- TeX line 175: `TPC370_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN`
- TeX line 176: `TPC370_GROWING_OPERATOR_BOUND = OPEN`
- TeX line 177: `TPC370_SOURCE_UNIFORM_L2 = OPEN`
- TeX line 180: `TPC370_FULL_GATE_B = OPEN`
- TeX line 184: `The strongest positive result is finite support replication of the six-key`
- TeX line 186: `simultaneous magnitude change: support persistence alone does not yield a`
- TeX line 191: `No growing operator bound, source-valid normalization, source-uniform`
- TeX line 202: `\texttt{NO}, fixed-power credit remains zero, and full Gate B remains open.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:phase` → `main.tex#L110` (existing project target or original TeX label line).
