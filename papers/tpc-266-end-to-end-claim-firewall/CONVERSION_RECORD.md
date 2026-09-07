# TPC-266 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `524af4ad2c623e839511e915db5d85e6c41c7c9e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `f0d34afefafa49ebc2184e719d62b37dded7a9916195db83a6ac42abf959c160`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `9b5508565dde37b7de116207b807209ae222b1b57f52bd536d21a75113208b0d`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `edf27fd316e00edf225fe2775ee8890b4a7a416374854dcc0209f01da8e9f8d7`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC265_269.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `The three-stage interface` | 84 | 2 | `HEADING_TEXT_MATCH` |
| `Typed endpoint compiler` | 123 | 2 | `HEADING_TEXT_MATCH` |
| `Two hostile firewalls` | 188 | 3 | `HEADING_TEXT_MATCH` |
| `Exact hostile matrix` | 221 | 4 | `HEADING_TEXT_MATCH` |
| `Route consequence and limitations` | 265 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 298 | 5 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 306 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `84` before writing and `84` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `15`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `aba60cf675f1b97c0995757647c06e5564538322fcfe4c4c72aa2739a7666e76`.
- Source theorem/proof environment starts: remark at TeX line 117, definition at TeX line 135, theorem at TeX line 142, proof at TeX line 161, theorem at TeX line 174, proof at TeX line 182, theorem at TeX line 190, proof at TeX line 199, theorem at TeX line 205, proof at TeX line 215, theorem at TeX line 249, proof at TeX line 255.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 53–55 | `0cf45c86bc5a9c949a4ce70503ca762db2c4583aa1953864526e446c0c714da6` |
| D02 | \[...\] | 57–59 | `3406f2118abe5f18ceba6d7e2f3cc3f6ea7dd63e196e5de138fae5b8061adac4` |
| D03 | \[...\] | 61–63 | `89d4094262c33296e8c2928fac6048ee45abad740f3fc2e0f058cce4467cab93` |
| D04 | \[...\] | 87–89 | `e82322edd39365e4df543b87bf5406fd671d478db632077a3b295a53ece35219` |
| D05 | equation | 91–94 | `d4a16f0b2645c31e0a0424f28e47a6eefea833f92b7fb642ca0123c8b48a0fdb` |
| D06 | \[...\] | 99–101 | `8abea2987e5db9e2905c68d64883a706211106a5158c058c50bd598630501859` |
| D07 | \[...\] | 126–129 | `6600ff8e3c9e62c262713d95c1de291dac925a470a67081116d617ad0d06991f` |
| D08 | \[...\] | 131–133 | `98d3868122c94d94912cfbf36e6664ee4dc9fd0379173d9599163f3f39a43419` |
| D09 | \[...\] | 144–146 | `88ed355260d474711d6c19615543a12b76c98f2aa6753544b702da9ecd0264b3` |
| D10 | align | 148–152 | `064ef8c7df091472521b13bcaf7dc5795b3cf0b7bad2e0f96648e41091442813` |
| D11 | \[...\] | 154–157 | `8271c89fcdf2b2ab349ab04cefd7ea0156cc1a59ef0afa6a478fce1976826ee8` |
| D12 | \[...\] | 163–165 | `7dd42473269bf73797b4172445005242d52ebc416ef31319d020c500b413f7ea` |
| D13 | \[...\] | 192–194 | `9439c8710c5f3b04a6254a06bab9ad57a216f2ff913b650f7e08c06ef9b1c877` |
| D14 | \[...\] | 207–209 | `f52c162656146e23b67a8d1151a2b5d892a28c8dfea072a2845a94c6f5aa0208` |
| D15 | \[...\] | 268–274 | `e18938128eef9f6bc43aee41a1d1f0d04ba1f6431a515558ea7abb27eb98f496` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 46: `arithmetic $L^2$, and the twin-prime conjecture remain open.`
- TeX line 72: `shortcuts are invalid.  In particular, the paper does not treat an arbitrary`
- TeX line 73: `small numerical slope as a theorem and does not remove an unestimated`
- TeX line 96: `semidefinite and hence $|z_x|\leq ab$.  In complement dimension at least two,`
- TeX line 202: `$\LogType\to\Pow(\delta)$ is not a valid interface transition.`
- TeX line 238: `Fixed-log center & fixed-log center + power radius & \texttt{OPEN\_LOG\_CENTER}\\`
- TeX line 239: `Missing radius & power center + missing radius & \texttt{OPEN\_RADIUS}\\`
- TeX line 271: `\text{residual}&=\text{Schur set with radius OPEN},\\`
- TeX line 275: `It is therefore correctly open for the literal V59 endpoint.  TPC-266 pays no`
- TeX line 291: `Literal V59 radius and phase & \texttt{OPEN}\\`
- TeX line 292: `Arithmetic $L^2$ and full Gate B & \texttt{NONE / OPEN}\\`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:powerlanes` → `main.tex#L151` (existing project target or original TeX label line).
- Link relocation: `#tab:matrix` → `main.tex#L246` (existing project target or original TeX label line).
