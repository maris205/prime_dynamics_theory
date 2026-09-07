# TPC-416 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `ad8887481d4627e249acc26ae010fc12214a10913c5f0750b49ee3b472930aed`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `e27f2cbf606ea9c54e25e53c57d41591e117b625c5387ef68dc50db82cd65fec`; 1 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8eca0e0c6716e83e64a83adcb4e1cd0770f5dfd172cfc5df9ead475efefe4739`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Four-shell profile` | 17 | 1 | `HEADING_TEXT_MATCH` |
| `Exact observation` | 31 | 1 | `HEADING_TEXT_MATCH` |
| `Scope and reproduction` | 36 | 1 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `20` before writing and `20` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `2`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `dccd497f90a6cf2616ef492974cb30cf83c700a62333059a8bef037a0db436de`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 24–26 | `7b100f808d18d4052eeded8e2aca476db7e047c1abb646590cb246ebb1f82299` |
| D02 | \[...\] | 28–30 | `d2656677cd223d644d8f1cfbc5df78c4f5c8af0f15723669b48548a2a2077ed4` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 15: `verify the finite row; no arithmetic theorem is claimed.`
- TeX line 37: `This one finite synthetic adjacent normalized proxy entry does not prove a full`
- TeX line 38: `operator estimate, physical $h_0$ or arithmetic signs, pay arithmetic $L^2$ or`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
