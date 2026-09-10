# TPC-231 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `8e2a4ca9ce5da715d5ad28b6c868e886c65855fe4100be7527661f05bfe3d960`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `64522f722c3c8d609bd17a339a1ef2a21d296d74fba38876b2a1b2767343fa62`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `4b542c29773f1ae2f41ff0d9bb8f96dd3f5212dbe8c9d13eef541c2083fcc0d0`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `b1d2170a5af9f57cbf08d4859b76a8241db6e72bbe523c84975e36d10667f6a6`.
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
| [paper/main.tex](paper/main.tex) | `8e2a4ca9ce5da715d5ad28b6c868e886c65855fe4100be7527661f05bfe3d960` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `625eb1b202a8d9f36b79626e459de3f1d0c87ea250f81074d80a758919c1bacf` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `333df01513d9626291c49691341d9ea19aa46b176c7caeecb3bfd64dfb577377` |
| [paper/sections/2_local_arithmetic.tex](paper/sections/2_local_arithmetic.tex) | `cf407dbf71b44d5f7a23451d2dc012aeac332815c2354eb4c3afd33b03d350f7` |
| [paper/sections/3_selberg_bound.tex](paper/sections/3_selberg_bound.tex) | `2e25d8b215438a19fe438b4da4071a6631054c7903ec1fe303b21f784d2f4f1f` |
| [paper/sections/4_finite_families.tex](paper/sections/4_finite_families.tex) | `c5c12a0f3e6151ae661aacb0048cbc6ac55e403d5b77a5615aa2caa0b55e6d04` |
| [paper/sections/5_certificate.tex](paper/sections/5_certificate.tex) | `8fb86bbfd30b4080114f8fed50954fd4d1613186f4a1313ceee25c5d13c13e18` |
| [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) | `5375fd6d7988005fba9be733dec21eac66f2ddf4512904716d9e21d6198d5cca` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L21](paper/main.tex#L21) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L22](paper/main.tex#L22) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L23](paper/main.tex#L23) | `\input{sections/2_local_arithmetic}` | [paper/sections/2_local_arithmetic.tex](paper/sections/2_local_arithmetic.tex) |
| [paper/main.tex:L24](paper/main.tex#L24) | `\input{sections/3_selberg_bound}` | [paper/sections/3_selberg_bound.tex](paper/sections/3_selberg_bound.tex) |
| [paper/main.tex:L25](paper/main.tex#L25) | `\input{sections/4_finite_families}` | [paper/sections/4_finite_families.tex](paper/sections/4_finite_families.tex) |
| [paper/main.tex:L26](paper/main.tex#L26) | `\input{sections/5_certificate}` | [paper/sections/5_certificate.tex](paper/sections/5_certificate.tex) |
| [paper/main.tex:L27](paper/main.tex#L27) | `\input{sections/6_conclusion}` | [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Exact local arithmetic` | [paper/sections/2_local_arithmetic.tex:L1](paper/sections/2_local_arithmetic.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `The sieve density theorem` | [paper/sections/3_selberg_bound.tex:L1](paper/sections/3_selberg_bound.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Finite families and the matched-mass consequence` | [paper/sections/4_finite_families.tex:L1](paper/sections/4_finite_families.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Finite certification and adversarial controls` | [paper/sections/5_certificate.tex:L1](paper/sections/5_certificate.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion and firewall` | [paper/sections/6_conclusion.tex:L1](paper/sections/6_conclusion.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | [paper/main.tex:L29](paper/main.tex#L29) | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `110` before writing and `110` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `15`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `c8b4b271538b2d99381d9994babc8e9bb3ad14a9e9669507c42b48e3781842f8`.
- Source theorem/proof environment starts: lemma at [paper/sections/2_local_arithmetic.tex:L20](paper/sections/2_local_arithmetic.tex#L20), proof at [paper/sections/2_local_arithmetic.tex:L32](paper/sections/2_local_arithmetic.tex#L32), theorem at [paper/sections/3_selberg_bound.tex:L3](paper/sections/3_selberg_bound.tex#L3), proof at [paper/sections/3_selberg_bound.tex:L12](paper/sections/3_selberg_bound.tex#L12), theorem at [paper/sections/4_finite_families.tex:L5](paper/sections/4_finite_families.tex#L5), proof at [paper/sections/4_finite_families.tex:L19](paper/sections/4_finite_families.tex#L19), corollary at [paper/sections/4_finite_families.tex:L53](paper/sections/4_finite_families.tex#L53).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/0_abstract.tex:L6](paper/sections/0_abstract.tex#L6) – [paper/sections/0_abstract.tex:L9](paper/sections/0_abstract.tex#L9) | `70263eac2bb6c834dbbe1e8e9fc5b93ce07b9f27afa482d2339182357f9831fe` |
| D02 | equation | [paper/sections/1_introduction.tex:L4](paper/sections/1_introduction.tex#L4) – [paper/sections/1_introduction.tex:L6](paper/sections/1_introduction.tex#L6) | `e8daefd32e95b5cae6bf7bf131251b3a1a8341f5fd7579005fe9d06072db3c7b` |
| D03 | equation | [paper/sections/1_introduction.tex:L11](paper/sections/1_introduction.tex#L11) – [paper/sections/1_introduction.tex:L13](paper/sections/1_introduction.tex#L13) | `4ea24e50744075427603f1da3b14a658e6a97404872b55627249266e461fa8b6` |
| D04 | equation | [paper/sections/2_local_arithmetic.tex:L6](paper/sections/2_local_arithmetic.tex#L6) – [paper/sections/2_local_arithmetic.tex:L8](paper/sections/2_local_arithmetic.tex#L8) | `d6d6f83c3332a9ee2a899f6534e78a0a5e0f9a6f86e74261d7b26f490c0e8b17` |
| D05 | equation | [paper/sections/2_local_arithmetic.tex:L10](paper/sections/2_local_arithmetic.tex#L10) – [paper/sections/2_local_arithmetic.tex:L12](paper/sections/2_local_arithmetic.tex#L12) | `cddcd0ab4b884523b23de5dfb7755528fc0cd734f499a50513338aeff236a908` |
| D06 | \[...\] | [paper/sections/2_local_arithmetic.tex:L22](paper/sections/2_local_arithmetic.tex#L22) – [paper/sections/2_local_arithmetic.tex:L28](paper/sections/2_local_arithmetic.tex#L28) | `bc0f8aef77a528771aea58d6368d72cdd6fe6be277950dc4a50e4ea8a9e83864` |
| D07 | equation | [paper/sections/2_local_arithmetic.tex:L41](paper/sections/2_local_arithmetic.tex#L41) – [paper/sections/2_local_arithmetic.tex:L45](paper/sections/2_local_arithmetic.tex#L45) | `0771f60dfc37d7bbd12eb7754a44053429b4962706399b99e321deeedcd5c298` |
| D08 | \[...\] | [paper/sections/3_selberg_bound.tex:L5](paper/sections/3_selberg_bound.tex#L5) – [paper/sections/3_selberg_bound.tex:L8](paper/sections/3_selberg_bound.tex#L8) | `259af2a43988cc160818f903737868e40d56b2de4db9c22522cc5ba6b5954cab` |
| D09 | \[...\] | [paper/sections/3_selberg_bound.tex:L15](paper/sections/3_selberg_bound.tex#L15) – [paper/sections/3_selberg_bound.tex:L18](paper/sections/3_selberg_bound.tex#L18) | `ee4942f0a3a3677b0b27a17a4f1b27a70dadfa2d19cc72891635ba61d4d85cf4` |
| D10 | \[...\] | [paper/sections/3_selberg_bound.tex:L25](paper/sections/3_selberg_bound.tex#L25) – [paper/sections/3_selberg_bound.tex:L29](paper/sections/3_selberg_bound.tex#L29) | `b18823cbe3f43ae6cf7823359e8f744f722a9fe0470fd523df925f6e07148e10` |
| D11 | \[...\] | [paper/sections/4_finite_families.tex:L8](paper/sections/4_finite_families.tex#L8) – [paper/sections/4_finite_families.tex:L10](paper/sections/4_finite_families.tex#L10) | `00f94eef79e323a9f83a11298249b4ad14a225647c6a9f0dba3bae151fb2266d` |
| D12 | \[...\] | [paper/sections/4_finite_families.tex:L12](paper/sections/4_finite_families.tex#L12) – [paper/sections/4_finite_families.tex:L15](paper/sections/4_finite_families.tex#L15) | `889ca5c5b4c60a34359ed0ecceb789fb315f50f51a236ba39422a2d7fbda482e` |
| D13 | \[...\] | [paper/sections/4_finite_families.tex:L31](paper/sections/4_finite_families.tex#L31) – [paper/sections/4_finite_families.tex:L33](paper/sections/4_finite_families.tex#L33) | `fe887f7eb35b3a5d634fc9737432fef3ef0496e5757eb12cc6fb773283d440d1` |
| D14 | equation | [paper/sections/4_finite_families.tex:L37](paper/sections/4_finite_families.tex#L37) – [paper/sections/4_finite_families.tex:L41](paper/sections/4_finite_families.tex#L41) | `615ae443cbee28c4e2b05d1d83346ea8d94db3e25974bdcd882b9344ea28df38` |
| D15 | \[...\] | [paper/sections/4_finite_families.tex:L49](paper/sections/4_finite_families.tex#L49) – [paper/sections/4_finite_families.tex:L51](paper/sections/4_finite_families.tex#L51) | `321ea295c684e55f269fce10afd6b4543ca5f409e3215c54a272c462aa7958cf` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/main.tex:L14](paper/main.tex#L14): `\title{A Finite-Resonance Sieve Obstruction on Prime Shells}`
- [paper/sections/0_abstract.tex:L10](paper/sections/0_abstract.tex#L10): `The same conclusion holds for every fixed finite family of primitive nondegenerate`
- [paper/sections/0_abstract.tex:L14](paper/sections/0_abstract.tex#L14): `anti-alignment.  This is a scoped arithmetic obstruction, not a prime-pair lower bound`
- [paper/sections/1_introduction.tex:L24](paper/sections/1_introduction.tex#L24): `Our second result isolates the real scope of the obstruction: any \emph{fixed finite}`
- [paper/sections/2_local_arithmetic.tex:L3](paper/sections/2_local_arithmetic.tex#L3): `Assume $(Q,21)=1$ and write $Q=3t+a$, where $a\in\{1,2\}$.  Reducing`
- [paper/sections/3_selberg_bound.tex:L4](paper/sections/3_selberg_bound.tex#L4): `Uniformly for $Q\ge8$,`
- [paper/sections/4_finite_families.tex:L1](paper/sections/4_finite_families.tex#L1): `\section{Finite families and the matched-mass consequence}`
- [paper/sections/4_finite_families.tex:L5](paper/sections/4_finite_families.tex#L5): `\begin{theorem}[fixed finite resonance families]\label{thm:family}`
- [paper/sections/4_finite_families.tex:L6](paper/sections/4_finite_families.tex#L6): `Fix a finite set $\mathcal R$ of triples $(a,b,c)$ with $a,b>0$, $(a,b)=1$, and`
- [paper/sections/4_finite_families.tex:L45](paper/sections/4_finite_families.tex#L45): `fixed finite family.`
- [paper/sections/4_finite_families.tex:L62](paper/sections/4_finite_families.tex#L62): `It does not address a number of channels growing with $Q$.`
- [paper/sections/5_certificate.tex:L1](paper/sections/5_certificate.tex#L1): `\section{Finite certification and adversarial controls}`
- [paper/sections/5_certificate.tex:L27](paper/sections/5_certificate.tex#L27): `\caption{Exact finite reproduction scan.}`
- [paper/sections/6_conclusion.tex:L7](paper/sections/6_conclusion.tex#L7): `obstruction holds for every fixed finite family of linear resonances.`
- [paper/sections/6_conclusion.tex:L12](paper/sections/6_conclusion.tex#L12): `first-resonance and fixed-finite-family branches are closed, while full Gate B and its`
- [paper/sections/6_conclusion.tex:L13](paper/sections/6_conclusion.tex#L13): `strict $1/400$ endpoint remain open globally.`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:toll` → `sections/1_introduction.tex#L12` (existing project target or original TeX label line).
- Link relocation: `#eq:resonance` → `sections/1_introduction.tex#L5` (existing project target or original TeX label line).
- Link relocation: `#eq:forms` → `sections/2_local_arithmetic.tex#L7` (existing project target or original TeX label line).
- Link relocation: `#eq:determinant` → `sections/2_local_arithmetic.tex#L11` (existing project target or original TeX label line).
- Link relocation: `#lem:roots` → `sections/2_local_arithmetic.tex#L20` (existing project target or original TeX label line).
- Link relocation: `#eq:series` → `sections/2_local_arithmetic.tex#L44` (existing project target or original TeX label line).
- Link relocation: `#thm:3716` → `sections/3_selberg_bound.tex#L3` (existing project target or original TeX label line).
- Link relocation: `#thm:family` → `sections/4_finite_families.tex#L5` (existing project target or original TeX label line).
- Link relocation: `#eq:graphtransfer` → `sections/4_finite_families.tex#L40` (existing project target or original TeX label line).
- Link relocation: `#thm:family` → `sections/4_finite_families.tex#L5` (existing project target or original TeX label line).
- Link relocation: `#tab:scan` → `sections/5_certificate.tex#L28` (existing project target or original TeX label line).
