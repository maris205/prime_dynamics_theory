# TPC-240 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `60c2c19d8e343af0661fdd2cd73a5306437ebea13f9723159902805dad832b35`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `5ac7c035abf9b5c67a7af55e3cab0d4fe82fa27ea0147f163d28ba5ac2fb324e`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `52d28f6d4aee8844835c84adba0426df9a11cedb512cee10ec9c3771c51bee7d`; 7 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `63da97f5c9713ea4f76bbf82b888230f60f38f2a362d89cd57f5d30435605b77`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC240_244.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 11 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `60c2c19d8e343af0661fdd2cd73a5306437ebea13f9723159902805dad832b35` |
| [paper/math_commands.tex](paper/math_commands.tex) | `99e1b6f2a773846ec426fb5a615985d5e2b5c46dbbcb2d71f7fa7edd1df03a23` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `50bee35f0195e343eccf656b52c65efe67460d09b0237af8ae1803d9a09fa48c` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `572fc3ce1ef81f4f7f956ff6805b1f9ed9d85140ad9ddf5bf2d5fc1d02fc865e` |
| [paper/sections/2_frozen_setup.tex](paper/sections/2_frozen_setup.tex) | `1d2131a2ca82be9aa11f0f3e6df7022e50b291b275aae393e5fcd222f6c11798` |
| [paper/sections/3_exact_row_riemann.tex](paper/sections/3_exact_row_riemann.tex) | `b76149e31271711edcfe1b8ac0646d722f9a498964afe28ba3676cc07bb2b137` |
| [paper/sections/4_weighted_pnt_aggregation.tex](paper/sections/4_weighted_pnt_aggregation.tex) | `b50c91a4846941d1d3b703966324fecae90b330e9028bb430c069d49f976d61c` |
| [paper/sections/5_certificate.tex](paper/sections/5_certificate.tex) | `f9b66e4cdd5c2b046c424a3904d33006804783b3519810817f74efa26c98cc0c` |
| [paper/sections/6_route_boundary.tex](paper/sections/6_route_boundary.tex) | `d4efcb9641356ba32b6e5c011366d56fe4f08d94e8245846aef29fd2bc79e77e` |
| [paper/sections/7_conclusion.tex](paper/sections/7_conclusion.tex) | `2de7117d3bcaa65dce6a90f7c153205c03a55e3f1924df94ef88c6fce3e395e0` |
| [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) | `5bc7b75629b8a45584717e12856a14f6857cd98b109f876c4ca2d4e53333de28` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L19](paper/main.tex#L19) | `\input{math_commands}` | [paper/math_commands.tex](paper/math_commands.tex) |
| [paper/main.tex:L42](paper/main.tex#L42) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L45](paper/main.tex#L45) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L46](paper/main.tex#L46) | `\input{sections/2_frozen_setup}` | [paper/sections/2_frozen_setup.tex](paper/sections/2_frozen_setup.tex) |
| [paper/main.tex:L47](paper/main.tex#L47) | `\input{sections/3_exact_row_riemann}` | [paper/sections/3_exact_row_riemann.tex](paper/sections/3_exact_row_riemann.tex) |
| [paper/main.tex:L48](paper/main.tex#L48) | `\input{sections/4_weighted_pnt_aggregation}` | [paper/sections/4_weighted_pnt_aggregation.tex](paper/sections/4_weighted_pnt_aggregation.tex) |
| [paper/main.tex:L49](paper/main.tex#L49) | `\input{sections/5_certificate}` | [paper/sections/5_certificate.tex](paper/sections/5_certificate.tex) |
| [paper/main.tex:L50](paper/main.tex#L50) | `\input{sections/6_route_boundary}` | [paper/sections/6_route_boundary.tex](paper/sections/6_route_boundary.tex) |
| [paper/main.tex:L51](paper/main.tex#L51) | `\input{sections/7_conclusion}` | [paper/sections/7_conclusion.tex](paper/sections/7_conclusion.tex) |
| [paper/main.tex:L57](paper/main.tex#L57) | `\input{sections/A_status_ledger}` | [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Frozen source and exact object` | [paper/sections/2_frozen_setup.tex:L1](paper/sections/2_frozen_setup.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Primitive row identity and lattice asymptotic` | [paper/sections/3_exact_row_riemann.tex:L1](paper/sections/3_exact_row_riemann.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Weighted-prime aggregation` | [paper/sections/4_weighted_pnt_aggregation.tex:L1](paper/sections/4_weighted_pnt_aggregation.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Deterministic certificate and finite stress tests` | [paper/sections/5_certificate.tex:L1](paper/sections/5_certificate.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Finite-window consequence and route boundary` | [paper/sections/6_route_boundary.tex:L1](paper/sections/6_route_boundary.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/7_conclusion.tex:L1](paper/sections/7_conclusion.tex#L1) | 6 | `HEADING_TEXT_MATCH` |
| `Status ledger and declarations` | [paper/sections/A_status_ledger.tex:L1](paper/sections/A_status_ledger.tex#L1) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `References (external bibliography)` | [paper/main.tex:L54](paper/main.tex#L54) | 6 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `148` before writing and `148` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `31`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `0049d408d2049ef3ce29b34831dd2cfdacee1b67aeba1a6a33c3f9dcdf3e28a8`.
- Source theorem/proof environment starts: theorem at [paper/sections/2_frozen_setup.tex:L56](paper/sections/2_frozen_setup.tex#L56), lemma at [paper/sections/3_exact_row_riemann.tex:L7](paper/sections/3_exact_row_riemann.tex#L7), proof at [paper/sections/3_exact_row_riemann.tex:L12](paper/sections/3_exact_row_riemann.tex#L12), lemma at [paper/sections/3_exact_row_riemann.tex:L22](paper/sections/3_exact_row_riemann.tex#L22), proof at [paper/sections/3_exact_row_riemann.tex:L34](paper/sections/3_exact_row_riemann.tex#L34), lemma at [paper/sections/3_exact_row_riemann.tex:L52](paper/sections/3_exact_row_riemann.tex#L52), proof at [paper/sections/3_exact_row_riemann.tex:L63](paper/sections/3_exact_row_riemann.tex#L63), proof at [paper/sections/4_weighted_pnt_aggregation.tex:L49](paper/sections/4_weighted_pnt_aggregation.tex#L49), corollary at [paper/sections/6_route_boundary.tex:L28](paper/sections/6_route_boundary.tex#L28).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/0_abstract.tex:L8](paper/sections/0_abstract.tex#L8) – [paper/sections/0_abstract.tex:L13](paper/sections/0_abstract.tex#L13) | `a22bb3e5fb2e8a633536c4576c98a2889842c3de478d40d7f8f67f4e2241badd` |
| D02 | \[...\] | [paper/sections/1_introduction.tex:L22](paper/sections/1_introduction.tex#L22) – [paper/sections/1_introduction.tex:L25](paper/sections/1_introduction.tex#L25) | `7f0c8d28b03afcc71ffb21fa88827aa1edf9d8552acf2f5fdc089f5994d31de0` |
| D03 | equation | [paper/sections/2_frozen_setup.tex:L5](paper/sections/2_frozen_setup.tex#L5) – [paper/sections/2_frozen_setup.tex:L8](paper/sections/2_frozen_setup.tex#L8) | `75f8140c4bd65eb870b3af9fc7333316d1b49e281bf299cf506d3e7532b01890` |
| D04 | \[...\] | [paper/sections/2_frozen_setup.tex:L10](paper/sections/2_frozen_setup.tex#L10) – [paper/sections/2_frozen_setup.tex:L13](paper/sections/2_frozen_setup.tex#L13) | `4e3e8e4003e780ed42ebca674aff42a6aa9516fb5cc0cc872fd91c98b93329f4` |
| D05 | align | [paper/sections/2_frozen_setup.tex:L15](paper/sections/2_frozen_setup.tex#L15) – [paper/sections/2_frozen_setup.tex:L20](paper/sections/2_frozen_setup.tex#L20) | `7a7a3ed06f443ba32c44d02721726064f9a02268509972af507ffa6477a69242` |
| D06 | equation | [paper/sections/2_frozen_setup.tex:L24](paper/sections/2_frozen_setup.tex#L24) – [paper/sections/2_frozen_setup.tex:L29](paper/sections/2_frozen_setup.tex#L29) | `480c08b8290edbc3acaf8b161f75f660d89677182b31b7f2f93d12babf7583cd` |
| D07 | equation | [paper/sections/2_frozen_setup.tex:L31](paper/sections/2_frozen_setup.tex#L31) – [paper/sections/2_frozen_setup.tex:L34](paper/sections/2_frozen_setup.tex#L34) | `bc152dc1b1f7f7cc2726f6dcc2733c79be621a1c31223f9c18710ffa440b932f` |
| D08 | equation | [paper/sections/2_frozen_setup.tex:L36](paper/sections/2_frozen_setup.tex#L36) – [paper/sections/2_frozen_setup.tex:L43](paper/sections/2_frozen_setup.tex#L43) | `0a1419f191484287e8a2097814d4f89672e56f28a46a52e9fad3f7a53145a2f6` |
| D09 | equation | [paper/sections/2_frozen_setup.tex:L45](paper/sections/2_frozen_setup.tex#L45) – [paper/sections/2_frozen_setup.tex:L52](paper/sections/2_frozen_setup.tex#L52) | `b60b5e0829e7a0c5d06326d55154f055cc3e6b76d12aaa855a4e23c97e5b5b42` |
| D10 | equation | [paper/sections/2_frozen_setup.tex:L59](paper/sections/2_frozen_setup.tex#L59) – [paper/sections/2_frozen_setup.tex:L62](paper/sections/2_frozen_setup.tex#L62) | `c29ccb5c191d8b9141a91dd857695b549796fcef25cc641408566e1e371f8bad` |
| D11 | equation | [paper/sections/2_frozen_setup.tex:L64](paper/sections/2_frozen_setup.tex#L64) – [paper/sections/2_frozen_setup.tex:L70](paper/sections/2_frozen_setup.tex#L70) | `0fb0560e1c001f2bab3f3258f19a0aaf65c80b082293594e2172d63dee7451ee` |
| D12 | \[...\] | [paper/sections/3_exact_row_riemann.tex:L14](paper/sections/3_exact_row_riemann.tex#L14) – [paper/sections/3_exact_row_riemann.tex:L17](paper/sections/3_exact_row_riemann.tex#L17) | `f385f2f4265335d1408a1bb83d938d3e8423cfddddece123b09336d9b18d506d` |
| D13 | equation | [paper/sections/3_exact_row_riemann.tex:L26](paper/sections/3_exact_row_riemann.tex#L26) – [paper/sections/3_exact_row_riemann.tex:L31](paper/sections/3_exact_row_riemann.tex#L31) | `a896d74222b3c60915b366516990f4105bd9e46ede69f7355ac9dcd3c2dc4b2f` |
| D14 | \[...\] | [paper/sections/3_exact_row_riemann.tex:L37](paper/sections/3_exact_row_riemann.tex#L37) – [paper/sections/3_exact_row_riemann.tex:L39](paper/sections/3_exact_row_riemann.tex#L39) | `68b2776a514a809fca72056e114dfe300351d79a20c0aa724a037dcf85d80f21` |
| D15 | equation | [paper/sections/3_exact_row_riemann.tex:L56](paper/sections/3_exact_row_riemann.tex#L56) – [paper/sections/3_exact_row_riemann.tex:L60](paper/sections/3_exact_row_riemann.tex#L60) | `8134c80f7d552e9c2037053e63d6ed1046f8677a46ecb5fd614fb6441ba693ba` |
| D16 | align* | [paper/sections/3_exact_row_riemann.tex:L66](paper/sections/3_exact_row_riemann.tex#L66) – [paper/sections/3_exact_row_riemann.tex:L70](paper/sections/3_exact_row_riemann.tex#L70) | `1daa7f34cdc4ba866c289f75d838936435d84c5fcc10a965b9fb1273f271fb5f` |
| D17 | equation | [paper/sections/3_exact_row_riemann.tex:L72](paper/sections/3_exact_row_riemann.tex#L72) – [paper/sections/3_exact_row_riemann.tex:L75](paper/sections/3_exact_row_riemann.tex#L75) | `044e78c0b0f7d6798dc2307ab5037e8ed228547316bcf8cbec0d49723dda54f2` |
| D18 | \[...\] | [paper/sections/4_weighted_pnt_aggregation.tex:L6](paper/sections/4_weighted_pnt_aggregation.tex#L6) – [paper/sections/4_weighted_pnt_aggregation.tex:L10](paper/sections/4_weighted_pnt_aggregation.tex#L10) | `fa2716f48c2af187f40c57269a5cb315f2b2d40af8058322ab6955cae403af67` |
| D19 | equation | [paper/sections/4_weighted_pnt_aggregation.tex:L12](paper/sections/4_weighted_pnt_aggregation.tex#L12) – [paper/sections/4_weighted_pnt_aggregation.tex:L15](paper/sections/4_weighted_pnt_aggregation.tex#L15) | `fd95a340ad3e0e0704726ffe80d00199e24ffd76489aca1c40c9b46254295c2f` |
| D20 | equation | [paper/sections/4_weighted_pnt_aggregation.tex:L21](paper/sections/4_weighted_pnt_aggregation.tex#L21) – [paper/sections/4_weighted_pnt_aggregation.tex:L26](paper/sections/4_weighted_pnt_aggregation.tex#L26) | `90a5c6c53825fa0ceba8b8786196256e8a972cdc2a0b0e8f57422f7bbab1fc86` |
| D21 | align | [paper/sections/4_weighted_pnt_aggregation.tex:L32](paper/sections/4_weighted_pnt_aggregation.tex#L32) – [paper/sections/4_weighted_pnt_aggregation.tex:L37](paper/sections/4_weighted_pnt_aggregation.tex#L37) | `2c0b6c565272cad320c89ccacb4180f77b5dc24c6aff5cdd6c073655de02dead` |
| D22 | \[...\] | [paper/sections/4_weighted_pnt_aggregation.tex:L39](paper/sections/4_weighted_pnt_aggregation.tex#L39) – [paper/sections/4_weighted_pnt_aggregation.tex:L42](paper/sections/4_weighted_pnt_aggregation.tex#L42) | `72cb02885fcbcf0e07b9bf21860665da10b4db192fae9fc6d7fb547f3c252929` |
| D23 | \[...\] | [paper/sections/4_weighted_pnt_aggregation.tex:L44](paper/sections/4_weighted_pnt_aggregation.tex#L44) – [paper/sections/4_weighted_pnt_aggregation.tex:L47](paper/sections/4_weighted_pnt_aggregation.tex#L47) | `cbb18ae91b6ca32a84ea4bee1da50cd982a9586ef84d5a4002e8cba570a01af3` |
| D24 | \[...\] | [paper/sections/4_weighted_pnt_aggregation.tex:L53](paper/sections/4_weighted_pnt_aggregation.tex#L53) – [paper/sections/4_weighted_pnt_aggregation.tex:L57](paper/sections/4_weighted_pnt_aggregation.tex#L57) | `4371f79dbf15c069e7587fe84bf8e2d2d753d784dd3898c63508e0e35a352f76` |
| D25 | \[...\] | [paper/sections/4_weighted_pnt_aggregation.tex:L59](paper/sections/4_weighted_pnt_aggregation.tex#L59) – [paper/sections/4_weighted_pnt_aggregation.tex:L61](paper/sections/4_weighted_pnt_aggregation.tex#L61) | `3eab8954befbd6e8a9c27d62547107eb42899ab5129999afed263979249893f1` |
| D26 | \[...\] | [paper/sections/4_weighted_pnt_aggregation.tex:L64](paper/sections/4_weighted_pnt_aggregation.tex#L64) – [paper/sections/4_weighted_pnt_aggregation.tex:L66](paper/sections/4_weighted_pnt_aggregation.tex#L66) | `2c0eedf9002d0cbda9ba46c2f789a388eac20d5b5faf74cc34a1242e65a0913e` |
| D27 | \[...\] | [paper/sections/5_certificate.tex:L19](paper/sections/5_certificate.tex#L19) – [paper/sections/5_certificate.tex:L23](paper/sections/5_certificate.tex#L23) | `b47d22b2fa61436d105f64e996cc4690ccad9eb67d03558f3cf8263b724fb77c` |
| D28 | \[...\] | [paper/sections/6_route_boundary.tex:L5](paper/sections/6_route_boundary.tex#L5) – [paper/sections/6_route_boundary.tex:L7](paper/sections/6_route_boundary.tex#L7) | `6746b65002674be249423faaa69d37d41f00b13f508e8456fd93c309a7aeaac5` |
| D29 | equation | [paper/sections/6_route_boundary.tex:L9](paper/sections/6_route_boundary.tex#L9) – [paper/sections/6_route_boundary.tex:L15](paper/sections/6_route_boundary.tex#L15) | `d8c5ad0c13d0c99251aa69706360e42a5883c5c40d2b92f58bb6f5ec1f9df064` |
| D30 | \[...\] | [paper/sections/6_route_boundary.tex:L20](paper/sections/6_route_boundary.tex#L20) – [paper/sections/6_route_boundary.tex:L24](paper/sections/6_route_boundary.tex#L24) | `f097183a94f426f969bbc837adcaf59cb10fbf5b0ae1ae2c45b8b8cca4dca850` |
| D31 | equation | [paper/sections/6_route_boundary.tex:L31](paper/sections/6_route_boundary.tex#L31) – [paper/sections/6_route_boundary.tex:L36](paper/sections/6_route_boundary.tex#L36) | `2a938a9a4343f6c61322b9215ffb209360dd0ac6c190eb7a77416c905a8fd6a9` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/0_abstract.tex:L19](paper/sections/0_abstract.tex#L19): `not uniform over the full profile class.  It concerns neither the`
- [paper/sections/0_abstract.tex:L21](paper/sections/0_abstract.tex#L21): `particular, it does not establish the $x^{1/48}$ collision exponent or full`
- [paper/sections/1_introduction.tex:L4](paper/sections/1_introduction.tex#L4): `The collision-compressed finite-window route reduces a substantial part of the`
- [paper/sections/1_introduction.tex:L8](paper/sections/1_introduction.tex#L8): `upper bounds and does not prove that one physical object saturates all of them`
- [paper/sections/1_introduction.tex:L9](paper/sections/1_introduction.tex#L9): `\cite{WangTPC237}.  Before searching for another uniform saving, one must know`
- [paper/sections/1_introduction.tex:L40](paper/sections/1_introduction.tex#L40): `cancellation.  A finite-window consequence follows from nonnegativity and the`
- [paper/sections/1_introduction.tex:L43](paper/sections/1_introduction.tex#L43): `not an arithmetic Gate-B advance.`
- [paper/sections/2_frozen_setup.tex:L54](paper/sections/2_frozen_setup.tex#L54): `finite-window normalization in \eqref{eq:direct-energy}.`
- [paper/sections/2_frozen_setup.tex:L74](paper/sections/2_frozen_setup.tex#L74): `uniform over the whole profile class is asserted.`
- [paper/sections/3_exact_row_riemann.tex:L50](paper/sections/3_exact_row_riemann.tex#L50): `profile, uniformly across the two prime shells.`
- [paper/sections/3_exact_row_riemann.tex:L54](paper/sections/3_exact_row_riemann.tex#L54): `For every fixed admissible $\psi$, uniformly for`
- [paper/sections/3_exact_row_riemann.tex:L84](paper/sections/3_exact_row_riemann.tex#L84): `error therefore applies uniformly over both shells.  Its dependence on`
- [paper/sections/3_exact_row_riemann.tex:L85](paper/sections/3_exact_row_riemann.tex#L85): `$\|f'\|_1$ and $f(0)$ explains why the result is not uniform over all profiles.`
- [paper/sections/5_certificate.tex:L1](paper/sections/5_certificate.tex#L1): `\section{Deterministic certificate and finite stress tests}`
- [paper/sections/5_certificate.tex:L6](paper/sections/5_certificate.tex#L6): `theorem status, route firewall, and a finite algebraic row fixture in canonical`
- [paper/sections/5_certificate.tex:L11](paper/sections/5_certificate.tex#L11): `The independent checker does not import the producer.  It reconstructs the`
- [paper/sections/5_certificate.tex:L30](paper/sections/5_certificate.tex#L30): `All finite values in this section are classified`
- [paper/sections/5_certificate.tex:L31](paper/sections/5_certificate.tex#L31): `\texttt{NUMERICAL\_FINITE\_ILLUSTRATION\_ONLY}.  They test implementation`
- [paper/sections/6_route_boundary.tex:L1](paper/sections/6_route_boundary.tex#L1): `\section{Finite-window consequence and route boundary}`
- [paper/sections/6_route_boundary.tex:L16](paper/sections/6_route_boundary.tex#L16): `This inequality sees the direct floor but does not quantify the positive`
- [paper/sections/6_route_boundary.tex:L28](paper/sections/6_route_boundary.tex#L28): `\begin{corollary}[firewalled finite-window lower bound]`
- [paper/sections/6_route_boundary.tex:L48](paper/sections/6_route_boundary.tex#L48): `available.  The paper supplies no signed four-packet projection, no arithmetic`
- [paper/sections/6_route_boundary.tex:L50](paper/sections/6_route_boundary.tex#L50): `B and the twin-prime endpoint remain open.`
- [paper/sections/A_status_ledger.tex:L15](paper/sections/A_status_ledger.tex#L15): `Finite calculations & \texttt{NUMERICAL} & Finite illustration only; not theorem evidence \\`
- [paper/sections/A_status_ledger.tex:L16](paper/sections/A_status_ledger.tex#L16): `q-collision $x^{1/48}$ sharpness & \texttt{OPEN} & Not inferred from the floor \\`
- [paper/sections/A_status_ledger.tex:L18](paper/sections/A_status_ledger.tex#L18): `Signed four-packet scalar & \texttt{OPEN} & No projection in this paper \\`
- [paper/sections/A_status_ledger.tex:L19](paper/sections/A_status_ledger.tex#L19): `Arithmetic $L2$ & \texttt{NONE} & No arithmetic advance \\`
- [paper/sections/A_status_ledger.tex:L20](paper/sections/A_status_ledger.tex#L20): `Strict $1/400$ & \texttt{UNPAID\_GLOBAL} & Full gate remains open \\`
- [paper/sections/A_status_ledger.tex:L27](paper/sections/A_status_ledger.tex#L27): `The complete deterministic certificate, independent checker, finite stress`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 6 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#sec:setup` → `sections/2_frozen_setup.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#sec:rows` → `sections/3_exact_row_riemann.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#sec:aggregation` → `sections/4_weighted_pnt_aggregation.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#sec:certificate` → `sections/5_certificate.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#sec:boundary` → `sections/6_route_boundary.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#eq:direct-energy` → `sections/2_frozen_setup.tex#L51` (existing project target or original TeX label line).
- Link relocation: `#eq:profile` → `sections/2_frozen_setup.tex#L28` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `sections/2_frozen_setup.tex#L57` (existing project target or original TeX label line).
- Link relocation: `#sec:rows` → `sections/3_exact_row_riemann.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#sec:aggregation` → `sections/4_weighted_pnt_aggregation.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#eq:profile` → `sections/2_frozen_setup.tex#L28` (existing project target or original TeX label line).
- Link relocation: `#eq:separation` → `sections/2_frozen_setup.tex#L17` (existing project target or original TeX label line).
- Link relocation: `#eq:row` → `sections/2_frozen_setup.tex#L42` (existing project target or original TeX label line).
- Link relocation: `#eq:row-identity` → `sections/3_exact_row_riemann.tex#L30` (existing project target or original TeX label line).
- Link relocation: `#eq:riemann` → `sections/3_exact_row_riemann.tex#L74` (existing project target or original TeX label line).
- Link relocation: `#lem:row` → `sections/3_exact_row_riemann.tex#L23` (existing project target or original TeX label line).
- Link relocation: `#eq:row-asymptotic` → `sections/3_exact_row_riemann.tex#L59` (existing project target or original TeX label line).
- Link relocation: `#eq:depth` → `sections/2_frozen_setup.tex#L19` (existing project target or original TeX label line).
- Link relocation: `#lem:riemann` → `sections/3_exact_row_riemann.tex#L53` (existing project target or original TeX label line).
- Link relocation: `#eq:direct-energy` → `sections/2_frozen_setup.tex#L51` (existing project target or original TeX label line).
- Link relocation: `#eq:aggregate` → `sections/4_weighted_pnt_aggregation.tex#L14` (existing project target or original TeX label line).
- Link relocation: `#eq:q-pnt` → `sections/4_weighted_pnt_aggregation.tex#L34` (existing project target or original TeX label line).
- Link relocation: `#eq:p-pnt` → `sections/4_weighted_pnt_aggregation.tex#L36` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `sections/2_frozen_setup.tex#L57` (existing project target or original TeX label line).
- Link relocation: `#lem:kappa` → `sections/3_exact_row_riemann.tex#L8` (existing project target or original TeX label line).
- Link relocation: `#eq:kappa-range` → `sections/2_frozen_setup.tex#L61` (existing project target or original TeX label line).
- Link relocation: `#eq:aggregate` → `sections/4_weighted_pnt_aggregation.tex#L14` (existing project target or original TeX label line).
- Link relocation: `#eq:p-pnt` → `sections/4_weighted_pnt_aggregation.tex#L36` (existing project target or original TeX label line).
- Link relocation: `#eq:relative-error` → `sections/4_weighted_pnt_aggregation.tex#L25` (existing project target or original TeX label line).
- Link relocation: `#eq:main-asymptotic` → `sections/2_frozen_setup.tex#L69` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `sections/2_frozen_setup.tex#L57` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `sections/2_frozen_setup.tex#L57` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `sections/2_frozen_setup.tex#L57` (existing project target or original TeX label line).
- Link relocation: `#lem:row` → `sections/3_exact_row_riemann.tex#L23` (existing project target or original TeX label line).
- Link relocation: `#lem:riemann` → `sections/3_exact_row_riemann.tex#L53` (existing project target or original TeX label line).
- Link relocation: `#eq:nonnegative-collapse` → `sections/6_route_boundary.tex#L14` (existing project target or original TeX label line).
- Link relocation: `#cor:window` → `sections/6_route_boundary.tex#L29` (existing project target or original TeX label line).
