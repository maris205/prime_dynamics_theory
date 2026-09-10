# TPC-238 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `20fea45dbfdcde663a81968c885d37d2982a2f2bd652df65a7bb76375dbad5ae`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `43499360092552165c5c7343ad438a2588cffaec517fec7040d8343c3666a2dc`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `4ba2f92970804bdda61bd5ab239107975b001950f8d2e3c2a276f5786051303b`; 7 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `ce6ff057fd0efdcc159abc5ba9af7ecf706ac8be9f20223b12a8ccb8d8c7b453`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC235_239.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 10 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `20fea45dbfdcde663a81968c885d37d2982a2f2bd652df65a7bb76375dbad5ae` |
| [paper/math_commands.tex](paper/math_commands.tex) | `50176b15bc1346e3ce12413d13aaa62dfc7aa581d72873076d11689c0acce820` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `08b9fd94ef44e3c5f9b1717fc223a8691c078e228af0e7f9a7933065f16988a2` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `299d06389db9fc5a6c355e6be4182d1d6eda0472fe0741b24b84de7b70334918` |
| [paper/sections/2_setup.tex](paper/sections/2_setup.tex) | `1f2677267c6c18cc03ae2b6c6a3ecf317e61480443a3e044d7d7160814f9406f` |
| [paper/sections/3_lower_frame.tex](paper/sections/3_lower_frame.tex) | `1099661935347fcb8dcebe1e6540ac5e19a9f441565ff8da72b0c47286da773e` |
| [paper/sections/4_route_consequence.tex](paper/sections/4_route_consequence.tex) | `9f7fd7654000eafa5b8470fa286bcc31e4ecc30f1a13cd77bb81fe95d86c8751` |
| [paper/sections/5_finite_audit.tex](paper/sections/5_finite_audit.tex) | `f0a45fab5a16ae8d21693a21131527158e541e28aae032b60376b2d40f7db8e2` |
| [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) | `da0d73421c34b6662e1fe8f4902a56dd3564c07c75d14a6fb8f4ca5b57ea4a99` |
| [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) | `feeea490651687b51f3a21276a7ccae284fdfa3ee543e691660bf0097befdd81` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L22](paper/main.tex#L22) | `\input{math_commands}` | [paper/math_commands.tex](paper/math_commands.tex) |
| [paper/main.tex:L44](paper/main.tex#L44) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L47](paper/main.tex#L47) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L48](paper/main.tex#L48) | `\input{sections/2_setup}` | [paper/sections/2_setup.tex](paper/sections/2_setup.tex) |
| [paper/main.tex:L49](paper/main.tex#L49) | `\input{sections/3_lower_frame}` | [paper/sections/3_lower_frame.tex](paper/sections/3_lower_frame.tex) |
| [paper/main.tex:L50](paper/main.tex#L50) | `\input{sections/4_route_consequence}` | [paper/sections/4_route_consequence.tex](paper/sections/4_route_consequence.tex) |
| [paper/main.tex:L51](paper/main.tex#L51) | `\input{sections/5_finite_audit}` | [paper/sections/5_finite_audit.tex](paper/sections/5_finite_audit.tex) |
| [paper/main.tex:L52](paper/main.tex#L52) | `\input{sections/6_conclusion}` | [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) |
| [paper/main.tex:L53](paper/main.tex#L53) | `\input{sections/A_status_ledger}` | [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Finite-window setup` | [paper/sections/2_setup.tex:L1](paper/sections/2_setup.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Triangular-window proof` | [paper/sections/3_lower_frame.tex:L1](paper/sections/3_lower_frame.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `The exact Fejér Gram matrix` | [paper/sections/3_lower_frame.tex:L4](paper/sections/3_lower_frame.tex#L4) | 3 | `HEADING_TEXT_MATCH` |
| `Spacing and packing` | [paper/sections/3_lower_frame.tex:L41](paper/sections/3_lower_frame.tex#L41) | 3 | `HEADING_TEXT_MATCH` |
| `Spectral conclusion` | [paper/sections/3_lower_frame.tex:L102](paper/sections/3_lower_frame.tex#L102) | 4 | `HEADING_TEXT_MATCH` |
| `Route consequence and claim firewall` | [paper/sections/4_route_consequence.tex:L1](paper/sections/4_route_consequence.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Finite certificate and independent audit` | [paper/sections/5_finite_audit.tex:L1](paper/sections/5_finite_audit.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Exact fixture` | [paper/sections/5_finite_audit.tex:L8](paper/sections/5_finite_audit.tex#L8) | 6 | `HEADING_TEXT_MATCH` |
| `Independent implementation and stress` | [paper/sections/5_finite_audit.tex:L51](paper/sections/5_finite_audit.tex#L51) | 6 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/6_conclusion.tex:L1](paper/sections/6_conclusion.tex#L1) | 6 | `HEADING_TEXT_MATCH` |
| `Status ledger and reproduction markers` | [paper/sections/A_status_ledger.tex:L2](paper/sections/A_status_ledger.tex#L2) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `References (external bibliography)` | [paper/main.tex:L56](paper/main.tex#L56) | 7 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `154` before writing and `154` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `34`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `7fae7cadf4ae1230877bbfa83b37f899c3d24e894d8bb5a43d6c6e8c6a626a52`.
- Source theorem/proof environment starts: theorem at [paper/sections/2_setup.tex:L28](paper/sections/2_setup.tex#L28), corollary at [paper/sections/2_setup.tex:L38](paper/sections/2_setup.tex#L38), corollary at [paper/sections/2_setup.tex:L47](paper/sections/2_setup.tex#L47), lemma at [paper/sections/3_lower_frame.tex:L6](paper/sections/3_lower_frame.tex#L6), proof at [paper/sections/3_lower_frame.tex:L25](paper/sections/3_lower_frame.tex#L25), lemma at [paper/sections/3_lower_frame.tex:L43](paper/sections/3_lower_frame.tex#L43), proof at [paper/sections/3_lower_frame.tex:L52](paper/sections/3_lower_frame.tex#L52), lemma at [paper/sections/3_lower_frame.tex:L61](paper/sections/3_lower_frame.tex#L61), proof at [paper/sections/3_lower_frame.tex:L69](paper/sections/3_lower_frame.tex#L69), lemma at [paper/sections/3_lower_frame.tex:L80](paper/sections/3_lower_frame.tex#L80), proof at [paper/sections/3_lower_frame.tex:L90](paper/sections/3_lower_frame.tex#L90), proof at [paper/sections/3_lower_frame.tex:L104](paper/sections/3_lower_frame.tex#L104), proof at [paper/sections/3_lower_frame.tex:L136](paper/sections/3_lower_frame.tex#L136), proof at [paper/sections/3_lower_frame.tex:L145](paper/sections/3_lower_frame.tex#L145), proposition at [paper/sections/4_route_consequence.tex:L33](paper/sections/4_route_consequence.tex#L33), proof at [paper/sections/4_route_consequence.tex:L41](paper/sections/4_route_consequence.tex#L41).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/0_abstract.tex:L7](paper/sections/0_abstract.tex#L7) – [paper/sections/0_abstract.tex:L11](paper/sections/0_abstract.tex#L11) | `098615c1e7942dc49c7a40120c0f69d9ccefd2b6cbbdff812afc7a430df1b278` |
| D02 | \[...\] | [paper/sections/1_introduction.tex:L23](paper/sections/1_introduction.tex#L23) – [paper/sections/1_introduction.tex:L26](paper/sections/1_introduction.tex#L26) | `65bb25eedbb76ed601af6919b81b6381674578bd20aa17a0821afd9853bed39d` |
| D03 | \[...\] | [paper/sections/1_introduction.tex:L28](paper/sections/1_introduction.tex#L28) – [paper/sections/1_introduction.tex:L31](paper/sections/1_introduction.tex#L31) | `0b02914341f49829284d175a5ffd3fafb9d03fec3003b68d21695f95b2397b9d` |
| D04 | \[...\] | [paper/sections/2_setup.tex:L8](paper/sections/2_setup.tex#L8) – [paper/sections/2_setup.tex:L10](paper/sections/2_setup.tex#L10) | `efae5c2877ad4cbc65599b8b6bb96700cb9ac4eb58c8471466a1c98ae780195a` |
| D05 | \[...\] | [paper/sections/2_setup.tex:L16](paper/sections/2_setup.tex#L16) – [paper/sections/2_setup.tex:L19](paper/sections/2_setup.tex#L19) | `063aa362118ddcfed88a2d91dab5933d5b40c4b45e898fe08183c55b208d0dad` |
| D06 | \[...\] | [paper/sections/2_setup.tex:L21](paper/sections/2_setup.tex#L21) – [paper/sections/2_setup.tex:L24](paper/sections/2_setup.tex#L24) | `0c287504330dc058c19f4ec2bc79befe2114ee14a11d28af01b15d1dce7c6870` |
| D07 | \[...\] | [paper/sections/2_setup.tex:L32](paper/sections/2_setup.tex#L32) – [paper/sections/2_setup.tex:L35](paper/sections/2_setup.tex#L35) | `65bb25eedbb76ed601af6919b81b6381674578bd20aa17a0821afd9853bed39d` |
| D08 | \[...\] | [paper/sections/2_setup.tex:L41](paper/sections/2_setup.tex#L41) – [paper/sections/2_setup.tex:L44](paper/sections/2_setup.tex#L44) | `ea0cd37a9a023f708a41269b76b1c7174187c7039e90a96b8819cb9bea7c8b88` |
| D09 | \[...\] | [paper/sections/2_setup.tex:L50](paper/sections/2_setup.tex#L50) – [paper/sections/2_setup.tex:L52](paper/sections/2_setup.tex#L52) | `8713930bc8d9b93e3dc751777d80392cd5a5b50f07b1efaa5565dff44f033dc6` |
| D10 | \[...\] | [paper/sections/3_lower_frame.tex:L9](paper/sections/3_lower_frame.tex#L9) – [paper/sections/3_lower_frame.tex:L15](paper/sections/3_lower_frame.tex#L15) | `eeafa4436cc4d6aa54f2d0dcfb6cdd8eaf1639811edc61c2fe163add8df95e9a` |
| D11 | \[...\] | [paper/sections/3_lower_frame.tex:L17](paper/sections/3_lower_frame.tex#L17) – [paper/sections/3_lower_frame.tex:L21](paper/sections/3_lower_frame.tex#L21) | `16e168abfd89764272f86b83b9b73a05ee5a068941798219b88f933904adcc8e` |
| D12 | \[...\] | [paper/sections/3_lower_frame.tex:L30](paper/sections/3_lower_frame.tex#L30) – [paper/sections/3_lower_frame.tex:L33](paper/sections/3_lower_frame.tex#L33) | `21b82f792cc3149566c3d2fd01138e79e262ee68ffae1fd78c335e0062e61c6d` |
| D13 | \[...\] | [paper/sections/3_lower_frame.tex:L47](paper/sections/3_lower_frame.tex#L47) – [paper/sections/3_lower_frame.tex:L49](paper/sections/3_lower_frame.tex#L49) | `c2331dca8eaa872df6a3a164eb5a6908e6d93cb9f8006f20a14d112b2fdfa5bc` |
| D14 | \[...\] | [paper/sections/3_lower_frame.tex:L55](paper/sections/3_lower_frame.tex#L55) – [paper/sections/3_lower_frame.tex:L58](paper/sections/3_lower_frame.tex#L58) | `07432b13b8e992fce6107dce3f924fcf249b324ea7ad761517eb38501b936567` |
| D15 | \[...\] | [paper/sections/3_lower_frame.tex:L64](paper/sections/3_lower_frame.tex#L64) – [paper/sections/3_lower_frame.tex:L66](paper/sections/3_lower_frame.tex#L66) | `caf9595c27b165219d4bb061edd95a4b6a0113ea0a89f5cf86a08fe136512398` |
| D16 | \[...\] | [paper/sections/3_lower_frame.tex:L71](paper/sections/3_lower_frame.tex#L71) – [paper/sections/3_lower_frame.tex:L75](paper/sections/3_lower_frame.tex#L75) | `c0d2a0fec980c0caca5a6f6a6a475936c50733d2e72a1f843b4125e3e2179560` |
| D17 | \[...\] | [paper/sections/3_lower_frame.tex:L84](paper/sections/3_lower_frame.tex#L84) – [paper/sections/3_lower_frame.tex:L87](paper/sections/3_lower_frame.tex#L87) | `b7bbf8878042c4368cb61264f6df792838bfa1ea1e700e1f9101431929e4a3d7` |
| D18 | \[...\] | [paper/sections/3_lower_frame.tex:L95](paper/sections/3_lower_frame.tex#L95) – [paper/sections/3_lower_frame.tex:L99](paper/sections/3_lower_frame.tex#L99) | `ae2c0265da89d1ba1613277bf81d49d191a152dfb1cc2ade158578214b6b5bc8` |
| D19 | \[...\] | [paper/sections/3_lower_frame.tex:L106](paper/sections/3_lower_frame.tex#L106) – [paper/sections/3_lower_frame.tex:L110](paper/sections/3_lower_frame.tex#L110) | `4d29d4e7aba71fdeb238b2bcb86935ce4413ff15ad1a31531a100aa8b6402520` |
| D20 | \[...\] | [paper/sections/3_lower_frame.tex:L112](paper/sections/3_lower_frame.tex#L112) – [paper/sections/3_lower_frame.tex:L115](paper/sections/3_lower_frame.tex#L115) | `54236e7f220541c0319aebf458461d73bfabe5f0df936e8016384667a9cd4dc8` |
| D21 | \[...\] | [paper/sections/3_lower_frame.tex:L121](paper/sections/3_lower_frame.tex#L121) – [paper/sections/3_lower_frame.tex:L126](paper/sections/3_lower_frame.tex#L126) | `34a241cf0d849761479b26fdb75e29b796a8d63d68c45a337a87583015e76152` |
| D22 | \[...\] | [paper/sections/3_lower_frame.tex:L128](paper/sections/3_lower_frame.tex#L128) – [paper/sections/3_lower_frame.tex:L131](paper/sections/3_lower_frame.tex#L131) | `7cbe4a798c2416f5c97e44fa85b9bd1e0644584f8f7eb191b712645b18385426` |
| D23 | \[...\] | [paper/sections/3_lower_frame.tex:L138](paper/sections/3_lower_frame.tex#L138) – [paper/sections/3_lower_frame.tex:L141](paper/sections/3_lower_frame.tex#L141) | `f2dd86b4d7f5a1a582a3c98d9b387776d63dc39945071cd3aaa3699ace1d76f2` |
| D24 | \[...\] | [paper/sections/3_lower_frame.tex:L147](paper/sections/3_lower_frame.tex#L147) – [paper/sections/3_lower_frame.tex:L151](paper/sections/3_lower_frame.tex#L151) | `881d1b7215fa99ec9ef1d6df7b0daf0802685f32628037a3b02db4bf446cf1c9` |
| D25 | \[...\] | [paper/sections/4_route_consequence.tex:L6](paper/sections/4_route_consequence.tex#L6) – [paper/sections/4_route_consequence.tex:L8](paper/sections/4_route_consequence.tex#L8) | `64d7c98dfd333fbcbe777b6bb62b6827f795bbd7f22dad05e6c65fd20e8837c9` |
| D26 | \[...\] | [paper/sections/4_route_consequence.tex:L11](paper/sections/4_route_consequence.tex#L11) – [paper/sections/4_route_consequence.tex:L13](paper/sections/4_route_consequence.tex#L13) | `f1242ab3cad1541f2b0cb86c6a55b1241ab20fa1c414b37c56cf85bd623ac8a0` |
| D27 | \[...\] | [paper/sections/4_route_consequence.tex:L15](paper/sections/4_route_consequence.tex#L15) – [paper/sections/4_route_consequence.tex:L18](paper/sections/4_route_consequence.tex#L18) | `d166ac07dbc32a4d0b9224c1dee476dd41378299eee0ff6dbd902d660f8314e1` |
| D28 | \[...\] | [paper/sections/4_route_consequence.tex:L24](paper/sections/4_route_consequence.tex#L24) – [paper/sections/4_route_consequence.tex:L28](paper/sections/4_route_consequence.tex#L28) | `a28fd370f0da0ec0189da79e9f04c17706feb3c47b70fe50f6e32cb900eb336e` |
| D29 | \[...\] | [paper/sections/4_route_consequence.tex:L48](paper/sections/4_route_consequence.tex#L48) – [paper/sections/4_route_consequence.tex:L57](paper/sections/4_route_consequence.tex#L57) | `ae467e253e8b95261b929d5336a760dca20e6af53ec8d71b296c5ce7ee664056` |
| D30 | \[...\] | [paper/sections/5_finite_audit.tex:L11](paper/sections/5_finite_audit.tex#L11) – [paper/sections/5_finite_audit.tex:L13](paper/sections/5_finite_audit.tex#L13) | `2fef8533a3db132112be334c875f6ab6f774435be49a6c6c64b2da83f5f29baf` |
| D31 | \[...\] | [paper/sections/5_finite_audit.tex:L15](paper/sections/5_finite_audit.tex#L15) – [paper/sections/5_finite_audit.tex:L17](paper/sections/5_finite_audit.tex#L17) | `81f749cff62d445101d24fb9099b838196f4496396d8e05ac31d07f5a64c78e1` |
| D32 | \[...\] | [paper/sections/5_finite_audit.tex:L21](paper/sections/5_finite_audit.tex#L21) – [paper/sections/5_finite_audit.tex:L25](paper/sections/5_finite_audit.tex#L25) | `d033eb7bf7ecc2325cebc7e21412ae37b367395ef15b93a00518d6980ffb585a` |
| D33 | \[...\] | [paper/sections/5_finite_audit.tex:L60](paper/sections/5_finite_audit.tex#L60) – [paper/sections/5_finite_audit.tex:L62](paper/sections/5_finite_audit.tex#L62) | `1bfe18893bcdfda100cf1ff68ab35f65aed9ab4ae6c5d459557980f2ea11e878` |
| D34 | \[...\] | [paper/sections/6_conclusion.tex:L7](paper/sections/6_conclusion.tex#L7) – [paper/sections/6_conclusion.tex:L10](paper/sections/6_conclusion.tex#L10) | `65bb25eedbb76ed601af6919b81b6381674578bd20aa17a0821afd9853bed39d` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/main.tex:L18](paper/main.tex#L18): `pdftitle={A Finite-Window Lower Frame Obstruction for Primitive Rational Frequencies},`
- [paper/main.tex:L31](paper/main.tex#L31): `\title{\textbf{A Finite-Window Lower Frame Obstruction\\`
- [paper/sections/0_abstract.tex:L1](paper/sections/0_abstract.tex#L1): `We prove a lower-frame obstruction for finite exponential sums on primitive`
- [paper/sections/0_abstract.tex:L19](paper/sections/0_abstract.tex#L19): `coefficient energy.  The theorem does not address cancellation inside a`
- [paper/sections/1_introduction.tex:L3](paper/sections/1_introduction.tex#L3): `Finite-window reassembly often turns arithmetic packet estimates into an`
- [paper/sections/1_introduction.tex:L9](paper/sections/1_introduction.tex#L9): `direction for a separated finite family.`
- [paper/sections/1_introduction.tex:L11](paper/sections/1_introduction.tex#L11): `We give a uniform lower bound with an explicit defect.  The proof inserts a`
- [paper/sections/1_introduction.tex:L22](paper/sections/1_introduction.tex#L22): `\item We prove the exact finite-window inequality`
- [paper/sections/1_introduction.tex:L40](paper/sections/1_introduction.tex#L40): `into the collapsed coefficient itself; it does not prove arithmetic`
- [paper/sections/1_introduction.tex:L44](paper/sections/1_introduction.tex#L44): `Section~\ref{sec:audit} describes the finite audit.`
- [paper/sections/2_setup.tex:L1](paper/sections/2_setup.tex#L1): `\section{Finite-window setup}`
- [paper/sections/2_setup.tex:L7](paper/sections/2_setup.tex#L7): `\(\gcd(a,h)=1\).  We use a finite set`
- [paper/sections/2_setup.tex:L12](paper/sections/2_setup.tex#L12): `applies to finitely supported coefficient families without taking the full`
- [paper/sections/2_setup.tex:L28](paper/sections/2_setup.tex#L28): `\begin{theorem}[finite-window lower frame]`
- [paper/sections/2_setup.tex:L30](paper/sections/2_setup.tex#L30): `For every \(N\geq1\), \(U\geq1\), interval \(I\) as above, and finite`
- [paper/sections/3_lower_frame.tex:L82](paper/sections/3_lower_frame.tex#L82): `If a finite subset \(\mathcal X\subset\T\) is`
- [paper/sections/4_route_consequence.tex:L22](paper/sections/4_route_consequence.tex#L22): `This is a structural obstruction, not an arithmetic estimate.  In particular,`
- [paper/sections/4_route_consequence.tex:L38](paper/sections/4_route_consequence.tex#L38): `open.`
- [paper/sections/4_route_consequence.tex:L42](paper/sections/4_route_consequence.tex#L42): `The first statement follows from Corollary~\ref{cor:v59}.  The three open`
- [paper/sections/4_route_consequence.tex:L53](paper/sections/4_route_consequence.tex#L53): `\texttt{FULL\_GATE\_B=OPEN},\\`
- [paper/sections/5_finite_audit.tex:L1](paper/sections/5_finite_audit.tex#L1): `\section{Finite certificate and independent audit}`
- [paper/sections/5_finite_audit.tex:L5](paper/sections/5_finite_audit.tex#L5): `deterministic finite certificate to test the identities, matrix directions,`
- [paper/sections/5_finite_audit.tex:L29](paper/sections/5_finite_audit.tex#L29): `\caption{Finite checks on four translated \(41\)-point intervals.  The`
- [paper/sections/5_finite_audit.tex:L47](paper/sections/5_finite_audit.tex#L47): `\texttt{NUMERICALLY\_CERTIFIED\_FINITE\_CHECK}.  The observed excess over the`
- [paper/sections/5_finite_audit.tex:L53](paper/sections/5_finite_audit.tex#L53): `The independent checker does not import the producer.  It separately`
- [paper/sections/6_conclusion.tex:L3](paper/sections/6_conclusion.tex#L3): `A translated triangular minorant converts finite-window energy into a Fejér`
- [paper/sections/6_conclusion.tex:L13](paper/sections/6_conclusion.tex#L13): `positive proportion of the collapsed coefficient energy, uniformly in the`
- [paper/sections/6_conclusion.tex:L20](paper/sections/6_conclusion.tex#L20): `finite-window lower-frame module and its fail-closed boundary.`
- [paper/sections/A_status_ledger.tex:L20](paper/sections/A_status_ledger.tex#L20): `\item \nolinkurl{TPC238_WITHIN_Q_BUCKET_CANCELLATION = OPEN}`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#sec:setup` → `sections/2_setup.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#sec:theorem` → `sections/3_lower_frame.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#sec:route` → `sections/4_route_consequence.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#sec:audit` → `sections/5_finite_audit.tex#L2` (existing project target or original TeX label line).
- Link relocation: `#thm:lower-frame` → `sections/2_setup.tex#L29` (existing project target or original TeX label line).
- Link relocation: `#cor:normalized` → `sections/2_setup.tex#L39` (existing project target or original TeX label line).
- Link relocation: `#thm:lower-frame` → `sections/2_setup.tex#L29` (existing project target or original TeX label line).
- Link relocation: `#lem:triangle` → `sections/3_lower_frame.tex#L7` (existing project target or original TeX label line).
- Link relocation: `#lem:spacing` → `sections/3_lower_frame.tex#L44` (existing project target or original TeX label line).
- Link relocation: `#lem:packing` → `sections/3_lower_frame.tex#L81` (existing project target or original TeX label line).
- Link relocation: `#cor:normalized` → `sections/2_setup.tex#L39` (existing project target or original TeX label line).
- Link relocation: `#cor:v59` → `sections/2_setup.tex#L48` (existing project target or original TeX label line).
- Link relocation: `#thm:lower-frame` → `sections/2_setup.tex#L29` (existing project target or original TeX label line).
- Link relocation: `#cor:v59` → `sections/2_setup.tex#L48` (existing project target or original TeX label line).
