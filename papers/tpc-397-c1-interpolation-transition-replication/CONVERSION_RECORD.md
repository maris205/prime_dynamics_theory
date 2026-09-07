# TPC-397 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `fe7e6c6294a75e76a65e146c1027a0893045635243f260a8f972f7787d48b60f`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `67e14be927bde5932b38169722a3e8962b1f3dfd4f469db97450fc6427e54ce4`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `70368d64211f2c445800028ed478d5e0f60ed4566e214edfb6c8ab4229569e3c`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 32 | 1 | `HEADING_TEXT_MATCH` |
| `Finite construction` | 50 | 1 | `HEADING_TEXT_MATCH` |
| `Statistics and certification` | 84 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 104 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and next question` | 149 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 170 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `40` before writing and `40` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `7ec612817f7b974bf2293bb4e0bac67602513b3f9a2e41ecb18a77a8d3aa97f8`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 42–46 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D02 | align* | 53–57 | `e45a400781bc5be90d8bc6bb698ce42c5d39943f089bd457ef70e2d2bb288927` |
| D03 | \[...\] | 60–63 | `2618df2cb471769cfcb0428e6d37dd2981616bcf6e9675edd4e0ed422113c324` |
| D04 | \[...\] | 65–68 | `161624d6120fa90b173e7a49eca1517475f66d2e6bf9387c37583745eb4f2950` |
| D05 | \[...\] | 74–77 | `6520120678b5da3cc0e2baace57a554ee8d9322280dc24ca0993e0f5baee3a64` |
| D06 | \[...\] | 87–89 | `26c02151d9f57280d32a7cb7219776d9974abc3de8022160767372af1336b9cc` |
| D07 | \[...\] | 131–136 | `19a4cdaa7049d8f7b7521805f364dfc96a8d85fb6d63c84ce918195b0ffe8397` |
| D08 | \[...\] | 164–166 | `005433e786f696f7ad9fc47ab518c85f42ef73c6c4fb63b00e1493d965ee606d` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 8: `\title{TPC-397: Fine-Grid Replication of a Finite Interpolation Endpoint Transition}`
- TeX line 18: `TPC-396 sampled a finite origin-spread change coarsely at`
- TeX line 28: `finite proxy observations and a replication of endpoint localization, not a`
- TeX line 37: `family.  We use a response-blind finite panel to test that question.`
- TeX line 45: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 48: `proof and Bridge-B artifacts are fail-closed finite consistency evidence only.`
- TeX line 50: `\section{Finite construction}`
- TeX line 64: `For the four declared probes we use the exact finite identity`
- TeX line 112: `\caption{Finite TPC-397 panel: 96 rows and 16 cells.}`
- TeX line 141: `pass their fixed $0.03$ caps.  The finite spectral cap $0.64$ fails on no row,`
- TeX line 146: `matrices, the rational identity is proved at the anchor; this does not promote`
- TeX line 147: `the float64 finite observations to an asymptotic assertion.`
- TeX line 151: `The strongest positive result is a replicated finite phase localization: all`
- TeX line 156: `statement is only that endpoint localization reappears on this fifth finite`
- TeX line 167: `Source-valid origin uniformity, growing operator control, arithmetic $L^2$,`
- TeX line 168: `Route closure, and the twin-prime endpoint remain open.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:summary` → `main.tex#L113` (existing project target or original TeX label line).
