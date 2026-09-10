# TPC-228 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `571ea4f32939d1b642638bd0c7690e2a67bf3bf7573851cd1ebdc1c3b9253209`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `5ed11991d82af0d31c296e96df483b6267d7d8f844fee60a2048d0443c086eeb`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `ec48f7cf95a6b46d0b7dc6b9237dfe71eb9180b7bcf04eca552a2a1127e80304`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `e058f5355e2ee01a61c44780d5dbbc2bff3957ba2fecb5c7bca0bcc6b54fb54f`.
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
| [paper/main.tex](paper/main.tex) | `571ea4f32939d1b642638bd0c7690e2a67bf3bf7573851cd1ebdc1c3b9253209` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `3612595a4f816c8a83a4115a2988f1d761e9ff198ed0a31ea96e88746fd90bd9` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `26b298fd696bf07d1f1be443b0f1a8b23a224752727a82810df3aa8162475f0c` |
| [paper/sections/2_common_profile.tex](paper/sections/2_common_profile.tex) | `6564f723ff28ab48fdea3b72175db9f436a9218f036ba8da74386031145ffd61` |
| [paper/sections/3_compiler.tex](paper/sections/3_compiler.tex) | `ed6b685fc3b16dc06e865da4cd845cc8174c67c31dfb01c50605ddefbc6755e7` |
| [paper/sections/4_q25_block.tex](paper/sections/4_q25_block.tex) | `71a138844c709614365c4252634f548a39b7645f9725e392c3368da647d157cf` |
| [paper/sections/5_certification.tex](paper/sections/5_certification.tex) | `a1d1217e4dc6f8c990b56d22ba3113b8022bc491a57b50b2de0abef60241a143` |
| [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) | `e6e44644e4683c0a7b52237b79fb9f5930abca4df67062edbc0904abb11ccaca` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L19](paper/main.tex#L19) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L20](paper/main.tex#L20) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L21](paper/main.tex#L21) | `\input{sections/2_common_profile}` | [paper/sections/2_common_profile.tex](paper/sections/2_common_profile.tex) |
| [paper/main.tex:L22](paper/main.tex#L22) | `\input{sections/3_compiler}` | [paper/sections/3_compiler.tex](paper/sections/3_compiler.tex) |
| [paper/main.tex:L23](paper/main.tex#L23) | `\input{sections/4_q25_block}` | [paper/sections/4_q25_block.tex](paper/sections/4_q25_block.tex) |
| [paper/main.tex:L24](paper/main.tex#L24) | `\input{sections/5_certification}` | [paper/sections/5_certification.tex](paper/sections/5_certification.tex) |
| [paper/main.tex:L25](paper/main.tex#L25) | `\input{sections/6_conclusion}` | [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Common-profile packet rows` | [paper/sections/2_common_profile.tex:L1](paper/sections/2_common_profile.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Exact polarized collision identity` | [paper/sections/3_compiler.tex:L1](paper/sections/3_compiler.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `The first 3--7 source block` | [paper/sections/4_q25_block.tex:L1](paper/sections/4_q25_block.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Certification and boundary` | [paper/sections/5_certification.tex:L1](paper/sections/5_certification.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/6_conclusion.tex:L1](paper/sections/6_conclusion.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | [paper/main.tex:L26](paper/main.tex#L26) | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `54` before writing and `54` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `6bf6bf862620fcb2f04baaadac875d48939a7c74db4239c6f6bd2552cac9eab1`.
- Source theorem/proof environment starts: theorem at [paper/sections/3_compiler.tex:L3](paper/sections/3_compiler.tex#L3), proof at [paper/sections/3_compiler.tex:L15](paper/sections/3_compiler.tex#L15), corollary at [paper/sections/3_compiler.tex:L29](paper/sections/3_compiler.tex#L29).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/1_introduction.tex:L15](paper/sections/1_introduction.tex#L15) – [paper/sections/1_introduction.tex:L17](paper/sections/1_introduction.tex#L17) | `6b537ff38d01f6569f2fd8399daa7d2cfbd5c348c2de9af990517d894ce0af07` |
| D02 | \[...\] | [paper/sections/2_common_profile.tex:L7](paper/sections/2_common_profile.tex#L7) – [paper/sections/2_common_profile.tex:L9](paper/sections/2_common_profile.tex#L9) | `2eb36d752d89e8d25d972de1451abbb1d36b504231c309e615db3e0af7e89f9b` |
| D03 | equation | [paper/sections/2_common_profile.tex:L11](paper/sections/2_common_profile.tex#L11) – [paper/sections/2_common_profile.tex:L14](paper/sections/2_common_profile.tex#L14) | `6eece134ee029fca907cf20b184b05d607002404118b5c90dc91e97644ec8a4c` |
| D04 | equation | [paper/sections/2_common_profile.tex:L16](paper/sections/2_common_profile.tex#L16) – [paper/sections/2_common_profile.tex:L21](paper/sections/2_common_profile.tex#L21) | `4d7ba9c4d79cda26482a2888cc1a044d4eb09efa45891a10431b5eeb74bd0363` |
| D05 | equation | [paper/sections/3_compiler.tex:L6](paper/sections/3_compiler.tex#L6) – [paper/sections/3_compiler.tex:L12](paper/sections/3_compiler.tex#L12) | `c3ee9f2a59cb5f80df96637fb43bb9bf85fd3acd6bbc727ff6b677070984058a` |
| D06 | \[...\] | [paper/sections/3_compiler.tex:L17](paper/sections/3_compiler.tex#L17) – [paper/sections/3_compiler.tex:L21](paper/sections/3_compiler.tex#L21) | `9eac3d49d4d0b5ed2f8960a87591b9a48f97612e0cfaa81cdac0c3d030ad5b73` |
| D07 | \[...\] | [paper/sections/4_q25_block.tex:L4](paper/sections/4_q25_block.tex#L4) – [paper/sections/4_q25_block.tex:L6](paper/sections/4_q25_block.tex#L6) | `20f9f6adabe7b22fcf3caf4dd35e7508745bbdae1339d069e06573d45b0afcd6` |
| D08 | equation | [paper/sections/4_q25_block.tex:L10](paper/sections/4_q25_block.tex#L10) – [paper/sections/4_q25_block.tex:L16](paper/sections/4_q25_block.tex#L16) | `851b6963f6c8e29063e2b1b12eb14475dc5f5807619fa18d2d2ffb666881de7a` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/0_abstract.tex:L10](paper/sections/0_abstract.tex#L10): `identifies the missing arithmetic correlation but does not estimate it; Route-B level~2`
- [paper/sections/0_abstract.tex:L11](paper/sections/0_abstract.tex#L11): `and any twin-prime conclusion remain open.`
- [paper/sections/1_introduction.tex:L10](paper/sections/1_introduction.tex#L10): `We answer that question at the finite Hilbert level.  Prime-labelled row transforms of`
- [paper/sections/1_introduction.tex:L20](paper/sections/1_introduction.tex#L20): `minimal four-term block.  This does not determine an arithmetic sign, but it replaces`
- [paper/sections/2_common_profile.tex:L3](paper/sections/2_common_profile.tex#L3): `Let $\mathcal Q$ be a finite set of prime labels and let $\mathcal H$ be a complex`
- [paper/sections/3_compiler.tex:L25](paper/sections/3_compiler.tex#L25): `$\sum_j\ii^{2j}=0$.  The desired coefficient sums to four.  Interchanging the finite`
- [paper/sections/4_q25_block.tex:L24](paper/sections/4_q25_block.tex#L24): `These controls prove that geometry alone still does not determine the sign.  Their`

## Conversion limitations

- Restricted compact/standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:energies` → `sections/2_common_profile.tex#L20` (existing project target or original TeX label line).
- Link relocation: `#eq:packet-row` → `sections/2_common_profile.tex#L13` (existing project target or original TeX label line).
- Link relocation: `#eq:compiler` → `sections/3_compiler.tex#L11` (existing project target or original TeX label line).
- Link relocation: `#thm:compiler` → `sections/3_compiler.tex#L4` (existing project target or original TeX label line).
- Link relocation: `#eq:q25` → `sections/4_q25_block.tex#L15` (existing project target or original TeX label line).
- Link relocation: `#thm:compiler` → `sections/3_compiler.tex#L4` (existing project target or original TeX label line).
- Link relocation: `#eq:q25` → `sections/4_q25_block.tex#L15` (existing project target or original TeX label line).
- Link relocation: `#eq:q25` → `sections/4_q25_block.tex#L15` (existing project target or original TeX label line).
- Link relocation: `#eq:q25` → `sections/4_q25_block.tex#L15` (existing project target or original TeX label line).
