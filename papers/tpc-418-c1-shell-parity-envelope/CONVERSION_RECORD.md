# TPC-418 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `2ed5fa45c0bdd4b406431901e7dc9bd6566da0d7322fb79abe69440cf645cd76`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `61919cb38b2dee011292c11d8d96ec8542b896fc102b8dece22bb13dcd34b049`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `7ce37f8b1c7f65b4a00713cf20f1202bc52ce868bee02a6e563312fc6694e72a`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Finite family and signs` | 18 | 1 | `HEADING_TEXT_MATCH` |
| `Scalar envelope` | 30 | 1 | `HEADING_TEXT_MATCH` |
| `Exact matrix bound` | 44 | 1 | `HEADING_TEXT_MATCH` |
| `Audit and scope` | 60 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `48` before writing and `48` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `7e080365c92124b0c74328af8bef2a66d59f8beaa597d644da82c2095992991c`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 23–26 | `7a326e687e19ba130a35c490033727dc9bc25937e2eb05ba7388dfeefc69ce38` |
| D02 | \[...\] | 34–36 | `99bde3a0d0dc33c3d36b582b1ce094bc1668f23670f03203d64c32fa43a02b3f` |
| D03 | \[...\] | 41–43 | `7142effd2a3c9176a2618449b8e903a958053c6a95720c18c2a9f0b11523b12d` |
| D04 | \[...\] | 47–50 | `096b6f791c39a5de903e80e5fa8a5a46c0e41760a890383e589b76a484980c7f` |
| D05 | \[...\] | 56–59 | `15ed6190607577c03d0e4104553e11e7bad620c0bed5f447b219f38fe66010be` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 4: `\title{TPC-418: A Finite-Family Shell-Parity Envelope}`
- TeX line 9: `We prove a finite-family synthetic envelope for disjoint ordered complete`
- TeX line 15: `$\|Z\|_2\le2/(a_{\min}\sqrt H)+16B_*/V_-$. The result is finite and synthetic`
- TeX line 18: `\section{Finite family and signs}`
- TeX line 64: `This is a finite synthetic envelope, not a growing uniform theorem, and it`
- TeX line 65: `does not identify physical $h_0$, prove arithmetic signs or $L^2$ savings,`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
