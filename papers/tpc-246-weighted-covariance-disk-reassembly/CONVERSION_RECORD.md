# TPC-246 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `10d0c7a5483e18e2246f1ad4388f2ce3884a13b01081bc247be5e545a3e93165`.

- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `18e9f2c50dfaff35953be9d8f439a5d32ae0ce6bdfedb27d2c498dbd1ad49c54`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `eb540b5c7257ed7d57a2bb4f68b6a8fa8451a8ef46f7302fc04240ffa494d669`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC245_249.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 12 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `10d0c7a5483e18e2246f1ad4388f2ce3884a13b01081bc247be5e545a3e93165` |
| [paper/math_commands.tex](paper/math_commands.tex) | `f8fadd6e26339a3da5521a57c7cfb1ba72f47d6a35deb4a7bde940354e277f98` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `af3685ab92908adfae515990bbba6d6da596b497b514875a050ddda6d85d785a` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `6b6a7abaddeaa56389fb43d0dd349fdf0aa0908e78869913e74b40136f72cc91` |
| [paper/sections/2_joint_geometry.tex](paper/sections/2_joint_geometry.tex) | `f588f4f48b1face54973cec11f19e5b263cc73f2d20b75211cb0ca926b1e0488` |
| [paper/sections/3_exact_reassembly.tex](paper/sections/3_exact_reassembly.tex) | `612ce2f939f43543d71df00707b1ceaaeb0f53b7b949f700465417f38fbc0781` |
| [paper/sections/4_sharp_corollaries.tex](paper/sections/4_sharp_corollaries.tex) | `14b657030b1e9e4ce6a207d4c54c9b7ee52b74724679b4ae4a9fa43afc0e9e09` |
| [paper/sections/5_source_transfer.tex](paper/sections/5_source_transfer.tex) | `d3f3a48213d80912e8101fddf8618e475958b086d3de7d74856971153d584172` |
| [paper/sections/6_certificate.tex](paper/sections/6_certificate.tex) | `8cfc28cf0fb0162aa68924f00623dc144a8fda94365899e3e8f07fda8e21dbfb` |
| [paper/sections/7_route_boundary.tex](paper/sections/7_route_boundary.tex) | `2cb8aef2dfa42f9d58518568cc909b7cc5e81c6fa2cc670d2e0dbad7973ef2a1` |
| [paper/sections/8_conclusion.tex](paper/sections/8_conclusion.tex) | `40218f089a3961d5cd9d7ba76d556f3b48ba764506e0c392562481b63096d953` |
| [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) | `286762e0b77b5ed1c49f74d3985b38a6eb3e9e9b28d005c560fa03607686c62f` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L16](paper/main.tex#L16) | `\input{math_commands}` | [paper/math_commands.tex](paper/math_commands.tex) |
| [paper/main.tex:L44](paper/main.tex#L44) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L47](paper/main.tex#L47) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L48](paper/main.tex#L48) | `\input{sections/2_joint_geometry}` | [paper/sections/2_joint_geometry.tex](paper/sections/2_joint_geometry.tex) |
| [paper/main.tex:L49](paper/main.tex#L49) | `\input{sections/3_exact_reassembly}` | [paper/sections/3_exact_reassembly.tex](paper/sections/3_exact_reassembly.tex) |
| [paper/main.tex:L50](paper/main.tex#L50) | `\input{sections/4_sharp_corollaries}` | [paper/sections/4_sharp_corollaries.tex](paper/sections/4_sharp_corollaries.tex) |
| [paper/main.tex:L51](paper/main.tex#L51) | `\input{sections/5_source_transfer}` | [paper/sections/5_source_transfer.tex](paper/sections/5_source_transfer.tex) |
| [paper/main.tex:L52](paper/main.tex#L52) | `\input{sections/6_certificate}` | [paper/sections/6_certificate.tex](paper/sections/6_certificate.tex) |
| [paper/main.tex:L53](paper/main.tex#L53) | `\input{sections/7_route_boundary}` | [paper/sections/7_route_boundary.tex](paper/sections/7_route_boundary.tex) |
| [paper/main.tex:L54](paper/main.tex#L54) | `\input{sections/8_conclusion}` | [paper/sections/8_conclusion.tex](paper/sections/8_conclusion.tex) |
| [paper/main.tex:L57](paper/main.tex#L57) | `\input{sections/A_status_ledger}` | [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Joint feasible sets and unconditional containment` | [paper/sections/2_joint_geometry.tex:L1](paper/sections/2_joint_geometry.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Exact weighted-disk reassembly` | [paper/sections/3_exact_reassembly.tex:L1](paper/sections/3_exact_reassembly.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Sharp cancellation and insufficiency` | [paper/sections/4_sharp_corollaries.tex:L1](paper/sections/4_sharp_corollaries.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Common multipliers and hard-window inflation` | [paper/sections/5_source_transfer.tex:L1](paper/sections/5_source_transfer.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Exact finite certificate` | [paper/sections/6_certificate.tex:L1](paper/sections/6_certificate.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Source lock and route boundary` | [paper/sections/7_route_boundary.tex:L1](paper/sections/7_route_boundary.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/8_conclusion.tex:L1](paper/sections/8_conclusion.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Status ledger` | [paper/sections/A_status_ledger.tex:L1](paper/sections/A_status_ledger.tex#L1) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `76` before writing and `76` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `21`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `fbbed7ebeda711e608b697c85c4c10bd3fca5231262e228b7fd665bc01ed2937`.
- Source theorem/proof environment starts: proposition at [paper/sections/2_joint_geometry.tex:L21](paper/sections/2_joint_geometry.tex#L21), proof at [paper/sections/2_joint_geometry.tex:L30](paper/sections/2_joint_geometry.tex#L30), theorem at [paper/sections/3_exact_reassembly.tex:L3](paper/sections/3_exact_reassembly.tex#L3), proof at [paper/sections/3_exact_reassembly.tex:L15](paper/sections/3_exact_reassembly.tex#L15), corollary at [paper/sections/4_sharp_corollaries.tex:L3](paper/sections/4_sharp_corollaries.tex#L3), proof at [paper/sections/4_sharp_corollaries.tex:L14](paper/sections/4_sharp_corollaries.tex#L14), theorem at [paper/sections/5_source_transfer.tex:L36](paper/sections/5_source_transfer.tex#L36), proof at [paper/sections/5_source_transfer.tex:L48](paper/sections/5_source_transfer.tex#L48).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/2_joint_geometry.tex:L6](paper/sections/2_joint_geometry.tex#L6) – [paper/sections/2_joint_geometry.tex:L8](paper/sections/2_joint_geometry.tex#L8) | `1cbb5f0ce49f1d758847fa8ca2c0d1559d57849b341694293c2f91a5dd24bd85` |
| D02 | \[...\] | [paper/sections/2_joint_geometry.tex:L10](paper/sections/2_joint_geometry.tex#L10) – [paper/sections/2_joint_geometry.tex:L14](paper/sections/2_joint_geometry.tex#L14) | `a3dc34aa318389442ad0fde0a79345f8ac9830f2c95cab932d1cd5bc48cd9d2d` |
| D03 | \[...\] | [paper/sections/2_joint_geometry.tex:L16](paper/sections/2_joint_geometry.tex#L16) – [paper/sections/2_joint_geometry.tex:L19](paper/sections/2_joint_geometry.tex#L19) | `eb4ecd746cd24989e4adba09598625cfa2e417e62a804a42a5a0187e4e0ef582` |
| D04 | \[...\] | [paper/sections/2_joint_geometry.tex:L23](paper/sections/2_joint_geometry.tex#L23) – [paper/sections/2_joint_geometry.tex:L26](paper/sections/2_joint_geometry.tex#L26) | `dfda9f23e7967ce681053d5ca303066064ac8485fb8bc3b2747a68a615bc9ae9` |
| D05 | \[...\] | [paper/sections/2_joint_geometry.tex:L33](paper/sections/2_joint_geometry.tex#L33) – [paper/sections/2_joint_geometry.tex:L37](paper/sections/2_joint_geometry.tex#L37) | `29c3f779c7b209b318be79c7f27f54e4b7526a764ace0fad5ecd388b52961c71` |
| D06 | \[...\] | [paper/sections/3_exact_reassembly.tex:L5](paper/sections/3_exact_reassembly.tex#L5) – [paper/sections/3_exact_reassembly.tex:L7](paper/sections/3_exact_reassembly.tex#L7) | `8eacb6547abba4816542a2c0c5ded5c94cff3999f42fbaa39348bad252506f8d` |
| D07 | \[...\] | [paper/sections/3_exact_reassembly.tex:L9](paper/sections/3_exact_reassembly.tex#L9) – [paper/sections/3_exact_reassembly.tex:L11](paper/sections/3_exact_reassembly.tex#L11) | `fa32ff346f03fba9495cc30612e0bbd6524ffba70851207bba1cf0e46d854b54` |
| D08 | \[...\] | [paper/sections/3_exact_reassembly.tex:L21](paper/sections/3_exact_reassembly.tex#L21) – [paper/sections/3_exact_reassembly.tex:L29](paper/sections/3_exact_reassembly.tex#L29) | `daa8b45ab1eb368d04cce9a9eb6d5b7fcfab67431a1e8473fd59b588d0df90a8` |
| D09 | \[...\] | [paper/sections/3_exact_reassembly.tex:L31](paper/sections/3_exact_reassembly.tex#L31) – [paper/sections/3_exact_reassembly.tex:L34](paper/sections/3_exact_reassembly.tex#L34) | `a3625f2029c46346bdb62bfaf873e33918c3acd60920bcaffee7f8f912b5b5ec` |
| D10 | \[...\] | [paper/sections/4_sharp_corollaries.tex:L5](paper/sections/4_sharp_corollaries.tex#L5) – [paper/sections/4_sharp_corollaries.tex:L9](paper/sections/4_sharp_corollaries.tex#L9) | `b6ac66744c4e6bc5d716509663c5be1bfca9a83956e6124ffc2abdc97d432efc` |
| D11 | \[...\] | [paper/sections/5_source_transfer.tex:L4](paper/sections/5_source_transfer.tex#L4) – [paper/sections/5_source_transfer.tex:L9](paper/sections/5_source_transfer.tex#L9) | `3dd2d1c8362d9734fee4587a6bfcdcb2cdb3a4559cd3b4f5088400392334609e` |
| D12 | \[...\] | [paper/sections/5_source_transfer.tex:L13](paper/sections/5_source_transfer.tex#L13) – [paper/sections/5_source_transfer.tex:L17](paper/sections/5_source_transfer.tex#L17) | `d18320125b4fe2198200865b1f9faec8abcebf9c6b20c25c2960dd5ece3d2e95` |
| D13 | \[...\] | [paper/sections/5_source_transfer.tex:L22](paper/sections/5_source_transfer.tex#L22) – [paper/sections/5_source_transfer.tex:L26](paper/sections/5_source_transfer.tex#L26) | `b1d0398bfbb1585834b6bb4662cc8053d0eb75beed08e87c7096992527d561c2` |
| D14 | \[...\] | [paper/sections/5_source_transfer.tex:L29](paper/sections/5_source_transfer.tex#L29) – [paper/sections/5_source_transfer.tex:L34](paper/sections/5_source_transfer.tex#L34) | `b986e83fe5851330c86f3ccdc0547a32293eada6ea4a5c66a5e5f3fac3357519` |
| D15 | \[...\] | [paper/sections/5_source_transfer.tex:L38](paper/sections/5_source_transfer.tex#L38) – [paper/sections/5_source_transfer.tex:L40](paper/sections/5_source_transfer.tex#L40) | `96546aedeb550828d5698b5f82141a5e211f769baa7e551508a5bc224cc16870` |
| D16 | \[...\] | [paper/sections/5_source_transfer.tex:L42](paper/sections/5_source_transfer.tex#L42) – [paper/sections/5_source_transfer.tex:L44](paper/sections/5_source_transfer.tex#L44) | `bd9815ff4fbd9a7845c3ead58546f1f0217707f81af96570c9c57cdf22d80744` |
| D17 | \[...\] | [paper/sections/5_source_transfer.tex:L50](paper/sections/5_source_transfer.tex#L50) – [paper/sections/5_source_transfer.tex:L52](paper/sections/5_source_transfer.tex#L52) | `c3fb55a17b12ce1df51a19d6bafac038f8115a38b6d9fb38add5f0cf9aa0d86e` |
| D18 | \[...\] | [paper/sections/6_certificate.tex:L5](paper/sections/6_certificate.tex#L5) – [paper/sections/6_certificate.tex:L7](paper/sections/6_certificate.tex#L7) | `22bf8cf97fbed90acf27a35b2e73f2aa5aa1b5de4fe11e75879ff6feeafaf547` |
| D19 | \[...\] | [paper/sections/7_route_boundary.tex:L4](paper/sections/7_route_boundary.tex#L4) – [paper/sections/7_route_boundary.tex:L11](paper/sections/7_route_boundary.tex#L11) | `e7fd433073e50ce56f01b80afa741e926731f01662d10248fda9b52fb002c9e0` |
| D20 | \[...\] | [paper/sections/7_route_boundary.tex:L19](paper/sections/7_route_boundary.tex#L19) – [paper/sections/7_route_boundary.tex:L21](paper/sections/7_route_boundary.tex#L21) | `98fd57abf3ea6360ee1bbe849e986588242fd3b922ef2951058702901231adb7` |
| D21 | \[...\] | [paper/sections/7_route_boundary.tex:L26](paper/sections/7_route_boundary.tex#L26) – [paper/sections/7_route_boundary.tex:L28](paper/sections/7_route_boundary.tex#L28) | `08fdf031e104688a93da573d819b0810f6e85b322488d6bfc8a30c9f3a50f3d1` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/0_abstract.tex:L1](paper/sections/0_abstract.tex#L1): `We determine the exact aggregate geometry of finitely many local complex`
- [paper/sections/0_abstract.tex:L13](paper/sections/0_abstract.tex#L13): `attachment, and every arithmetic estimate remain open; no twin-prime`
- [paper/sections/2_joint_geometry.tex:L3](paper/sections/2_joint_geometry.tex#L3): `Let $A$ be finite.  For $h\in A$, fix $c_h,\lambda_h\in\C$ and $r_h\ge0$.`
- [paper/sections/2_joint_geometry.tex:L27](paper/sections/2_joint_geometry.tex#L27): `No product-realizability assumption is needed.`
- [paper/sections/3_exact_reassembly.tex:L4](paper/sections/3_exact_reassembly.tex#L4): `Assume blockwise product realizability,`
- [paper/sections/5_source_transfer.tex:L19](paper/sections/5_source_transfer.tex#L19): `Assume additionally that both coefficient lanes lie in one finite`
- [paper/sections/5_source_transfer.tex:L45](paper/sections/5_source_transfer.tex#L45): `In particular, $|\Cagg|>\Ragg+\Ewin$ implies uniform nonvanishing.`
- [paper/sections/5_source_transfer.tex:L58](paper/sections/5_source_transfer.tex#L58): `uniform supremum.  The displayed physical set is only contained in the`
- [paper/sections/5_source_transfer.tex:L59](paper/sections/5_source_transfer.tex#L59): `inflated disk: the transfer theorem does not realize every error phase.  The`
- [paper/sections/6_certificate.tex:L1](paper/sections/6_certificate.tex#L1): `\section{Exact finite certificate}`
- [paper/sections/6_certificate.tex:L15](paper/sections/6_certificate.tex#L15): `zero-radius system), and a circle-annulus control.  These are finite`
- [paper/sections/7_route_boundary.tex:L15](paper/sections/7_route_boundary.tex#L15): `The committed source does not construct literal V59 coefficient lanes in one`
- [paper/sections/7_route_boundary.tex:L17](paper/sections/7_route_boundary.tex#L17): `each block, or blockwise product realizability.  It also does not pay the local`
- [paper/sections/7_route_boundary.tex:L29](paper/sections/7_route_boundary.tex#L29): `There is no arithmetic L2 estimate, fixed-atom credit, payment of strict`
- [paper/sections/A_status_ledger.tex:L16](paper/sections/A_status_ledger.tex#L16): `Blockwise product realizability & open for the arithmetic source \\`
- [paper/sections/A_status_ledger.tex:L17](paper/sections/A_status_ledger.tex#L17): `Literal V59 two-lane attachment & open \\`
- [paper/sections/A_status_ledger.tex:L18](paper/sections/A_status_ledger.tex#L18): `Canonical block directions / payable margin & open / open \\`
- [paper/sections/A_status_ledger.tex:L20](paper/sections/A_status_ledger.tex#L20): `Strict $1/400$ / full Gate B & unpaid / open \\`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- The preamble-only glyphtounicode input was resolved with kpsewhich and checked against the audited SHA-256; its non-content mapping table was not expanded. The original command, source line, and dependency hash are retained in the reading layer.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#prop:containment` → `sections/2_joint_geometry.tex#L21` (existing project target or original TeX label line).
- Link relocation: `#thm:disk` → `sections/3_exact_reassembly.tex#L3` (existing project target or original TeX label line).
- Link relocation: `#thm:disk` → `sections/3_exact_reassembly.tex#L3` (existing project target or original TeX label line).
