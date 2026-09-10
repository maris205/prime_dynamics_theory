# TPC-244 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `236b82c15b5f71aba9d9f29600152e85ad34d181d230eb4aeb11cffad9cbe39d`.

- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `22a134b2adec640b73ddfb4ab8135c02a7bea3f9fa77ab202f4998d2da4c16b1`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `396e030823922b5c5bbabe1ecaead9a410083825149e001283bb1c80bb674223`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC240_244.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 12 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `236b82c15b5f71aba9d9f29600152e85ad34d181d230eb4aeb11cffad9cbe39d` |
| [paper/math_commands.tex](paper/math_commands.tex) | `ab60be518e1226a10cc3b445496ea84cf3d21a42fa9a7b72367342705d1f4695` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `069d0199e6bebb2533c38fa0d0a1d7e9c7453cdc32ff77559cb192a010ef112f` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `f4d581393a6bfb74f11e64b5928a4de881561abbbb39e25f8f39703d3acffc8b` |
| [paper/sections/2_source_lock.tex](paper/sections/2_source_lock.tex) | `31ee1b35ea20360b3417b5541097374189bf1da1fd86c589c1bbe6faeaf8c3ea` |
| [paper/sections/3_direct_sum.tex](paper/sections/3_direct_sum.tex) | `028cee0488b64eaa9259f13512cf8f877a94f17301f7ad2e6bbb85d16d4fc34d` |
| [paper/sections/4_sign_cut.tex](paper/sections/4_sign_cut.tex) | `faf526d7c781078801e67b247eeff1163b43b406c051841423b7aae29485216b` |
| [paper/sections/5_hard_window.tex](paper/sections/5_hard_window.tex) | `d1e6cfb75e18baa67071baa7f83ca0c2d982bfa3203e58687e975e5328adaa87` |
| [paper/sections/6_certificate.tex](paper/sections/6_certificate.tex) | `a656a39731b7f700b846697c0ef20ed156e5ce26ab6e0b45cacbeb97396cf9fc` |
| [paper/sections/7_route_boundary.tex](paper/sections/7_route_boundary.tex) | `e06c75be601bc6ecca0817f1e46ff8bf99fd03a8441f0edc53b71b9e3c0e2b22` |
| [paper/sections/8_conclusion.tex](paper/sections/8_conclusion.tex) | `9288c85f44f47ea1634b6f6c9f3c702d27e77a5cf6ac34fc8a084caf4dfcf21f` |
| [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) | `7e96ab6d05143fce07f397c2ab217e882d592079286df42b80e2aef19941f0c1` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L17](paper/main.tex#L17) | `\input{math_commands}` | [paper/math_commands.tex](paper/math_commands.tex) |
| [paper/main.tex:L46](paper/main.tex#L46) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L49](paper/main.tex#L49) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L50](paper/main.tex#L50) | `\input{sections/2_source_lock}` | [paper/sections/2_source_lock.tex](paper/sections/2_source_lock.tex) |
| [paper/main.tex:L51](paper/main.tex#L51) | `\input{sections/3_direct_sum}` | [paper/sections/3_direct_sum.tex](paper/sections/3_direct_sum.tex) |
| [paper/main.tex:L52](paper/main.tex#L52) | `\input{sections/4_sign_cut}` | [paper/sections/4_sign_cut.tex](paper/sections/4_sign_cut.tex) |
| [paper/main.tex:L53](paper/main.tex#L53) | `\input{sections/5_hard_window}` | [paper/sections/5_hard_window.tex](paper/sections/5_hard_window.tex) |
| [paper/main.tex:L54](paper/main.tex#L54) | `\input{sections/6_certificate}` | [paper/sections/6_certificate.tex](paper/sections/6_certificate.tex) |
| [paper/main.tex:L55](paper/main.tex#L55) | `\input{sections/7_route_boundary}` | [paper/sections/7_route_boundary.tex](paper/sections/7_route_boundary.tex) |
| [paper/main.tex:L56](paper/main.tex#L56) | `\input{sections/8_conclusion}` | [paper/sections/8_conclusion.tex](paper/sections/8_conclusion.tex) |
| [paper/main.tex:L59](paper/main.tex#L59) | `\input{sections/A_status_ledger}` | [paper/sections/A_status_ledger.tex](paper/sections/A_status_ledger.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `Source lock and conventions` | [paper/sections/2_source_lock.tex:L1](paper/sections/2_source_lock.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Common-multiplier phase blindness` | [paper/sections/3_direct_sum.tex:L1](paper/sections/3_direct_sum.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Nonorthogonal reassembly as a sign cut` | [paper/sections/4_sign_cut.tex:L1](paper/sections/4_sign_cut.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Hard-window leakage bound` | [paper/sections/5_hard_window.tex:L1](paper/sections/5_hard_window.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Exact finite certification` | [paper/sections/6_certificate.tex:L1](paper/sections/6_certificate.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Route evaluation and source boundary` | [paper/sections/7_route_boundary.tex:L1](paper/sections/7_route_boundary.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/8_conclusion.tex:L1](paper/sections/8_conclusion.tex#L1) | 5 | `HEADING_TEXT_MATCH` |
| `Status ledger` | [paper/sections/A_status_ledger.tex:L1](paper/sections/A_status_ledger.tex#L1) | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `97` before writing and `97` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `18`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `3ef5af6fadc1b4b3ec37238957ff6451dcdbc0d234163adfac7f3536b4e482f1`.
- Source theorem/proof environment starts: theorem at [paper/sections/3_direct_sum.tex:L3](paper/sections/3_direct_sum.tex#L3), proof at [paper/sections/3_direct_sum.tex:L20](paper/sections/3_direct_sum.tex#L20), theorem at [paper/sections/4_sign_cut.tex:L19](paper/sections/4_sign_cut.tex#L19), proof at [paper/sections/4_sign_cut.tex:L29](paper/sections/4_sign_cut.tex#L29), corollary at [paper/sections/5_hard_window.tex:L19](paper/sections/5_hard_window.tex#L19), proof at [paper/sections/5_hard_window.tex:L28](paper/sections/5_hard_window.tex#L28).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/2_source_lock.tex:L5](paper/sections/2_source_lock.tex#L5) – [paper/sections/2_source_lock.tex:L10](paper/sections/2_source_lock.tex#L10) | `9eea66b1a9c002a43ac8f16b9eef58caab62c53ab0e3934ff06bb08f6304f829` |
| D02 | \[...\] | [paper/sections/2_source_lock.tex:L23](paper/sections/2_source_lock.tex#L23) – [paper/sections/2_source_lock.tex:L25](paper/sections/2_source_lock.tex#L25) | `0daccd3779aeeded8065e320a541a6fc1e336819c3a3db22e04c646f7559bd33` |
| D03 | \[...\] | [paper/sections/3_direct_sum.tex:L5](paper/sections/3_direct_sum.tex#L5) – [paper/sections/3_direct_sum.tex:L9](paper/sections/3_direct_sum.tex#L9) | `b033297aaffd68b241027f65c97691930199795dd68c04bf601a2e5a5265d74b` |
| D04 | align | [paper/sections/3_direct_sum.tex:L11](paper/sections/3_direct_sum.tex#L11) – [paper/sections/3_direct_sum.tex:L15](paper/sections/3_direct_sum.tex#L15) | `78a3781831e11d9da62f2e9bf07592622f201bda8e4620b7978ef72d1b1a50c6` |
| D05 | \[...\] | [paper/sections/3_direct_sum.tex:L22](paper/sections/3_direct_sum.tex#L22) – [paper/sections/3_direct_sum.tex:L26](paper/sections/3_direct_sum.tex#L26) | `6ed5aaac279f52b0ab4585607f223fffeeb9b366615edb1697d9946829920181` |
| D06 | \[...\] | [paper/sections/4_sign_cut.tex:L6](paper/sections/4_sign_cut.tex#L6) – [paper/sections/4_sign_cut.tex:L11](paper/sections/4_sign_cut.tex#L11) | `5218b3c7b752fd5f3b4a7aaad8cb2c280d27d431ad2dcec8b87cba7868b84c87` |
| D07 | \[...\] | [paper/sections/4_sign_cut.tex:L13](paper/sections/4_sign_cut.tex#L13) – [paper/sections/4_sign_cut.tex:L17](paper/sections/4_sign_cut.tex#L17) | `d46f9416d28a3c4903bd8666badb626046961e7bbfacb9bb89855d63cfd926eb` |
| D08 | align | [paper/sections/4_sign_cut.tex:L21](paper/sections/4_sign_cut.tex#L21) – [paper/sections/4_sign_cut.tex:L24](paper/sections/4_sign_cut.tex#L24) | `6e2e778a5daac7f412eda6bbea7139187751f6fe29d4ec42f9b41e1d201bd6f5` |
| D09 | \[...\] | [paper/sections/4_sign_cut.tex:L38](paper/sections/4_sign_cut.tex#L38) – [paper/sections/4_sign_cut.tex:L40](paper/sections/4_sign_cut.tex#L40) | `e7ac1a0e4fd0164fa66a364343dc1cc000ccddbfe951a43d6429e4561daf7b42` |
| D10 | \[...\] | [paper/sections/4_sign_cut.tex:L48](paper/sections/4_sign_cut.tex#L48) – [paper/sections/4_sign_cut.tex:L50](paper/sections/4_sign_cut.tex#L50) | `e23f68a8576ce88b06070584dd57e9845e501fe453a891ab2e6946ef18b422be` |
| D11 | \[...\] | [paper/sections/5_hard_window.tex:L5](paper/sections/5_hard_window.tex#L5) – [paper/sections/5_hard_window.tex:L10](paper/sections/5_hard_window.tex#L10) | `1d5d837bfa493cea9a85bee7b0ba9bbe15995a0b154bddc2be5e18d7f4651af7` |
| D12 | \[...\] | [paper/sections/5_hard_window.tex:L15](paper/sections/5_hard_window.tex#L15) – [paper/sections/5_hard_window.tex:L17](paper/sections/5_hard_window.tex#L17) | `6a1d0d765047556634693a1012fadb7cbfaf4aeab774a55aaa2d7264ec56e584` |
| D13 | \[...\] | [paper/sections/5_hard_window.tex:L21](paper/sections/5_hard_window.tex#L21) – [paper/sections/5_hard_window.tex:L24](paper/sections/5_hard_window.tex#L24) | `b166d9f23c71ae84b42bb9218ef1095f13010279fcb153429b8fef8f2ceaec95` |
| D14 | \[...\] | [paper/sections/5_hard_window.tex:L32](paper/sections/5_hard_window.tex#L32) – [paper/sections/5_hard_window.tex:L36](paper/sections/5_hard_window.tex#L36) | `c58ffefa422f8a7a849b0ba5de5b6479976b9e79addf7c4d60069d9d2a79c90b` |
| D15 | \[...\] | [paper/sections/5_hard_window.tex:L45](paper/sections/5_hard_window.tex#L45) – [paper/sections/5_hard_window.tex:L48](paper/sections/5_hard_window.tex#L48) | `265209953271e7ac0932535a8ce5401306ec3b92b6ce97d15a411294b0450da2` |
| D16 | \[...\] | [paper/sections/6_certificate.tex:L8](paper/sections/6_certificate.tex#L8) – [paper/sections/6_certificate.tex:L10](paper/sections/6_certificate.tex#L10) | `cb877637994d0b9776254b05462180cc55ea9425c733e3541e8231e11bbc1dd4` |
| D17 | \[...\] | [paper/sections/7_route_boundary.tex:L9](paper/sections/7_route_boundary.tex#L9) – [paper/sections/7_route_boundary.tex:L11](paper/sections/7_route_boundary.tex#L11) | `477b2a5c955cf4c9a8b95a842055f9a3a1c827a2c4783c738ccb0cc034c389e8` |
| D18 | \[...\] | [paper/sections/7_route_boundary.tex:L18](paper/sections/7_route_boundary.tex#L18) – [paper/sections/7_route_boundary.tex:L20](paper/sections/7_route_boundary.tex#L20) | `e4ae5857c92335f4ca76303d6d2ad7f5555b3d0392de263cbcb002d5b289ba36` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/1_introduction.tex:L12](paper/sections/1_introduction.tex#L12): `sign or phase disappears exactly.  This does not make the arithmetic tail`
- [paper/sections/1_introduction.tex:L19](paper/sections/1_introduction.tex#L19): `sign flips is a finite Walsh polynomial indexed by the edges of the block`
- [paper/sections/1_introduction.tex:L27](paper/sections/1_introduction.tex#L27): `coefficient lanes in one common synthesis map.  No arithmetic cancellation,`
- [paper/sections/2_source_lock.tex:L17](paper/sections/2_source_lock.tex#L17): `particular, the current source compiler leaves open a literal map from the V59`
- [paper/sections/2_source_lock.tex:L19](paper/sections/2_source_lock.tex#L19): `space.  We therefore separate the unconditional finite-dimensional theorems`
- [paper/sections/2_source_lock.tex:L22](paper/sections/2_source_lock.tex#L22): `For a finite index set $\cA$, write`
- [paper/sections/2_source_lock.tex:L27](paper/sections/2_source_lock.tex#L27): `linear embedding into one ambient Hilbert space; it is not assumed isometric.`
- [paper/sections/2_source_lock.tex:L30](paper/sections/2_source_lock.tex#L30): `$|\eta_h|=1$ after $C_h$ has been formed.  It is not a change of any individual`
- [paper/sections/3_direct_sum.tex:L39](paper/sections/3_direct_sum.tex#L39): `change $|C_h|$, so the theorem does not erase or estimate internal arithmetic`
- [paper/sections/4_sign_cut.tex:L45](paper/sections/4_sign_cut.tex#L45): `does not assign a real saving sign.  Vanishing of $S_{hk}$ only requires the`
- [paper/sections/5_hard_window.tex:L3](paper/sections/5_hard_window.tex#L3): `Let $T$ be the common synthesis map on a finite $\delta$-separated frequency`
- [paper/sections/5_hard_window.tex:L51](paper/sections/5_hard_window.tex#L51): `payable estimate for $\norm W\norm B$ remain open.`
- [paper/sections/6_certificate.tex:L1](paper/sections/6_certificate.tex#L1): `\section{Exact finite certification}`
- [paper/sections/6_certificate.tex:L24](paper/sections/6_certificate.tex#L24): `sign-cut identities.  These records are finite illustrations only; the proofs`
- [paper/sections/7_route_boundary.tex:L22](paper/sections/7_route_boundary.tex#L22): `result is therefore conditional at that interface.  It supplies no arithmetic`
- [paper/sections/8_conclusion.tex:L8](paper/sections/8_conclusion.tex#L8): `signs cannot control the same-bucket main term.  The open road is now the local`
- [paper/sections/A_status_ledger.tex:L16](paper/sections/A_status_ledger.tex#L16): `Literal V59 two-lane attachment & Open \\`
- [paper/sections/A_status_ledger.tex:L17](paper/sections/A_status_ledger.tex#L17): `Coefficient norm payment & Open \\`
- [paper/sections/A_status_ledger.tex:L20](paper/sections/A_status_ledger.tex#L20): `Strict $1/400$ / full Gate B & Unpaid / open \\`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- The preamble-only glyphtounicode input was resolved with kpsewhich and checked against the audited SHA-256; its non-content mapping table was not expanded. The original command, source line, and dependency hash are retained in the reading layer.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:cov` → `sections/3_direct_sum.tex#L12` (existing project target or original TeX label line).
- Link relocation: `#eq:norms` → `sections/3_direct_sum.tex#L14` (existing project target or original TeX label line).
- Link relocation: `#eq:walsh` → `sections/4_sign_cut.tex#L22` (existing project target or original TeX label line).
- Link relocation: `#eq:cut` → `sections/4_sign_cut.tex#L23` (existing project target or original TeX label line).
- Link relocation: `#eq:walsh` → `sections/4_sign_cut.tex#L22` (existing project target or original TeX label line).
- Link relocation: `#eq:walsh` → `sections/4_sign_cut.tex#L22` (existing project target or original TeX label line).
