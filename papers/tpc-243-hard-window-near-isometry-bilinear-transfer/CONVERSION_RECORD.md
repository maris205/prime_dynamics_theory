# TPC-243 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `e713a3d35efcc1fefa1a819f4a2f30b1d8e2ae72d461e5635a4e32a3653b8a7f`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `ee8dda20ef16f910921f2f9080c43745eb56634708b25c594f70d883809b331f`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `00a37a5c7f18c7574ff4e6ccc9ce78c6c8f4b4acb5aba351525af9d1c95de0b4`; 7 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `41b659207d1f80ea432f10f0a275bd7e69290110029c51f115582b95b278a05e`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC240_244.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 13 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `e713a3d35efcc1fefa1a819f4a2f30b1d8e2ae72d461e5635a4e32a3653b8a7f` |
| [paper/math_commands.tex](paper/math_commands.tex) | `52287dc68d6f7f0d37206cfa32be2810c18d282a799ad1a7cc228d324dd137ee` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `d15a1437e80e565d7f33bdf6bb95b5a715dc6daedc77cb62f7b1e6e127f3edc1` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `24592b938082a32c1e3481a12b26521f850b41c3116efb733d2464bb908f51ce` |
| [paper/sections/2_setup_source_lock.tex](paper/sections/2_setup_source_lock.tex) | `c303bf01463709728929ddb31abf8ec2ac5a7e91b1d3eb7de12bd6234d4192f5` |
| [paper/sections/3_harmonic_row_bound.tex](paper/sections/3_harmonic_row_bound.tex) | `b1e4e46b5a604cd946b3196adad9528666576bb5a5c6e4c3512a239788dbb96a` |
| [paper/sections/4_near_isometry_bilinear.tex](paper/sections/4_near_isometry_bilinear.tex) | `65f7e96d8cf9f52ae493381043385fda43e5f4f73d7eb4da137aee4d960d3617` |
| [paper/sections/5_primitive_v59.tex](paper/sections/5_primitive_v59.tex) | `9b7ecbfecef7f0dbc57b70bb2deece1318d9331ab0f45c97e1f41ef2d4db88cc` |
| [paper/sections/6_tpc242_transport.tex](paper/sections/6_tpc242_transport.tex) | `609746d2842d44627578c3a928b5c3ab78faa717f72f1e1b5edc957393e86188` |
| [paper/sections/7_exact_certificate.tex](paper/sections/7_exact_certificate.tex) | `a58087ea8c84e7404894f631d4ff4ec19dcf31bd75f7ad8e7babd36883bffc19` |
| [paper/sections/8_route_boundary.tex](paper/sections/8_route_boundary.tex) | `057f7caa853ca5e23ba192d63dfa4d7dae2eddfc987e5bb2245ffe1bc63a308c` |
| [paper/sections/9_conclusion.tex](paper/sections/9_conclusion.tex) | `412d28d435616983201e09e429e1bc9cb4bca20bc758942961217630ef1d7232` |
| [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) | `1559e23ac09f9ef76b5d082234caae6ec02b999b0cb5c38c7e524b26bf1ddeec` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L17](paper/main.tex#L17) | `\input{math_commands}` | [paper/math_commands.tex](paper/math_commands.tex) |
| [paper/main.tex:L46](paper/main.tex#L46) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L49](paper/main.tex#L49) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L50](paper/main.tex#L50) | `\input{sections/2_setup_source_lock}` | [paper/sections/2_setup_source_lock.tex](paper/sections/2_setup_source_lock.tex) |
| [paper/main.tex:L51](paper/main.tex#L51) | `\input{sections/3_harmonic_row_bound}` | [paper/sections/3_harmonic_row_bound.tex](paper/sections/3_harmonic_row_bound.tex) |
| [paper/main.tex:L52](paper/main.tex#L52) | `\input{sections/4_near_isometry_bilinear}` | [paper/sections/4_near_isometry_bilinear.tex](paper/sections/4_near_isometry_bilinear.tex) |
| [paper/main.tex:L53](paper/main.tex#L53) | `\input{sections/5_primitive_v59}` | [paper/sections/5_primitive_v59.tex](paper/sections/5_primitive_v59.tex) |
| [paper/main.tex:L54](paper/main.tex#L54) | `\input{sections/6_tpc242_transport}` | [paper/sections/6_tpc242_transport.tex](paper/sections/6_tpc242_transport.tex) |
| [paper/main.tex:L55](paper/main.tex#L55) | `\input{sections/7_exact_certificate}` | [paper/sections/7_exact_certificate.tex](paper/sections/7_exact_certificate.tex) |
| [paper/main.tex:L56](paper/main.tex#L56) | `\input{sections/8_route_boundary}` | [paper/sections/8_route_boundary.tex](paper/sections/8_route_boundary.tex) |
| [paper/main.tex:L57](paper/main.tex#L57) | `\input{sections/9_conclusion}` | [paper/sections/9_conclusion.tex](paper/sections/9_conclusion.tex) |
| [paper/main.tex:L63](paper/main.tex#L63) | `\input{sections/A_status_ledger}` | [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Setup and source lock` | [paper/sections/2_setup_source_lock.tex:L1](paper/sections/2_setup_source_lock.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Repository-relative position` | [paper/sections/2_setup_source_lock.tex:L35](paper/sections/2_setup_source_lock.tex#L35) | 2 | `HEADING_TEXT_MATCH` |
| `The hard-window harmonic row bound` | [paper/sections/3_harmonic_row_bound.tex:L1](paper/sections/3_harmonic_row_bound.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Near-isometry and signed bilinear transfer` | [paper/sections/4_near_isometry_bilinear.tex:L1](paper/sections/4_near_isometry_bilinear.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Primitive rational specialization and V59 scale` | [paper/sections/5_primitive_v59.tex:L1](paper/sections/5_primitive_v59.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Transport of the TPC-242 selected mode` | [paper/sections/6_tpc242_transport.tex:L1](paper/sections/6_tpc242_transport.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Exact finite certificate` | [paper/sections/7_exact_certificate.tex:L1](paper/sections/7_exact_certificate.tex#L1) | 6 | `HEADING_TEXT_MATCH` |
| `Route evaluation and claim boundary` | [paper/sections/8_route_boundary.tex:L1](paper/sections/8_route_boundary.tex#L1) | 6 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/9_conclusion.tex:L1](paper/sections/9_conclusion.tex#L1) | 7 | `HEADING_TEXT_MATCH` |
| `Status and reproducibility ledger` | [paper/sections/A_status_ledger.tex:L1](paper/sections/A_status_ledger.tex#L1) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `References (external bibliography)` | [paper/main.tex:L60](paper/main.tex#L60) | 7 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `153` before writing and `153` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `24`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `600b3ead85a9f61c28fa7dc93ad3bee3133a99a11c4eebd709679bd4c437bbc1`.
- Source theorem/proof environment starts: lemma at [paper/sections/3_harmonic_row_bound.tex:L6](paper/sections/3_harmonic_row_bound.tex#L6), proof at [paper/sections/3_harmonic_row_bound.tex:L14](paper/sections/3_harmonic_row_bound.tex#L14), lemma at [paper/sections/3_harmonic_row_bound.tex:L27](paper/sections/3_harmonic_row_bound.tex#L27), proof at [paper/sections/3_harmonic_row_bound.tex:L36](paper/sections/3_harmonic_row_bound.tex#L36), proposition at [paper/sections/3_harmonic_row_bound.tex:L55](paper/sections/3_harmonic_row_bound.tex#L55), proof at [paper/sections/3_harmonic_row_bound.tex:L60](paper/sections/3_harmonic_row_bound.tex#L60), theorem at [paper/sections/4_near_isometry_bilinear.tex:L3](paper/sections/4_near_isometry_bilinear.tex#L3), proof at [paper/sections/4_near_isometry_bilinear.tex:L17](paper/sections/4_near_isometry_bilinear.tex#L17), remark at [paper/sections/4_near_isometry_bilinear.tex:L49](paper/sections/4_near_isometry_bilinear.tex#L49), corollary at [paper/sections/5_primitive_v59.tex:L3](paper/sections/5_primitive_v59.tex#L3), proof at [paper/sections/5_primitive_v59.tex:L14](paper/sections/5_primitive_v59.tex#L14).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/0_abstract.tex:L10](paper/sections/0_abstract.tex#L10) – [paper/sections/0_abstract.tex:L13](paper/sections/0_abstract.tex#L13) | `08f552070e3b07d734b716d8633205cd08aaaff0dd5068722d76951016511b83` |
| D02 | \[...\] | [paper/sections/2_setup_source_lock.tex:L8](paper/sections/2_setup_source_lock.tex#L8) – [paper/sections/2_setup_source_lock.tex:L10](paper/sections/2_setup_source_lock.tex#L10) | `522a14d68c9606f1db7fabb77927f9196897e4eda208487c4a842f1fd255b4a7` |
| D03 | \[...\] | [paper/sections/2_setup_source_lock.tex:L12](paper/sections/2_setup_source_lock.tex#L12) – [paper/sections/2_setup_source_lock.tex:L17](paper/sections/2_setup_source_lock.tex#L17) | `b01bae3219f40109df728080eee9d8682e0c94b236701d98b91a09a6528b24ce` |
| D04 | \[...\] | [paper/sections/2_setup_source_lock.tex:L22](paper/sections/2_setup_source_lock.tex#L22) – [paper/sections/2_setup_source_lock.tex:L30](paper/sections/2_setup_source_lock.tex#L30) | `dce1345256b55b715462145e30ce867f80af9b1f66c17ee1edfc6fb49dfba61f` |
| D05 | \[...\] | [paper/sections/3_harmonic_row_bound.tex:L8](paper/sections/3_harmonic_row_bound.tex#L8) – [paper/sections/3_harmonic_row_bound.tex:L11](paper/sections/3_harmonic_row_bound.tex#L11) | `cf42f5c4d18491552fd0369b16e070f655d961386488e6b731b064aacb469d41` |
| D06 | \[...\] | [paper/sections/3_harmonic_row_bound.tex:L17](paper/sections/3_harmonic_row_bound.tex#L17) – [paper/sections/3_harmonic_row_bound.tex:L21](paper/sections/3_harmonic_row_bound.tex#L21) | `16c39a30adedc90a9e4ab665705856cac6743204a4a53cff418f8ebeb21d283d` |
| D07 | \[...\] | [paper/sections/3_harmonic_row_bound.tex:L29](paper/sections/3_harmonic_row_bound.tex#L29) – [paper/sections/3_harmonic_row_bound.tex:L33](paper/sections/3_harmonic_row_bound.tex#L33) | `cad7a90dd4da3dc76508841ad0a0c68ae27dc469edf00098c0b1728578d6274f` |
| D08 | \[...\] | [paper/sections/3_harmonic_row_bound.tex:L46](paper/sections/3_harmonic_row_bound.tex#L46) – [paper/sections/3_harmonic_row_bound.tex:L50](paper/sections/3_harmonic_row_bound.tex#L50) | `4c56aa3113c2d990827fd4ddddeadc412e2e91ec26afa2004abd6f98dbaac34e` |
| D09 | \[...\] | [paper/sections/3_harmonic_row_bound.tex:L62](paper/sections/3_harmonic_row_bound.tex#L62) – [paper/sections/3_harmonic_row_bound.tex:L65](paper/sections/3_harmonic_row_bound.tex#L65) | `4c28b3ca86ba045e6453d09309460dce7a6d4518637e1652b8e4f722e8e4f8c2` |
| D10 | \[...\] | [paper/sections/4_near_isometry_bilinear.tex:L5](paper/sections/4_near_isometry_bilinear.tex#L5) – [paper/sections/4_near_isometry_bilinear.tex:L9](paper/sections/4_near_isometry_bilinear.tex#L9) | `d13047a5d995b2642aad5de16f48b98f4fc11d1012d87a721e96e42c6b3405a7` |
| D11 | \[...\] | [paper/sections/4_near_isometry_bilinear.tex:L11](paper/sections/4_near_isometry_bilinear.tex#L11) – [paper/sections/4_near_isometry_bilinear.tex:L14](paper/sections/4_near_isometry_bilinear.tex#L14) | `13935d84d5436608eaebf87acb62094c28c0ae81cd031f967332ccf025094f04` |
| D12 | \[...\] | [paper/sections/4_near_isometry_bilinear.tex:L22](paper/sections/4_near_isometry_bilinear.tex#L22) – [paper/sections/4_near_isometry_bilinear.tex:L26](paper/sections/4_near_isometry_bilinear.tex#L26) | `23de653ed6e7979125087190b2d0bb782ff73598fd08963f720ba46cfe747d08` |
| D13 | \[...\] | [paper/sections/4_near_isometry_bilinear.tex:L37](paper/sections/4_near_isometry_bilinear.tex#L37) – [paper/sections/4_near_isometry_bilinear.tex:L44](paper/sections/4_near_isometry_bilinear.tex#L44) | `e5197cb4663c646a0a40a3a179f50e1978f84be885b2a777af71f1cc5d5542dd` |
| D14 | \[...\] | [paper/sections/5_primitive_v59.tex:L6](paper/sections/5_primitive_v59.tex#L6) – [paper/sections/5_primitive_v59.tex:L11](paper/sections/5_primitive_v59.tex#L11) | `f9f35c62671bc2517fc3574fa6888f86745f0489b770cdcae1d14fdbade33018` |
| D15 | \[...\] | [paper/sections/5_primitive_v59.tex:L18](paper/sections/5_primitive_v59.tex#L18) – [paper/sections/5_primitive_v59.tex:L22](paper/sections/5_primitive_v59.tex#L22) | `863fb560956933a9cc12aed54e60fa0d85e7aa3e0b13526d5ba5e2187584df2a` |
| D16 | \[...\] | [paper/sections/5_primitive_v59.tex:L28](paper/sections/5_primitive_v59.tex#L28) – [paper/sections/5_primitive_v59.tex:L32](paper/sections/5_primitive_v59.tex#L32) | `ee4de996d883ee771dc8b57232c16be8e8ebfd793be9209c42ea05e2c2bf23f0` |
| D17 | \[...\] | [paper/sections/5_primitive_v59.tex:L35](paper/sections/5_primitive_v59.tex#L35) – [paper/sections/5_primitive_v59.tex:L40](paper/sections/5_primitive_v59.tex#L40) | `5b120afce8e25e7bd6d69716313135776553d6d9dfda601981b410e12c7af734` |
| D18 | \[...\] | [paper/sections/5_primitive_v59.tex:L44](paper/sections/5_primitive_v59.tex#L44) – [paper/sections/5_primitive_v59.tex:L52](paper/sections/5_primitive_v59.tex#L52) | `8e429c1ddcecbd33de7fefdbf5f7c237e135e26ce98b928eab571674bc5c65ce` |
| D19 | \[...\] | [paper/sections/6_tpc242_transport.tex:L9](paper/sections/6_tpc242_transport.tex#L9) – [paper/sections/6_tpc242_transport.tex:L11](paper/sections/6_tpc242_transport.tex#L11) | `eeee6eecd7a3c7ca153675b66e5b73ec593b4dd6cb0bd5fa756bfb8af6be46ac` |
| D20 | \[...\] | [paper/sections/6_tpc242_transport.tex:L13](paper/sections/6_tpc242_transport.tex#L13) – [paper/sections/6_tpc242_transport.tex:L15](paper/sections/6_tpc242_transport.tex#L15) | `8194ba71c0def409e882dc74c118a773e6c4507bd0b301cf31df5d3432e61a54` |
| D21 | equation | [paper/sections/6_tpc242_transport.tex:L18](paper/sections/6_tpc242_transport.tex#L18) – [paper/sections/6_tpc242_transport.tex:L21](paper/sections/6_tpc242_transport.tex#L21) | `e2af65e16468899e0f1b42edc4e84215f83fcdb50ba889b7dfc649a93074bf84` |
| D22 | \[...\] | [paper/sections/7_exact_certificate.tex:L6](paper/sections/7_exact_certificate.tex#L6) – [paper/sections/7_exact_certificate.tex:L12](paper/sections/7_exact_certificate.tex#L12) | `313dd83f468a3a79a323330660c0e661a34f4555b5f9bcfdfff39f8616fd5523` |
| D23 | \[...\] | [paper/sections/8_route_boundary.tex:L4](paper/sections/8_route_boundary.tex#L4) – [paper/sections/8_route_boundary.tex:L7](paper/sections/8_route_boundary.tex#L7) | `f4acd64eb1b0f0d8217b821ecd7410b40bd699908996b66b07476b21b09b7645` |
| D24 | \[...\] | [paper/sections/8_route_boundary.tex:L26](paper/sections/8_route_boundary.tex#L26) – [paper/sections/8_route_boundary.tex:L33](paper/sections/8_route_boundary.tex#L33) | `4367d4748ca90a97dacd22321b2695f226043bcbb819482bab92d7cb23dfe23f` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/0_abstract.tex:L2](paper/sections/0_abstract.tex#L2): `finite separated subset of the circle.  If the frequencies are`
- [paper/sections/1_introduction.tex:L3](paper/sections/1_introduction.tex#L3): `Hard finite intervals do not automatically preserve coefficient geometry.`
- [paper/sections/1_introduction.tex:L11](paper/sections/1_introduction.tex#L11): `standard additive large sieve to obtain an upper finite-window estimate at the`
- [paper/sections/1_introduction.tex:L35](paper/sections/1_introduction.tex#L35): `does not bound the literal physical coefficient norms, identify the top-prime`
- [paper/sections/1_introduction.tex:L44](paper/sections/1_introduction.tex#L44): `sections separate finite reproduction checks from the remaining route gates.`
- [paper/sections/2_setup_source_lock.tex:L3](paper/sections/2_setup_source_lock.tex#L3): `Let $\cF\subset\Torus$ be finite.  Circular distance is denoted by`
- [paper/sections/2_setup_source_lock.tex:L48](paper/sections/2_setup_source_lock.tex#L48): `TPC-242 & $F_1=\ip{Y}{X}$ for the literal $i^j$ phase convention & Fixes the selected orientation, not a physical attachment \\`
- [paper/sections/3_harmonic_row_bound.tex:L4](paper/sections/3_harmonic_row_bound.tex#L4): `changes only phases and therefore does not affect entry magnitudes.`
- [paper/sections/4_near_isometry_bilinear.tex:L32](paper/sections/4_near_isometry_bilinear.tex#L32): `semidefinite.  Taking the stronger of this lower estimate and zero, then`
- [paper/sections/4_near_isometry_bilinear.tex:L45](paper/sections/4_near_isometry_bilinear.tex#L45): `The argument controls the complex bilinear quantity directly; it does not`
- [paper/sections/6_tpc242_transport.tex:L28](paper/sections/6_tpc242_transport.tex#L28): `explicit norm-weighted error.  It does not show that $F_1$ is small, large,`
- [paper/sections/6_tpc242_transport.tex:L29](paper/sections/6_tpc242_transport.tex#L29): `nonzero, or of a prescribed sign.  More importantly, the repository does not`
- [paper/sections/7_exact_certificate.tex:L1](paper/sections/7_exact_certificate.tex#L1): `\section{Exact finite certificate}\label{sec:certificate}`
- [paper/sections/7_exact_certificate.tex:L26](paper/sections/7_exact_certificate.tex#L26): `parsing rejects duplicate keys, nonfinite constants, nonminimal fractions,`
- [paper/sections/7_exact_certificate.tex:L27](paper/sections/7_exact_certificate.tex#L27): `and Boolean substitutions for integers.  The independent checker does not`
- [paper/sections/7_exact_certificate.tex:L33](paper/sections/7_exact_certificate.tex#L33): `All finite checks are`
- [paper/sections/7_exact_certificate.tex:L34](paper/sections/7_exact_certificate.tex#L34): `\texttt{NUMERICAL\_FINITE\_ILLUSTRATION\_ONLY}.  Exact arithmetic removes`
- [paper/sections/7_exact_certificate.tex:L35](paper/sections/7_exact_certificate.tex#L35): `rounding ambiguity from reproduction; it does not prove the general theorem.`
- [paper/sections/8_route_boundary.tex:L18](paper/sections/8_route_boundary.tex#L18): `The next open theorem is therefore source-typed: identify both polarized V59`
- [paper/sections/8_route_boundary.tex:L40](paper/sections/8_route_boundary.tex#L40): `twin-prime conclusion all remain open or absent.`
- [paper/sections/A_status_ledger.tex:L12](paper/sections/A_status_ledger.tex#L12): `Finite computation & Illustration only \\`
- [paper/sections/A_status_ledger.tex:L13](paper/sections/A_status_ledger.tex#L13): `Physical attachment & Open \\`
- [paper/sections/A_status_ledger.tex:L15](paper/sections/A_status_ledger.tex#L15): `Full Gate B & Open \\`
- [paper/sections/A_status_ledger.tex:L40](paper/sections/A_status_ledger.tex#L40): `and create no theorem claim from their finite output.`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- The preamble-only glyphtounicode input was resolved with kpsewhich and checked against the audited SHA-256; its non-content mapping table was not expanded. The original command, source line, and dependency hash are retained in the reading layer.
- 5 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#sec:setup` → `sections/2_setup_source_lock.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:row` → `sections/3_harmonic_row_bound.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:operator` → `sections/4_near_isometry_bilinear.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:primitive` → `sections/5_primitive_v59.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:transport` → `sections/6_tpc242_transport.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#lem:geometric` → `sections/3_harmonic_row_bound.tex#L6` (existing project target or original TeX label line).
- Link relocation: `#lem:packing` → `sections/3_harmonic_row_bound.tex#L27` (existing project target or original TeX label line).
- Link relocation: `#prop:rows` → `sections/3_harmonic_row_bound.tex#L55` (existing project target or original TeX label line).
- Link relocation: `#lem:geometric` → `sections/3_harmonic_row_bound.tex#L6` (existing project target or original TeX label line).
- Link relocation: `#prop:rows` → `sections/3_harmonic_row_bound.tex#L55` (existing project target or original TeX label line).
- Link relocation: `#sec:setup` → `sections/2_setup_source_lock.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `sections/4_near_isometry_bilinear.tex#L3` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `sections/4_near_isometry_bilinear.tex#L3` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `sections/4_near_isometry_bilinear.tex#L3` (existing project target or original TeX label line).
- Link relocation: `#eq:selected-transfer` → `sections/6_tpc242_transport.tex#L18` (existing project target or original TeX label line).
- Link relocation: `#sec:row` → `sections/3_harmonic_row_bound.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:transport` → `sections/6_tpc242_transport.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#eq:selected-transfer` → `sections/6_tpc242_transport.tex#L18` (existing project target or original TeX label line).
