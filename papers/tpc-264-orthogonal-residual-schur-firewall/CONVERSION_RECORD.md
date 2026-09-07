# TPC-264 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `bdc7bb8c00508788363faa2db8691f1128ab3d3e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `a2c6796189554a33cb6b97ad18c94f0389379fadbfca1143c5621eff6768be19`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `90da7239f20a9741db4ffc456328bfe77440e1f068a539fc216e2e5241550206`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `7bbb9e1334af2cddccb4569d6908743be530a3a771e32c14444f589658a80c60`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC260_264.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Scope and motivation` | 47 | 1 | `HEADING_TEXT_MATCH` |
| `The projected and residual data` | 87 | 2 | `HEADING_TEXT_MATCH` |
| `The Schur feasible set` | 123 | 2 | `HEADING_TEXT_MATCH` |
| `An exact finite audit` | 196 | 3 | `HEADING_TEXT_MATCH` |
| `Endpoint-scale consequence` | 226 | 4 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route consequence` | 261 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 285 | 5 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 295 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `95` before writing and `95` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `21`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b0c9cb96b4bc75fc2453c3c98eec43b916cd61b359742dbc3165958b0da5aa5a`.
- Source theorem/proof environment starts: lemma at TeX line 103, proof at TeX line 111, definition at TeX line 125, theorem at TeX line 138, proof at TeX line 156, remark at TeX line 189.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 50–52 | `0cf45c86bc5a9c949a4ce70503ca762db2c4583aa1953864526e446c0c714da6` |
| D02 | \[...\] | 56–59 | `3d3ca36f49f0fe0c2c1149f13b09b8178ac66cf41c87f0bb6e2c9611fcc1cc20` |
| D03 | \[...\] | 61–63 | `d79b682223e3a8f15557f09dd54d48a6d55d91cd527cc3d616772aa48881e988` |
| D04 | \[...\] | 91–93 | `809fb9e569dbfa99415390ce7cb8ba6fb750adab703208ec8f9a4198a215aca4` |
| D05 | \[...\] | 95–97 | `c58118ebca198899118233daceffd09f19b1c4f1504be352fed7379e15fa8d4e` |
| D06 | \[...\] | 99–101 | `e6aaf81858dba1426fa97575fc03ec717f10c0d0d0152afcf6ef2fa1d474c501` |
| D07 | equation | 105–108 | `88526e78cfcbf8ca241f6e1f456c4c5355e735d8bc980c58973817a4d99720f8` |
| D08 | \[...\] | 114–116 | `85abbbc44b49aec27fc04aa2d279ea0a12347ea81e6c8575378c91ef8584dce6` |
| D09 | \[...\] | 127–133 | `81abba81465c47663851f30fd7784d41b5da78b951a01fdba8911d0d671120cf` |
| D10 | \[...\] | 143–145 | `3dc80ee1838ce3570d9ee91acfec375acd6d43dfdcae154a40e1d084002fe994` |
| D11 | \[...\] | 147–149 | `bf0a58468f6138052e46cbfc5f15c0132db0425f33204197f2a84c210df1c56c` |
| D12 | \[...\] | 159–162 | `733385da0f557c4982c58a8f3cef7ad7d12c17b3592bd3b58f966c8b8524bf58` |
| D13 | \[...\] | 167–169 | `867c5cd796dd6c0d229edc3e85b66fcfe9252a1f31ff1b790d7f8acf118bb25f` |
| D14 | \[...\] | 171–174 | `b7d627cf817591d04b4b5cdcd458962bd5783d52722142163b47755dc8f88256` |
| D15 | \[...\] | 180–182 | `cffd1c9d60096d97a26223863fd34b6516c5d0d98e56535323c99cdf42b2e61a` |
| D16 | \[...\] | 200–202 | `9500378736fd3abb04ca4689291f1d92df47c87374ab65d932cc92513e6cccf7` |
| D17 | \[...\] | 205–213 | `6ce654d1d828d407f1040f7c941f347d7ee346b68e682b147ad951d1895af914` |
| D18 | \[...\] | 231–233 | `301b214ad542c5886d4538425ea5193dbf9dc29c66755bbdbd02483a16228973` |
| D19 | \[...\] | 236–238 | `6547f8b7f52afa813994966d08fb78927ef5d28c67a3038e2d3a56885cc7b925` |
| D20 | \[...\] | 243–245 | `1178e3315b6534d9f244bc428dde5506ec9b6286e01bc805fca13aab341465c5` |
| D21 | \[...\] | 249–252 | `f3a84c9b727e9f5df37cb8eca8f88b4db54469bfed8a1ebc81d912699eab154e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 35: `an exact finite-dimensional Schur classification of that residual.  If the`
- TeX line 41: `disk endpoints, its interior, and the dimension transition.  A synthetic`
- TeX line 44: `structural firewall, not a literal prime-shell counterexample.`
- TeX line 68: `There are two reasons to isolate this finite question.  First, a positive`
- TeX line 69: `semidefinite Gram constraint is an exact source of information, and its sharp`
- TeX line 84: `All finite vectors below are audit objects.  They do not model a new prime`
- TeX line 85: `distribution law, and no finite witness is treated as asymptotic evidence.`
- TeX line 134: `The set of $z$ for which this matrix is positive semidefinite is the Schur`
- TeX line 158: `positive semidefinite.  Its determinant is nonnegative, so`
- TeX line 193: `finite-dimensional constraint has been left in the disk statement.`
- TeX line 196: `\section{An exact finite audit}`
- TeX line 223: `This finite audit is deliberately small enough to inspect line by line and`
- TeX line 230: `radius is left at the natural baseline scale.  Consider the synthetic choice`
- TeX line 269: `Finite Gaussian-rational witnesses & \texttt{NUMERICALLY\_CERTIFIED}\\`
- TeX line 270: `Literal V59 residual radius or phase & \texttt{OPEN}\\`
- TeX line 272: `Arithmetic $L^2$ and full Gate B & \texttt{NONE / OPEN}\\`
- TeX line 281: `coupling.  It does not block a future literal estimate.  The next natural`
- TeX line 287: `TPC-264 turns the unresolved term in TPC-263 into a complete finite geometry.`
- TeX line 293: `claims remain open.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:split` → `main.tex#L107` (existing project target or original TeX label line).
- Link relocation: `#eq:split` → `main.tex#L107` (existing project target or original TeX label line).
- Link relocation: `#eq:schur` → `main.tex#L161` (existing project target or original TeX label line).
