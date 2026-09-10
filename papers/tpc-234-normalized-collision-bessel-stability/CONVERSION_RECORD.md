# TPC-234 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `8a38d253aeb60a816ac5a58c4092e62f42de2e1a4c21c5984e770e43a2070c26`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `ed3b2418f00145600402e2ee671407dc4241e9132ea36257004b29a13091d91c`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `6ecf2f31050d5bf93c04becc402724acb2fc4d612eb4a035775c8cb364575603`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `94d0ecb348e2de341d0e973edfae3c031a14fb51e7526012c055ee72510345f4`.
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
| [paper/main.tex](paper/main.tex) | `8a38d253aeb60a816ac5a58c4092e62f42de2e1a4c21c5984e770e43a2070c26` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `2b10998f276004c8b735003d5767f03c5893cefb73ec608775e0fdcbeadb6976` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `77e496c6cbdd7fee61aac286badbc35a2c6271f37450094d72795f0cdc53ab17` |
| [paper/sections/2_bessel_theorem.tex](paper/sections/2_bessel_theorem.tex) | `c4bc7807e9265816839d2f0d22a8407d9b694296846d53b86375cf387cc7706f` |
| [paper/sections/3_literal_block.tex](paper/sections/3_literal_block.tex) | `cd78b0fe926f8f14666c256b27466cf7c9aaee333254ccec47e14adcb10c8309` |
| [paper/sections/4_certificate.tex](paper/sections/4_certificate.tex) | `aa9cda6bc27f9d8d408a0b939c4d58d1015b382816fb1c1794b319d177ef14fc` |
| [paper/sections/5_conclusion.tex](paper/sections/5_conclusion.tex) | `b2b2a597933e12fce9e1c1f196a3d8fb0563bdc167d8b59b38c1e69a2247ccef` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L19](paper/main.tex#L19) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L20](paper/main.tex#L20) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L21](paper/main.tex#L21) | `\input{sections/2_bessel_theorem}` | [paper/sections/2_bessel_theorem.tex](paper/sections/2_bessel_theorem.tex) |
| [paper/main.tex:L22](paper/main.tex#L22) | `\input{sections/3_literal_block}` | [paper/sections/3_literal_block.tex](paper/sections/3_literal_block.tex) |
| [paper/main.tex:L23](paper/main.tex#L23) | `\input{sections/4_certificate}` | [paper/sections/4_certificate.tex](paper/sections/4_certificate.tex) |
| [paper/main.tex:L24](paper/main.tex#L24) | `\input{sections/5_conclusion}` | [paper/sections/5_conclusion.tex](paper/sections/5_conclusion.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `The multiplicity-two Bessel theorem` | [paper/sections/2_bessel_theorem.tex:L1](paper/sections/2_bessel_theorem.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `A literal normalized block` | [paper/sections/3_literal_block.tex:L1](paper/sections/3_literal_block.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Finite reproduction and claim boundary` | [paper/sections/4_certificate.tex:L1](paper/sections/4_certificate.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/5_conclusion.tex:L1](paper/sections/5_conclusion.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | [paper/main.tex:L26](paper/main.tex#L26) | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `50` before writing and `50` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `075be6e3c3301ea15b44f1ad616b3851b1b56e04ec0abcce69ffd3d01ae03736`.
- Source theorem/proof environment starts: theorem at [paper/sections/2_bessel_theorem.tex:L12](paper/sections/2_bessel_theorem.tex#L12), proof at [paper/sections/2_bessel_theorem.tex:L26](paper/sections/2_bessel_theorem.tex#L26).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/2_bessel_theorem.tex:L5](paper/sections/2_bessel_theorem.tex#L5) – [paper/sections/2_bessel_theorem.tex:L9](paper/sections/2_bessel_theorem.tex#L9) | `c24204983b266f9bb732313cf81c35c2e58d341a0a492fe8f74b5044308cfa63` |
| D02 | \[...\] | [paper/sections/2_bessel_theorem.tex:L14](paper/sections/2_bessel_theorem.tex#L14) – [paper/sections/2_bessel_theorem.tex:L16](paper/sections/2_bessel_theorem.tex#L16) | `03960baa56da129489cad0cf3e294e4dc238afa55254260fe155196e9f0e95a9` |
| D03 | \[...\] | [paper/sections/2_bessel_theorem.tex:L18](paper/sections/2_bessel_theorem.tex#L18) – [paper/sections/2_bessel_theorem.tex:L22](paper/sections/2_bessel_theorem.tex#L22) | `43013d30b46fbfbeb98551381be6266aa21e70662f58458d48498a9cd7be102f` |
| D04 | \[...\] | [paper/sections/2_bessel_theorem.tex:L28](paper/sections/2_bessel_theorem.tex#L28) – [paper/sections/2_bessel_theorem.tex:L31](paper/sections/2_bessel_theorem.tex#L31) | `a3d526bda1bc8c1f94b7330739e9b57613462cf3a8e4d6fdc3615679496ce2fc` |
| D05 | \[...\] | [paper/sections/2_bessel_theorem.tex:L42](paper/sections/2_bessel_theorem.tex#L42) – [paper/sections/2_bessel_theorem.tex:L45](paper/sections/2_bessel_theorem.tex#L45) | `74edcbd8b843e25c77644fa5740551755f276775ea5d7a492d49a9ecad12f79b` |
| D06 | \[...\] | [paper/sections/3_literal_block.tex:L4](paper/sections/3_literal_block.tex#L4) – [paper/sections/3_literal_block.tex:L7](paper/sections/3_literal_block.tex#L7) | `9bb9bdc05712ec7d9e381839313b775a2c68ed781153db53054eef43c63ac2ce` |
| D07 | \[...\] | [paper/sections/3_literal_block.tex:L10](paper/sections/3_literal_block.tex#L10) – [paper/sections/3_literal_block.tex:L16](paper/sections/3_literal_block.tex#L16) | `0994e4559732fb02ec0f40d70e21a3f17e0384ac791df67723b0fee4fc70f958` |
| D08 | \[...\] | [paper/sections/3_literal_block.tex:L19](paper/sections/3_literal_block.tex#L19) – [paper/sections/3_literal_block.tex:L23](paper/sections/3_literal_block.tex#L23) | `f78da6cebb8b9378305bd472db8ecb850a9587dc8c03e563e4fcb156ef5c2623` |
| D09 | \[...\] | [paper/sections/4_certificate.tex:L4](paper/sections/4_certificate.tex#L4) – [paper/sections/4_certificate.tex:L6](paper/sections/4_certificate.tex#L6) | `81c44ea0feba5368b88340ecf6d289745c6cf075a8e7a0fd5bf1bf67d9a5d980` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/main.tex:L13](paper/main.tex#L13): `\title{Depth-Uniform Bessel Stability\\for Normalized Prime-Shell Collision Rows}`
- [paper/sections/0_abstract.tex:L2](paper/sections/0_abstract.tex#L2): `We prove a depth-uniform conditioning theorem for normalized collision rows in a`
- [paper/sections/0_abstract.tex:L13](paper/sections/0_abstract.tex#L13): `open.`
- [paper/sections/1_introduction.tex:L9](paper/sections/1_introduction.tex#L9): `We show that this does not happen in the short-multiplier dilated clock.  The decisive`
- [paper/sections/1_introduction.tex:L17](paper/sections/1_introduction.tex#L17): `the operator uniformly bounded as $L$ grows, but it does not force the assembled energy`
- [paper/sections/1_introduction.tex:L24](paper/sections/1_introduction.tex#L24): `separate crosswalk theorem, not a consequence of the Bessel estimate.`
- [paper/sections/2_bessel_theorem.tex:L3](paper/sections/2_bessel_theorem.tex#L3): `Let $X$ be a finite coordinate set and $\Hcal$ a Hilbert space.  For each prime-row`
- [paper/sections/2_bessel_theorem.tex:L10](paper/sections/2_bessel_theorem.tex#L10): `No common profile or equal support size is assumed.`
- [paper/sections/2_bessel_theorem.tex:L50](paper/sections/2_bessel_theorem.tex#L50): `uniform in $Q,L$ and in all nonzero row amplitudes.`
- [paper/sections/3_literal_block.tex:L17](paper/sections/3_literal_block.tex#L17): `because $5\cdot71+11\cdot67=1092$.  Uniform unit rows have inner product $2/6=1/3$.`
- [paper/sections/4_certificate.tex:L1](paper/sections/4_certificate.tex#L1): `\section{Finite reproduction and claim boundary}`
- [paper/sections/4_certificate.tex:L20](paper/sections/4_certificate.tex#L20): `All computations are exact finite reproduction, not evidence for arithmetic`
- [paper/sections/5_conclusion.tex:L3](paper/sections/5_conclusion.tex#L3): `Multiplicity two turns unit-row normalization into a complete depth-uniform`
- [paper/sections/5_conclusion.tex:L7](paper/sections/5_conclusion.tex#L7): `It is not an arithmetic saving.  The literal Q39 block realizes both amplification and`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#thm:bessel` → `sections/2_bessel_theorem.tex#L12` (existing project target or original TeX label line).
- Link relocation: `#thm:bessel` → `sections/2_bessel_theorem.tex#L12` (existing project target or original TeX label line).
