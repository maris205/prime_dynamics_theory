# TPC-194 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `297233ff3085439444209e1e05d5238ef93d4bb5227f681d1c0d7107120687c8`.
- Bibliography: [references.bib](references.bib), SHA-256 `e3de68e5a5b78731b757215d9d557348d348c812eab9b8575355d063f28f59c5`.
- Preserved PDF: [tpc-194-maximal-source-backed-direct-prefix.pdf](tpc-194-maximal-source-backed-direct-prefix.pdf), SHA-256 `a01c3853114a6e41f932ef3cc27c7deacba2cf8277a88d2657db8b7463c684ad`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2dbd7a37df74e754f9e212e2b0a9792df531dce28d192d03013dbd1c46a19f45`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC190_194.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Target contract and source boundary` | 25 | 1 | `HEADING_TEXT_MATCH` |
| `Resolved packet and physical coefficient` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `The maximal per-packet contribution` | 73 | 2 | `HEADING_TEXT_MATCH` |
| `Three noninterchangeable formula types` | 90 | 2 | `HEADING_TEXT_MATCH` |
| `Loss, level and scope ledger` | 123 | 2 | `HEADING_TEXT_MATCH` |
| `Machine certificate` | 138 | 2 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 147 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `31` before writing and `31` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `d868975446df88a34694ebcc94327c3bb0024da1774d8b5dbbf4aef0bd238781`.
- Source theorem/proof environment starts: theorem at TeX line 105, proof at TeX line 114.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 38–42 | `214a1ec7cdd20b21c60faa4106689f5b83cedf9c643eadc556e60916e89c1e25` |
| D02 | \[...\] | 45–47 | `0525b8a9301b7dd3715b0758bd007a1c144d97e84c3db595ad7c8bf9f1ac435d` |
| D03 | \[...\] | 53–59 | `ed5c4ae70441e09067d2f131f21e5967d01281d07b427d853f7bd7bd8928be6e` |
| D04 | \[...\] | 62–65 | `97d693a46d8b34ede65476a4e4dfad5810200bb0b658aa1b9d531515c25629de` |
| D05 | \[...\] | 67–71 | `cf88b82468af23751c22117166d0e1227b1338c6f9f7cc230c36c3fa0ea46e78` |
| D06 | equation | 75–79 | `bae64eb7aad950dfda2d26913c6d7d6ee5e234a9bd0ce18416587352f284530f` |
| D07 | equation | 81–84 | `cea1d33223692ae0a592af7ce280ad37a4af9eb23176179a1f7b998aff816c5e` |
| D08 | \[...\] | 92–98 | `9a96a54ddedbc62ba36ded245aacb8b88eb7d9bc990a877437330218649e5e4b` |
| D09 | \[...\] | 125–127 | `cc3f8e17e917a61ee81cbbb80448a18280020619e6cf0886f8ce44e7380cb8c0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 19: `The physical determinant-two summand and additive atom can be written without placeholders for each resolved packet key.  This does not freeze a production packet schedule, uniform constant, positive exponent, common parameter range, or complete loss ledger.`
- TeX line 26: `The target has six simultaneous axes: actual fixed-\(h_0\) packet,`
- TeX line 29: `support.  The value \(h_0=2\) is source-backed data only.  Repository hashes`
- TeX line 110: `production atom, exact packet schedule, common \(X/N/q\) range, uniform`
- TeX line 139: `The adjacent canonical payload freezes the formula or finite witness,`
- TeX line 143: `constant leaves.  The checker recomputes the finite certificate and executes`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:physical-prefix` → `../main.tex#L75` (existing project target or original TeX label line).
- Link relocation: `#eq:physical-contribution` → `../main.tex#L81` (existing project target or original TeX label line).
- Link relocation: `#eq:physical-prefix` → `../main.tex#L75` (existing project target or original TeX label line).
