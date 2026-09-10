# TPC-201 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `4f89507c4d994e77fa49ebfe5ed2be2400c9eb19bebeaf9b8471abe0abde2562`.
- Bibliography: [references.bib](references.bib), SHA-256 `e3de68e5a5b78731b757215d9d557348d348c812eab9b8575355d063f28f59c5`.
- Preserved PDF: [tpc-201-degenerate-shift-fejer-absorption.pdf](tpc-201-degenerate-shift-fejer-absorption.pdf), SHA-256 `d96bc644375539382c553c4ce1b9e85a2eefdb1b9976b7c518b410853e62bfe8`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `3efe3bd3ace3925455503b879ec117762bd3a443c3539c7f7f9408f4530f8a30`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC200_204.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Target contract and source boundary` | 25 | 1 | `HEADING_TEXT_MATCH` |
| `Imported normalized inequality` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Remaining gate` | 80 | 2 | `HEADING_TEXT_MATCH` |
| `Loss, level and scope ledger` | 87 | 2 | `HEADING_TEXT_MATCH` |
| `Machine certificate` | 102 | 2 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 111 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `29` before writing and `29` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `734dc8cc751d896c0636cb3fddbe48d197367275f2fb7618de8664c69303ab9f`.
- Source theorem/proof environment starts: theorem at TeX line 52, proof at TeX line 72.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 39–43 | `b1059994e517644c68090412e3d3fc2b999c2f11ed3b25309415ba88be98d654` |
| D02 | \[...\] | 45–48 | `b57445dd7b3f3cf42a6afae3c66c787b7d37faaa140d9650de845686d7c61435` |
| D03 | \[...\] | 58–60 | `dfa0a34f8dcd374020d78d80d4cb826994af9329fb734d4adf7476c7feff8514` |
| D04 | \[...\] | 64–68 | `e55d7134b8ce770cbfb76307c35eacddc0c9cfa1b3f5466fdf229f25c49a5958` |
| D05 | \[...\] | 89–91 | `46373fd3df8d2ac99272a19b98c69dce57a3cbd860e9c8132ea2abed6963bca6` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 26: `The target has six simultaneous axes: actual fixed-\(h_0\) packet,`
- TeX line 29: `support.  The value \(h_0=2\) is source-backed data only.  Repository hashes`
- TeX line 53: `Assume \(3\le H\le N\).  For the unique degenerate cell`
- TeX line 83: `rows of TPC-200.  The missing theorem is therefore a uniform local or`
- TeX line 90: `\texttt{UNIFORM\_\allowbreak{}NONDEGENERATE\_\allowbreak{}FOUR\_\allowbreak{}MOBIUS\_\allowbreak{}OFFDIAGONAL\_\allowbreak{}POWER\_\allowbreak{}BOUND}.`
- TeX line 103: `The adjacent canonical payload freezes the formula or finite witness,`
- TeX line 107: `constant leaves.  The checker recomputes the finite certificate and executes`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
