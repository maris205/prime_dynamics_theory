# TPC-226 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `3e2f4ce8a9036c87614d372b8402f995b529ceeee856714cbae328b6c13be159`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `715684b37846056875c94c497d79d4a802a16d49cb926424eaa8ad6cd61ce749`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `7eacfb5ab87e559531db672b64c40367ccc6f0608bdab3defb2ed379cc43820e`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `c5d5c8ca3a013448322a8c51d0d2d21d5d1924951220e944868b03266645a1c3`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC225_229.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 9 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `3e2f4ce8a9036c87614d372b8402f995b529ceeee856714cbae328b6c13be159` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `5372aabe11f3f340c838dfa7ded98cdf7011b3b4363e5a7f12afe5e0be5ed1c6` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `5ce4305fef8388edd48bbeb03edf1fe35b9401f9b38692bfa2b1e910404bc81d` |
| [paper/sections/2_setup.tex](paper/sections/2_setup.tex) | `db789ca3c291c55e056769c585ba8f38bfabdac83e0bb526db904c994599f9f2` |
| [paper/sections/3_collision_transition.tex](paper/sections/3_collision_transition.tex) | `2def508daac1a340481ff7962a55b5557ca6ab28e15415cf1233b42be5ee31ad` |
| [paper/sections/4_signed_energy.tex](paper/sections/4_signed_energy.tex) | `c2a3bb9febcf3fd41dd12579a18a28e2d24d1d54dfb58b50b44e4750f831aa49` |
| [paper/sections/5_certification.tex](paper/sections/5_certification.tex) | `776d11eb57b8bfe85b745933c43b489b0224f645b1d3e9170e1497523eacbbb5` |
| [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) | `59173c4766acff55ab8ba0f455994a9b2d0275fe08f5cd8649bc9c627b28d2e0` |
| [paper/sections/A_case_table.tex](paper/sections/A_case_table.tex) | `66d6804b7237ac106dbfcb0f3e20780b553aae9bb1ff4a3839bb6f7e7ba7d4a0` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L47](paper/main.tex#L47) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L50](paper/main.tex#L50) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L51](paper/main.tex#L51) | `\input{sections/2_setup}` | [paper/sections/2_setup.tex](paper/sections/2_setup.tex) |
| [paper/main.tex:L52](paper/main.tex#L52) | `\input{sections/3_collision_transition}` | [paper/sections/3_collision_transition.tex](paper/sections/3_collision_transition.tex) |
| [paper/main.tex:L53](paper/main.tex#L53) | `\input{sections/4_signed_energy}` | [paper/sections/4_signed_energy.tex](paper/sections/4_signed_energy.tex) |
| [paper/main.tex:L54](paper/main.tex#L54) | `\input{sections/5_certification}` | [paper/sections/5_certification.tex](paper/sections/5_certification.tex) |
| [paper/main.tex:L55](paper/main.tex#L55) | `\input{sections/6_conclusion}` | [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) |
| [paper/main.tex:L61](paper/main.tex#L61) | `\input{sections/A_case_table}` | [paper/sections/A_case_table.tex](paper/sections/A_case_table.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Literal primitive rows and claim boundary` | [paper/sections/2_setup.tex:L1](paper/sections/2_setup.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `The first primitive-collision transition` | [paper/sections/3_collision_transition.tex:L1](paper/sections/3_collision_transition.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Signed energy on the resonance graph` | [paper/sections/4_signed_energy.tex:L1](paper/sections/4_signed_energy.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Exact certification and adversarial controls` | [paper/sections/5_certification.tex:L1](paper/sections/5_certification.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/6_conclusion.tex:L1](paper/sections/6_conclusion.tex#L1) | 2, 4 | `UNMAPPED_OR_AMBIGUOUS` |
| `Coefficient case table` | [paper/sections/A_case_table.tex:L1](paper/sections/A_case_table.tex#L1) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `References (external bibliography)` | [paper/main.tex:L58](paper/main.tex#L58) | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `174` before writing and `174` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `320c6658d5d98a8c5d687861c16af1d1bf00f05dac39be14e995ab2ee2c5ca1e`.
- Source theorem/proof environment starts: theorem at [paper/sections/3_collision_transition.tex:L11](paper/sections/3_collision_transition.tex#L11), proof at [paper/sections/3_collision_transition.tex:L24](paper/sections/3_collision_transition.tex#L24), proposition at [paper/sections/4_signed_energy.tex:L19](paper/sections/4_signed_energy.tex#L19), proof at [paper/sections/4_signed_energy.tex:L33](paper/sections/4_signed_energy.tex#L33).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/1_introduction.tex:L19](paper/sections/1_introduction.tex#L19) – [paper/sections/1_introduction.tex:L21](paper/sections/1_introduction.tex#L21) | `079ada9b041a3668293741fc885357518bcfb3320dc612792c819600ec373c33` |
| D02 | \[...\] | [paper/sections/2_setup.tex:L5](paper/sections/2_setup.tex#L5) – [paper/sections/2_setup.tex:L7](paper/sections/2_setup.tex#L7) | `5f71e436d292f79a0706bc5d513c592de8dbc609e18128a5bf8cf1293ec2792b` |
| D03 | \[...\] | [paper/sections/2_setup.tex:L9](paper/sections/2_setup.tex#L9) – [paper/sections/2_setup.tex:L13](paper/sections/2_setup.tex#L13) | `eb56cadc2b95b0844e61b2017e51f57fe9297dc6a6ebfe88a9abaaa2d1f7f40d` |
| D04 | equation | [paper/sections/2_setup.tex:L15](paper/sections/2_setup.tex#L15) – [paper/sections/2_setup.tex:L21](paper/sections/2_setup.tex#L21) | `49a271cd32a202c5a8c68ac7a5d1342b762b7c1bd763e0d293e62d708d0ed1df` |
| D05 | align | [paper/sections/2_setup.tex:L26](paper/sections/2_setup.tex#L26) – [paper/sections/2_setup.tex:L33](paper/sections/2_setup.tex#L33) | `9fd9352373165c400b848458c8711b6f9c454f2f93b96cfe6bc88e80125a0ade` |
| D06 | \[...\] | [paper/sections/3_collision_transition.tex:L4](paper/sections/3_collision_transition.tex#L4) – [paper/sections/3_collision_transition.tex:L6](paper/sections/3_collision_transition.tex#L6) | `a093c16cf12a326fbb4b8c0f63a32bd4e6c47596db0f028de6c6747893cfe85a` |
| D07 | equation | [paper/sections/3_collision_transition.tex:L16](paper/sections/3_collision_transition.tex#L16) – [paper/sections/3_collision_transition.tex:L19](paper/sections/3_collision_transition.tex#L19) | `6fd0067c38f5e38db7ee03bb84e2b40deb536b2790b18af40017db8ed5d8d2ce` |
| D08 | \[...\] | [paper/sections/3_collision_transition.tex:L26](paper/sections/3_collision_transition.tex#L26) – [paper/sections/3_collision_transition.tex:L28](paper/sections/3_collision_transition.tex#L28) | `c5f827705c60e20c4a852f6a1860327c7ab38aeeb2f9d6c4fd80032c2c46ff27` |
| D09 | equation | [paper/sections/3_collision_transition.tex:L32](paper/sections/3_collision_transition.tex#L32) – [paper/sections/3_collision_transition.tex:L36](paper/sections/3_collision_transition.tex#L36) | `57a7abe29624a50620d954670addb54c86240d68262275f6018ecc7f4cc27fc0` |
| D10 | \[...\] | [paper/sections/3_collision_transition.tex:L75](paper/sections/3_collision_transition.tex#L75) – [paper/sections/3_collision_transition.tex:L79](paper/sections/3_collision_transition.tex#L79) | `b063c28cd3dcdb4594bfb2a63ac639b44e617df2e4b905f2e06cf7635f8a7384` |
| D11 | \[...\] | [paper/sections/4_signed_energy.tex:L5](paper/sections/4_signed_energy.tex#L5) – [paper/sections/4_signed_energy.tex:L7](paper/sections/4_signed_energy.tex#L7) | `772c008e5f89177001161b75c6cd7fd8e9cedc240af4ae54154cb680caea86fb` |
| D12 | equation | [paper/sections/4_signed_energy.tex:L9](paper/sections/4_signed_energy.tex#L9) – [paper/sections/4_signed_energy.tex:L15](paper/sections/4_signed_energy.tex#L15) | `0f7208f63d0d112a0ca1b8c559c4c84ea96c52b00878e21e0b8556a6287fea14` |
| D13 | \[...\] | [paper/sections/4_signed_energy.tex:L36](paper/sections/4_signed_energy.tex#L36) – [paper/sections/4_signed_energy.tex:L39](paper/sections/4_signed_energy.tex#L39) | `34b1cd01cf966514d5526330e94c5a1526ba9ed6aea18e92392f8cddcc41ce8b` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/0_abstract.tex:L14](paper/sections/0_abstract.tex#L14): `physical sign and the arithmetic transfer remain open.`
- [paper/sections/1_introduction.tex:L13](paper/sections/1_introduction.tex#L13): `\cite{lichtman2023primes}.  The present paper does not import such an estimate.  It asks`
- [paper/sections/1_introduction.tex:L14](paper/sections/1_introduction.tex#L14): `a prior structural question: when does the exact finite row geometry first permit a`
- [paper/sections/1_introduction.tex:L33](paper/sections/1_introduction.tex#L33): `\item We prove that the first-transition Gram correction is sign-indefinite across`
- [paper/sections/1_introduction.tex:L39](paper/sections/1_introduction.tex#L39): `The strongest finite witness occurs at $Q=25$.  The same full prime shell gives`
- [paper/sections/1_introduction.tex:L41](paper/sections/1_introduction.tex#L41): `Thus overlap is necessary for the correction, but overlap alone does not pay an AP`
- [paper/sections/1_introduction.tex:L43](paper/sections/1_introduction.tex#L43): `source rather than select it as a finite profile.`
- [paper/sections/2_setup.tex:L23](paper/sections/2_setup.tex#L23): `crosswalk \cite{tpc220}; it is not an optional simplification.`
- [paper/sections/2_setup.tex:L38](paper/sections/2_setup.tex#L38): `The dilation parameter $L$ is a finite modeling choice.  Equation`
- [paper/sections/2_setup.tex:L41](paper/sections/2_setup.tex#L41): `statements.  No arithmetic $L^2$ estimate, fixed-atom credit, or twin-prime conclusion`
- [paper/sections/3_collision_transition.tex:L8](paper/sections/3_collision_transition.tex#L8): `has magnitude at most seven.  The stable assumption $Q\ge8$ therefore gives`
- [paper/sections/5_certification.tex:L7](paper/sections/5_certification.tex#L7): `These counts certify the finite census only.  They are not a density theorem for the`
- [paper/sections/5_certification.tex:L13](paper/sections/5_certification.tex#L13): `floating-point tolerance.  The independent checker does not import the producer and`
- [paper/sections/6_conclusion.tex:L11](paper/sections/6_conclusion.tex#L11): `It does not source the negative sign required by the arithmetic bridge, identify the`
- [paper/sections/6_conclusion.tex:L14](paper/sections/6_conclusion.tex#L14): `$3$--$7$ packet resonance before attempting a uniform AP saving.`
- [paper/sections/A_case_table.tex:L4](paper/sections/A_case_table.tex#L4): `$2L<a+b<4L$ leave only a short finite table.  At $L=2$, the pair $(3,3)$ is`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 5 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:literal-row` → `sections/2_setup.tex#L20` (existing project target or original TeX label line).
- Link relocation: `#eq:resonance` → `sections/3_collision_transition.tex#L18` (existing project target or original TeX label line).
- Link relocation: `#eq:positive-collision` → `sections/3_collision_transition.tex#L35` (existing project target or original TeX label line).
- Link relocation: `#eq:signed-correction` → `sections/4_signed_energy.tex#L14` (existing project target or original TeX label line).
- Link relocation: `#prop:trichotomy` → `sections/4_signed_energy.tex#L20` (existing project target or original TeX label line).
- Link relocation: `#tab:profiles` → `sections/4_signed_energy.tex#L62` (existing project target or original TeX label line).
