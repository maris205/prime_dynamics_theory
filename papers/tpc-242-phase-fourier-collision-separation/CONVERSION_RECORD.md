# TPC-242 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `1ae9b2e254f93c7742cb1023ec88e21c4bab3ca2cd297e06e1c8cb89162c4852`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `3ae00fc156d7666a0d28dc8aeb85a87557b6780cbb6730776b7e90288aa061d1`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `e661fd4ba04437a34d0b1aaec789ec271301244ccfa322767815a5e141a8e2e6`; 8 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `0f91ae19f69249f8c333e803515918fa5755407829b7e20f6c10246d4d6b2f3a`.
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
| [paper/main.tex](paper/main.tex) | `1ae9b2e254f93c7742cb1023ec88e21c4bab3ca2cd297e06e1c8cb89162c4852` |
| [paper/math_commands.tex](paper/math_commands.tex) | `e61b99466e15481646eb827e1f7a58790f4342a7c2b19fb4881cc64d78c24125` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `2e677522fb9282528ce8296703076df91f938832d08b8e3f80bd10e5f234dd61` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `52116977c5cdb41c256e01f98edcba969210a0b002a8be91dce72d5e458c5307` |
| [paper/sections/2_v59_source_lock.tex](paper/sections/2_v59_source_lock.tex) | `1b5397b32e1f0502249b27e393e2a20a04183e0df59da6d3988b22ad2725e9ac` |
| [paper/sections/3_phase_fourier_theorem.tex](paper/sections/3_phase_fourier_theorem.tex) | `a05a6d80f7028df694c81326218f2161dea104581ca7a52c7ff31b66d2087cc0` |
| [paper/sections/4_feasible_disk.tex](paper/sections/4_feasible_disk.tex) | `a13a53c66db726e76608bb579b8e26626e762b57f0fbcdb2a769ba41e194f665` |
| [paper/sections/5_tpc241_no_transfer.tex](paper/sections/5_tpc241_no_transfer.tex) | `c387a12c8e2537d095c33960860036a7a48f5e38dcaee178e150955f4697d666` |
| [paper/sections/6_certificate.tex](paper/sections/6_certificate.tex) | `df70ed192686175aaaa502730a399c780160132d51ad3711b394e8aa0fc7ba9f` |
| [paper/sections/7_route_boundary.tex](paper/sections/7_route_boundary.tex) | `166737023f36a3d93fca67d9bd59ae8a39f81da0ebc02ebdfd7bf9647f9b91b9` |
| [paper/sections/8_conclusion.tex](paper/sections/8_conclusion.tex) | `77451abd9b34ee361e29fef62f49b3528b3b290826f1d85bb913ac7c4722ead6` |
| [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) | `bcaa5f46319532f28d22dba0dc493d76593bc06fe7e71f18a2bf3f52cbb59ebc` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L13](paper/main.tex#L13) | `\input{math_commands}` | [paper/math_commands.tex](paper/math_commands.tex) |
| [paper/main.tex:L40](paper/main.tex#L40) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L43](paper/main.tex#L43) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L44](paper/main.tex#L44) | `\input{sections/2_v59_source_lock}` | [paper/sections/2_v59_source_lock.tex](paper/sections/2_v59_source_lock.tex) |
| [paper/main.tex:L45](paper/main.tex#L45) | `\input{sections/3_phase_fourier_theorem}` | [paper/sections/3_phase_fourier_theorem.tex](paper/sections/3_phase_fourier_theorem.tex) |
| [paper/main.tex:L46](paper/main.tex#L46) | `\input{sections/4_feasible_disk}` | [paper/sections/4_feasible_disk.tex](paper/sections/4_feasible_disk.tex) |
| [paper/main.tex:L47](paper/main.tex#L47) | `\input{sections/5_tpc241_no_transfer}` | [paper/sections/5_tpc241_no_transfer.tex](paper/sections/5_tpc241_no_transfer.tex) |
| [paper/main.tex:L48](paper/main.tex#L48) | `\input{sections/6_certificate}` | [paper/sections/6_certificate.tex](paper/sections/6_certificate.tex) |
| [paper/main.tex:L49](paper/main.tex#L49) | `\input{sections/7_route_boundary}` | [paper/sections/7_route_boundary.tex](paper/sections/7_route_boundary.tex) |
| [paper/main.tex:L50](paper/main.tex#L50) | `\input{sections/8_conclusion}` | [paper/sections/8_conclusion.tex](paper/sections/8_conclusion.tex) |
| [paper/main.tex:L56](paper/main.tex#L56) | `\input{sections/A_status_ledger}` | [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Literal V59 convention and source lock` | [paper/sections/2_v59_source_lock.tex:L1](paper/sections/2_v59_source_lock.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `The complete phase-Fourier theorem` | [paper/sections/3_phase_fourier_theorem.tex:L1](paper/sections/3_phase_fourier_theorem.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `The sharp feasible disk and phase defect` | [paper/sections/4_feasible_disk.tex:L1](paper/sections/4_feasible_disk.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Typed no-transfer from TPC-241` | [paper/sections/5_tpc241_no_transfer.tex:L1](paper/sections/5_tpc241_no_transfer.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Exact executable certificate` | [paper/sections/6_certificate.tex:L1](paper/sections/6_certificate.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Route boundary and remaining loss ledger` | [paper/sections/7_route_boundary.tex:L1](paper/sections/7_route_boundary.tex#L1) | 6 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/8_conclusion.tex:L1](paper/sections/8_conclusion.tex#L1) | 2, 6 | `UNMAPPED_OR_AMBIGUOUS` |
| `Source and status ledger` | [paper/sections/A_status_ledger.tex:L1](paper/sections/A_status_ledger.tex#L1) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `References (external bibliography)` | [paper/main.tex:L53](paper/main.tex#L53) | 7 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `122` before writing and `122` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `19`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `6509357ce51c9a7ebb79ab37dd7a0b2b918158473c21d87b5b0ba955f67a2176`.
- Source theorem/proof environment starts: theorem at [paper/sections/3_phase_fourier_theorem.tex:L11](paper/sections/3_phase_fourier_theorem.tex#L11), proof at [paper/sections/3_phase_fourier_theorem.tex:L21](paper/sections/3_phase_fourier_theorem.tex#L21), corollary at [paper/sections/3_phase_fourier_theorem.tex:L49](paper/sections/3_phase_fourier_theorem.tex#L49), proof at [paper/sections/3_phase_fourier_theorem.tex:L61](paper/sections/3_phase_fourier_theorem.tex#L61), remark at [paper/sections/3_phase_fourier_theorem.tex:L66](paper/sections/3_phase_fourier_theorem.tex#L66), theorem at [paper/sections/4_feasible_disk.tex:L5](paper/sections/4_feasible_disk.tex#L5), proof at [paper/sections/4_feasible_disk.tex:L15](paper/sections/4_feasible_disk.tex#L15), theorem at [paper/sections/4_feasible_disk.tex:L54](paper/sections/4_feasible_disk.tex#L54), proof at [paper/sections/4_feasible_disk.tex:L64](paper/sections/4_feasible_disk.tex#L64), corollary at [paper/sections/5_tpc241_no_transfer.tex:L24](paper/sections/5_tpc241_no_transfer.tex#L24), proof at [paper/sections/5_tpc241_no_transfer.tex:L32](paper/sections/5_tpc241_no_transfer.tex#L32).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/0_abstract.tex:L13](paper/sections/0_abstract.tex#L13) – [paper/sections/0_abstract.tex:L17](paper/sections/0_abstract.tex#L17) | `d738837b4e56ff017141706fbf528ee47d9f346ccdc59bc7a106854ce476b7f1` |
| D02 | equation | [paper/sections/1_introduction.tex:L13](paper/sections/1_introduction.tex#L13) – [paper/sections/1_introduction.tex:L16](paper/sections/1_introduction.tex#L16) | `1632838de0866f5356a91ae18401e3b9f2167ea7979533e6388448986f011c68` |
| D03 | \[...\] | [paper/sections/2_v59_source_lock.tex:L6](paper/sections/2_v59_source_lock.tex#L6) – [paper/sections/2_v59_source_lock.tex:L10](paper/sections/2_v59_source_lock.tex#L10) | `29296ab91144cc38b9d19a3c2ed1ba09c7327475b30ead491cc9116b492e859e` |
| D04 | \[...\] | [paper/sections/2_v59_source_lock.tex:L15](paper/sections/2_v59_source_lock.tex#L15) – [paper/sections/2_v59_source_lock.tex:L17](paper/sections/2_v59_source_lock.tex#L17) | `585c3d767684a8a2f8fed5f536af2df2a3cbd2552c9707ee6470906976296067` |
| D05 | \[...\] | [paper/sections/2_v59_source_lock.tex:L21](paper/sections/2_v59_source_lock.tex#L21) – [paper/sections/2_v59_source_lock.tex:L23](paper/sections/2_v59_source_lock.tex#L23) | `b5e7bbd9e54258c5663ced8b0adef528ee1e3f0302d4d848b7aee37875548735` |
| D06 | equation | [paper/sections/3_phase_fourier_theorem.tex:L4](paper/sections/3_phase_fourier_theorem.tex#L4) – [paper/sections/3_phase_fourier_theorem.tex:L9](paper/sections/3_phase_fourier_theorem.tex#L9) | `707def0dc236f547fae3d9e867c0583da6e2016c484cf8cd96e1bacfd11dcf65` |
| D07 | equation | [paper/sections/3_phase_fourier_theorem.tex:L13](paper/sections/3_phase_fourier_theorem.tex#L13) – [paper/sections/3_phase_fourier_theorem.tex:L18](paper/sections/3_phase_fourier_theorem.tex#L18) | `4b911c26295fb2d5907fd78ab089f00a071d254b754ce99001915601d2dacbc2` |
| D08 | align* | [paper/sections/3_phase_fourier_theorem.tex:L24](paper/sections/3_phase_fourier_theorem.tex#L24) – [paper/sections/3_phase_fourier_theorem.tex:L29](paper/sections/3_phase_fourier_theorem.tex#L29) | `ffbe249be241a232be2e694873e1e567a7740253c6f46c17c776fc1bddd3513e` |
| D09 | equation | [paper/sections/3_phase_fourier_theorem.tex:L31](paper/sections/3_phase_fourier_theorem.tex#L31) – [paper/sections/3_phase_fourier_theorem.tex:L34](paper/sections/3_phase_fourier_theorem.tex#L34) | `d3abc7796d49e47a7402ade125eadd21dfae4d8971aab8a98ec48c1bd08da3f2` |
| D10 | \[...\] | [paper/sections/3_phase_fourier_theorem.tex:L36](paper/sections/3_phase_fourier_theorem.tex#L36) – [paper/sections/3_phase_fourier_theorem.tex:L40](paper/sections/3_phase_fourier_theorem.tex#L40) | `2013eee6d7e83ecb9efc9c253b6d64a4f17d2e74670b44d3af5779059b5ebc19` |
| D11 | \[...\] | [paper/sections/3_phase_fourier_theorem.tex:L52](paper/sections/3_phase_fourier_theorem.tex#L52) – [paper/sections/3_phase_fourier_theorem.tex:L56](paper/sections/3_phase_fourier_theorem.tex#L56) | `760039eb8c551cba5eaf442083b97d4f4b1d09cfb1d616d447baadee413d2db1` |
| D12 | equation | [paper/sections/4_feasible_disk.tex:L9](paper/sections/4_feasible_disk.tex#L9) – [paper/sections/4_feasible_disk.tex:L11](paper/sections/4_feasible_disk.tex#L11) | `78ae288d24f8949acf0f4d38fd9fec62810bccca0d023d25e80124c7f3d51dbd` |
| D13 | \[...\] | [paper/sections/4_feasible_disk.tex:L17](paper/sections/4_feasible_disk.tex#L17) – [paper/sections/4_feasible_disk.tex:L20](paper/sections/4_feasible_disk.tex#L20) | `6352ffac796a85a5670f3f9306d9a1216afeb6160e9b7389ef2b5dc0e4ac0153` |
| D14 | \[...\] | [paper/sections/4_feasible_disk.tex:L25](paper/sections/4_feasible_disk.tex#L25) – [paper/sections/4_feasible_disk.tex:L28](paper/sections/4_feasible_disk.tex#L28) | `15f2be406e2a9628697431685819d957c882bfbb1237d2a8ab7fdf88ef6d08c7` |
| D15 | equation | [paper/sections/4_feasible_disk.tex:L31](paper/sections/4_feasible_disk.tex#L31) – [paper/sections/4_feasible_disk.tex:L34](paper/sections/4_feasible_disk.tex#L34) | `418e7c837741aaa7d1c31cb6896f2733f23ac2909f8aba087961aaaecda3b570` |
| D16 | \[...\] | [paper/sections/4_feasible_disk.tex:L36](paper/sections/4_feasible_disk.tex#L36) – [paper/sections/4_feasible_disk.tex:L41](paper/sections/4_feasible_disk.tex#L41) | `a621c1254f3fdc4bff1b9c835dae29297e8d6d02054db049d9d4cbdf48ce18c9` |
| D17 | equation | [paper/sections/4_feasible_disk.tex:L56](paper/sections/4_feasible_disk.tex#L56) – [paper/sections/4_feasible_disk.tex:L60](paper/sections/4_feasible_disk.tex#L60) | `eeca8c9de8e2c8bf494839c59d5ddf397e1f757ca3d2056d3f78dbc8801c2ece` |
| D18 | \[...\] | [paper/sections/4_feasible_disk.tex:L66](paper/sections/4_feasible_disk.tex#L66) – [paper/sections/4_feasible_disk.tex:L69](paper/sections/4_feasible_disk.tex#L69) | `9a82b065bc00fb0aaaf54b37bc5f149a7c7a9cd9175fd8130830b9a249e24b48` |
| D19 | equation | [paper/sections/5_tpc241_no_transfer.tex:L15](paper/sections/5_tpc241_no_transfer.tex#L15) – [paper/sections/5_tpc241_no_transfer.tex:L19](paper/sections/5_tpc241_no_transfer.tex#L19) | `5b9d988b04f50def021aded138de95f0e84b15da9fdc3254e4441093a298c34a` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/1_introduction.tex:L33](paper/sections/1_introduction.tex#L33): `not a heuristic assertion that an unrelated unsigned term is ''common.''`
- [paper/sections/1_introduction.tex:L38](paper/sections/1_introduction.tex#L38): `standalone common-profile kernel and explicitly does not project the four`
- [paper/sections/1_introduction.tex:L46](paper/sections/1_introduction.tex#L46): `does not imply that the physical top-prime contribution vanishes: survival,`
- [paper/sections/2_v59_source_lock.tex:L30](paper/sections/2_v59_source_lock.tex#L30): `does not identify signed reassembly \cite{WangTPC222}.  TPC-228 performs the`
- [paper/sections/2_v59_source_lock.tex:L32](paper/sections/2_v59_source_lock.tex#L32): `but leaves the literal physical packet-to-primitive-atom crosswalk open`
- [paper/sections/2_v59_source_lock.tex:L50](paper/sections/2_v59_source_lock.tex#L50): `generates the four energies.  It does not manufacture the missing map.`
- [paper/sections/3_phase_fourier_theorem.tex:L67](paper/sections/3_phase_fourier_theorem.tex#L67): `Corollary~\ref{cor:offset} assumes the same scalar is proved to occur inside`
- [paper/sections/3_phase_fourier_theorem.tex:L68](paper/sections/3_phase_fourier_theorem.tex#L68): `each of the four labelled energies.  It does not license the replacement of`
- [paper/sections/5_tpc241_no_transfer.tex:L5](paper/sections/5_tpc241_no_transfer.tex#L5): `finite-window norm of a standalone common-profile synthesis $K_\psi$`
- [paper/sections/5_tpc241_no_transfer.tex:L8](paper/sections/5_tpc241_no_transfer.tex#L8): `scope statement records that it does not use the sign after absolute`
- [paper/sections/5_tpc241_no_transfer.tex:L9](paper/sections/5_tpc241_no_transfer.tex#L9): `squaring and does not project through the four literal packets.`
- [paper/sections/5_tpc241_no_transfer.tex:L37](paper/sections/5_tpc241_no_transfer.tex#L37): `not a numerical loss that can be absorbed into an estimate.`
- [paper/sections/5_tpc241_no_transfer.tex:L40](paper/sections/5_tpc241_no_transfer.tex#L40): `Corollary~\ref{cor:no-transfer} is deliberately scoped.  It does not say that`
- [paper/sections/5_tpc241_no_transfer.tex:L43](paper/sections/5_tpc241_no_transfer.tex#L43): `possibilities remain open until the top-prime contribution is expressed in`
- [paper/sections/6_certificate.tex:L3](paper/sections/6_certificate.tex#L3): `The accompanying executable artifact checks the convention-sensitive finite`
- [paper/sections/6_certificate.tex:L15](paper/sections/6_certificate.tex#L15): `document with duplicate-key and nonfinite-constant rejection and recomputes`
- [paper/sections/6_certificate.tex:L24](paper/sections/6_certificate.tex#L24): `also test duplicate keys and nonfinite constants.`
- [paper/sections/6_certificate.tex:L31](paper/sections/6_certificate.tex#L31): `\texttt{NUMERICAL\_FINITE\_ILLUSTRATION\_ONLY}.`
- [paper/sections/6_certificate.tex:L33](paper/sections/6_certificate.tex#L33): `The executable artifacts test transcription, representation, and finite`
- [paper/sections/6_certificate.tex:L35](paper/sections/6_certificate.tex#L35): `and~\ref{sec:disk}, rather than the finite census, establish the theorem.`
- [paper/sections/7_route_boundary.tex:L18](paper/sections/7_route_boundary.tex#L18): `TPC-241-to-V59 physical identification & Open \\`
- [paper/sections/7_route_boundary.tex:L24](paper/sections/7_route_boundary.tex#L24): `Full Gate B & Open \\`
- [paper/sections/8_conclusion.tex:L18](paper/sections/8_conclusion.tex#L18): `the twin-prime objective all remain open.`
- [paper/sections/A_status_ledger.tex:L29](paper/sections/A_status_ledger.tex#L29): `\noindent\path{TPC242_TPC241_TO_V59_IDENTIFICATION=OPEN}\par`
- [paper/sections/A_status_ledger.tex:L35](paper/sections/A_status_ledger.tex#L35): `\noindent\path{TPC242_FULL_GATE_B=OPEN}\par`
- [paper/sections/A_status_ledger.tex:L43](paper/sections/A_status_ledger.tex#L43): `does not identify any physical top-prime V59 marginal.`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 7 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#sec:source-lock` → `sections/2_v59_source_lock.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:spectrum` → `sections/3_phase_fourier_theorem.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:disk` → `sections/4_feasible_disk.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:no-transfer` → `sections/5_tpc241_no_transfer.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:certificate` → `sections/6_certificate.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:boundary` → `sections/7_route_boundary.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#eq:known-polarization` → `sections/1_introduction.tex#L13` (existing project target or original TeX label line).
- Link relocation: `#eq:def-energy-dft` → `sections/3_phase_fourier_theorem.tex#L4` (existing project target or original TeX label line).
- Link relocation: `#eq:complete-spectrum` → `sections/3_phase_fourier_theorem.tex#L13` (existing project target or original TeX label line).
- Link relocation: `#eq:root-filter` → `sections/3_phase_fourier_theorem.tex#L31` (existing project target or original TeX label line).
- Link relocation: `#cor:offset` → `sections/3_phase_fourier_theorem.tex#L49` (existing project target or original TeX label line).
- Link relocation: `#eq:disk` → `sections/4_feasible_disk.tex#L9` (existing project target or original TeX label line).
- Link relocation: `#eq:defect` → `sections/4_feasible_disk.tex#L56` (existing project target or original TeX label line).
- Link relocation: `#thm:spectrum` → `sections/3_phase_fourier_theorem.tex#L11` (existing project target or original TeX label line).
- Link relocation: `#eq:missing-maps` → `sections/5_tpc241_no_transfer.tex#L15` (existing project target or original TeX label line).
- Link relocation: `#thm:disk` → `sections/4_feasible_disk.tex#L5` (existing project target or original TeX label line).
- Link relocation: `#cor:offset` → `sections/3_phase_fourier_theorem.tex#L49` (existing project target or original TeX label line).
- Link relocation: `#cor:no-transfer` → `sections/5_tpc241_no_transfer.tex#L24` (existing project target or original TeX label line).
- Link relocation: `#sec:spectrum` → `sections/3_phase_fourier_theorem.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#sec:disk` → `sections/4_feasible_disk.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#tab:ledger` → `sections/7_route_boundary.tex#L29` (existing project target or original TeX label line).
