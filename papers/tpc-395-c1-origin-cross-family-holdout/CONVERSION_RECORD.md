# TPC-395 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `c7cd011abff865d31669d9b74e429ee23f0d5550ad30664adbb60cf5b1cfa99a`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `da7386adbd43e71eea3a19c503c57ff0ba055b7f3c0346489f1c300f7da1795f`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `b9592710f7e86fbbdd9a9f10e9872a092a483949e1916f43447201ed70e0e7a6`.
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
| `Finite proxy and cross-family protocol` | 50 | 1 | `HEADING_TEXT_MATCH` |
| `Certification protocol` | 81 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 93 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and next clue` | 134 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 154 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `28` before writing and `28` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `5f9ae347cf993140d71b9c4a74b81666f89db677d3adfabb009f13456a6ae1c8`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 41–45 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D02 | align* | 53–57 | `1523c178a1e7cea0660f3469721d0ba97a206c9acc487e57603ea1c06cdbd611` |
| D03 | \[...\] | 65–68 | `cd39c8fab23e43938c931a1745f859c29e43adf9cf9b95616863a1c98608ee03` |
| D04 | \[...\] | 72–74 | `e9f9520709fd6f1f2ebe3c593031bf3b675a2a7120361eeca8d95b7a2ba2c12c` |
| D05 | \[...\] | 115–120 | `e1a45cc423fd8de45319f9929d5bf06f096d13b3cf356dbeaf4c9672206daa1b` |
| D06 | \[...\] | 147–149 | `8faf4f2e43c963a19f3d7ba87a6874b6ec3a58bf298450d9d92abbe71463db36` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 8: `\title{TPC-395: Cross-Family Holdout of a Finite $c=1$ Origin Obstruction}`
- TeX line 18: `TPC-394 found a law-dependent origin-spread split on an eight-origin finite`
- TeX line 26: `holdout-transfer cells pass a $3\%$ cap.  The finite spectral cap fails on all`
- TeX line 27: `24 all-plus rows and the Schur cap fails on no row.  These are certified finite`
- TeX line 28: `proxy observations, not a source-valid, asymptotic, arithmetic, Route, or`
- TeX line 44: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 47: `proof and Bridge-B artifacts are fail-closed finite evidence only and cannot`
- TeX line 50: `\section{Finite proxy and cross-family protocol}`
- TeX line 93: `\section{Finite results}`
- TeX line 129: `maximum absolute error $0.021220574691123151$.  The finite spectral cap fails`
- TeX line 131: `These envelope statements are scoped to this finite proxy and do not imply a`
- TeX line 141: `or single-normalization explanation, but it does not identify a source-valid`
- TeX line 152: `No arithmetic power credit is assigned.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
