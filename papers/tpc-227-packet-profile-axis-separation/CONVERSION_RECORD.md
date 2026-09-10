# TPC-227 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `a57f9023157a2c420a15d0ae86e57843b7636eb881eba74009618406f826ebae`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `9b68ac9c726ef8e871943fc5a4a116ef1ac98d95b506a1ed365cc1bfa0aafa31`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `7541c930a2e65f7fa097af9e852d8bd3ac424e2abec70bcebbedd644dae67832`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `4e5213985f2d6f3f8955235382d1fc22bbd350a5dcf1c60b1f6521426c8ddf43`.
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
| [paper/main.tex](paper/main.tex) | `a57f9023157a2c420a15d0ae86e57843b7636eb881eba74009618406f826ebae` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `d74a1e7ee2279901279de8fe1807557514889910f505cc9ea7b9503bc07550bf` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `d1214b26582e277c2efcee543eccdbfb97430ad10cc495b2192d9a350710335b` |
| [paper/sections/2_source_typing.tex](paper/sections/2_source_typing.tex) | `032594269988fa0da36e8b0efa4403f8ae6b5975bc9964f263a17fcd9fd6c2f6` |
| [paper/sections/3_gram_criterion.tex](paper/sections/3_gram_criterion.tex) | `dd541ad6e1da9f735616aadedabe96cf6c6b0b63093d8b5dd05645b0598e776e` |
| [paper/sections/4_collision_witness.tex](paper/sections/4_collision_witness.tex) | `ab57c99f168c20f2518a7b09497ffb8cbb1cf4b553f326d67157829beb810100` |
| [paper/sections/5_certification.tex](paper/sections/5_certification.tex) | `36cd03bf3760621c7dbc738c5407ac86996fd5ce9ce77580cd44a16e3e506720` |
| [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) | `02260096bc2945c38640d2f1c68ff7f7942b7e29bc634b132565c074ff1ad619` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L33](paper/main.tex#L33) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L36](paper/main.tex#L36) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L37](paper/main.tex#L37) | `\input{sections/2_source_typing}` | [paper/sections/2_source_typing.tex](paper/sections/2_source_typing.tex) |
| [paper/main.tex:L38](paper/main.tex#L38) | `\input{sections/3_gram_criterion}` | [paper/sections/3_gram_criterion.tex](paper/sections/3_gram_criterion.tex) |
| [paper/main.tex:L39](paper/main.tex#L39) | `\input{sections/4_collision_witness}` | [paper/sections/4_collision_witness.tex](paper/sections/4_collision_witness.tex) |
| [paper/main.tex:L40](paper/main.tex#L40) | `\input{sections/5_certification}` | [paper/sections/5_certification.tex](paper/sections/5_certification.tex) |
| [paper/main.tex:L41](paper/main.tex#L41) | `\input{sections/6_conclusion}` | [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `The two axes in the source compiler` | [paper/sections/2_source_typing.tex:L1](paper/sections/2_source_typing.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Exact Gram compatibility` | [paper/sections/3_gram_criterion.tex:L1](paper/sections/3_gram_criterion.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `The first-collision obstruction` | [paper/sections/4_collision_witness.tex:L1](paper/sections/4_collision_witness.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Exact certification` | [paper/sections/5_certification.tex:L1](paper/sections/5_certification.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/6_conclusion.tex:L1](paper/sections/6_conclusion.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | [paper/main.tex:L44](paper/main.tex#L44) | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `60` before writing and `60` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `6719a8c3b945c4e53dc7dd7bbd44b292d16995f7a2120b486c2f02fd8f67bb78`.
- Source theorem/proof environment starts: remark at [paper/sections/2_source_typing.tex:L24](paper/sections/2_source_typing.tex#L24), theorem at [paper/sections/3_gram_criterion.tex:L5](paper/sections/3_gram_criterion.tex#L5), proof at [paper/sections/3_gram_criterion.tex:L20](paper/sections/3_gram_criterion.tex#L20), corollary at [paper/sections/4_collision_witness.tex:L33](paper/sections/4_collision_witness.tex#L33).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | [paper/sections/1_introduction.tex:L6](paper/sections/1_introduction.tex#L6) – [paper/sections/1_introduction.tex:L11](paper/sections/1_introduction.tex#L11) | `669ed47563b150077379f57e096c78cf9bfccbb16f7ea4385b189b00dfda1369` |
| D02 | equation | [paper/sections/2_source_typing.tex:L6](paper/sections/2_source_typing.tex#L6) – [paper/sections/2_source_typing.tex:L10](paper/sections/2_source_typing.tex#L10) | `2174d97a71a5789381426d170ce68c6bad88f3fa5aad67c5517e05861700b3c3` |
| D03 | equation | [paper/sections/2_source_typing.tex:L14](paper/sections/2_source_typing.tex#L14) – [paper/sections/2_source_typing.tex:L18](paper/sections/2_source_typing.tex#L18) | `50a125b2bbd4b29ee9e6ef48b80c3a8fbd44e4ed33add297102dd6a3f77bda4f` |
| D04 | equation | [paper/sections/3_gram_criterion.tex:L8](paper/sections/3_gram_criterion.tex#L8) – [paper/sections/3_gram_criterion.tex:L12](paper/sections/3_gram_criterion.tex#L12) | `a829a9094752690e1e77cf46124eabe76cc27ccbbba0b4f5d75d7c8efe464069` |
| D05 | equation | [paper/sections/3_gram_criterion.tex:L14](paper/sections/3_gram_criterion.tex#L14) – [paper/sections/3_gram_criterion.tex:L17](paper/sections/3_gram_criterion.tex#L17) | `3db9505df881544596a75c02f4bf1f430b3a761f33a146d408ae05c5e30f1d83` |
| D06 | \[...\] | [paper/sections/3_gram_criterion.tex:L23](paper/sections/3_gram_criterion.tex#L23) – [paper/sections/3_gram_criterion.tex:L25](paper/sections/3_gram_criterion.tex#L25) | `f98df6cb94d9a53ca923b5f4ea516e05544a8f5b6e787d87fd35fc6d8574b01f` |
| D07 | equation | [paper/sections/3_gram_criterion.tex:L27](paper/sections/3_gram_criterion.tex#L27) – [paper/sections/3_gram_criterion.tex:L32](paper/sections/3_gram_criterion.tex#L32) | `250f3d13fd28be3f6760dfb1eff4884b9c54d35cbe31a889f868e2576966a766` |
| D08 | equation | [paper/sections/3_gram_criterion.tex:L35](paper/sections/3_gram_criterion.tex#L35) – [paper/sections/3_gram_criterion.tex:L38](paper/sections/3_gram_criterion.tex#L38) | `55a365c4a70d6495203f26e0120ad6ae4401578e5db189d2a3373a1321aac8d9` |
| D09 | \[...\] | [paper/sections/3_gram_criterion.tex:L50](paper/sections/3_gram_criterion.tex#L50) – [paper/sections/3_gram_criterion.tex:L55](paper/sections/3_gram_criterion.tex#L55) | `209a07dd1177a17cee41e853e5987869c9e2e7051aae1396171401cd27726fe5` |
| D10 | \[...\] | [paper/sections/4_collision_witness.tex:L4](paper/sections/4_collision_witness.tex#L4) – [paper/sections/4_collision_witness.tex:L6](paper/sections/4_collision_witness.tex#L6) | `4b830bb8ceae9161a023159a372f7cf5abd859316ba78f10c161115dfb6a21cc` |
| D11 | \[...\] | [paper/sections/4_collision_witness.tex:L10](paper/sections/4_collision_witness.tex#L10) – [paper/sections/4_collision_witness.tex:L12](paper/sections/4_collision_witness.tex#L12) | `12c475026b0c80071445e55b816e8ebcb8ea5329498ae93af970450b615d61a8` |
| D12 | equation | [paper/sections/4_collision_witness.tex:L14](paper/sections/4_collision_witness.tex#L14) – [paper/sections/4_collision_witness.tex:L18](paper/sections/4_collision_witness.tex#L18) | `0a20999f2f23651dabf2208fa0c682743aba63114442508c83ded4621b869e22` |
| D13 | equation | [paper/sections/4_collision_witness.tex:L20](paper/sections/4_collision_witness.tex#L20) – [paper/sections/4_collision_witness.tex:L23](paper/sections/4_collision_witness.tex#L23) | `4bb6de22e6225839d443021993372394d2764b1ec5ab92c94e5b4653f7dc5bc4` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/0_abstract.tex:L2](paper/sections/0_abstract.tex#L2): `packet energies.  A previous finite collision model obtained a negative cross term by`
- [paper/sections/0_abstract.tex:L11](paper/sections/0_abstract.tex#L11): `transfer of the finite profile sign to the physical source compiler while preserving the`
- [paper/sections/0_abstract.tex:L12](paper/sections/0_abstract.tex#L12): `finite model result itself.  The result is structural; no arithmetic cancellation or`
- [paper/sections/1_introduction.tex:L13](paper/sections/1_introduction.tex#L13): `$\mathcal V^{\circ}_{\mathcal Q,H}$ \cite{tpc59}.  Later finite row models allowed`
- [paper/sections/1_introduction.tex:L21](paper/sections/1_introduction.tex#L21): `the source phase in \eqref{eq:physical-polarization}.  The answer is not a matter of`
- [paper/sections/1_introduction.tex:L31](paper/sections/1_introduction.tex#L31): `and a fail-closed certificate.  It does not estimate the arithmetic source sequences.`
- [paper/sections/2_source_typing.tex:L11](paper/sections/2_source_typing.tex#L11): `The packet label $j$ changes the input $x+\ii^j y$; it does not change $T$.`
- [paper/sections/2_source_typing.tex:L21](paper/sections/2_source_typing.tex#L21): `a uniform norm bound on $T_j$ controls size but not the phase moments that remove the`
- [paper/sections/3_gram_criterion.tex:L33](paper/sections/3_gram_criterion.tex#L33): `Assume \eqref{eq:target}.  Setting $y=0$ and polarizing the real and imaginary`
- [paper/sections/3_gram_criterion.tex:L49](paper/sections/3_gram_criterion.tex#L49): `For real finite matrices, Theorem~\ref{thm:gram} is checked by the exact conditions`
- [paper/sections/4_collision_witness.tex:L28](paper/sections/4_collision_witness.tex#L28): `This conclusion is scoped.  It does not invalidate the finite odd-profile theorem:`
- [paper/sections/5_certification.tex:L30](paper/sections/5_certification.tex#L30): `negative controls, and witness check.  These tests certify the finite algebra and claim`
- [paper/sections/6_conclusion.tex:L13](paper/sections/6_conclusion.tex#L13): `$1/400$ budget remain open.`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:physical-polarization` → `sections/1_introduction.tex#L10` (existing project target or original TeX label line).
- Link relocation: `#eq:physical-polarization` → `sections/1_introduction.tex#L10` (existing project target or original TeX label line).
- Link relocation: `#eq:packet-transform` → `sections/2_source_typing.tex#L17` (existing project target or original TeX label line).
- Link relocation: `#eq:common-transform` → `sections/2_source_typing.tex#L9` (existing project target or original TeX label line).
- Link relocation: `#eq:packet-transform` → `sections/2_source_typing.tex#L17` (existing project target or original TeX label line).
- Link relocation: `#eq:packet-transform` → `sections/2_source_typing.tex#L17` (existing project target or original TeX label line).
- Link relocation: `#eq:target` → `sections/3_gram_criterion.tex#L11` (existing project target or original TeX label line).
- Link relocation: `#eq:two-crosses` → `sections/3_gram_criterion.tex#L37` (existing project target or original TeX label line).
- Link relocation: `#eq:four-gram` → `sections/3_gram_criterion.tex#L16` (existing project target or original TeX label line).
- Link relocation: `#eq:packet-transform` → `sections/2_source_typing.tex#L17` (existing project target or original TeX label line).
- Link relocation: `#eq:target` → `sections/3_gram_criterion.tex#L11` (existing project target or original TeX label line).
- Link relocation: `#thm:gram` → `sections/3_gram_criterion.tex#L6` (existing project target or original TeX label line).
- Link relocation: `#thm:gram` → `sections/3_gram_criterion.tex#L6` (existing project target or original TeX label line).
- Link relocation: `#eq:witness-difference` → `sections/4_collision_witness.tex#L22` (existing project target or original TeX label line).
- Link relocation: `#tab:fixtures` → `sections/5_certification.tex#L23` (existing project target or original TeX label line).
- Link relocation: `#thm:gram` → `sections/3_gram_criterion.tex#L6` (existing project target or original TeX label line).
