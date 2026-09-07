# TPC-390 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `af5d2d7b75a2c66234d03413807d25b6464794cd0213059f1f6c5d696705861a`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `1dd7e2cf07fe237ebdf58dbec224019bc618eadcc4ffa1ae2aa8843182714680`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `4b03f413b12526860d7a34887c70c857c376c63f934cfe999e043ef07d33dd9a`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 32 | 1 | `HEADING_TEXT_MATCH` |
| `Finite proxy` | 55 | 1 | `HEADING_TEXT_MATCH` |
| `Forecast interface` | 71 | 2 | `HEADING_TEXT_MATCH` |
| `Certification and finite result` | 98 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion and next clue` | 149 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 162 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `42` before writing and `42` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `8f10c06b77f51797f56d9a35adb987e6199fd002973edcda7c637647ed635e03`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 38–40 | `440b08b57d93110b03049246f06ac66f072563db3bca661599ded700af43ecd1` |
| D02 | \[...\] | 47–51 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D03 | align* | 58–62 | `56f851d416802d2953adc2c69573c54ab07ea8f03b0d1239ac208f52ce06bb72` |
| D04 | \[...\] | 76–79 | `0ce11fa965bda150c01aac02b5bdeb6d0d37019fa5f91891d98f6a69e726b3b1` |
| D05 | \[...\] | 81–86 | `f2ab37518aa892de821ccc4b4161116fc4adeb0a5dab5e3e1849f9e4773e583a` |
| D06 | \[...\] | 88–92 | `c29408455cdd3d3593a903794dfc0a803cc0b3afe9086f99fd7388202c3b9132` |
| D07 | \[...\] | 156–158 | `947be1098c068cf1e896af46c3af63817b8484c14a52d497d81bffc583188090` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `TPC-389 found a finite long-horizon transfer of a frozen count slope through`
- TeX line 25: `predeclared 3\% finite cap.  The one-step parent and local-control forecasts`
- TeX line 27: `$23/32$, with maximum error $0.0490741652$.  The resulting finite`
- TeX line 28: `pass/failure census is an obstruction audit, not an asymptotic law, an`
- TeX line 34: `The previous releases transferred a finite logarithmic count-slope interface`
- TeX line 50: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 55: `\section{Finite proxy}`
- TeX line 63: `The row geometry is the finite square energy`
- TeX line 95: `divided by its declared forecast, minus one; a finite pass requires absolute`
- TeX line 98: `\section{Certification and finite result}`
- TeX line 102: `the same finite matrices in descending shell order, recomputes the row`
- TeX line 109: `certificate; all decimal values are finite diagnostics, not claimed limits.`
- TeX line 113: `\caption{TPC-390 finite recursive-composition census.}`
- TeX line 142: `The interpretation is intentionally conditional on this finite panel.  A`
- TeX line 144: `declared proxy and normalization; it does not refute a different source-valid`
- TeX line 145: `theorem.  Conversely, a finite pass would not establish count or origin`
- TeX line 146: `uniformity.  In either case the inherited spectral diagnostic and the open`
- TeX line 159: `No arithmetic power credit is assigned, and Route-A/Route-B reassembly and`
- TeX line 160: `the twin-prime endpoint remain open.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
