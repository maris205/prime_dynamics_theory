# TPC-237 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `d0cff31560f106f1762a8acc0e9b9cdecd461c860b0e4545bf30095905a7778c`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `7ddabf63118cced5acb0b6b499b6fe2a714c76c2c9028c88f8c863423d6c4b06`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `437d7088cc492469b6b01479c19b1fb7fec39e7eced8e13e6434210f31ae83a5`; 6 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `d76dd2e0b3cee8872cc65a6364595c06215a3b1285bb5d3e247d2bbfb3b84a43`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC235_239.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 10 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `d0cff31560f106f1762a8acc0e9b9cdecd461c860b0e4545bf30095905a7778c` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `69f5ea32632feae514055e5cad77def3da67060e5081ff2e69d8b1ae8e4846cd` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `5a7720765ade0ff5dff68b3a5321430ac013a7fa61c52eda691070340499d523` |
| [paper/sections/2_source.tex](paper/sections/2_source.tex) | `6f078f2e8316e9911b0722d4846fbca2b825756e0c22908cbfe83ceaaca15a7a` |
| [paper/sections/3_collision_compression.tex](paper/sections/3_collision_compression.tex) | `9be604414343e2482016ba9f001927fb140a4362b47506bb149136f3313019fd` |
| [paper/sections/4_finite_window.tex](paper/sections/4_finite_window.tex) | `59b53038353fb8366403bda3a891ef5e379a0bf0df276a32aeb63edb782b9869` |
| [paper/sections/5_exponent_ledger.tex](paper/sections/5_exponent_ledger.tex) | `01b37ef6d047838629d25ebaf548af214004ea8d8aef85cdce09afd65d7c81c9` |
| [paper/sections/6_certificate.tex](paper/sections/6_certificate.tex) | `f4b68bddb7b8df95fdd29d87ba25dc9bf9a494bdfce27b8f737c8db6bde01916` |
| [paper/sections/7_conclusion.tex](paper/sections/7_conclusion.tex) | `8ce3b3d44b5084647b5d72a7d84338fbbd30dedd13d45c7e726c159d935f4de4` |
| [paper/sections/8_declarations.tex](paper/sections/8_declarations.tex) | `0b056f90627d1f5d6a02a2c4f552830776f44d94d5ea8b813adea1b97a0b3478` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L33](paper/main.tex#L33) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L34](paper/main.tex#L34) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L35](paper/main.tex#L35) | `\input{sections/2_source}` | [paper/sections/2_source.tex](paper/sections/2_source.tex) |
| [paper/main.tex:L36](paper/main.tex#L36) | `\input{sections/3_collision_compression}` | [paper/sections/3_collision_compression.tex](paper/sections/3_collision_compression.tex) |
| [paper/main.tex:L37](paper/main.tex#L37) | `\input{sections/4_finite_window}` | [paper/sections/4_finite_window.tex](paper/sections/4_finite_window.tex) |
| [paper/main.tex:L38](paper/main.tex#L38) | `\input{sections/5_exponent_ledger}` | [paper/sections/5_exponent_ledger.tex](paper/sections/5_exponent_ledger.tex) |
| [paper/main.tex:L39](paper/main.tex#L39) | `\input{sections/6_certificate}` | [paper/sections/6_certificate.tex](paper/sections/6_certificate.tex) |
| [paper/main.tex:L40](paper/main.tex#L40) | `\input{sections/7_conclusion}` | [paper/sections/7_conclusion.tex](paper/sections/7_conclusion.tex) |
| [paper/main.tex:L41](paper/main.tex#L41) | `\input{sections/8_declarations}` | [paper/sections/8_declarations.tex](paper/sections/8_declarations.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Frozen common-source object` | [paper/sections/2_source.tex:L1](paper/sections/2_source.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Prime-shell collision compression` | [paper/sections/3_collision_compression.tex:L1](paper/sections/3_collision_compression.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Finite-window theorem` | [paper/sections/4_finite_window.tex:L1](paper/sections/4_finite_window.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `V59 exponent ledger and method boundary` | [paper/sections/5_exponent_ledger.tex:L1](paper/sections/5_exponent_ledger.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Independent finite reproduction` | [paper/sections/6_certificate.tex:L1](paper/sections/6_certificate.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/7_conclusion.tex:L1](paper/sections/7_conclusion.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Reproducibility and declarations` | [paper/sections/8_declarations.tex:L1](paper/sections/8_declarations.tex#L1) | 6 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | [paper/main.tex:L43](paper/main.tex#L43) | 6 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `127` before writing and `127` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `24`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `7fee6cdfb04db0cbbdcd8af082273a44dfdf013b05f0b087a7b353ba6d158dfe`.
- Source theorem/proof environment starts: lemma at [paper/sections/3_collision_compression.tex:L8](paper/sections/3_collision_compression.tex#L8), proof at [paper/sections/3_collision_compression.tex:L24](paper/sections/3_collision_compression.tex#L24), lemma at [paper/sections/3_collision_compression.tex:L34](paper/sections/3_collision_compression.tex#L34), proof at [paper/sections/3_collision_compression.tex:L42](paper/sections/3_collision_compression.tex#L42), lemma at [paper/sections/4_finite_window.tex:L11](paper/sections/4_finite_window.tex#L11), proof at [paper/sections/4_finite_window.tex:L16](paper/sections/4_finite_window.tex#L16), theorem at [paper/sections/4_finite_window.tex:L22](paper/sections/4_finite_window.tex#L22), proof at [paper/sections/4_finite_window.tex:L34](paper/sections/4_finite_window.tex#L34).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/0_abstract.tex:L7](paper/sections/0_abstract.tex#L7) – [paper/sections/0_abstract.tex:L9](paper/sections/0_abstract.tex#L9) | `1705c25f65924774c2bf63e7d9c4d61a280f08be244629e8d0ce9e2980c93b05` |
| D02 | \[...\] | [paper/sections/0_abstract.tex:L13](paper/sections/0_abstract.tex#L13) – [paper/sections/0_abstract.tex:L16](paper/sections/0_abstract.tex#L16) | `adde44e53b9a34c654519d67267e87b023e445cb62cc8ef61d054607ba97d473` |
| D03 | \[...\] | [paper/sections/1_introduction.tex:L12](paper/sections/1_introduction.tex#L12) – [paper/sections/1_introduction.tex:L14](paper/sections/1_introduction.tex#L14) | `9e5e6797c1b65afc997d470387974a1f4d3375982e944f058893b9fe04d93ce2` |
| D04 | equation | [paper/sections/2_source.tex:L4](paper/sections/2_source.tex#L4) – [paper/sections/2_source.tex:L7](paper/sections/2_source.tex#L7) | `b7220e93647432436df511d8f7749c8929d579c2d291d104612bb827c519460c` |
| D05 | align | [paper/sections/2_source.tex:L9](paper/sections/2_source.tex#L9) – [paper/sections/2_source.tex:L14](paper/sections/2_source.tex#L14) | `2b7d9199f1d0dea94b0bcd392ce8b267e1a94033002fb9b39c0b503d08b5b0a7` |
| D06 | equation | [paper/sections/2_source.tex:L17](paper/sections/2_source.tex#L17) – [paper/sections/2_source.tex:L22](paper/sections/2_source.tex#L22) | `c62140d12bb6dedd686fe446b48f7bb77aa11f5f80077ae9e7c68b2dafe334cf` |
| D07 | equation | [paper/sections/2_source.tex:L24](paper/sections/2_source.tex#L24) – [paper/sections/2_source.tex:L29](paper/sections/2_source.tex#L29) | `7902da00e76d080b2597077bf5f52f8fe12aa7784bf5033777430e5ef794dc0c` |
| D08 | equation | [paper/sections/3_collision_compression.tex:L10](paper/sections/3_collision_compression.tex#L10) – [paper/sections/3_collision_compression.tex:L13](paper/sections/3_collision_compression.tex#L13) | `19d890e15f139e8b4337ea90e0dc6bad73f84b69a5b1cce9c3c4bc2cf4514a0d` |
| D09 | equation | [paper/sections/3_collision_compression.tex:L15](paper/sections/3_collision_compression.tex#L15) – [paper/sections/3_collision_compression.tex:L20](paper/sections/3_collision_compression.tex#L20) | `67c99839d29b7b8c89e05b53e4df847859cc034565cca8cb0cecfcdca5192f41` |
| D10 | equation | [paper/sections/3_collision_compression.tex:L36](paper/sections/3_collision_compression.tex#L36) – [paper/sections/3_collision_compression.tex:L39](paper/sections/3_collision_compression.tex#L39) | `544e5e0b642d2545f1a7a8264b73c0d71f37ef35931c32b6407e4c126bb40e0b` |
| D11 | \[...\] | [paper/sections/3_collision_compression.tex:L45](paper/sections/3_collision_compression.tex#L45) – [paper/sections/3_collision_compression.tex:L48](paper/sections/3_collision_compression.tex#L48) | `aea835fb459da2ae9b9bfe19bf7eda17096c0dbf34fc3f0558b662e9c6ab743e` |
| D12 | \[...\] | [paper/sections/3_collision_compression.tex:L51](paper/sections/3_collision_compression.tex#L51) – [paper/sections/3_collision_compression.tex:L54](paper/sections/3_collision_compression.tex#L54) | `b77865bf59064445ab50b41afc4bcf4adb3a710705220fb1319aa6157be3cde4` |
| D13 | \[...\] | [paper/sections/3_collision_compression.tex:L56](paper/sections/3_collision_compression.tex#L56) – [paper/sections/3_collision_compression.tex:L60](paper/sections/3_collision_compression.tex#L60) | `8fc7655e8f67ecd592d3ff50f3b2c65b4b5703f057f1bf869dd359a1b7905b1b` |
| D14 | equation | [paper/sections/4_finite_window.tex:L6](paper/sections/4_finite_window.tex#L6) – [paper/sections/4_finite_window.tex:L9](paper/sections/4_finite_window.tex#L9) | `2a9aeed1a6033f6a775e2e2305dd46f11d956c8356b8db8fdd4dc2f50b6c36dc` |
| D15 | align | [paper/sections/4_finite_window.tex:L25](paper/sections/4_finite_window.tex#L25) – [paper/sections/4_finite_window.tex:L31](paper/sections/4_finite_window.tex#L31) | `c39271058b05f7cb4dd43fb27103de17966e0b32877fb957fc57e4eb062f93d0` |
| D16 | \[...\] | [paper/sections/4_finite_window.tex:L36](paper/sections/4_finite_window.tex#L36) – [paper/sections/4_finite_window.tex:L38](paper/sections/4_finite_window.tex#L38) | `72c21c221851c7145a2a2c920ef22a5e84e3ecfc6195a83d4acb2ab78ad9ffa0` |
| D17 | align | [paper/sections/5_exponent_ledger.tex:L4](paper/sections/5_exponent_ledger.tex#L4) – [paper/sections/5_exponent_ledger.tex:L10](paper/sections/5_exponent_ledger.tex#L10) | `e79cb389b4437d19aded5202cd9ca700b41c8c7a02e3b5335594e7791863f84b` |
| D18 | equation | [paper/sections/5_exponent_ledger.tex:L12](paper/sections/5_exponent_ledger.tex#L12) – [paper/sections/5_exponent_ledger.tex:L16](paper/sections/5_exponent_ledger.tex#L16) | `569480378e0261b89f491835007627e846be6a78da0c85a5bb40c31de8e4753e` |
| D19 | \[...\] | [paper/sections/5_exponent_ledger.tex:L37](paper/sections/5_exponent_ledger.tex#L37) – [paper/sections/5_exponent_ledger.tex:L40](paper/sections/5_exponent_ledger.tex#L40) | `ae224edb58161d984bb87c16cd653c66cfa8058be2869a5104aeab5b2a2a0f1e` |
| D20 | \[...\] | [paper/sections/6_certificate.tex:L4](paper/sections/6_certificate.tex#L4) – [paper/sections/6_certificate.tex:L6](paper/sections/6_certificate.tex#L6) | `bd4f0aee5e3db089bc6c0691fe1c4355e21982630e6eb819985e2f63103cd69c` |
| D21 | \[...\] | [paper/sections/6_certificate.tex:L8](paper/sections/6_certificate.tex#L8) – [paper/sections/6_certificate.tex:L11](paper/sections/6_certificate.tex#L11) | `da939094931358aaa97ee356d606762b3f69686bd016453747ce8af13eff8f86` |
| D22 | \[...\] | [paper/sections/6_certificate.tex:L15](paper/sections/6_certificate.tex#L15) – [paper/sections/6_certificate.tex:L17](paper/sections/6_certificate.tex#L17) | `299058678e05999fc14d4f62343efff1b22121723b0b68ffb9b83debfbde4341` |
| D23 | \[...\] | [paper/sections/6_certificate.tex:L23](paper/sections/6_certificate.tex#L23) – [paper/sections/6_certificate.tex:L27](paper/sections/6_certificate.tex#L27) | `7184fd93e5e0a5377da4b0b3bd6aa5b44e5362a643a35da7d53f9db225fc8974` |
| D24 | \[...\] | [paper/sections/7_conclusion.tex:L14](paper/sections/7_conclusion.tex#L14) – [paper/sections/7_conclusion.tex:L17](paper/sections/7_conclusion.tex#L17) | `698c055185c3663b5db5eec7f861668e0873ca65458de10fabbf9623409a8f90` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/main.tex:L25](paper/main.tex#L25): `\title{\textbf{Collision-Compressed Prime-Shell Reassembly on Finite Windows}}`
- [paper/sections/0_abstract.tex:L2](paper/sections/0_abstract.tex#L2): `We prove a collision-compressed finite-window envelope for the exact TPC-218`
- [paper/sections/0_abstract.tex:L6](paper/sections/0_abstract.tex#L6): `large sieve.  The TPC-236 incidence theorem gives the uniform bucket factor`
- [paper/sections/0_abstract.tex:L18](paper/sections/0_abstract.tex#L18): `$U^2/|I_x|=x^{-67/200+o(1)}$ makes the finite-window correction lower order.`
- [paper/sections/0_abstract.tex:L27](paper/sections/0_abstract.tex#L27): `collision-compressed finite-window packet trace.`
- [paper/sections/1_introduction.tex:L3](paper/sections/1_introduction.tex#L3): `The common-source finite-window kernel retains two outer labels that should not be`
- [paper/sections/1_introduction.tex:L15](paper/sections/1_introduction.tex#L15): `prime rows \citep{WangTPC236}.  The finite-window kernel already uses reduced`
- [paper/sections/1_introduction.tex:L24](paper/sections/1_introduction.tex#L24): `the finite-window attachment of TPC-217 applies without changing the physical object`
- [paper/sections/1_introduction.tex:L33](paper/sections/1_introduction.tex#L33): `\item an exact exponent ledger and an independently checked source-active finite`
- [paper/sections/1_introduction.tex:L36](paper/sections/1_introduction.tex#L36): `Every step is unsigned.  In particular, the theorem does not convert the packet trace`
- [paper/sections/1_introduction.tex:L37](paper/sections/1_introduction.tex#L37): `into the signed four-packet Gate-B scalar and does not exploit signs of $C_h$.`
- [paper/sections/3_collision_compression.tex:L4](paper/sections/3_collision_compression.tex#L4): `$B_{h,q}^{(j)}(a)$ can be nonzero.  TPC-236 proves its gcd-fiber bound uniformly in`
- [paper/sections/4_finite_window.tex:L1](paper/sections/4_finite_window.tex#L1): `\section{Finite-window theorem}`
- [paper/sections/4_finite_window.tex:L22](paper/sections/4_finite_window.tex#L22): `\begin{theorem}[Collision-compressed finite-window reassembly]`
- [paper/sections/4_finite_window.tex:L23](paper/sections/4_finite_window.tex#L23): `\label{thm:finite-window}`
- [paper/sections/4_finite_window.tex:L46](paper/sections/4_finite_window.tex#L46): `occupancy replaces $P$ before the finite-window Gram is diagonalized.`
- [paper/sections/5_exponent_ledger.tex:L26](paper/sections/5_exponent_ledger.tex#L26): `Theorem~\ref{thm:finite-window} & $1/48$ (main) & primitive physical occupancy \\`
- [paper/sections/5_exponent_ledger.tex:L31](paper/sections/5_exponent_ledger.tex#L31): `The comparison records a structural upper bound, not a sharp asymptotic.  The proof`
- [paper/sections/5_exponent_ledger.tex:L41](paper/sections/5_exponent_ledger.tex#L41): `No arithmetic $L^2$, fixed-atom credit, strict $1/400$ payment, full Gate B, or`
- [paper/sections/6_certificate.tex:L1](paper/sections/6_certificate.tex#L1): `\section{Independent finite reproduction}`
- [paper/sections/6_certificate.tex:L18](paper/sections/6_certificate.tex#L18): `The replacement of $\log d$ by $1$ makes the finite ledger rational; it is not used in`
- [paper/sections/6_certificate.tex:L40](paper/sections/6_certificate.tex#L40): `Finite agreement certifies the implementation and displayed algebra only.`
- [paper/sections/7_conclusion.tex:L3](paper/sections/7_conclusion.tex#L3): `Physical collision compression can be performed before reduced-frequency finite-window`
- [paper/sections/7_conclusion.tex:L11](paper/sections/7_conclusion.tex#L11): `\eqref{eq:collision-bessel} uses only a uniform occupancy maximum, while`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:kernel` → `sections/2_source.tex#L28` (existing project target or original TeX label line).
- Link relocation: `#eq:kernel` → `sections/2_source.tex#L28` (existing project target or original TeX label line).
- Link relocation: `#eq:Rstar` → `sections/3_collision_compression.tex#L12` (existing project target or original TeX label line).
- Link relocation: `#eq:collision-bessel` → `sections/3_collision_compression.tex#L19` (existing project target or original TeX label line).
- Link relocation: `#eq:collision-bessel` → `sections/3_collision_compression.tex#L19` (existing project target or original TeX label line).
- Link relocation: `#eq:scales` → `sections/2_source.tex#L6` (existing project target or original TeX label line).
- Link relocation: `#eq:row` → `sections/2_source.tex#L21` (existing project target or original TeX label line).
- Link relocation: `#eq:Ch` → `sections/2_source.tex#L13` (existing project target or original TeX label line).
- Link relocation: `#eq:direct-energy` → `sections/3_collision_compression.tex#L38` (existing project target or original TeX label line).
- Link relocation: `#eq:large-sieve` → `sections/4_finite_window.tex#L8` (existing project target or original TeX label line).
- Link relocation: `#lem:spacing` → `sections/4_finite_window.tex#L11` (existing project target or original TeX label line).
- Link relocation: `#lem:collision` → `sections/3_collision_compression.tex#L8` (existing project target or original TeX label line).
- Link relocation: `#eq:exact-chain` → `sections/4_finite_window.tex#L28` (existing project target or original TeX label line).
- Link relocation: `#lem:direct` → `sections/3_collision_compression.tex#L34` (existing project target or original TeX label line).
- Link relocation: `#eq:source-chain` → `sections/4_finite_window.tex#L30` (existing project target or original TeX label line).
- Link relocation: `#eq:source-chain` → `sections/4_finite_window.tex#L30` (existing project target or original TeX label line).
- Link relocation: `#thm:finite-window` → `sections/4_finite_window.tex#L23` (existing project target or original TeX label line).
- Link relocation: `#eq:main-result` → `sections/5_exponent_ledger.tex#L15` (existing project target or original TeX label line).
- Link relocation: `#eq:collision-bessel` → `sections/3_collision_compression.tex#L19` (existing project target or original TeX label line).
- Link relocation: `#lem:direct` → `sections/3_collision_compression.tex#L34` (existing project target or original TeX label line).
