# TPC-412 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `3395b1c1842031a707d24ccba89ea0620592601a852f7d6c3be52c3026357478`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `3b14dd10869c295349b49a03e185fc7cb8377ad996acb78b79b8317a5e5f9295`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `912af2736326c900292dbf39571d2e9d8bf2c296024a6f510124353b694f2295`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Profile and theorem` | 17 | 1 | `HEADING_TEXT_MATCH` |
| `Exact observations` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Scope and reproduction` | 47 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `30` before writing and `30` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `3`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `cf1a6a4fb50bccf8c2c2bb82323d2c92aad515064cd8f636766527b6854a19bd`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 24–26 | `117e3d90a4573521a043f829c143ed1810f871ef776a54ca2c6adb7a960bbf16` |
| D02 | \[...\] | 28–31 | `8a9f2d8689e17fee51faa83f848f3a5bff38862a864a3df1aed672af70cf7c12` |
| D03 | \[...\] | 36–44 | `7dac5dee926c1ce8c06eb84c2bc21c889b17d8a05965fbd126e088d7f903a7a8` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 14: `and an independent literal replay verify all four rows.  This is finite`
- TeX line 15: `synthetic evidence, not an arithmetic or twin-prime theorem.`
- TeX line 48: `This finite four-height synthetic proxy does not prove a full normalized`
- TeX line 49: `operator estimate, identify physical $h_0$ or arithmetic signs, pay arithmetic`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
