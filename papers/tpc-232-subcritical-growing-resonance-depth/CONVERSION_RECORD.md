# TPC-232 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `f92aa2f237cc93a7a46a6a67a841bbc8995ed3879206cbf9e28dfe7af427a6a7`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `4b97ae758773709a7b258546ce140bd3be4a6778fdeff70518459f6a53ddec68`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `4ab4b9fbbd0da15d82b7c08b86af539fa5e50a00f006ad900aadd305b1c52288`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `9ad89bce77c3acf56e4cdd549fb25a20f11911dacfe1325bcf08202343968bab`.
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
| [paper/main.tex](paper/main.tex) | `f92aa2f237cc93a7a46a6a67a841bbc8995ed3879206cbf9e28dfe7af427a6a7` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `22a3e8e7dd2a88bb3517004dc6d7b1215cb76e0eb31ef4ca91b0746f20fe9142` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `fdc1a4f8ef30579f0fe5c7c8f4e74dd6683679f05682f4e8ac120c9bbca7fa54` |
| [paper/sections/2_collision_geometry.tex](paper/sections/2_collision_geometry.tex) | `96773546044548ae060c63e6135bf248f289f8bfa31bb5c569704a2a60fc5886` |
| [paper/sections/3_uniform_sieve.tex](paper/sections/3_uniform_sieve.tex) | `84368cb9e9aa232c82880a372dafd06218190abcb95366589da059ac879e33ff` |
| [paper/sections/4_depth_threshold.tex](paper/sections/4_depth_threshold.tex) | `7c23041e70bdecba5fab6b05ecd9a08d3f3d3d37673c77a341cf9fcf24d8dd82` |
| [paper/sections/5_certificate.tex](paper/sections/5_certificate.tex) | `954ce23948c55a7fd83471e80ba2f6c930993096b1af5b70b2ffd351decd0315` |
| [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) | `6fba640d863c06a74c7489221212d2e6800630921b76a9ac1b9dc880b9ecf959` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L19](paper/main.tex#L19) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L20](paper/main.tex#L20) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L21](paper/main.tex#L21) | `\input{sections/2_collision_geometry}` | [paper/sections/2_collision_geometry.tex](paper/sections/2_collision_geometry.tex) |
| [paper/main.tex:L22](paper/main.tex#L22) | `\input{sections/3_uniform_sieve}` | [paper/sections/3_uniform_sieve.tex](paper/sections/3_uniform_sieve.tex) |
| [paper/main.tex:L23](paper/main.tex#L23) | `\input{sections/4_depth_threshold}` | [paper/sections/4_depth_threshold.tex](paper/sections/4_depth_threshold.tex) |
| [paper/main.tex:L24](paper/main.tex#L24) | `\input{sections/5_certificate}` | [paper/sections/5_certificate.tex](paper/sections/5_certificate.tex) |
| [paper/main.tex:L25](paper/main.tex#L25) | `\input{sections/6_conclusion}` | [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Growing-depth collision geometry` | [paper/sections/2_collision_geometry.tex:L1](paper/sections/2_collision_geometry.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `A coefficient-uniform upper-bound sieve` | [paper/sections/3_uniform_sieve.tex:L1](paper/sections/3_uniform_sieve.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `The subcritical depth threshold` | [paper/sections/4_depth_threshold.tex:L1](paper/sections/4_depth_threshold.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Finite reproduction and adversarial checks` | [paper/sections/5_certificate.tex:L1](paper/sections/5_certificate.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/6_conclusion.tex:L1](paper/sections/6_conclusion.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | [paper/main.tex:L27](paper/main.tex#L27) | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `103` before writing and `103` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `9a95096d9f21fd5377b23a845459322be7c4e742ef65841bb9b023bbee34a1fa`.
- Source theorem/proof environment starts: lemma at [paper/sections/2_collision_geometry.tex:L8](paper/sections/2_collision_geometry.tex#L8), proof at [paper/sections/2_collision_geometry.tex:L18](paper/sections/2_collision_geometry.tex#L18), lemma at [paper/sections/4_depth_threshold.tex:L5](paper/sections/4_depth_threshold.tex#L5), proof at [paper/sections/4_depth_threshold.tex:L12](paper/sections/4_depth_threshold.tex#L12), theorem at [paper/sections/4_depth_threshold.tex:L17](paper/sections/4_depth_threshold.tex#L17), proof at [paper/sections/4_depth_threshold.tex:L24](paper/sections/4_depth_threshold.tex#L24), corollary at [paper/sections/4_depth_threshold.tex:L29](paper/sections/4_depth_threshold.tex#L29), proof at [paper/sections/4_depth_threshold.tex:L37](paper/sections/4_depth_threshold.tex#L37).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/0_abstract.tex:L10](paper/sections/0_abstract.tex#L10) – [paper/sections/0_abstract.tex:L12](paper/sections/0_abstract.tex#L12) | `eaa67ad25b2039ad82af45a41c059810b932c40a18461bc0f51e2a58eda23cda` |
| D02 | \[...\] | [paper/sections/1_introduction.tex:L12](paper/sections/1_introduction.tex#L12) – [paper/sections/1_introduction.tex:L15](paper/sections/1_introduction.tex#L15) | `d5bc64b3ff2998ae61f057ef282949c698024851cd394d86ac8e6e3ce33adf79` |
| D03 | \[...\] | [paper/sections/2_collision_geometry.tex:L11](paper/sections/2_collision_geometry.tex#L11) – [paper/sections/2_collision_geometry.tex:L13](paper/sections/2_collision_geometry.tex#L13) | `0d24da442e625ee2bbf725513a8795c3dbb8a6ebf7c7f64c59eccca4c21acf80` |
| D04 | \[...\] | [paper/sections/2_collision_geometry.tex:L20](paper/sections/2_collision_geometry.tex#L20) – [paper/sections/2_collision_geometry.tex:L22](paper/sections/2_collision_geometry.tex#L22) | `0123ba0a68b8077eef44b1e96511ef8b5990412fa491bc7e7299e85bec31760c` |
| D05 | \[...\] | [paper/sections/3_uniform_sieve.tex:L5](paper/sections/3_uniform_sieve.tex#L5) – [paper/sections/3_uniform_sieve.tex:L7](paper/sections/3_uniform_sieve.tex#L7) | `b5f26e8d2ab3602e6fb4babb296454425e784afa2a5bc3bb5d4034ee8324befe` |
| D06 | \[...\] | [paper/sections/3_uniform_sieve.tex:L9](paper/sections/3_uniform_sieve.tex#L9) – [paper/sections/3_uniform_sieve.tex:L11](paper/sections/3_uniform_sieve.tex#L11) | `f65d597165a46bc5d8e56f5d6b8bc3acaff8ed19d1661e016966a26fbe721c36` |
| D07 | \[...\] | [paper/sections/3_uniform_sieve.tex:L13](paper/sections/3_uniform_sieve.tex#L13) – [paper/sections/3_uniform_sieve.tex:L15](paper/sections/3_uniform_sieve.tex#L15) | `dbcac0c4c866f5ec81eccfbef5d2ede445547d15ff41f8d93f30efb9aed08f8b` |
| D08 | \[...\] | [paper/sections/3_uniform_sieve.tex:L21](paper/sections/3_uniform_sieve.tex#L21) – [paper/sections/3_uniform_sieve.tex:L25](paper/sections/3_uniform_sieve.tex#L25) | `646a7b7f2beabdb6685bf2950cd046560fcdd479da6e1e966051c186c9ae988d` |
| D09 | \[...\] | [paper/sections/3_uniform_sieve.tex:L31](paper/sections/3_uniform_sieve.tex#L31) – [paper/sections/3_uniform_sieve.tex:L34](paper/sections/3_uniform_sieve.tex#L34) | `494bfb04984182f8e60783a51a11ba4cab6c4b2f4355d79717525e5ff429230c` |
| D10 | \[...\] | [paper/sections/3_uniform_sieve.tex:L45](paper/sections/3_uniform_sieve.tex#L45) – [paper/sections/3_uniform_sieve.tex:L53](paper/sections/3_uniform_sieve.tex#L53) | `11e2b8107cae341338e7199b9caf3739ac893dd1cf6446c42797f6def68dc756` |
| D11 | \[...\] | [paper/sections/4_depth_threshold.tex:L7](paper/sections/4_depth_threshold.tex#L7) – [paper/sections/4_depth_threshold.tex:L10](paper/sections/4_depth_threshold.tex#L10) | `043753309ec3be5535a79bb9cadb2b75062c4f531805717f8853064ac9919bde` |
| D12 | \[...\] | [paper/sections/4_depth_threshold.tex:L19](paper/sections/4_depth_threshold.tex#L19) – [paper/sections/4_depth_threshold.tex:L22](paper/sections/4_depth_threshold.tex#L22) | `86cc9683c8eb850c2c9394c37afcddb891e259f910e08b27bd11cfbbe7f23f5b` |
| D13 | \[...\] | [paper/sections/4_depth_threshold.tex:L31](paper/sections/4_depth_threshold.tex#L31) – [paper/sections/4_depth_threshold.tex:L33](paper/sections/4_depth_threshold.tex#L33) | `182ab30389c042875794b31a6841f47cb2089075dd9de3264de6865fbcacfb09` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/0_abstract.tex:L8](paper/sections/0_abstract.tex#L8): `sign-symmetric coordinates.  A coefficient-uniform Selberg upper-bound sieve`
- [paper/sections/0_abstract.tex:L18](paper/sections/0_abstract.tex#L18): `agree on 19 finite scales; these records reproduce the collision geometry but`
- [paper/sections/0_abstract.tex:L20](paper/sections/0_abstract.tex#L20): `obstruction, not a lower bound at critical depth and not an identification`
- [paper/sections/1_introduction.tex:L16](paper/sections/1_introduction.tex#L16): `This is an exact finite family, but the dilation parameter is a modeling`
- [paper/sections/1_introduction.tex:L25](paper/sections/1_introduction.tex#L25): `uniform for all \(L\le(\log Q)^A\), rather than summing a theorem whose`
- [paper/sections/2_collision_geometry.tex:L3](paper/sections/2_collision_geometry.tex#L3): `Let \(\PP_Q\) be the primes in \((Q,2Q)\), put \(h=4LQ\), and assume`
- [paper/sections/2_collision_geometry.tex:L38](paper/sections/2_collision_geometry.tex#L38): `growing-depth channel compiler.  It does not assert that any particular`
- [paper/sections/3_uniform_sieve.tex:L1](paper/sections/3_uniform_sieve.tex#L1): `\section{A coefficient-uniform upper-bound sieve}`
- [paper/sections/3_uniform_sieve.tex:L35](paper/sections/3_uniform_sieve.tex#L35): `This formula controls the uniformity in \(a,b\).  Apply Selberg weights with`
- [paper/sections/3_uniform_sieve.tex:L54](paper/sections/3_uniform_sieve.tex#L54): `Thus (8) is a genuinely uniform growing-coefficient estimate, not a formal`
- [paper/sections/4_depth_threshold.tex:L18](paper/sections/4_depth_threshold.tex#L18): `For fixed \(A>0\), uniformly over \(1\le L\le(\log Q)^A\),`
- [paper/sections/5_certificate.tex:L1](paper/sections/5_certificate.tex#L1): `\section{Finite reproduction and adversarial checks}`
- [paper/sections/5_certificate.tex:L13](paper/sections/5_certificate.tex#L13): `simple-graph degree 28.  These larger finite densities illustrate why a`
- [paper/sections/5_certificate.tex:L23](paper/sections/5_certificate.tex#L23): `All finite records are reproducibility checks.  The asymptotic conclusion`
- [paper/sections/6_conclusion.tex:L3](paper/sections/6_conclusion.tex#L3): `Allowing resonance depth to grow does not immediately remove the support`
- [paper/sections/6_conclusion.tex:L4](paper/sections/6_conclusion.tex#L4): `obstruction.  The exact collision compiler and a coefficient-uniform Selberg`
- [paper/sections/6_conclusion.tex:L11](paper/sections/6_conclusion.tex#L11): `does not prove enough resonances at critical depth.  Second, the dilated clock`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
