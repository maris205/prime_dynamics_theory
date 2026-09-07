# TPC-403 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `64a412a9b1f0a3248addf7c4830ae9eb31d11e5c0d2a44159d03a7cf898b4379`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `473ace2fe82dde740d2f0979e2835a3bf8096c439562aecd37977cd7922fc8e9`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `3a0e0b1e6f6603577b3f625c11f923600519b91fc0b5eb98b6c119b91797c6cf`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Finite object` | 20 | 1 | `HEADING_TEXT_MATCH` |
| `CRT construction` | 32 | 1 | `HEADING_TEXT_MATCH` |
| `Exact certificate` | 56 | 2 | `HEADING_TEXT_MATCH` |
| `Scope and obstruction` | 78 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 95 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `37` before writing and `37` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `bcf3106106dc53087f18c0e82daf61562130ccedc7307c5f845e97d514afe28c`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 24–28 | `3526bd35e1e392ebdff1d5b767cc42f45f9afe5f2aa75a9ee1f8811393c2dcd5` |
| D02 | \[...\] | 34–36 | `4ae0018a74ab2ece519a9d9f11d9639123cb37d40f1dd960317599fe983d4db2` |
| D03 | \[...\] | 43–46 | `5c8f10cc12107548975b2763efbd18fd94bd430de749e6f549d004aad1f1d32c` |
| D04 | \[...\] | 49–52 | `d138d57b43b23dce9ead74fe2a4bb1ecc9855ddadce28104bf2b37a043059330` |
| D05 | \[...\] | 86–93 | `89bec58eb194381a48c018dafe610ea43db1e32ed5d8a71f9c369ee851506eeb` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 10: `We give an exact adversarial construction for the finite signed coefficient`
- TeX line 11: `model isolated in TPC-402.  For alternating signs on any finite set of primes`
- TeX line 20: `\section{Finite object}`
- TeX line 30: `the signs are the declared synthetic law $\sigma_i=(-1)^i$.`
- TeX line 79: `The theorem is parameterized by a finite prime set and an unbounded positive`
- TeX line 80: `origin class.  It does not say that a predeclared bounded interval, including`
- TeX line 82: `It also does not lower-bound a locally normalized entry: the geometry`
- TeX line 84: `signs remain a synthetic modeling choice rather than the arithmetic source`
- TeX line 88: `\texttt{PROVED\_EXACT\_FINITE},\qquad`
- TeX line 91: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 97: `proof package, and PDF.  No arithmetic sign theorem or twin-prime result is`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
