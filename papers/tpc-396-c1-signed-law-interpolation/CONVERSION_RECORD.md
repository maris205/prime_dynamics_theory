# TPC-396 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `4a466e42ae079573ed9100228b99d7d27435451109a77d7976408d541cbe34f2`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `55da35eaad3787e8e3a503bbd173b6d6e4317c2767bf8b2dba524385ff320321`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `12b14efc186b3775da6f91b44ada152621db4a87d0d020f0b52bb7c9f35565bd`.
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
| `Finite construction` | 51 | 1 | `HEADING_TEXT_MATCH` |
| `Statistics and certification` | 85 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 104 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and next question` | 156 | 3 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 178 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `42` before writing and `42` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b9019ed5b1a0df619084adb950bf1a1f581d5a6db735e6b2b12cba7a63ffd1cc`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 43–47 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D02 | align* | 54–58 | `e45a400781bc5be90d8bc6bb698ce42c5d39943f089bd457ef70e2d2bb288927` |
| D03 | \[...\] | 61–64 | `2618df2cb471769cfcb0428e6d37dd2981616bcf6e9675edd4e0ed422113c324` |
| D04 | \[...\] | 66–69 | `7311e9b23bd105fafa55bdad5518091b3361990e759f5dc841d59c30b164d6fb` |
| D05 | \[...\] | 75–78 | `b3c18e57eadaddfb1f8552a758bcb63e29c7c0012b8857dd259b6e7c94c686fa` |
| D06 | \[...\] | 88–90 | `26c02151d9f57280d32a7cb7219776d9974abc3de8022160767372af1336b9cc` |
| D07 | \[...\] | 131–136 | `b009d24eb19a60ada7a0f144a7e0f56ca3840eef219b1f73dccbb209992fb6dc` |
| D08 | \[...\] | 141–146 | `1a4994049dd4cf2054b152ac796845ceb81d0d99ae8ae26c9d3fb82ec97f9738` |
| D09 | \[...\] | 172–174 | `d8fef565e1d9a96e5d933545db71bbdf8dacc574122d3975f5281a3323c8e821` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 8: `\title{TPC-396: Finite Signed-Law Interpolation and an Origin-Spread Transition}`
- TeX line 19: `coordinate-disjoint finite family.  We now probe its mechanism by forming four`
- TeX line 28: `are finite proxy observations and an obstruction-localization result, not a`
- TeX line 35: `finite matrices behave differently across origins, even after changing the`
- TeX line 38: `mixed.  We use a response-blind finite panel to locate a possible transition.`
- TeX line 46: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 49: `proof and Bridge-B artifacts are fail-closed finite consistency evidence only.`
- TeX line 51: `\section{Finite construction}`
- TeX line 65: `For the four declared probes we use the exact finite identity`
- TeX line 112: `\caption{Finite TPC-396 panel: 96 rows and 16 cells.}`
- TeX line 147: `The last three exceed $0.03$ and are retained as failures.  The finite spectral`
- TeX line 153: `matrices, the rational identity is proved at the anchor; this does not promote`
- TeX line 154: `the float64 finite observations to an asymptotic assertion.`
- TeX line 158: `The strongest positive result is phase localization inside the declared finite`
- TeX line 163: `statement is therefore the scoped finite observation that the tested endpoint`
- TeX line 175: `Source-valid origin uniformity, growing operator control, arithmetic $L^2$,`
- TeX line 176: `Route closure, and the twin-prime endpoint remain open.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:summary` → `main.tex#L113` (existing project target or original TeX label line).
