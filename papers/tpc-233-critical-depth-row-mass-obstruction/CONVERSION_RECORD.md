# TPC-233 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `ee10a3c73cc7db6f30d029b49bcbba9328905ea6dc7a9f4781c1eed04d74193a`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `7a84286cf79c75ff5a9dc4eb39b1dfe7b4f6995be19bc943f93e583a2c6b9a05`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `efd0ce485b5e43eb276398c2ab5d88011d2c0564b9c139b26263c04cd2064e49`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2cd42b6b24e9720c4ec0e90879822ea288c5e3c7fe5ca038f4d2a15b6dd2d844`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC230_234.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 7 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `ee10a3c73cc7db6f30d029b49bcbba9328905ea6dc7a9f4781c1eed04d74193a` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `093464c9465e810a1c2dc63dcf54e68ccf48f32ad0f2c2765171f374adf47ed4` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `eb3cbbeafeb61f655c0a3c3d1cc5687f9d918133c7ef6a5aee4c247fd4dcb863` |
| [paper/sections/2_raw_mass.tex](paper/sections/2_raw_mass.tex) | `eb2ec66ea74f97195f6442321299a767ed1a402ac27829045f8c129d8cb60310` |
| [paper/sections/3_critical_clock.tex](paper/sections/3_critical_clock.tex) | `4785a8b7c232619591551de12fcd33ff757be1bd68db41ea9776f1e4f2a196ae` |
| [paper/sections/4_certificate.tex](paper/sections/4_certificate.tex) | `0ea63ca55e16a068bed0553751e2f909e33f9e56a6f05047309516330da04c17` |
| [paper/sections/5_conclusion.tex](paper/sections/5_conclusion.tex) | `b6b0fb26e619cff3d000b39642458d6d40b8aa959bff65ba7c91e5ec7e455d7c` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L20](paper/main.tex#L20) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L21](paper/main.tex#L21) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L22](paper/main.tex#L22) | `\input{sections/2_raw_mass}` | [paper/sections/2_raw_mass.tex](paper/sections/2_raw_mass.tex) |
| [paper/main.tex:L23](paper/main.tex#L23) | `\input{sections/3_critical_clock}` | [paper/sections/3_critical_clock.tex](paper/sections/3_critical_clock.tex) |
| [paper/main.tex:L24](paper/main.tex#L24) | `\input{sections/4_certificate}` | [paper/sections/4_certificate.tex](paper/sections/4_certificate.tex) |
| [paper/main.tex:L25](paper/main.tex#L25) | `\input{sections/5_conclusion}` | [paper/sections/5_conclusion.tex](paper/sections/5_conclusion.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Raw row mass and a universal envelope` | [paper/sections/2_raw_mass.tex:L1](paper/sections/2_raw_mass.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `A critical primorial clock` | [paper/sections/3_critical_clock.tex:L1](paper/sections/3_critical_clock.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Finite reproduction and route consequence` | [paper/sections/4_certificate.tex:L1](paper/sections/4_certificate.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/5_conclusion.tex:L1](paper/sections/5_conclusion.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | [paper/main.tex:L27](paper/main.tex#L27) | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `86` before writing and `86` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `12`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `1f901d6a4ec05f1106b6f2caf8f7e9acdc382c2fce6fbb1f16774f28c6d3c7ba`.
- Source theorem/proof environment starts: lemma at [paper/sections/2_raw_mass.tex:L19](paper/sections/2_raw_mass.tex#L19), proof at [paper/sections/2_raw_mass.tex:L30](paper/sections/2_raw_mass.tex#L30), lemma at [paper/sections/3_critical_clock.tex:L19](paper/sections/3_critical_clock.tex#L19), proof at [paper/sections/3_critical_clock.tex:L29](paper/sections/3_critical_clock.tex#L29), theorem at [paper/sections/3_critical_clock.tex:L46](paper/sections/3_critical_clock.tex#L46), proof at [paper/sections/3_critical_clock.tex:L61](paper/sections/3_critical_clock.tex#L61).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/2_raw_mass.tex:L5](paper/sections/2_raw_mass.tex#L5) – [paper/sections/2_raw_mass.tex:L9](paper/sections/2_raw_mass.tex#L9) | `d9953996eb75e28ba73025abe02726959c540a44092e59efb87ca5a09fe33e19` |
| D02 | \[...\] | [paper/sections/2_raw_mass.tex:L11](paper/sections/2_raw_mass.tex#L11) – [paper/sections/2_raw_mass.tex:L14](paper/sections/2_raw_mass.tex#L14) | `f5554d01305f88d455ef1b3e20043affb4d158b4e53bb6493510736a041a002f` |
| D03 | \[...\] | [paper/sections/2_raw_mass.tex:L21](paper/sections/2_raw_mass.tex#L21) – [paper/sections/2_raw_mass.tex:L26](paper/sections/2_raw_mass.tex#L26) | `3c9fbee97fe29dfcc4eb1d2a42a1ebfbfe8ff65750c2db1e1c244b99844acef0` |
| D04 | \[...\] | [paper/sections/3_critical_clock.tex:L4](paper/sections/3_critical_clock.tex#L4) – [paper/sections/3_critical_clock.tex:L9](paper/sections/3_critical_clock.tex#L9) | `bb313a20f6f8e65bfdb708619b19a9f90abf2a23ee8f9f8a4166df0fe9b2dd00` |
| D05 | \[...\] | [paper/sections/3_critical_clock.tex:L12](paper/sections/3_critical_clock.tex#L12) – [paper/sections/3_critical_clock.tex:L16](paper/sections/3_critical_clock.tex#L16) | `927d5d565580c30da1097b28332c7b608b6d96f79f66f32c17bcfde53b41faf5` |
| D06 | \[...\] | [paper/sections/3_critical_clock.tex:L21](paper/sections/3_critical_clock.tex#L21) – [paper/sections/3_critical_clock.tex:L25](paper/sections/3_critical_clock.tex#L25) | `d42a495adee94379fccefc489d0552f44c604ad96baa8dd1d760ec3fa3d7d4bd` |
| D07 | \[...\] | [paper/sections/3_critical_clock.tex:L31](paper/sections/3_critical_clock.tex#L31) – [paper/sections/3_critical_clock.tex:L33](paper/sections/3_critical_clock.tex#L33) | `95140e0ce5d1d772402c8e55ece4cc1465e9f5ae1c25e7ba0d941a918b449e60` |
| D08 | \[...\] | [paper/sections/3_critical_clock.tex:L37](paper/sections/3_critical_clock.tex#L37) – [paper/sections/3_critical_clock.tex:L39](paper/sections/3_critical_clock.tex#L39) | `b4cd603d141a8bea5617ce7a8d2a3151dd18ddcf89ef1ed525714dbef2220971` |
| D09 | \[...\] | [paper/sections/3_critical_clock.tex:L48](paper/sections/3_critical_clock.tex#L48) – [paper/sections/3_critical_clock.tex:L52](paper/sections/3_critical_clock.tex#L52) | `f2a3907bb3f271133e4aa217fe92bf1fa221b0091658341251a4de72ae66f0ed` |
| D10 | \[...\] | [paper/sections/3_critical_clock.tex:L54](paper/sections/3_critical_clock.tex#L54) – [paper/sections/3_critical_clock.tex:L58](paper/sections/3_critical_clock.tex#L58) | `0e9ca04829df2d3db44a7aa5be5c3cb77df982a4a0aa31aa2059d1d7d4f1cd34` |
| D11 | \[...\] | [paper/sections/4_certificate.tex:L7](paper/sections/4_certificate.tex#L7) – [paper/sections/4_certificate.tex:L11](paper/sections/4_certificate.tex#L11) | `f378198e576abb5133b2d18d2528b0dd78cea0711e9e711c0f5b179326c68b7c` |
| D12 | \[...\] | [paper/sections/4_certificate.tex:L13](paper/sections/4_certificate.tex#L13) – [paper/sections/4_certificate.tex:L17](paper/sections/4_certificate.tex#L17) | `b499c215154977bc9fb631345b83e7987e4b7d39c833c1a7ac4dd02ac0e85a88` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/0_abstract.tex:L11](paper/sections/0_abstract.tex#L11): `window.  Four exact finite clocks are reproduced by independent deterministic`
- [paper/sections/1_introduction.tex:L14](paper/sections/1_introduction.tex#L14): `particular transfer assumption, not to the resonance model as a whole.`
- [paper/sections/1_introduction.tex:L26](paper/sections/1_introduction.tex#L26): `analyzed separately.  Second, uniform atom weights are part of this modeled clock and`
- [paper/sections/2_raw_mass.tex:L15](paper/sections/2_raw_mass.tex#L15): `For a common uniform atom amplitude, diagonal row mass is a common scalar times`
- [paper/sections/2_raw_mass.tex:L37](paper/sections/2_raw_mass.tex#L37): `The lemma already shows that fixed comparability is not a formal consequence of the`
- [paper/sections/3_critical_clock.tex:L73](paper/sections/3_critical_clock.tex#L73): `theorem of the modeled support.  It does not refute comparability for a particular`
- [paper/sections/3_critical_clock.tex:L74](paper/sections/3_critical_clock.tex#L74): `source after nonuniform weighting or normalization.`
- [paper/sections/4_certificate.tex:L1](paper/sections/4_certificate.tex#L1): `\section{Finite reproduction and route consequence}`
- [paper/sections/4_certificate.tex:L19](paper/sections/4_certificate.tex#L19): `$2,3,4,4$.  These small values are finite reproduction only; divergence is supplied`
- [paper/sections/4_certificate.tex:L34](paper/sections/4_certificate.tex#L34): `critical depth, raw support count does not supply that control.  The next minimal`
- [paper/sections/4_certificate.tex:L35](paper/sections/4_certificate.tex#L35): `question is therefore whether unit-row normalization yields a uniformly stable`
- [paper/sections/5_conclusion.tex:L3](paper/sections/5_conclusion.tex#L3): `Critical resonance depth does not automatically produce a well-conditioned raw row`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#lem:endpoints` → `sections/3_critical_clock.tex#L19` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `sections/3_critical_clock.tex#L46` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `sections/3_critical_clock.tex#L46` (existing project target or original TeX label line).
