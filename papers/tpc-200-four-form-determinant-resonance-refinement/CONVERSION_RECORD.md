# TPC-200 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `ab8c23d22ce7a55804b00385610d361062c97a2f3e8f466ae552ff84b748ada7`.
- Bibliography: [references.bib](references.bib), SHA-256 `e3de68e5a5b78731b757215d9d557348d348c812eab9b8575355d063f28f59c5`.
- Preserved PDF: [tpc-200-four-form-determinant-resonance-refinement.pdf](tpc-200-four-form-determinant-resonance-refinement.pdf), SHA-256 `d0eba4f101a78f97b9a93dd14d6df57b5fed2f268c76a68105965a56a71ba4eb`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `de79b3f95f475a47a4767b2efcc3691a732b83202e7f902fcc83ac8274f72b07`.
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
| `Four shifted forms` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Refined arithmetic gate` | 68 | 1 | `HEADING_TEXT_MATCH` |
| `Loss, level and scope ledger` | 76 | 2 | `HEADING_TEXT_MATCH` |
| `Machine certificate` | 91 | 2 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 100 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `31` before writing and `31` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `3`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `bd8968482598b5234bbebc586558147873ce3adecc1a6df4092a60645ded41cc`.
- Source theorem/proof environment starts: theorem at TeX line 49, proof at TeX line 61.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 40–45 | `5b5aa21f15823a6a90a753c5b1dfa08548da871483ae7562cbb978a1d17be2b0` |
| D02 | \[...\] | 51–56 | `03a80fc431463a0f67cd033014e6ba38461ddad587f7baf051c4b2a2ea78d352` |
| D03 | \[...\] | 78–80 | `e081c2d9190f5e49e2ae93c00cc51b3ead8013368f0713774ea1bb82845b2265` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 26: `The target has six simultaneous axes: actual fixed-\(h_0\) packet,`
- TeX line 29: `support.  The value \(h_0=2\) is source-backed data only.  Repository hashes`
- TeX line 92: `The adjacent canonical payload freezes the formula or finite witness,`
- TeX line 96: `constant leaves.  The checker recomputes the finite certificate and executes`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
