# TPC-239 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `1896315fa6b34f7950c9d197cf3ce9d4843619195237cf3919cdccd63deb986c`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `db337c3967acee95e738662e125a74269de3db1cd2276c12d7e8ffc33940a25a`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `fb66154b3253ad1ef53250ce823bd0d271607b55844a6aeee7b7da52a4b33a88`; 9 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `c278d3f6adf50b724dfd6e613ca46e66a175bc9b9c6a9ac27fdef7bd9da9b68c`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC235_239.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 11 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `1896315fa6b34f7950c9d197cf3ce9d4843619195237cf3919cdccd63deb986c` |
| [paper/math_commands.tex](paper/math_commands.tex) | `b0f2c47abbc983615fafc7f84272215e8f3d3c2ed60669a767a41da3614ced47` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `0e0a5c2f58b45ec69a6da9784846ba1cf27b3676709837e43340d2bfe5afcdf8` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `74d68401468601da9dd053f32880a80c3ee0b00c071bea504bf3a87f8952cd9c` |
| [paper/sections/2_source_setup.tex](paper/sections/2_source_setup.tex) | `7d44aa10904986520158079d6c9f2f650ecdf5b15d64c4d4e080e8203bd95a4b` |
| [paper/sections/3_primitive_ap_compiler.tex](paper/sections/3_primitive_ap_compiler.tex) | `354885fc0787509cc20eea4762439e044120ae17480470addc8a0856e80c473b` |
| [paper/sections/4_v59_composition.tex](paper/sections/4_v59_composition.tex) | `fb248630ae5c53bb5c9b2f2f35dce7a44886e9cec1d4416da8b286870d51082a` |
| [paper/sections/5_finite_certificate.tex](paper/sections/5_finite_certificate.tex) | `6aab8a5e985c3a05503fee6948a314956230023d10e8bf4282b289889ddec640` |
| [paper/sections/6_route_boundary.tex](paper/sections/6_route_boundary.tex) | `6b104458428d70f685b039bb784065fba608a158b71a2d6f0fc9bcbf4503cc98` |
| [paper/sections/7_conclusion.tex](paper/sections/7_conclusion.tex) | `f2ef4f3fcbcddabe5545d3bdfb1006d36ac930e3160292945a3a7b00f649f029` |
| [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) | `5206e3ab42d7bba7aff3d4a57de0e6a9804d2f5b4130d9581fdd2deef776c579` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L24](paper/main.tex#L24) | `\input{math_commands}` | [paper/math_commands.tex](paper/math_commands.tex) |
| [paper/main.tex:L45](paper/main.tex#L45) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L48](paper/main.tex#L48) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L49](paper/main.tex#L49) | `\input{sections/2_source_setup}` | [paper/sections/2_source_setup.tex](paper/sections/2_source_setup.tex) |
| [paper/main.tex:L50](paper/main.tex#L50) | `\input{sections/3_primitive_ap_compiler}` | [paper/sections/3_primitive_ap_compiler.tex](paper/sections/3_primitive_ap_compiler.tex) |
| [paper/main.tex:L51](paper/main.tex#L51) | `\input{sections/4_v59_composition}` | [paper/sections/4_v59_composition.tex](paper/sections/4_v59_composition.tex) |
| [paper/main.tex:L52](paper/main.tex#L52) | `\input{sections/5_finite_certificate}` | [paper/sections/5_finite_certificate.tex](paper/sections/5_finite_certificate.tex) |
| [paper/main.tex:L53](paper/main.tex#L53) | `\input{sections/6_route_boundary}` | [paper/sections/6_route_boundary.tex](paper/sections/6_route_boundary.tex) |
| [paper/main.tex:L54](paper/main.tex#L54) | `\input{sections/7_conclusion}` | [paper/sections/7_conclusion.tex](paper/sections/7_conclusion.tex) |
| [paper/main.tex:L55](paper/main.tex#L55) | `\input{sections/A_status_ledger}` | [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Frozen source and setup` | [paper/sections/2_source_setup.tex:L1](paper/sections/2_source_setup.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Scales and common-source kernel` | [paper/sections/2_source_setup.tex:L4](paper/sections/2_source_setup.tex#L4) | 2 | `HEADING_TEXT_MATCH` |
| `Inherited physical and analytic interfaces` | [paper/sections/2_source_setup.tex:L50](paper/sections/2_source_setup.tex#L50) | 3 | `HEADING_TEXT_MATCH` |
| `The primitive-residue to reduced-prime-AP compiler` | [paper/sections/3_primitive_ap_compiler.tex:L1](paper/sections/3_primitive_ap_compiler.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `V59 specialization and finite-window composition` | [paper/sections/4_v59_composition.tex:L1](paper/sections/4_v59_composition.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Uniform primitive-row density` | [paper/sections/4_v59_composition.tex:L4](paper/sections/4_v59_composition.tex#L4) | 5 | `HEADING_TEXT_MATCH` |
| `Substitution before the large sieve` | [paper/sections/4_v59_composition.tex:L48](paper/sections/4_v59_composition.tex#L48) | 5 | `HEADING_TEXT_MATCH` |
| `Loss ledger` | [paper/sections/4_v59_composition.tex:L104](paper/sections/4_v59_composition.tex#L104) | 6 | `HEADING_TEXT_MATCH` |
| `Deterministic finite certificate` | [paper/sections/5_finite_certificate.tex:L1](paper/sections/5_finite_certificate.tex#L1) | 6 | `HEADING_TEXT_MATCH` |
| `Route consequence and claim boundary` | [paper/sections/6_route_boundary.tex:L1](paper/sections/6_route_boundary.tex#L1) | 7 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/7_conclusion.tex:L1](paper/sections/7_conclusion.tex#L1) | 8 | `HEADING_TEXT_MATCH` |
| `Status ledger and declarations` | [paper/sections/A_status_ledger.tex:L2](paper/sections/A_status_ledger.tex#L2) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `Machine-readable status vocabulary` | [paper/sections/A_status_ledger.tex:L5](paper/sections/A_status_ledger.tex#L5) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `Research extraction` | [paper/sections/A_status_ledger.tex:L34](paper/sections/A_status_ledger.tex#L34) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `Reproducibility and competing interests` | [paper/sections/A_status_ledger.tex:L51](paper/sections/A_status_ledger.tex#L51) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `References (external bibliography)` | [paper/main.tex:L58](paper/main.tex#L58) | 9 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `180` before writing and `180` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `38`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `900fff718ee11dff41dc7b6994c1acb6eefeb53182da301d2669b2f8a9759007`.
- Source theorem/proof environment starts: lemma at [paper/sections/3_primitive_ap_compiler.tex:L16](paper/sections/3_primitive_ap_compiler.tex#L16), proof at [paper/sections/3_primitive_ap_compiler.tex:L21](paper/sections/3_primitive_ap_compiler.tex#L21), theorem at [paper/sections/3_primitive_ap_compiler.tex:L26](paper/sections/3_primitive_ap_compiler.tex#L26), proof at [paper/sections/3_primitive_ap_compiler.tex:L42](paper/sections/3_primitive_ap_compiler.tex#L42), remark at [paper/sections/3_primitive_ap_compiler.tex:L95](paper/sections/3_primitive_ap_compiler.tex#L95), corollary at [paper/sections/4_v59_composition.tex:L6](paper/sections/4_v59_composition.tex#L6), proof at [paper/sections/4_v59_composition.tex:L20](paper/sections/4_v59_composition.tex#L20), theorem at [paper/sections/4_v59_composition.tex:L66](paper/sections/4_v59_composition.tex#L66), proof at [paper/sections/4_v59_composition.tex:L79](paper/sections/4_v59_composition.tex#L79).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/0_abstract.tex:L8](paper/sections/0_abstract.tex#L8) – [paper/sections/0_abstract.tex:L12](paper/sections/0_abstract.tex#L12) | `c1b820d59c67b319daef6434c5f1f1b63219feb3230a0e1e95a1ab06dbc6aeda` |
| D02 | \[...\] | [paper/sections/0_abstract.tex:L18](paper/sections/0_abstract.tex#L18) – [paper/sections/0_abstract.tex:L21](paper/sections/0_abstract.tex#L21) | `b2d754806e3a61f4d9c27a72b0e8fd7e98e3276c8396e9f0c1c6dadb07f01636` |
| D03 | \[...\] | [paper/sections/0_abstract.tex:L26](paper/sections/0_abstract.tex#L26) – [paper/sections/0_abstract.tex:L29](paper/sections/0_abstract.tex#L29) | `5d1052ac7401f5c5ece046450a5d65429cfd285efa2eb32669b79e8d1ef56fdf` |
| D04 | \[...\] | [paper/sections/1_introduction.tex:L22](paper/sections/1_introduction.tex#L22) – [paper/sections/1_introduction.tex:L25](paper/sections/1_introduction.tex#L25) | `83866d971dcd67e8aae00c975a3dd3b59d3bd5259cb7d26b8cd059ffd1fb8ada` |
| D05 | \[...\] | [paper/sections/1_introduction.tex:L34](paper/sections/1_introduction.tex#L34) – [paper/sections/1_introduction.tex:L37](paper/sections/1_introduction.tex#L37) | `31d502afa3d11f683781a70a29d7c48820ffdfbc4d0f78f0ebd91706db95334f` |
| D06 | equation | [paper/sections/2_source_setup.tex:L8](paper/sections/2_source_setup.tex#L8) – [paper/sections/2_source_setup.tex:L12](paper/sections/2_source_setup.tex#L12) | `a2aef2c6926ac07013a756fad7c2b522f507c35231eedaeb5d773755744f3bcf` |
| D07 | \[...\] | [paper/sections/2_source_setup.tex:L16](paper/sections/2_source_setup.tex#L16) – [paper/sections/2_source_setup.tex:L20](paper/sections/2_source_setup.tex#L20) | `1bada2894c95276a465eaa9a9a3fb3ba9a36f3211772ba9015ee1ad206950b1d` |
| D08 | equation | [paper/sections/2_source_setup.tex:L24](paper/sections/2_source_setup.tex#L24) – [paper/sections/2_source_setup.tex:L27](paper/sections/2_source_setup.tex#L27) | `b1e3a66500af4f03307fb6b60cb5be7ba024d73cef922bc5386c1eb9cdfdf632` |
| D09 | align | [paper/sections/2_source_setup.tex:L32](paper/sections/2_source_setup.tex#L32) – [paper/sections/2_source_setup.tex:L43](paper/sections/2_source_setup.tex#L43) | `3f5e7db60e08b5aba8e159180b3a28051c5da7bb9032ba7a00b1d60dec14dc04` |
| D10 | equation | [paper/sections/2_source_setup.tex:L54](paper/sections/2_source_setup.tex#L54) – [paper/sections/2_source_setup.tex:L57](paper/sections/2_source_setup.tex#L57) | `f6e8187b2aeb50e86c632c05031145ce1ec509bf4b1b2e07da1a0b8a64459c69` |
| D11 | equation | [paper/sections/2_source_setup.tex:L61](paper/sections/2_source_setup.tex#L61) – [paper/sections/2_source_setup.tex:L64](paper/sections/2_source_setup.tex#L64) | `4426414938e921081a66f90adfcdae6bff24f4addd2f97e1bcdca2127c8c546a` |
| D12 | \[...\] | [paper/sections/2_source_setup.tex:L70](paper/sections/2_source_setup.tex#L70) – [paper/sections/2_source_setup.tex:L72](paper/sections/2_source_setup.tex#L72) | `b608fc717e1af5d2b982799509c9b7b6274c2fbeb14140b0fd6befab8e1cfce8` |
| D13 | equation | [paper/sections/2_source_setup.tex:L80](paper/sections/2_source_setup.tex#L80) – [paper/sections/2_source_setup.tex:L85](paper/sections/2_source_setup.tex#L85) | `c7569b9c16f0b191ef19e451fbebf49241d154ca901a49932caee36f0a883054` |
| D14 | equation | [paper/sections/2_source_setup.tex:L97](paper/sections/2_source_setup.tex#L97) – [paper/sections/2_source_setup.tex:L101](paper/sections/2_source_setup.tex#L101) | `98de504e7a4d6df3ba86b2e1fbaecfa1549a630971d0b1b13cbc273717daf70e` |
| D15 | equation | [paper/sections/3_primitive_ap_compiler.tex:L6](paper/sections/3_primitive_ap_compiler.tex#L6) – [paper/sections/3_primitive_ap_compiler.tex:L11](paper/sections/3_primitive_ap_compiler.tex#L11) | `e50ff5414421b5fb4f0c80a7f303cfc4b6a127c94ee33a50d27a25c7191e28b6` |
| D16 | align | [paper/sections/3_primitive_ap_compiler.tex:L31](paper/sections/3_primitive_ap_compiler.tex#L31) – [paper/sections/3_primitive_ap_compiler.tex:L39](paper/sections/3_primitive_ap_compiler.tex#L39) | `edfc59483cb3d47c7f1907cbf02f39b9edc98fb60fcef7ab1bfa83c51d0bc309` |
| D17 | \[...\] | [paper/sections/3_primitive_ap_compiler.tex:L46](paper/sections/3_primitive_ap_compiler.tex#L46) – [paper/sections/3_primitive_ap_compiler.tex:L50](paper/sections/3_primitive_ap_compiler.tex#L50) | `69ba55a6d4a0ff8a23c2a60ef2587c021eceaf48f3ac157b9d195024ed4e19d9` |
| D18 | \[...\] | [paper/sections/3_primitive_ap_compiler.tex:L55](paper/sections/3_primitive_ap_compiler.tex#L55) – [paper/sections/3_primitive_ap_compiler.tex:L57](paper/sections/3_primitive_ap_compiler.tex#L57) | `bbd5798aaab8a37d0967604c440f511658222a16f010f2b9afd526129566adf0` |
| D19 | equation | [paper/sections/3_primitive_ap_compiler.tex:L61](paper/sections/3_primitive_ap_compiler.tex#L61) – [paper/sections/3_primitive_ap_compiler.tex:L64](paper/sections/3_primitive_ap_compiler.tex#L64) | `494a9de7cb6d037f30482e91a2afbf32f480d67ac81542eb5a5b0327ce07c992` |
| D20 | equation | [paper/sections/3_primitive_ap_compiler.tex:L78](paper/sections/3_primitive_ap_compiler.tex#L78) – [paper/sections/3_primitive_ap_compiler.tex:L81](paper/sections/3_primitive_ap_compiler.tex#L81) | `619f05a345f4a457fd771311cc0fa9774fd31250b9e278007bb5b7a09f63f4fd` |
| D21 | \[...\] | [paper/sections/3_primitive_ap_compiler.tex:L85](paper/sections/3_primitive_ap_compiler.tex#L85) – [paper/sections/3_primitive_ap_compiler.tex:L89](paper/sections/3_primitive_ap_compiler.tex#L89) | `1aaea88c57420ce0a76549af62aa07f82f95b6f41f5bdaee66ca5f7e433970e8` |
| D22 | equation | [paper/sections/4_v59_composition.tex:L10](paper/sections/4_v59_composition.tex#L10) – [paper/sections/4_v59_composition.tex:L15](paper/sections/4_v59_composition.tex#L15) | `9e680e9756d269cf43ff17113ae07d3b8751667acee7f65226fd2168940e9f05` |
| D23 | equation | [paper/sections/4_v59_composition.tex:L24](paper/sections/4_v59_composition.tex#L24) – [paper/sections/4_v59_composition.tex:L27](paper/sections/4_v59_composition.tex#L27) | `ec588ed0f0a53e2f00e2620405e47706b23c1e7239dc0dd630e76d411e62431e` |
| D24 | \[...\] | [paper/sections/4_v59_composition.tex:L31](paper/sections/4_v59_composition.tex#L31) – [paper/sections/4_v59_composition.tex:L34](paper/sections/4_v59_composition.tex#L34) | `8c2d8991947bfdcd17bcf9671c37ed870425abff07f1a424f47debbe7f63f9c0` |
| D25 | equation | [paper/sections/4_v59_composition.tex:L40](paper/sections/4_v59_composition.tex#L40) – [paper/sections/4_v59_composition.tex:L43](paper/sections/4_v59_composition.tex#L43) | `cf7ad5976214d188e6fb9242be19f958ff0dd4972e7ca7f5d759c70a6cfe7c7e` |
| D26 | equation | [paper/sections/4_v59_composition.tex:L53](paper/sections/4_v59_composition.tex#L53) – [paper/sections/4_v59_composition.tex:L59](paper/sections/4_v59_composition.tex#L59) | `6982796dec917a79854b70b1533f254b419a7de44260b6a2786d5dfbf02f5ca7` |
| D27 | equation | [paper/sections/4_v59_composition.tex:L70](paper/sections/4_v59_composition.tex#L70) – [paper/sections/4_v59_composition.tex:L74](paper/sections/4_v59_composition.tex#L74) | `a9ed89164acac7225fff3dea77546c9db8a42559b29fb6d572309fb863473d86` |
| D28 | equation | [paper/sections/4_v59_composition.tex:L84](paper/sections/4_v59_composition.tex#L84) – [paper/sections/4_v59_composition.tex:L89](paper/sections/4_v59_composition.tex#L89) | `b307363567566e8ac3e4004f74f662d3923b885c1ff7e5064243d52cc7c12bb7` |
| D29 | \[...\] | [paper/sections/4_v59_composition.tex:L93](paper/sections/4_v59_composition.tex#L93) – [paper/sections/4_v59_composition.tex:L96](paper/sections/4_v59_composition.tex#L96) | `178ae061b3b9d41d2627333d3bb0ee5cc9cd31f7b8926c4ef7bb93671584cb40` |
| D30 | \[...\] | [paper/sections/4_v59_composition.tex:L111](paper/sections/4_v59_composition.tex#L111) – [paper/sections/4_v59_composition.tex:L113](paper/sections/4_v59_composition.tex#L113) | `8b10e5d9b00e27907389bb7c74d558c815bade14a1170c075d90212e5fee8c18` |
| D31 | equation | [paper/sections/5_finite_certificate.tex:L8](paper/sections/5_finite_certificate.tex#L8) – [paper/sections/5_finite_certificate.tex:L11](paper/sections/5_finite_certificate.tex#L11) | `58743fb466b392528cc5a168ab7a55349340b424fb34894b2d0dcb3843716b82` |
| D32 | \[...\] | [paper/sections/5_finite_certificate.tex:L46](paper/sections/5_finite_certificate.tex#L46) – [paper/sections/5_finite_certificate.tex:L50](paper/sections/5_finite_certificate.tex#L50) | `c15adc9f52d3227f6add50c7c0c6827313a49e4611d53f108eb7eca24a5b1a24` |
| D33 | \[...\] | [paper/sections/5_finite_certificate.tex:L56](paper/sections/5_finite_certificate.tex#L56) – [paper/sections/5_finite_certificate.tex:L60](paper/sections/5_finite_certificate.tex#L60) | `a5d619510a016b2c948fdbc0ea3d3446c5cd690871f738d42ac00cd49ec40f15` |
| D34 | \[...\] | [paper/sections/6_route_boundary.tex:L6](paper/sections/6_route_boundary.tex#L6) – [paper/sections/6_route_boundary.tex:L8](paper/sections/6_route_boundary.tex#L8) | `dad1acd486a0f1e58645d28ea46d8f97deef74d18480eb74473aaf495cf5d370` |
| D35 | \[...\] | [paper/sections/6_route_boundary.tex:L13](paper/sections/6_route_boundary.tex#L13) – [paper/sections/6_route_boundary.tex:L15](paper/sections/6_route_boundary.tex#L15) | `e9f57fea242ff37b8d3e9167162cfc1680ef50f504bcdea020f219a8ac7a0e86` |
| D36 | \[...\] | [paper/sections/6_route_boundary.tex:L21](paper/sections/6_route_boundary.tex#L21) – [paper/sections/6_route_boundary.tex:L23](paper/sections/6_route_boundary.tex#L23) | `552308a3ee524bd0a2c3f63a802a0b581b4d42d86930fd615c9306759da05c2b` |
| D37 | \[...\] | [paper/sections/6_route_boundary.tex:L36](paper/sections/6_route_boundary.tex#L36) – [paper/sections/6_route_boundary.tex:L39](paper/sections/6_route_boundary.tex#L39) | `50398416bbfeff06f227babbff313eb1861fe66f3f8dc725ef4601af428094fb` |
| D38 | \[...\] | [paper/sections/7_conclusion.tex:L14](paper/sections/7_conclusion.tex#L14) – [paper/sections/7_conclusion.tex:L17](paper/sections/7_conclusion.tex#L17) | `1cfd2a62df843a2dbca928cbb80c2fc7d773ec031beb357d40d881a3c981d68f` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/main.tex:L20](paper/main.tex#L20): `pdftitle={A Brun--Titchmarsh Primitive-Bucket Envelope for Finite-Window Prime-Shell Reassembly},`
- [paper/main.tex:L34](paper/main.tex#L34): `for Finite-Window Prime-Shell Reassembly}}`
- [paper/sections/0_abstract.tex:L2](paper/sections/0_abstract.tex#L2): `buckets in a finite-window prime-shell kernel.  If $4Q<H$,`
- [paper/sections/0_abstract.tex:L34](paper/sections/0_abstract.tex#L34): `does not prove signed cancellation, arithmetic $L^2$, Gate B, or a`
- [paper/sections/1_introduction.tex:L4](paper/sections/1_introduction.tex#L4): `The prime-shell labels in the finite-window kernel collide before distinct`
- [paper/sections/1_introduction.tex:L15](paper/sections/1_introduction.tex#L15): `a finite collection of reduced prime progressions without changing the packet`
- [paper/sections/1_introduction.tex:L29](paper/sections/1_introduction.tex#L29): `$R_h(a)\ll x^{1/96}\log\log x/\log x$, uniformly over active primitive`
- [paper/sections/1_introduction.tex:L38](paper/sections/1_introduction.tex#L38): `\item We give a deterministic finite certificate with an independent`
- [paper/sections/1_introduction.tex:L39](paper/sections/1_introduction.tex#L39): `reconstruction and mutation tests.  Its numerical rows illustrate the finite`
- [paper/sections/1_introduction.tex:L45](paper/sections/1_introduction.tex#L45): `but does not alter the fixed-power ledger.`
- [paper/sections/1_introduction.tex:L76](paper/sections/1_introduction.tex#L76): `sections document the finite audit and route boundary.`
- [paper/sections/2_source_setup.tex:L94](paper/sections/2_source_setup.tex#L94): `Finally, the inherited finite-window composition will be used only after the`
- [paper/sections/3_primitive_ap_compiler.tex:L28](paper/sections/3_primitive_ap_compiler.tex#L28): `Assume $4Q<H$ and $2\leq h\leq U<Q$.  For every`
- [paper/sections/3_primitive_ap_compiler.tex:L68](paper/sections/3_primitive_ap_compiler.tex#L68): `does not hide two copies of $a$ for the same $q$.  We do not invoke`
- [paper/sections/4_v59_composition.tex:L1](paper/sections/4_v59_composition.tex#L1): `\section{V59 specialization and finite-window composition}`
- [paper/sections/4_v59_composition.tex:L4](paper/sections/4_v59_composition.tex#L4): `\subsection{Uniform primitive-row density}`
- [paper/sections/4_v59_composition.tex:L38](paper/sections/4_v59_composition.tex#L38): `$h/\ph(h)\ll\log\log x$ uniformly in this range.  Since`
- [paper/sections/4_v59_composition.tex:L66](paper/sections/4_v59_composition.tex#L66): `\begin{theorem}[Prime-density finite-window packet trace]`
- [paper/sections/4_v59_composition.tex:L116](paper/sections/4_v59_composition.tex#L116): `therefore gives genuine logarithmic progress, not a fixed-power saving, and`
- [paper/sections/4_v59_composition.tex:L117](paper/sections/4_v59_composition.tex#L117): `does not establish sharpness of either fixed-power exponent.`
- [paper/sections/5_finite_certificate.tex:L1](paper/sections/5_finite_certificate.tex#L1): `\section{Deterministic finite certificate}`
- [paper/sections/5_finite_certificate.tex:L22](paper/sections/5_finite_certificate.tex#L22): `\caption{Primary finite-fixture summary.  The real upper bounds are numerical`
- [paper/sections/5_finite_certificate.tex:L76](paper/sections/5_finite_certificate.tex#L76): `\texttt{NUMERICAL\_FINITE\_ILLUSTRATION\_ONLY}.  The general bucket theorem is`
- [paper/sections/6_route_boundary.tex:L4](paper/sections/6_route_boundary.tex#L4): `The strongest positive result is the finite-window common-source packet trace`
- [paper/sections/6_route_boundary.tex:L32](paper/sections/6_route_boundary.tex#L32): `The open theorem is weighted or signed within-bucket cancellation beyond`
- [paper/sections/6_route_boundary.tex:L42](paper/sections/6_route_boundary.tex#L42): `the physical support algebra.  A further uniform nonnegative bucket bound,`
- [paper/sections/6_route_boundary.tex:L47](paper/sections/6_route_boundary.tex#L47): `seeking further uniform bucket savings.  Such a test must retain the literal`
- [paper/sections/6_route_boundary.tex:L51](paper/sections/6_route_boundary.tex#L51): `remain open or absent.`
- [paper/sections/7_conclusion.tex:L12](paper/sections/7_conclusion.tex#L12): `finite-window trace bound`
- [paper/sections/A_status_ledger.tex:L27](paper/sections/A_status_ledger.tex#L27): `\texttt{OPEN}`
- [paper/sections/A_status_ledger.tex:L38](paper/sections/A_status_ledger.tex#L38): `Finite-window common-source packet trace with`
- [paper/sections/A_status_ledger.tex:L42](paper/sections/A_status_ledger.tex#L42): `\item[Open theorem]`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:comparison` → `sections/1_introduction.tex#L52` (existing project target or original TeX label line).
- Link relocation: `#sec:source` → `sections/2_source_setup.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#sec:compiler` → `sections/3_primitive_ap_compiler.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#sec:composition` → `sections/4_v59_composition.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#eq:physical-support` → `sections/2_source_setup.tex#L56` (existing project target or original TeX label line).
- Link relocation: `#eq:K` → `sections/2_source_setup.tex#L42` (existing project target or original TeX label line).
- Link relocation: `#eq:direct-energy` → `sections/2_source_setup.tex#L100` (existing project target or original TeX label line).
- Link relocation: `#eq:ap-census` → `sections/3_primitive_ap_compiler.tex#L35` (existing project target or original TeX label line).
- Link relocation: `#eq:ap-census` → `sections/3_primitive_ap_compiler.tex#L35` (existing project target or original TeX label line).
- Link relocation: `#eq:BT-standard` → `sections/2_source_setup.tex#L84` (existing project target or original TeX label line).
- Link relocation: `#eq:BT-standard` → `sections/2_source_setup.tex#L84` (existing project target or original TeX label line).
- Link relocation: `#eq:m-count` → `sections/3_primitive_ap_compiler.tex#L80` (existing project target or original TeX label line).
- Link relocation: `#eq:factor16` → `sections/3_primitive_ap_compiler.tex#L38` (existing project target or original TeX label line).
- Link relocation: `#thm:bucket` → `sections/3_primitive_ap_compiler.tex#L27` (existing project target or original TeX label line).
- Link relocation: `#eq:scales` → `sections/2_source_setup.tex#L11` (existing project target or original TeX label line).
- Link relocation: `#lem:h-one` → `sections/3_primitive_ap_compiler.tex#L17` (existing project target or original TeX label line).
- Link relocation: `#thm:bucket` → `sections/3_primitive_ap_compiler.tex#L27` (existing project target or original TeX label line).
- Link relocation: `#eq:v59-row` → `sections/4_v59_composition.tex#L14` (existing project target or original TeX label line).
- Link relocation: `#eq:K` → `sections/2_source_setup.tex#L42` (existing project target or original TeX label line).
- Link relocation: `#cor:v59-row` → `sections/4_v59_composition.tex#L7` (existing project target or original TeX label line).
- Link relocation: `#eq:frozen-composition` → `sections/4_v59_composition.tex#L58` (existing project target or original TeX label line).
- Link relocation: `#eq:direct-energy` → `sections/2_source_setup.tex#L100` (existing project target or original TeX label line).
- Link relocation: `#eq:packet-trace` → `sections/4_v59_composition.tex#L73` (existing project target or original TeX label line).
- Link relocation: `#thm:packet-trace` → `sections/4_v59_composition.tex#L67` (existing project target or original TeX label line).
- Link relocation: `#eq:ap-census` → `sections/3_primitive_ap_compiler.tex#L35` (existing project target or original TeX label line).
- Link relocation: `#sec:compiler` → `sections/3_primitive_ap_compiler.tex#L2` (existing project target or original TeX label line).
