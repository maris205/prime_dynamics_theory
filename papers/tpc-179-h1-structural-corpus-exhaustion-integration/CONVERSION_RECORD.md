# TPC-179 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `ef3611d57741448950da204746c8e6bc3125a97a82d6eb1709dd25cb25a258be`.
- Bibliography: [references.bib](references.bib), SHA-256 `d0e9e20f2c8ac4cd19e44ca238ea13377f43f8c79ba9ab4f85f878f90261af2b`.
- Preserved PDF: [tpc-179-h1-structural-corpus-exhaustion-integration.pdf](tpc-179-h1-structural-corpus-exhaustion-integration.pdf), SHA-256 `56c2849b7d8f789e0ac26ce1b90650e8f2b3dea21994c6646d815bb9af927676`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8a418bcdc0bfdb49fca7f6968bcb78b44ff0529bb6e9f046857808fadc3f4eff`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC175_179.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Frozen source result` | 68 | 1 | `HEADING_TEXT_MATCH` |
| `Three structural roots` | 97 | 1 | `HEADING_TEXT_MATCH` |
| `The local-edge root` | 111 | 2 | `HEADING_TEXT_MATCH` |
| `The active-support root` | 118 | 2 | `HEADING_TEXT_MATCH` |
| `The representation root` | 130 | 2 | `HEADING_TEXT_MATCH` |
| `Recomputed antichain` | 138 | 2 | `HEADING_TEXT_MATCH` |
| `Scoped stops and legal continuations` | 186 | 3 | `HEADING_TEXT_MATCH` |
| `Literal fixed-\texorpdfstring{\(h_0\)}{h0} boundary` | 218 | 3 | `HEADING_TEXT_MATCH` |
| `Machine interface and regression audit` | 241 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 264 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 276 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `45` before writing and `45` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `842971e8f7d10fd1f898a3b06a4e2f6049d5097cfb0167f77d9cb4b1280393a8`.
- Source theorem/proof environment starts: theorem at TeX line 140, proof at TeX line 155.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 71–75 | `80ad66561cff2b96d9f5a9d7c08c210dc5d5b801596f6a0b18f15e67dcfb0dd9` |
| D02 | \[...\] | 81–83 | `df54a117a149ae8a6db8cc1726ded71d57741aa0d4bfe4b4e9711421306cf89b` |
| D03 | \[...\] | 88–94 | `df864d19cc0f1da6de15645179817cbf4b8a256d8067ad5c43e79aafff132524` |
| D04 | \[...\] | 100–106 | `71cfacb36627ad11922d77dcc56c8c4c69a07ff8566c2a0d15f4d06a7a740fea` |
| D05 | \[...\] | 122–125 | `529c8b695a0c3885916d8f7b58c0b09a8c820ba8e56d76a3600972c70a0b4d45` |
| D06 | \[...\] | 143–145 | `855dae46c905c5286571fdd276eab7f4eef141ed4a144abb6a5092cbb628114f` |
| D07 | \[...\] | 147–152 | `3209e536b8875c6fbd64b205ae6035e8cc45609e8d3831cb7ec3eb0baafb2382` |
| D08 | \[...\] | 192–200 | `07988b59e7dc5d81cbc5c0c34f9f79a30b678cb8927b51a414140feb1bc4f52c` |
| D09 | \[...\] | 221–223 | `adfb0bff65a402384677385d2a53eab39cbf86bce25c52752648efc417205ab0` |
| D10 | \[...\] | 227–233 | `3a2a1a4df719f97a97436f9e0d79f496cc56b2f7ad952bbb18f22365c231783f` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 64: `\(\Lzero\) executable audits, not fixed-phase or fixed-\(h_0\)`
- TeX line 85: `not a theorem that such edges do not exist in mathematics.`
- TeX line 156: `TPC-175 does not prove \(E\); it stops only the scoped extraction cell`
- TeX line 214: `Silently treating a synthetic witness as production evidence, or`
- TeX line 218: `\section{Literal fixed-\texorpdfstring{\(h_0\)}{h0} boundary}`
- TeX line 222: `h_0=2.                                                          \tag{9}`
- TeX line 230: `\text{eligible carrier with fixed-}h_0\text{ lineage}&=\text{none},\\`
- TeX line 231: `\text{fixed-}h_0\text{ arithmetic progress claimed}&=\text{false}.`
- TeX line 245: `node, full antichain, root ledger, scoped route cells, fixed-\(h_0\)`
- TeX line 257: `\item use of \(h_0=2\) as an arithmetic gain;`
- TeX line 271: `atom audits.  No fixed-phase or fixed-\(h_0\) arithmetic conclusion`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
