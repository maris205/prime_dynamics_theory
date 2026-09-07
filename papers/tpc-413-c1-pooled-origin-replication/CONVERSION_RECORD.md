# TPC-413 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `920a3aa9e490aebb0dce82528bc3ddbd04ecaf9607b846324a013f5512cce5c3`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `301dd2d4b573dd6b9419f08c87a2c7f0be40276f59f055d4f35d97aded435db4`; 1 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `6bbae7308131f3b95246027b65fe7303321a6cb16a6521b6a4d895d6e4165b40`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Representative replication` | 17 | 1 | `HEADING_TEXT_MATCH` |
| `Exact result` | 31 | 1 | `HEADING_TEXT_MATCH` |
| `Scope and reproduction` | 38 | 1 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `27` before writing and `27` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `2`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `129ae6023c4397a41e38e3bfa40339cc605c6b5cd6a576a4f14d97210d900a6b`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 23–25 | `7b100f808d18d4052eeded8e2aca476db7e047c1abb646590cb246ebb1f82299` |
| D02 | \[...\] | 28–30 | `d2656677cd223d644d8f1cfbc5df78c4f5c8af0f15723669b48548a2a2077ed4` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 15: `finite synthetic invariance result, not an arithmetic or twin-prime theorem.`
- TeX line 39: `This finite CRT-period invariance audit does not prove a full normalized`
- TeX line 40: `operator estimate, physical $h_0$, arithmetic signs or $L^2$, a fixed-power`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
