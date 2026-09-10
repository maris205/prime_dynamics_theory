# TPC-203 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `7df45da490a9c8fdad09362da1fc0e96a1b2b068ff9115a8d0e56c793036aa7e`.
- Bibliography: [references.bib](references.bib), SHA-256 `e3de68e5a5b78731b757215d9d557348d348c812eab9b8575355d063f28f59c5`.
- Preserved PDF: [tpc-203-mvp10-direct-pointwise-route-decision.pdf](tpc-203-mvp10-direct-pointwise-route-decision.pdf), SHA-256 `23bc8f5e4a1ee9c51628154c2986defb9109f7c95c63539441d6b31cd92e0992`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `47b68dbf1889dac493c0dac3ae7c5c4cf384201430572e2d4882949ecd06094a`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC200_204.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Target contract and source boundary` | 25 | 1 | `HEADING_TEXT_MATCH` |
| `Imported batch state` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Endpoint and route ledger` | 67 | 2 | `HEADING_TEXT_MATCH` |
| `Loss, level and scope ledger` | 102 | 2 | `HEADING_TEXT_MATCH` |
| `Machine certificate` | 117 | 2 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 126 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `13` before writing and `13` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `2`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `7306260cc6f7aed670a00806456708579a2e6cf821ce70fd36bff965d4153adf`.
- Source theorem/proof environment starts: theorem at TeX line 44, proof at TeX line 57.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 48–54 | `980e036667d00019cdd544a4b6875e7365fb39247f2d74c568a999d40f4ea9f9` |
| D02 | \[...\] | 71–80 | `1401a4bff4abf1836bf366981d94d07e088b925e7ca85f4279cf06a5b4d055e1` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 19: `MVP10 imports TPC-194--202 fail-closed.  The per-packet direct formula is complete, but the production crosswalk and named-atom power theorem are absent.  Both O161 pointwise parents and the global architecture remain open; fixed-atom endpoint credit is zero.`
- TeX line 26: `The target has six simultaneous axes: actual fixed-\(h_0\) packet,`
- TeX line 29: `support.  The value \(h_0=2\) is source-backed data only.  Repository hashes`
- TeX line 46: `level.  It does not fire at the production target level.  The declared`
- TeX line 55: `Both O161 pointwise parents and the global architecture remain open.`
- TeX line 58: `The integration checker opens the nine canonical payloads, verifies their`
- TeX line 62: `uniform \(C\), positive \(\sigma\), target normalization and full losses.`
- TeX line 84: `An admissible reopen trigger must be one of the following exact types:`
- TeX line 98: `claimed.  This decision does not authorize TPC-204: the batch stops for user`
- TeX line 118: `The adjacent canonical payload freezes the formula or finite witness,`
- TeX line 122: `constant leaves.  The checker recomputes the finite certificate and executes`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
