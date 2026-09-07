# TPC-383 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `32e89a786ef1a9e88d28ce06f2ace80b84423207a5dccef5da4d79292112f4e4`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `6b1777f09c513ea310783447b1e9bbb5266a737684f8d5758571edf775180bd1`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `7418e5141213d2a9a5705f607e57ff2b00c2a53599cc8809b11e205e362e989e`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question` | 28 | 1 | `HEADING_TEXT_MATCH` |
| `Protocol` | 36 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 63 | 1 | `HEADING_TEXT_MATCH` |
| `Verification and boundary` | 96 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `26` before writing and `26` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `3`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `c7326af374252b7c0eeba9005104218d8570e7f3c6bbd7e1c7c79c1e300a3963`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 47–50 | `5af6249e9e1d72c2d7b662652c8509330463e269a4d6c85eea5ecdf577d9cbcb` |
| D02 | \[...\] | 54–56 | `019534968a094a911cb13bf53b926b4587c3b33604baf58a26eaa4b0368ed1c7` |
| D03 | \[...\] | 70–73 | `64fbcc9c3b83e744a5657201102202a7543f9f8e039bb728ccb5c9c3fc11945e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{TPC-383: Local and Pooled Normalization in a Finite \(c=1\) Panel}`
- TeX line 16: `We test whether the finite origin stability observed in a normalized`
- TeX line 23: `with pooled high-\(Q\) spread \(10.104585338571119\%\).  This is a finite`
- TeX line 24: `normalization audit and does not identify an arithmetic source law or prove a`
- TeX line 34: `finite and response-blind; all four laws are retained as controls.`
- TeX line 103: `are absent, so this is not an official Route-A or Route-B verdict.`
- TeX line 111: `predeclared panel, mask, and normalization family & PROVED FINITE\\`
- TeX line 112: `72-row local/pooled replay & NUMERICALLY CERTIFIED / FINITE\\`
- TeX line 113: `all-plus high-\(Q\) transfer & NUMERICALLY CERTIFIED / FINITE\\`
- TeX line 114: `normalization magnitude shift & NUMERICALLY CERTIFIED / FINITE\\`
- TeX line 115: `source validity and growing uniformity & OPEN\\`
- TeX line 116: `Route-A / Route-B gates & OPEN\\`
- TeX line 123: `\texttt{FIXED\_POWER\_CREDIT}=0.  The next finite question is the`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
