# TPC-229 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `f878c22320d06df8f6f9d963a924645f1b9585fb66480c66028851f677b1e9b5`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `a2c9951e884c6935fb8640a2a6bd765ab1e4718c354439a5a9e018ee7944f76a`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `73a14e38ff9c750c9426650352cd6cccea53f4b5cc815bec8c827bb2596235af`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `a0feb71abaf9e8031bda0ce0884e6f0a24151e831de1764dc1bd8a59e00198ee`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC225_229.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 8 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `f878c22320d06df8f6f9d963a924645f1b9585fb66480c66028851f677b1e9b5` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `dfeed5912ac3e9b22e0d1666ec97daeac0d81fac5e691925d526d83e710b5eda` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `99cf03149a0862a9c4f935a9e5935eac71b02ee3cc101902c40d1c21cac5c215` |
| [paper/sections/2_matching.tex](paper/sections/2_matching.tex) | `4471126d251a7ffa33225bf8c043171ba91965fc31cba2de085689150711c127` |
| [paper/sections/3_spectrum.tex](paper/sections/3_spectrum.tex) | `35a6b41c8926b314edbc2888b52d4395ff641dfe82ba961363a35ac9f5c169ed` |
| [paper/sections/4_source_block.tex](paper/sections/4_source_block.tex) | `7ef62600ef09110c609960e4890ea27c0ea0517714c133261f6eee605a9d7fbf` |
| [paper/sections/5_certification.tex](paper/sections/5_certification.tex) | `e12d1b742cc23af72a52f1816ed9eaf2da66bc9a6543785891494830c48b8c60` |
| [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) | `6aaf0aaf277d363113d1815256ddc571bd1a7ecb2111dcfe3e40d60c5dbb1ff9` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L14](paper/main.tex#L14) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L15](paper/main.tex#L15) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L15](paper/main.tex#L15) | `\input{sections/2_matching}` | [paper/sections/2_matching.tex](paper/sections/2_matching.tex) |
| [paper/main.tex:L15](paper/main.tex#L15) | `\input{sections/3_spectrum}` | [paper/sections/3_spectrum.tex](paper/sections/3_spectrum.tex) |
| [paper/main.tex:L16](paper/main.tex#L16) | `\input{sections/4_source_block}` | [paper/sections/4_source_block.tex](paper/sections/4_source_block.tex) |
| [paper/main.tex:L16](paper/main.tex#L16) | `\input{sections/5_certification}` | [paper/sections/5_certification.tex](paper/sections/5_certification.tex) |
| [paper/main.tex:L16](paper/main.tex#L16) | `\input{sections/6_conclusion}` | [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `The resonance graph is a matching` | [paper/sections/2_matching.tex:L1](paper/sections/2_matching.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Sharp two-coordinate spectrum` | [paper/sections/3_spectrum.tex:L1](paper/sections/3_spectrum.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Sharp source-bilinear block bound` | [paper/sections/4_source_block.tex:L1](paper/sections/4_source_block.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Exact certification` | [paper/sections/5_certification.tex:L1](paper/sections/5_certification.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/6_conclusion.tex:L1](paper/sections/6_conclusion.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | [paper/main.tex:L17](paper/main.tex#L17) | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `46` before writing and `46` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `85aa5dcba08abc743698e8ce97d5bda14cf209a52b6f1a28d5f83fd86c3c84b2`.
- Source theorem/proof environment starts: theorem at [paper/sections/2_matching.tex:L7](paper/sections/2_matching.tex#L7), proof at [paper/sections/2_matching.tex:L17](paper/sections/2_matching.tex#L17), corollary at [paper/sections/2_matching.tex:L28](paper/sections/2_matching.tex#L28), theorem at [paper/sections/3_spectrum.tex:L25](paper/sections/3_spectrum.tex#L25), proof at [paper/sections/3_spectrum.tex:L37](paper/sections/3_spectrum.tex#L37).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | [paper/sections/1_introduction.tex:L4](paper/sections/1_introduction.tex#L4) – [paper/sections/1_introduction.tex:L7](paper/sections/1_introduction.tex#L7) | `33591b2b17b49679efe6be5f41e6123fd8a95da604de24455861740c35bec96d` |
| D02 | equation | [paper/sections/2_matching.tex:L10](paper/sections/2_matching.tex#L10) – [paper/sections/2_matching.tex:L13](paper/sections/2_matching.tex#L13) | `f6f1979ad8044fc0d5e38c5569ca6d367f3b0a29d407644123f6a3b17d5a67d9` |
| D03 | equation | [paper/sections/3_spectrum.tex:L5](paper/sections/3_spectrum.tex#L5) – [paper/sections/3_spectrum.tex:L8](paper/sections/3_spectrum.tex#L8) | `27d4904fd65489d7d0937e73831a26db4bc81dbdda3bf12ce923a29bfec6c91a` |
| D04 | align | [paper/sections/3_spectrum.tex:L12](paper/sections/3_spectrum.tex#L12) – [paper/sections/3_spectrum.tex:L17](paper/sections/3_spectrum.tex#L17) | `4e2d9c7b6079c580690eeb1c2a41a2012113969a27fed36ab6ceae71c7135afb` |
| D05 | equation | [paper/sections/3_spectrum.tex:L19](paper/sections/3_spectrum.tex#L19) – [paper/sections/3_spectrum.tex:L22](paper/sections/3_spectrum.tex#L22) | `22d126191f8c3637bebe8e9752a9bccdd1527cd67df1a56e7de5e56fc68921bc` |
| D06 | equation | [paper/sections/3_spectrum.tex:L27](paper/sections/3_spectrum.tex#L27) – [paper/sections/3_spectrum.tex:L32](paper/sections/3_spectrum.tex#L32) | `5e17f2758aa08a69c2b2c8a939933a38710ad554b394a2e8ab75dfc8527e9b92` |
| D07 | \[...\] | [paper/sections/4_source_block.tex:L4](paper/sections/4_source_block.tex#L4) – [paper/sections/4_source_block.tex:L6](paper/sections/4_source_block.tex#L6) | `ce809d8b26d189de01545965418f60f11f945e553d97609cb1961c40ac1448f2` |
| D08 | equation | [paper/sections/4_source_block.tex:L9](paper/sections/4_source_block.tex#L9) – [paper/sections/4_source_block.tex:L14](paper/sections/4_source_block.tex#L14) | `0e43c49af822dcd82b17dc36f8ccc3480627fba911a775169f1f0083a0f2b502` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/1_introduction.tex:L10](paper/sections/1_introduction.tex#L10): `$\beta$--$w$ block \cite{tpc228}.  The remaining finite geometry could in principle`
- [paper/sections/1_introduction.tex:L19](paper/sections/1_introduction.tex#L19): `geometry does not tell us how much physical source mass lies on matched vertices, nor`

## Conversion limitations

- Restricted compact/standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:resonance` → `sections/1_introduction.tex#L6` (existing project target or original TeX label line).
- Link relocation: `#eq:resonance` → `sections/1_introduction.tex#L6` (existing project target or original TeX label line).
- Link relocation: `#eq:resonance` → `sections/1_introduction.tex#L6` (existing project target or original TeX label line).
- Link relocation: `#eq:ranges` → `sections/2_matching.tex#L12` (existing project target or original TeX label line).
- Link relocation: `#eq:ranges` → `sections/2_matching.tex#L12` (existing project target or original TeX label line).
- Link relocation: `#eq:energies` → `sections/3_spectrum.tex#L16` (existing project target or original TeX label line).
- Link relocation: `#eq:bilinear-bound` → `sections/4_source_block.tex#L13` (existing project target or original TeX label line).
- Link relocation: `#eq:bilinear-bound` → `sections/4_source_block.tex#L13` (existing project target or original TeX label line).
