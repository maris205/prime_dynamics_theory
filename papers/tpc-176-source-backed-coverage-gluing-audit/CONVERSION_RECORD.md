# TPC-176 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `14418f88b38f1087b1afd5d944d8208f2be9d278a45452b8cf86bd2c535578a2`.
- Bibliography: [references.bib](references.bib), SHA-256 `0697be8464297062eaa0a90564ee8513a14931403505d45cd13c54ae8314ffd1`.
- Preserved PDF: [tpc-176-source-backed-coverage-gluing-audit.pdf](tpc-176-source-backed-coverage-gluing-audit.pdf), SHA-256 `b02d5a363ead95c9168e8bff21251b5734201cc6fd58e3ecf2fe5754c7f475bb`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `955ac4343f5a99b6f04f00a628f7bb93f71da7f8e04568e9dc36a091b6097251`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC175_179.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The admissible input` | 67 | 1 | `HEADING_TEXT_MATCH` |
| `The TPC-165 gate` | 91 | 1 | `HEADING_TEXT_MATCH` |
| `Exact coverage ledgers` | 119 | 2 | `HEADING_TEXT_MATCH` |
| `Scoped stop versus architecture status` | 178 | 2 | `HEADING_TEXT_MATCH` |
| `Reproducible audit and claim boundary` | 197 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 213 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 224 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `24` before writing and `24` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `83c80d81a25efea0536e9314fce63f1cef849cc18abd566f3eccc29a52b8f5a7`.
- Source theorem/proof environment starts: proposition at TeX line 98, proof at TeX line 103, theorem at TeX line 143, proof at TeX line 156.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 73–75 | `390ba0ba6b89149e552ef5e3ef0d32ab034fd58260a55d96ac91ffcb2d8ef66f` |
| D02 | \[...\] | 82–85 | `d4055044f73749c433456e018890a5e03bdff7ca10e0a16d162b7d25b09f6257` |
| D03 | \[...\] | 113–117 | `389dc966e24ac6038046b1a52d666c606948316f6788caaa1009799eb67f3483` |
| D04 | \[...\] | 125–131 | `3053f4bd75d817ef2f795a1490ff8d361f1e8438088fd165bfe502ce97353090` |
| D05 | \[...\] | 133–136 | `1a5bd131a5d5a7c293fff3af468fa3a5b684c847eb0be7113dce7e642418af96` |
| D06 | \[...\] | 145–152 | `0f9bad7256006986096fa974e7585b1199d7add11ccc6d3045abbc7cdc3f7c72` |
| D07 | \[...\] | 181–183 | `e915659458c154d7b5092e40a09ee0137b684432ce0158d7b258ca40562d082f` |
| D08 | \[...\] | 191–193 | `47cf1ef743bd09f445941b8a4eb5f9d9edead3620e7828b01fe91bd7c92bc122` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 63: `not an actual-support theorem, canonicality theorem, fixed-phase`
- TeX line 87: `deliberately narrow.  It does not identify \(\mathcal C_{\rm elig}\)`
- TeX line 93: `TPC-165 proves a finite descent theorem under supplied nonempty local`
- TeX line 96: `inputs.  It does not construct them.`
- TeX line 172: `unmatched cuts & 2988 & no proved local edge; not an actual-carrier claim\\`
- TeX line 195: `not a proof that the complete architecture is infeasible.`
- TeX line 208: `deterministic endpoint, normalization, or fixed-\(h_0=2\) arithmetic`
- TeX line 216: `empty-domain ledger plus a scoped stop, not a vacuous totality`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
