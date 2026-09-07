# TPC-388 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `96cf920c4e48f77910a929cc2ed5d367f3807993222d14e076cb320d63838ce6`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `a7571be727744f193d59e3aabdbf8141a6f39b62a157c3e85ad1bd0ba7c5b6bf`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2d570cd05ca63186bf4d7e8a1a85e9e5c95cdb8da5f93f33927f479a5f6417e0`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and boundary` | 29 | 1 | `HEADING_TEXT_MATCH` |
| `Finite proxy and transfer rule` | 48 | 1 | `HEADING_TEXT_MATCH` |
| `Certification` | 77 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 87 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion and next clue` | 117 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 129 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `42` before writing and `42` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b21592711ad8dc0713a92603278dc7b00ebf6a07edec1379c8517edc9ccbf5fe`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 40–44 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |
| D02 | align* | 51–55 | `53f8042701001239a26c5943d04cbe21892fe5640fbb65ec0f9b96b101be0d31` |
| D03 | \[...\] | 66–70 | `173ed6d0321d344e06daf7b15afc9323ea7e48f64064f74234df621940fd853b` |
| D04 | \[...\] | 72–74 | `a8eac4f238e893cd1f081dbe75e7990752bf00b358dc3a2c90e5d509b48dd09a` |
| D05 | \[...\] | 124–126 | `d44fa6acc5cba47dc5ecaeff3122ad8fbe36f541f99bc3aea9cd51494fba9fa0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 24: `predeclared 3\% finite cap; the worst parent-transfer error is`
- TeX line 25: `$0.0234026666$.  This is finite origin-transfer evidence, not an`
- TeX line 26: `origin-uniform theorem or an arithmetic result.`
- TeX line 32: `the finite $512\to1024$ comparison.  The next minimal question is whether the`
- TeX line 43: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 48: `\section{Finite proxy and transfer rule}`
- TeX line 50: `For $p\in(Q,2Q]$ we use the finite kernel`
- TeX line 114: `slopes is $0.0595582579$, so the finite success does not imply that the two`
- TeX line 119: `The strongest positive result is a response-blind finite transfer of a slope`
- TeX line 122: `uniform in origin or count.  The reusable structure is a hashed parent-slope`
- TeX line 127: `No arithmetic reassembly or twin-prime conclusion follows.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `papers/tpc-388-c1-cross-family-slope-transfer/` → `..` (existing project target or original TeX label line).
