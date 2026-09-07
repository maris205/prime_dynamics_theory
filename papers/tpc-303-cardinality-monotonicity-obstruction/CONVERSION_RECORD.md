# TPC-303 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `55240d2d7254cbf8bd7fc0b4755fa8f24254e424`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `122f39b34d57ad354dc6ee6e4469597ca63325d98df690d128ac5292ba0efedd`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `d5b1bec67deb33e39b5d6f389bb1c9054003df8de1997713d9a723b433ddd75f`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `96c2914f93ddbe123f14771fb073bc792c519163941c22387f3b5429d2354949`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `e22e17fdbf90b0099f33b85450d3b6843a2e6242317425b14c951b9acafb255f`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC300_304.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question` | 30 | 1 | `HEADING_TEXT_MATCH` |
| `Interval certificate` | 50 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 76 | 2 | `HEADING_TEXT_MATCH` |
| `Obstruction and next question` | 107 | 2 | `HEADING_TEXT_MATCH` |
| `Reproducibility and scope` | 118 | 2 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 127 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `36` before writing and `36` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `1`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `aa3eb1af5932a3820817f3c1a663edb385f500c35f89697b473d69dc94a49a7d`.
- Source theorem/proof environment starts: proposition at TeX line 52, proof at TeX line 57, proposition at TeX line 62, proof at TeX line 66.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 44–46 | `55fbc63f46bb443679f8a486fc315ca99b6c9a3a7ea2a1ac981e0c3a864d3217` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 26: `contraction is below $0.284422$.  This is a scoped finite obstruction, not a`
- TeX line 62: `\begin{proposition}[Finite scoped refutation]`
- TeX line 64: `declared finite Q-spine.`
- TeX line 102: `These are interval-certified finite comparisons inherited from a frozen`
- TeX line 114: `switching from the physical operator/shell change.  Uniform profile-budget`
- TeX line 116: `conclusion remain open.`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
