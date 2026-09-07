# TPC-414 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `ad284d89b62146e7996177ec7bb67f03a837426b12378a66d9a5ac3c99d945e7`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `e572b4d63ed85fc7025e563f9be5fde112babf8e1d6b53712d66b99b2fa6396a`; 1 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `67c6929b5564adf5c059252a0e939b920d04e7690a1f66b57fc923145d024e69`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Three-shell profile` | 17 | 1 | `HEADING_TEXT_MATCH` |
| `Exact observation` | 32 | 1 | `HEADING_TEXT_MATCH` |
| `Scope and reproduction` | 38 | 1 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `31` before writing and `31` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `2`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `69bec0211eae9d7c56a202e01acd7106941172e9a732471573cfa03b96e0858d`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 24–26 | `7b100f808d18d4052eeded8e2aca476db7e047c1abb646590cb246ebb1f82299` |
| D02 | \[...\] | 29–31 | `d2656677cd223d644d8f1cfbc5df78c4f5c8af0f15723669b48548a2a2077ed4` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 15: `the resulting finite row; no arithmetic theorem is claimed.`
- TeX line 35: `is a finite numerical value, not an asymptotic claim.  The independent checker`
- TeX line 39: `This one finite synthetic adjacent normalized proxy entry does not prove a full`
- TeX line 40: `operator estimate, physical $h_0$ or arithmetic signs, pay arithmetic $L^2$ or`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
