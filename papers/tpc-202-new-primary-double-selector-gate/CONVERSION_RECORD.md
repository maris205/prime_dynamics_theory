# TPC-202 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `7e3d3d6bc8504ba402a36b1ac6856c15f668a1ab1d84c0dd3a5cee48f76b7537`.
- Bibliography: [references.bib](references.bib), SHA-256 `e3de68e5a5b78731b757215d9d557348d348c812eab9b8575355d063f28f59c5`.
- Preserved PDF: [tpc-202-new-primary-double-selector-gate.pdf](tpc-202-new-primary-double-selector-gate.pdf), SHA-256 `c4aec1e7a378b4eb0b36299b06130a96306e1e4eed19a69ad27637864658c8f6`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `c8c73959a8b08aa31aa52f145134c3ea5ae8c18e2953d7a3388c133c7c42df3b`.
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
| `Primary theorem record` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Double-selector lemma` | 60 | 1 | `HEADING_TEXT_MATCH` |
| `Six-axis audit` | 78 | 2 | `HEADING_TEXT_MATCH` |
| `Declared-corpus boundary` | 87 | 2 | `HEADING_TEXT_MATCH` |
| `Loss, level and scope ledger` | 95 | 2 | `HEADING_TEXT_MATCH` |
| `Machine certificate` | 110 | 2 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 119 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `25` before writing and `25` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `3`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `0f11408d4e685f86d3519383f74b63f0d65bb6ac7d5f2cc9a59a60aff9757330`.
- Source theorem/proof environment starts: lemma at TeX line 61, proof at TeX line 68.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 36–43 | `d81169e439f61aeb79879c629dc52a2ec2d4100128eca143ad4260ba5ad3afdd` |
| D02 | \[...\] | 47–56 | `84a2eb4e91146d853048e22e28ee72bdd75173d6ce88407572b7895917731061` |
| D03 | \[...\] | 97–99 | `f8446b64891dd8421d931bd27fb47b99113e55d7a039baccc450d5211263a826` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 19: `Menon's 2026 Theorems 1.4 and 1.5 sharpen an origin-averaged single-Liouville Fourier bound and a shift-averaged Liouville correlation bound.  Their combination does not select the prescribed affine relation and deterministic packet simultaneously.`
- TeX line 26: `The target has six simultaneous axes: actual fixed-\(h_0\) packet,`
- TeX line 29: `support.  The value \(h_0=2\) is source-backed data only.  Repository hashes`
- TeX line 85: `Their juxtaposition does not create a theorem-backed selector.`
- TeX line 90: `it does not rewrite the seven-source V1 corpus or assert global`
- TeX line 111: `The adjacent canonical payload freezes the formula or finite witness,`
- TeX line 115: `constant leaves.  The checker recomputes the finite certificate and executes`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
