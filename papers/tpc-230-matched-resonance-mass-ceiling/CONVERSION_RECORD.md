# TPC-230 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `fdd37c54df65782f46bab96b0038782a65694e4bcaba3c66c07fdef947f257eb`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `be36435726bd4709ef50e87ec4be2b0e559cd8e2da7d1c5819c13410169b4e90`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `dcf47af3a470114b0d768aff7e3cc9c12edc0d18cac3bee4e03eb34a76f85138`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `57a1deb7ea1699b7b45ab1098741ec7eeaa513ff7c998dff9834a777ef43b0d7`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC230_234.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 8 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `fdd37c54df65782f46bab96b0038782a65694e4bcaba3c66c07fdef947f257eb` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `83ebea7d83c544810a97b4beb4cb628e98da51e93974694cac6da5d660bb9752` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `b05f70170e58dc94676823bf7e4ba4d5f35f9c6ad74c1a90763dcb653c83bfa0` |
| [paper/sections/2_mass_ceiling.tex](paper/sections/2_mass_ceiling.tex) | `cf7ca2207ad34c0ab0580f5bd7467a89989d76f9e20f475a16ec4583154500e3` |
| [paper/sections/3_density_toll.tex](paper/sections/3_density_toll.tex) | `bd29aa085d72bfa2511f69e6a9fd59a5bc52f7e73c3f90d32e3bedc93974d0aa` |
| [paper/sections/4_literal_rows.tex](paper/sections/4_literal_rows.tex) | `e3beaae55fcf0cd733d3fe82e13aabc659e8f3c4360b57159b0b39db20e28e4d` |
| [paper/sections/5_certification.tex](paper/sections/5_certification.tex) | `37ab1aac28fe0a934cfe2527ceaab07fcae4c961b9947fd5e7add8fc43576221` |
| [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) | `b25a22904fd7369f4ebc42b6f28fd889ad4705b85f698baf222c08a78661102a` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L8](paper/main.tex#L8) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L9](paper/main.tex#L9) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L9](paper/main.tex#L9) | `\input{sections/2_mass_ceiling}` | [paper/sections/2_mass_ceiling.tex](paper/sections/2_mass_ceiling.tex) |
| [paper/main.tex:L9](paper/main.tex#L9) | `\input{sections/3_density_toll}` | [paper/sections/3_density_toll.tex](paper/sections/3_density_toll.tex) |
| [paper/main.tex:L9](paper/main.tex#L9) | `\input{sections/4_literal_rows}` | [paper/sections/4_literal_rows.tex](paper/sections/4_literal_rows.tex) |
| [paper/main.tex:L9](paper/main.tex#L9) | `\input{sections/5_certification}` | [paper/sections/5_certification.tex](paper/sections/5_certification.tex) |
| [paper/main.tex:L9](paper/main.tex#L9) | `\input{sections/6_conclusion}` | [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) |

### Original CR/CRLF separator ledger

These counts refer to the hash-locked original bytes. Only reader whitespace is normalized; original-file links use LF-delimited source lines and no scientific source is repaired.

| Original source | CRLF pairs | Bare CR bytes |
|---|---:|---:|
| [paper/sections/2_mass_ceiling.tex](paper/sections/2_mass_ceiling.tex) | 0 | 2 |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `The sharp matched-mass ceiling` | [paper/sections/2_mass_ceiling.tex:L1](paper/sections/2_mass_ceiling.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `From matched mass to edge density` | [paper/sections/3_density_toll.tex:L1](paper/sections/3_density_toll.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Literal aligned row weights` | [paper/sections/4_literal_rows.tex:L1](paper/sections/4_literal_rows.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Exact certification` | [paper/sections/5_certification.tex:L1](paper/sections/5_certification.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/6_conclusion.tex:L1](paper/sections/6_conclusion.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | [paper/main.tex:L10](paper/main.tex#L10) | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files. This source contains CR separators: source lines count original LF delimiters, while expanded-block hashes use the explicitly normalized reader input. The separate file hashes preserve exact original bytes.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `49` before writing and `49` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `69ecf8e3cb3a7332baf1dac17bedebfe136277dc08dfce57499a63d387e21fe0`.
- Source theorem/proof environment starts: theorem at [paper/sections/2_mass_ceiling.tex:L10](paper/sections/2_mass_ceiling.tex#L10), proof at [paper/sections/2_mass_ceiling.tex:L25](paper/sections/2_mass_ceiling.tex#L25), corollary at [paper/sections/3_density_toll.tex:L15](paper/sections/3_density_toll.tex#L15).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/2_mass_ceiling.tex:L4](paper/sections/2_mass_ceiling.tex#L4) – [paper/sections/2_mass_ceiling.tex:L8](paper/sections/2_mass_ceiling.tex#L8) | `bb1f2de1d8a594e61780d38581ad0e3bacfc038bbaba121cddfb1882bb49f377` |
| D02 | equation | [paper/sections/2_mass_ceiling.tex:L13](paper/sections/2_mass_ceiling.tex#L13) – [paper/sections/2_mass_ceiling.tex:L17](paper/sections/2_mass_ceiling.tex#L17) | `979fadb742d90da54ed749a1093952af26de0bca4b5ef8d1294d8ef941f15b7f` |
| D03 | equation | [paper/sections/2_mass_ceiling.tex:L19](paper/sections/2_mass_ceiling.tex#L19) – [paper/sections/2_mass_ceiling.tex:L22](paper/sections/2_mass_ceiling.tex#L22) | `fef7ada188a8285966dd4dffbc0f8df15e233b46de63d32ab6c9be590a33fd9e` |
| D04 | \[...\] | [paper/sections/2_mass_ceiling.tex:L27](paper/sections/2_mass_ceiling.tex#L27) – [paper/sections/2_mass_ceiling.tex:L30](paper/sections/2_mass_ceiling.tex#L30) | `a7a3b5da168d0df82ea4df1bd16e13ac937630039a21731b442d3bc3838a58cc` |
| D05 | \[...\] | [paper/sections/3_density_toll.tex:L6](paper/sections/3_density_toll.tex#L6) – [paper/sections/3_density_toll.tex:L8](paper/sections/3_density_toll.tex#L8) | `ec45b8924d7b1f799f586ccfa64a19c51e4a6e5a35068ed918c3fdef7c5b1d2f` |
| D06 | equation | [paper/sections/3_density_toll.tex:L10](paper/sections/3_density_toll.tex#L10) – [paper/sections/3_density_toll.tex:L13](paper/sections/3_density_toll.tex#L13) | `f6a354f6ba511e46188a85bc116600040e1c77d494f979ffeea0a747ffe40915` |
| D07 | equation | [paper/sections/3_density_toll.tex:L17](paper/sections/3_density_toll.tex#L17) – [paper/sections/3_density_toll.tex:L20](paper/sections/3_density_toll.tex#L20) | `042c8197e8e2ad0da77ace738b12c58cf4f457136bedbd79b1dbe4fe108a95fc` |
| D08 | \[...\] | [paper/sections/4_literal_rows.tex:L5](paper/sections/4_literal_rows.tex#L5) – [paper/sections/4_literal_rows.tex:L7](paper/sections/4_literal_rows.tex#L7) | `032e9875c147e7ffb4bc91db2ae7b359d8ac93f09568615cfb2b82ee428e7636` |
| D09 | equation | [paper/sections/4_literal_rows.tex:L10](paper/sections/4_literal_rows.tex#L10) – [paper/sections/4_literal_rows.tex:L13](paper/sections/4_literal_rows.tex#L13) | `07c1fe8ce190032231e7029b0a7fbbec259e450e55be1b116eeec7963cc2f98f` |
| D10 | equation | [paper/sections/4_literal_rows.tex:L17](paper/sections/4_literal_rows.tex#L17) – [paper/sections/4_literal_rows.tex:L20](paper/sections/4_literal_rows.tex#L20) | `ea11c17145c4472db5d7dd4c9f9478f66856e17379b9d05070d805d3c6a9c46a` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/0_abstract.tex:L8](paper/sections/0_abstract.tex#L8): `$\kappa\le4$, so the strict $1/400$ target requires $E/P\ge1/3200$.  Exact finite`
- [paper/sections/0_abstract.tex:L10](paper/sections/0_abstract.tex#L10): `and physical source comparability remain open.`
- [paper/sections/1_introduction.tex:L13](paper/sections/1_introduction.tex#L13): `For the literal aligned rows of the finite dilation-four model \cite{tpc226}, elementary`
- [paper/sections/1_introduction.tex:L14](paper/sections/1_introduction.tex#L14): `primitive-multiplier counting gives a uniform comparability constant four.  The strict`
- [paper/sections/2_mass_ceiling.tex:L3](paper/sections/2_mass_ceiling.tex#L3): `Let $G$ be a matching on a finite set of Hilbert vectors $u_q$.  Write`
- [paper/sections/4_literal_rows.tex:L24](paper/sections/4_literal_rows.tex#L24): `The comparison is scoped to literal aligned finite-model rows.  Actual V59 source`
- [paper/sections/5_certification.tex:L8](paper/sections/5_certification.tex#L8): `At $Q=25$, six prime rows contain one edge.  Uniform mass gives $M/D=1/3$; literal`
- [paper/sections/5_certification.tex:L9](paper/sections/5_certification.tex#L9): `aligned atom mass gives $10/26=5/13$.  Across the finite scan, 2268 scales contain at`

## Conversion limitations

- Restricted compact/standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- CR/CRLF separators were normalized only in the in-memory reader input; all original file-byte hashes are unchanged. Source links count original LF-delimited lines, so multiple reader lines from a bare CR share one original line. Expanded-display hashes describe this normalized reader input, not literal source bytes. No missing TeX command or suspected source typo is reconstructed.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:ceiling` → `sections/2_mass_ceiling.tex#L16` (existing project target or original TeX label line).
- Link relocation: `#eq:necessary-mass` → `sections/2_mass_ceiling.tex#L21` (existing project target or original TeX label line).
- Link relocation: `#eq:density-bound` → `sections/3_density_toll.tex#L12` (existing project target or original TeX label line).
- Link relocation: `#eq:kappa` → `sections/4_literal_rows.tex#L12` (existing project target or original TeX label line).
- Link relocation: `#eq:density-toll` → `sections/3_density_toll.tex#L19` (existing project target or original TeX label line).
