# TPC-174 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `912398392187568bc2f77f6c0f960f481286beb55f6c4a43ec0a0a4300ebd448`.
- Bibliography: [references.bib](references.bib), SHA-256 `9afc1c375880f5f125463bca5d47b9ea4869127ea38ec9c721410f5f3db7b3b8`.
- Preserved PDF: [tpc-174-local-occurrence-edge-witness-schema.pdf](tpc-174-local-occurrence-edge-witness-schema.pdf), SHA-256 `975d1ecc72aee0fd14d5952f7fe83e0fac48388d3b2f7becc9813f6802ebb6b1`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `739d40b75aaa1dcfdf27ba1f7c138d3055d3cc8d1b7378452cc4d899aec342df`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC170_174.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Source contract` | 54 | 1 | `HEADING_TEXT_MATCH` |
| `Local completeness` | 81 | 1 | `HEADING_TEXT_MATCH` |
| `Finite verifier theorem` | 97 | 2 | `HEADING_TEXT_MATCH` |
| `Synthetic nonvacuity and production state` | 135 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall` | 162 | 2 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 170 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `26` before writing and `26` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `2c0b95ab73426b9bf907822b282ebd4a432944499fdbf953e76f5178a433fab2`.
- Source theorem/proof environment starts: definition at TeX line 64, definition at TeX line 83, theorem at TeX line 99, proof at TeX line 112, proposition at TeX line 122, proof at TeX line 128, theorem at TeX line 146, proof at TeX line 156.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 57–60 | `6a1eb032aee38f1d1306cad22f697a89cbc0272008385b4a6e6d3d0e7a736d91` |
| D02 | \[...\] | 66–69 | `3c73676a206af379cdbdd391df81cfdce6c7a9603d48aab73d42db7870d4305d` |
| D03 | \[...\] | 86–89 | `c9588e70f944aaefbf0f0c9b7a1eed4ae1968c7a1d795af540464ca9d1ce1da4` |
| D04 | \[...\] | 138–140 | `4ebaecb551a2dd2d0a26eb2850f847bbc40752266fd1d3fe261bfe67d5e2d70d` |
| D05 | \[...\] | 148–153 | `5648fc2ca37c820191c1f9e9103767c6ea02bff2baf074535a7ebf5d78004669` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 37: `frozen TPC-133--172 theorem corpus.  This does not remove the need for an`
- TeX line 41: `fixed \(h_0=2\), physical-normalization lineage, and source evidence resolving`
- TeX line 45: `A deterministic verifier proves finite internal consistency for supplied`
- TeX line 48: `fixture has weights \(1/3,2/3\) and is explicitly synthetic \(\Lzero\)`
- TeX line 51: `not-testable; no arithmetic \(\Ltwo\) conclusion is obtained.`
- TeX line 62: `cut row, not a downstream occurrence \citep{WangTPC165,WangTPC173}.`
- TeX line 67: `(\kappa(c),o,\lambda,h_0,\nu,\mathcal S),`
- TeX line 71: `\(\lambda\in\mathbb Q\setminus\{0\}\), \(h_0=2\), \(\nu\) is the physical`
- TeX line 84: `For a finite nonempty declared cut set \(U\), every \(c\in U\) has a finite`
- TeX line 97: `\section{Finite verifier theorem}`
- TeX line 106: `\item fixed \(h_0=2\) and physical normalization agree edgewise; and`
- TeX line 116: `sum in \(\mathbb Q\).  Equality checks enforce \(h_0\), normalization and`
- TeX line 119: `These are precisely the asserted finite predicates.`
- TeX line 123: `Verifier acceptance does not prove the mathematical truth of a cited`
- TeX line 129: `The verifier checks finite records and their source joins.  It contains no`
- TeX line 135: `\section{Synthetic nonvacuity and production state}`
- TeX line 142: `is \texttt{SYNTHETIC\_L0\_ONLY}; its source locators are deliberately null`
- TeX line 143: `and its source ID is \texttt{SYNTHETIC\_AXIOM\_L0}.  It is not a production`
- TeX line 158: `qualifying-claim map.  That map is empty.  The synthetic fixture is rejected`
- TeX line 164: `The schema and verifier are finite \(\Lzero\) interface results.  They do`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:conservation` → `../main.tex#L88` (existing project target or original TeX label line).
- Link relocation: `#eq:key` → `../main.tex#L59` (existing project target or original TeX label line).
