# TPC-241 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `6c6d48acf7229c93429668c90fba2938c489bc9f08b5417996afe14e1f58f504`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `f3d0dace0a45ec3c799b4b420f47dc18750079a6ded6c14ea0ada58a56debe4b`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `d644863c9185f4360dc3f5dcb9868d10340269ed82ce3d66a3b6789a0b21d03a`; 8 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `81a95aed7b676e8e879c779bb3026fe3ce4979289aae7d5513707ef12ae60e07`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC240_244.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 12 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `6c6d48acf7229c93429668c90fba2938c489bc9f08b5417996afe14e1f58f504` |
| [paper/math_commands.tex](paper/math_commands.tex) | `18faa9c0e8c7be9f6fea5bdc8b41f0fc6b3aefc3a0f8ae721e4f814c6420142a` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `4cb31772f16c1adece334ced06b1ed2c5cc53502791b8f7582cd63ec4f642c59` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `c5e26bae04708951e90c90c8ca523342f82082267beed291e8ff45f656e4e2c5` |
| [paper/sections/2_frozen_setup.tex](paper/sections/2_frozen_setup.tex) | `0f0e0b39adcdea4aa1200f2feafaa72bc3d7845da80c804a194fc47058ba81d1` |
| [paper/sections/3_row_mass_and_cauchy.tex](paper/sections/3_row_mass_and_cauchy.tex) | `55808d3714d6069ae189a8edc88e1f00386427fe5add37b5c216594fa4839e27` |
| [paper/sections/4_coefficient_liminf.tex](paper/sections/4_coefficient_liminf.tex) | `0213962e8bcea848325cbb072e6ee0236c7ec6c0655272887447ece2347ac150` |
| [paper/sections/5_finite_window_transfer.tex](paper/sections/5_finite_window_transfer.tex) | `44f1c876bd48601d670b17b255a27c2d32e6434adc0d6e0d6e469ef685985a1e` |
| [paper/sections/6_sharpness_and_route.tex](paper/sections/6_sharpness_and_route.tex) | `90fec097463f72faa3bf2934b46c0075fa7dd5938dd6ead81c43f985b3c23e5c` |
| [paper/sections/7_certificate.tex](paper/sections/7_certificate.tex) | `5827b84093b9c6587268aa426b0a5eb4b56f5f81bfcab7146d1a3015e190279d` |
| [paper/sections/8_conclusion.tex](paper/sections/8_conclusion.tex) | `14165c1ac2857c1884a706fea5689cffa3a631e16a78aaa0bf0e1e55c5bf29f7` |
| [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) | `781fa00a19408c63711bbcf89b83fcbc1411cf873d190c1c1f14bbfab7694f07` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L13](paper/main.tex#L13) | `\input{math_commands}` | [paper/math_commands.tex](paper/math_commands.tex) |
| [paper/main.tex:L38](paper/main.tex#L38) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L39](paper/main.tex#L39) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L40](paper/main.tex#L40) | `\input{sections/2_frozen_setup}` | [paper/sections/2_frozen_setup.tex](paper/sections/2_frozen_setup.tex) |
| [paper/main.tex:L41](paper/main.tex#L41) | `\input{sections/3_row_mass_and_cauchy}` | [paper/sections/3_row_mass_and_cauchy.tex](paper/sections/3_row_mass_and_cauchy.tex) |
| [paper/main.tex:L42](paper/main.tex#L42) | `\input{sections/4_coefficient_liminf}` | [paper/sections/4_coefficient_liminf.tex](paper/sections/4_coefficient_liminf.tex) |
| [paper/main.tex:L43](paper/main.tex#L43) | `\input{sections/5_finite_window_transfer}` | [paper/sections/5_finite_window_transfer.tex](paper/sections/5_finite_window_transfer.tex) |
| [paper/main.tex:L44](paper/main.tex#L44) | `\input{sections/6_sharpness_and_route}` | [paper/sections/6_sharpness_and_route.tex](paper/sections/6_sharpness_and_route.tex) |
| [paper/main.tex:L45](paper/main.tex#L45) | `\input{sections/7_certificate}` | [paper/sections/7_certificate.tex](paper/sections/7_certificate.tex) |
| [paper/main.tex:L46](paper/main.tex#L46) | `\input{sections/8_conclusion}` | [paper/sections/8_conclusion.tex](paper/sections/8_conclusion.tex) |
| [paper/main.tex:L52](paper/main.tex#L52) | `\input{sections/A_status_ledger}` | [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Frozen source object` | [paper/sections/2_frozen_setup.tex:L1](paper/sections/2_frozen_setup.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Uniform row mass and residue collision` | [paper/sections/3_row_mass_and_cauchy.tex:L1](paper/sections/3_row_mass_and_cauchy.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `The coefficient liminf` | [paper/sections/4_coefficient_liminf.tex:L1](paper/sections/4_coefficient_liminf.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Finite-window transfer without deleting cross terms` | [paper/sections/5_finite_window_transfer.tex:L1](paper/sections/5_finite_window_transfer.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Fixed-power sharpness and route closure` | [paper/sections/6_sharpness_and_route.tex:L1](paper/sections/6_sharpness_and_route.tex#L1) | 6 | `HEADING_TEXT_MATCH` |
| `Exact finite certificate and adversarial controls` | [paper/sections/7_certificate.tex:L1](paper/sections/7_certificate.tex#L1) | 6 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/8_conclusion.tex:L1](paper/sections/8_conclusion.tex#L1) | 7 | `HEADING_TEXT_MATCH` |
| `Claim and route ledger` | [paper/sections/A_status_ledger.tex:L1](paper/sections/A_status_ledger.tex#L1) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `References (external bibliography)` | [paper/main.tex:L49](paper/main.tex#L49) | 7 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `113` before writing and `113` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `35`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a45c23cb479cc3476be747e5763cb2cb54503298a1a863f9a9972593fa638d11`.
- Source theorem/proof environment starts: lemma at [paper/sections/3_row_mass_and_cauchy.tex:L5](paper/sections/3_row_mass_and_cauchy.tex#L5), proof at [paper/sections/3_row_mass_and_cauchy.tex:L12](paper/sections/3_row_mass_and_cauchy.tex#L12), lemma at [paper/sections/3_row_mass_and_cauchy.tex:L24](paper/sections/3_row_mass_and_cauchy.tex#L24), proof at [paper/sections/3_row_mass_and_cauchy.tex:L32](paper/sections/3_row_mass_and_cauchy.tex#L32), lemma at [paper/sections/3_row_mass_and_cauchy.tex:L61](paper/sections/3_row_mass_and_cauchy.tex#L61), proof at [paper/sections/3_row_mass_and_cauchy.tex:L69](paper/sections/3_row_mass_and_cauchy.tex#L69), theorem at [paper/sections/4_coefficient_liminf.tex:L3](paper/sections/4_coefficient_liminf.tex#L3), proof at [paper/sections/4_coefficient_liminf.tex:L11](paper/sections/4_coefficient_liminf.tex#L11), remark at [paper/sections/4_coefficient_liminf.tex:L48](paper/sections/4_coefficient_liminf.tex#L48), theorem at [paper/sections/5_finite_window_transfer.tex:L7](paper/sections/5_finite_window_transfer.tex#L7), proof at [paper/sections/5_finite_window_transfer.tex:L16](paper/sections/5_finite_window_transfer.tex#L16), remark at [paper/sections/5_finite_window_transfer.tex:L40](paper/sections/5_finite_window_transfer.tex#L40), corollary at [paper/sections/6_sharpness_and_route.tex:L3](paper/sections/6_sharpness_and_route.tex#L3), proof at [paper/sections/6_sharpness_and_route.tex:L14](paper/sections/6_sharpness_and_route.tex#L14).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/0_abstract.tex:L11](paper/sections/0_abstract.tex#L11) – [paper/sections/0_abstract.tex:L14](paper/sections/0_abstract.tex#L14) | `5ab43ec744fc9bb5c1fd273da05b8185922059da9903d985000f18f92a6078f6` |
| D02 | \[...\] | [paper/sections/0_abstract.tex:L17](paper/sections/0_abstract.tex#L17) – [paper/sections/0_abstract.tex:L21](paper/sections/0_abstract.tex#L21) | `eb445cb485707158a0b600c637ebd84fb401f678050b6f5b50aab217f8ad12c9` |
| D03 | \[...\] | [paper/sections/1_introduction.tex:L20](paper/sections/1_introduction.tex#L20) – [paper/sections/1_introduction.tex:L22](paper/sections/1_introduction.tex#L22) | `d9f66167ff679b9de9d10c7ba5f43a96a0a6f6b4f9899695785cbc4eb026e10e` |
| D04 | \[...\] | [paper/sections/1_introduction.tex:L27](paper/sections/1_introduction.tex#L27) – [paper/sections/1_introduction.tex:L29](paper/sections/1_introduction.tex#L29) | `5d28aaf7acca83821ddd3255eb233dfa11401472a39351fe6e1aa88b933e4a01` |
| D05 | equation | [paper/sections/2_frozen_setup.tex:L4](paper/sections/2_frozen_setup.tex#L4) – [paper/sections/2_frozen_setup.tex:L6](paper/sections/2_frozen_setup.tex#L6) | `8acc806564806a1dd7c64b1c24538ffb091080b7a22b02104a6dfb6d04e52638` |
| D06 | \[...\] | [paper/sections/2_frozen_setup.tex:L8](paper/sections/2_frozen_setup.tex#L8) – [paper/sections/2_frozen_setup.tex:L12](paper/sections/2_frozen_setup.tex#L12) | `75d852889073b35bc229a1896299e4032dee0493966096fcbd2b3ca30f2b1b05` |
| D07 | equation | [paper/sections/2_frozen_setup.tex:L14](paper/sections/2_frozen_setup.tex#L14) – [paper/sections/2_frozen_setup.tex:L17](paper/sections/2_frozen_setup.tex#L17) | `b859154a2c549f06c55cd1ebdd8ecd4189378698201643a511a37ea4bb59baf9` |
| D08 | equation | [paper/sections/2_frozen_setup.tex:L23](paper/sections/2_frozen_setup.tex#L23) – [paper/sections/2_frozen_setup.tex:L28](paper/sections/2_frozen_setup.tex#L28) | `1a4017b16ac5c2d4ceda835146b60febebadc7d7b140d864aba66f18f0a85231` |
| D09 | \[...\] | [paper/sections/2_frozen_setup.tex:L31](paper/sections/2_frozen_setup.tex#L31) – [paper/sections/2_frozen_setup.tex:L34](paper/sections/2_frozen_setup.tex#L34) | `2452fb1b1e70aff37ad1433195f9a32bdaecdd9194f5bf2632d97bc22e866810` |
| D10 | equation | [paper/sections/2_frozen_setup.tex:L36](paper/sections/2_frozen_setup.tex#L36) – [paper/sections/2_frozen_setup.tex:L40](paper/sections/2_frozen_setup.tex#L40) | `c68105fdb60cf929ad4efdc59c93b7d722559d05f62437df78463bdad4c565a0` |
| D11 | equation | [paper/sections/2_frozen_setup.tex:L45](paper/sections/2_frozen_setup.tex#L45) – [paper/sections/2_frozen_setup.tex:L47](paper/sections/2_frozen_setup.tex#L47) | `5e0f4e7fc01a0db661f35f68eb94d39ba6adc4efa4b630a62af87529e5450534` |
| D12 | align | [paper/sections/2_frozen_setup.tex:L49](paper/sections/2_frozen_setup.tex#L49) – [paper/sections/2_frozen_setup.tex:L55](paper/sections/2_frozen_setup.tex#L55) | `5f37858a4f5a47f14c3ab0186e5e471c74ebcfe6ab2ccb96388f4f6db37f5b6c` |
| D13 | equation | [paper/sections/2_frozen_setup.tex:L58](paper/sections/2_frozen_setup.tex#L58) – [paper/sections/2_frozen_setup.tex:L62](paper/sections/2_frozen_setup.tex#L62) | `ee348553d0ae4eb8ce7e803d27a7ac4edbd556660319dfa1100954ff0a883ee3` |
| D14 | \[...\] | [paper/sections/3_row_mass_and_cauchy.tex:L7](paper/sections/3_row_mass_and_cauchy.tex#L7) – [paper/sections/3_row_mass_and_cauchy.tex:L9](paper/sections/3_row_mass_and_cauchy.tex#L9) | `2d3d1801dd49fcbbe2149b93e61e812f180a6c0b934fb55146e06783eae89a93` |
| D15 | \[...\] | [paper/sections/3_row_mass_and_cauchy.tex:L15](paper/sections/3_row_mass_and_cauchy.tex#L15) – [paper/sections/3_row_mass_and_cauchy.tex:L18](paper/sections/3_row_mass_and_cauchy.tex#L18) | `125621e98132b0e36c64b8a01e9e38ab4516a3be22f8adb9e6eec15f1d7fafc5` |
| D16 | equation | [paper/sections/3_row_mass_and_cauchy.tex:L26](paper/sections/3_row_mass_and_cauchy.tex#L26) – [paper/sections/3_row_mass_and_cauchy.tex:L29](paper/sections/3_row_mass_and_cauchy.tex#L29) | `4b73222222a356c9ca0cd5ea040c1d4bca0138a24c1ae19a2840b7729fadc7df` |
| D17 | \[...\] | [paper/sections/3_row_mass_and_cauchy.tex:L37](paper/sections/3_row_mass_and_cauchy.tex#L37) – [paper/sections/3_row_mass_and_cauchy.tex:L41](paper/sections/3_row_mass_and_cauchy.tex#L41) | `04ea115a18f1f17710918486fd4d151e45ce72cb64c40308abc78abd46aba00b` |
| D18 | \[...\] | [paper/sections/3_row_mass_and_cauchy.tex:L44](paper/sections/3_row_mass_and_cauchy.tex#L44) – [paper/sections/3_row_mass_and_cauchy.tex:L46](paper/sections/3_row_mass_and_cauchy.tex#L46) | `7372039b3db83ccf29c472f80a38f12ba5e260259a690f197544e435d38f2f78` |
| D19 | equation | [paper/sections/3_row_mass_and_cauchy.tex:L48](paper/sections/3_row_mass_and_cauchy.tex#L48) – [paper/sections/3_row_mass_and_cauchy.tex:L51](paper/sections/3_row_mass_and_cauchy.tex#L51) | `fbc852849bf276e0060ae4d8c2045b44d72a43ace9bf753d69995f39a8ac4d0f` |
| D20 | \[...\] | [paper/sections/3_row_mass_and_cauchy.tex:L54](paper/sections/3_row_mass_and_cauchy.tex#L54) – [paper/sections/3_row_mass_and_cauchy.tex:L57](paper/sections/3_row_mass_and_cauchy.tex#L57) | `b2307d52fe4253c62071155ccb58fa857c2759aa368d672ac24f5f24cc8098fb` |
| D21 | equation | [paper/sections/3_row_mass_and_cauchy.tex:L63](paper/sections/3_row_mass_and_cauchy.tex#L63) – [paper/sections/3_row_mass_and_cauchy.tex:L66](paper/sections/3_row_mass_and_cauchy.tex#L66) | `f02bab8c197b7d1a7bfd5eb61aa6512cb102706aa6912d684a593e22b863f920` |
| D22 | equation | [paper/sections/4_coefficient_liminf.tex:L5](paper/sections/4_coefficient_liminf.tex#L5) – [paper/sections/4_coefficient_liminf.tex:L8](paper/sections/4_coefficient_liminf.tex#L8) | `924b8d88461e7520cf24d648375dcde9a8d226dc17ccf855b85fcdfdf141460c` |
| D23 | align | [paper/sections/4_coefficient_liminf.tex:L15](paper/sections/4_coefficient_liminf.tex#L15) – [paper/sections/4_coefficient_liminf.tex:L20](paper/sections/4_coefficient_liminf.tex#L20) | `5378d974f62fa4055f79df14ba3293590b645b80a7acdbc582d342896ceddb71` |
| D24 | equation | [paper/sections/4_coefficient_liminf.tex:L22](paper/sections/4_coefficient_liminf.tex#L22) – [paper/sections/4_coefficient_liminf.tex:L25](paper/sections/4_coefficient_liminf.tex#L25) | `c1a6bef01443c4bedca91ee6640b5bc74389463c0be690cda8250218f901d453` |
| D25 | equation | [paper/sections/4_coefficient_liminf.tex:L27](paper/sections/4_coefficient_liminf.tex#L27) – [paper/sections/4_coefficient_liminf.tex:L31](paper/sections/4_coefficient_liminf.tex#L31) | `7f6d56b082eb67d7078197b98586ede89196fdf6c1b5fb4a395872bc5f99d54d` |
| D26 | \[...\] | [paper/sections/4_coefficient_liminf.tex:L35](paper/sections/4_coefficient_liminf.tex#L35) – [paper/sections/4_coefficient_liminf.tex:L39](paper/sections/4_coefficient_liminf.tex#L39) | `59070b80a4ddad317c5e0db2eb3d0104b329c4cf8149cedb70389525f4615333` |
| D27 | \[...\] | [paper/sections/4_coefficient_liminf.tex:L41](paper/sections/4_coefficient_liminf.tex#L41) – [paper/sections/4_coefficient_liminf.tex:L44](paper/sections/4_coefficient_liminf.tex#L44) | `ed06520088a4b28059b290b7adce49325a17369e4dcb0fbb055870a8d63f6f86` |
| D28 | equation | [paper/sections/5_finite_window_transfer.tex:L9](paper/sections/5_finite_window_transfer.tex#L9) – [paper/sections/5_finite_window_transfer.tex:L13](paper/sections/5_finite_window_transfer.tex#L13) | `2bf23292b0604719ab27df679b33696fa9685bdf00b889412d59f1ca81e829a4` |
| D29 | align | [paper/sections/5_finite_window_transfer.tex:L19](paper/sections/5_finite_window_transfer.tex#L19) – [paper/sections/5_finite_window_transfer.tex:L26](paper/sections/5_finite_window_transfer.tex#L26) | `cbd9f02d7276c3d82780ee789dbda31d373a05997fc5713cb6754d9f98268296` |
| D30 | equation | [paper/sections/5_finite_window_transfer.tex:L30](paper/sections/5_finite_window_transfer.tex#L30) – [paper/sections/5_finite_window_transfer.tex:L34](paper/sections/5_finite_window_transfer.tex#L34) | `d0fe795ff5394df6eecdeb73b1d57a4d2d57bdb46c0b4467cd7ec7fe15d9a2e4` |
| D31 | equation | [paper/sections/6_sharpness_and_route.tex:L6](paper/sections/6_sharpness_and_route.tex#L6) – [paper/sections/6_sharpness_and_route.tex:L10](paper/sections/6_sharpness_and_route.tex#L10) | `3e368c2152f649028c22c9663ff592990e02e7b857b6d9accce23fff4145f4f2` |
| D32 | \[...\] | [paper/sections/6_sharpness_and_route.tex:L18](paper/sections/6_sharpness_and_route.tex#L18) – [paper/sections/6_sharpness_and_route.tex:L20](paper/sections/6_sharpness_and_route.tex#L20) | `2ce14e93cb5c7752cb80a84b9bc00d496ffb4d4edfcccc58050c7a62b02077d5` |
| D33 | \[...\] | [paper/sections/7_certificate.tex:L9](paper/sections/7_certificate.tex#L9) – [paper/sections/7_certificate.tex:L13](paper/sections/7_certificate.tex#L13) | `fe2269654bc7e9dbf8962bd4a0f6fc40be240b564724dd66694238070f826d56` |
| D34 | \[...\] | [paper/sections/7_certificate.tex:L22](paper/sections/7_certificate.tex#L22) – [paper/sections/7_certificate.tex:L25](paper/sections/7_certificate.tex#L25) | `6948a826bd5b14a5231b9f847dd797456ba5cf457d78fc84622072d116ebd59a` |
| D35 | align* | [paper/sections/A_status_ledger.tex:L31](paper/sections/A_status_ledger.tex#L31) – [paper/sections/A_status_ledger.tex:L36](paper/sections/A_status_ledger.tex#L36) | `80e12903c6a60b82e8797af34d4a70ef2f8c701f4619d23994b1b5d3a9a9ab35` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/0_abstract.tex:L2](paper/sections/0_abstract.tex#L2): `We study the unsigned common-profile kernel at the finite-window interface of a`
- [paper/sections/0_abstract.tex:L8](paper/sections/0_abstract.tex#L8): `nonnegative normalized smooth profile, a uniform first-moment lattice estimate,`
- [paper/sections/0_abstract.tex:L15](paper/sections/0_abstract.tex#L15): `Applying the finite-window lower frame to the complete coefficient vector`
- [paper/sections/0_abstract.tex:L25](paper/sections/0_abstract.tex#L25): `does not control the signed four-packet projection, prove arithmetic`
- [paper/sections/1_introduction.tex:L9](paper/sections/1_introduction.tex#L9): `collapsed inside each primitive frequency bucket before a finite-window large`
- [paper/sections/1_introduction.tex:L32](paper/sections/1_introduction.tex#L32): `The order of operations in the finite-window step matters.  It is not legal to`
- [paper/sections/1_introduction.tex:L53](paper/sections/1_introduction.tex#L53): `object.  Section~\ref{sec:row} proves the uniform row mass and the collision`
- [paper/sections/1_introduction.tex:L57](paper/sections/1_introduction.tex#L57): `boundary.  Section~\ref{sec:certificate} describes reproducible finite checks,`
- [paper/sections/2_frozen_setup.tex:L19](paper/sections/2_frozen_setup.tex#L19): `threshold uniform over the whole profile class.`
- [paper/sections/3_row_mass_and_cauchy.tex:L1](paper/sections/3_row_mass_and_cauchy.tex#L1): `\section{Uniform row mass and residue collision}\label{sec:row}`
- [paper/sections/3_row_mass_and_cauchy.tex:L24](paper/sections/3_row_mass_and_cauchy.tex#L24): `\begin{lemma}[Uniform top-prime row mass]\label{lem:rowmass}`
- [paper/sections/3_row_mass_and_cauchy.tex:L25](paper/sections/3_row_mass_and_cauchy.tex#L25): `Uniformly for primes $U/2<p\leq U$,`
- [paper/sections/3_row_mass_and_cauchy.tex:L43](paper/sections/3_row_mass_and_cauchy.tex#L43): `is consequently uniform and yields`
- [paper/sections/3_row_mass_and_cauchy.tex:L58](paper/sections/3_row_mass_and_cauchy.tex#L58): `uniformly for $p>U/2$.  This proves \eqref{eq:rowmass}.`
- [paper/sections/4_coefficient_liminf.tex:L14](paper/sections/4_coefficient_liminf.tex#L14): `$p/(p-1)=1+o(1)$ uniformly on the top shell, we obtain`
- [paper/sections/5_finite_window_transfer.tex:L1](paper/sections/5_finite_window_transfer.tex#L1): `\section{Finite-window transfer without deleting cross terms}\label{sec:window}`
- [paper/sections/5_finite_window_transfer.tex:L7](paper/sections/5_finite_window_transfer.tex#L7): `\begin{theorem}[Finite-window liminf]\label{thm:window}`
- [paper/sections/5_finite_window_transfer.tex:L17](paper/sections/5_finite_window_transfer.tex#L17): `The finite-window lower frame of \cite{WangTPC238}, applied to the complete`
- [paper/sections/6_sharpness_and_route.tex:L36](paper/sections/6_sharpness_and_route.tex#L36): `\item The theorem supplies no arithmetic $L^2$ saving, no strict $1/400$`
- [paper/sections/6_sharpness_and_route.tex:L49](paper/sections/6_sharpness_and_route.tex#L49): `an open refinement and is not needed for Corollary~\ref{cor:no_power}.`
- [paper/sections/7_certificate.tex:L1](paper/sections/7_certificate.tex#L1): `\section{Exact finite certificate and adversarial controls}\label{sec:certificate}`
- [paper/sections/7_certificate.tex:L19](paper/sections/7_certificate.tex#L19): `The finite fixture uses $Q=101$, $H=509$, $U=97$, three top primes, and all`
- [paper/sections/7_certificate.tex:L27](paper/sections/7_certificate.tex#L27): `These weights are finite algebraic illustrations, not substitutions for the`
- [paper/sections/7_certificate.tex:L30](paper/sections/7_certificate.tex#L30): `An independent checker does not import the producer.  It rejects duplicate JSON`
- [paper/sections/7_certificate.tex:L31](paper/sections/7_certificate.tex#L31): `keys and nonfinite constants, recomputes every rational row, and verifies strict`
- [paper/sections/8_conclusion.tex:L5](paper/sections/8_conclusion.tex#L5): `half of its explicit liminf constant to the literal finite window.  Hence the`
- [paper/sections/8_conclusion.tex:L11](paper/sections/8_conclusion.tex#L11): `that signed projection cancels the sharp positive mode is the principal open`
- [paper/sections/A_status_ledger.tex:L12](paper/sections/A_status_ledger.tex#L12): `Fixed-profile top-prime row mass & proved, uniform $3/2$ constant \\`
- [paper/sections/A_status_ledger.tex:L15](paper/sections/A_status_ledger.tex#L15): `Finite-window liminf & $10773\log2/3200$ \\`
- [paper/sections/A_status_ledger.tex:L17](paper/sections/A_status_ledger.tex#L17): `Class-uniform profile threshold & not claimed \\`
- [paper/sections/A_status_ledger.tex:L20](paper/sections/A_status_ledger.tex#L20): `Signed four-packet Gate-B scalar & open \\`
- [paper/sections/A_status_ledger.tex:L35](paper/sections/A_status_ledger.tex#L35): `\longrightarrow \text{full-vector finite-window lower frame}.`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#sec:setup` → `sections/2_frozen_setup.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:row` → `sections/3_row_mass_and_cauchy.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:coefficient` → `sections/4_coefficient_liminf.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:window` → `sections/5_finite_window_transfer.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:sharpness` → `sections/6_sharpness_and_route.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:certificate` → `sections/7_certificate.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#eq:B_hq` → `sections/2_frozen_setup.tex#L23` (existing project target or original TeX label line).
- Link relocation: `#lem:lattice` → `sections/3_row_mass_and_cauchy.tex#L5` (existing project target or original TeX label line).
- Link relocation: `#eq:rowmass` → `sections/3_row_mass_and_cauchy.tex#L26` (existing project target or original TeX label line).
- Link relocation: `#eq:Sp` → `sections/2_frozen_setup.tex#L51` (existing project target or original TeX label line).
- Link relocation: `#lem:cauchy` → `sections/3_row_mass_and_cauchy.tex#L61` (existing project target or original TeX label line).
- Link relocation: `#eq:profile` → `sections/2_frozen_setup.tex#L14` (existing project target or original TeX label line).
- Link relocation: `#lem:rowmass` → `sections/3_row_mass_and_cauchy.tex#L24` (existing project target or original TeX label line).
- Link relocation: `#lem:cauchy` → `sections/3_row_mass_and_cauchy.tex#L61` (existing project target or original TeX label line).
- Link relocation: `#eq:scales` → `sections/2_frozen_setup.tex#L4` (existing project target or original TeX label line).
- Link relocation: `#eq:coefficient_liminf` → `sections/4_coefficient_liminf.tex#L5` (existing project target or original TeX label line).
- Link relocation: `#eq:full_kernel` → `sections/2_frozen_setup.tex#L36` (existing project target or original TeX label line).
- Link relocation: `#eq:profile` → `sections/2_frozen_setup.tex#L14` (existing project target or original TeX label line).
- Link relocation: `#eq:scale_arithmetic` → `sections/2_frozen_setup.tex#L58` (existing project target or original TeX label line).
- Link relocation: `#eq:window_top_restriction` → `sections/5_finite_window_transfer.tex#L30` (existing project target or original TeX label line).
- Link relocation: `#thm:coefficient` → `sections/4_coefficient_liminf.tex#L3` (existing project target or original TeX label line).
- Link relocation: `#eq:window_liminf` → `sections/5_finite_window_transfer.tex#L9` (existing project target or original TeX label line).
- Link relocation: `#eq:full_lower_frame` → `sections/5_finite_window_transfer.tex#L25` (existing project target or original TeX label line).
- Link relocation: `#thm:window` → `sections/5_finite_window_transfer.tex#L7` (existing project target or original TeX label line).
- Link relocation: `#eq:false_upper` → `sections/6_sharpness_and_route.tex#L6` (existing project target or original TeX label line).
- Link relocation: `#eq:false_upper` → `sections/6_sharpness_and_route.tex#L6` (existing project target or original TeX label line).
- Link relocation: `#cor:no_power` → `sections/6_sharpness_and_route.tex#L3` (existing project target or original TeX label line).
- Link relocation: `#cor:no_power` → `sections/6_sharpness_and_route.tex#L3` (existing project target or original TeX label line).
- Link relocation: `#tab:ledger` → `sections/A_status_ledger.tex#L27` (existing project target or original TeX label line).
