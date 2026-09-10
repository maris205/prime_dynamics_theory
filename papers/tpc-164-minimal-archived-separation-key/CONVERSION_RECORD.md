# TPC-164 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `b637f3ea2e01c0e48d80d6ce4e5500b91a63727f709c3f3bcfd25f4aaf6bb279`.
- Bibliography: [references.bib](references.bib), SHA-256 `2e43a0ba8efd8e7a628e9255257f7a0dad7b8dfc0e5f8f91a4296b26b3376d68`.
- Preserved PDF: [tpc-164-minimal-archived-separation-key.pdf](tpc-164-minimal-archived-separation-key.pdf), SHA-256 `c8b620011d15c5c58f943fa741b16e2baff503f555f0dce488f0af74b9f0e10f`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `e74a17c971393232d715dbceae13d2b4fc51d8b641c771b0cbea3ba019206d35`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC160_164.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The finite addressing question` | 93 | 1 | `HEADING_TEXT_MATCH` |
| `Exhaustive theorem` | 149 | 2 | `HEADING_TEXT_MATCH` |
| `Quantifying the failed shortcuts` | 218 | 3 | `HEADING_TEXT_MATCH` |
| `What ``minimal'' does and does not mean` | 257 | 3 | `HEADING_TEXT_MATCH` |
| `Machine certificate and mutation audit` | 289 | 3 | `HEADING_TEXT_MATCH` |
| `Interface to local-to-global construction` | 304 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 318 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 329 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `60` before writing and `60` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `cb6cbfc39d15071923209c898a528273182cf4069a806467e524550dee039b2d`.
- Source theorem/proof environment starts: definition at TeX line 107, definition at TeX line 134, theorem at TeX line 151, proof at TeX line 175, corollary at TeX line 201, proof at TeX line 211, proposition at TeX line 240, proof at TeX line 251, proposition at TeX line 274, proof at TeX line 281.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 55–58 | `9aa9cd30ebb29c1add1cf2a6bc46dd5a48ea856d700cbc9d176664ae71a77ad4` |
| D02 | \[...\] | 61–63 | `16c40ba0b7a6797f09e805f8ad6d9a33e47c14c71531207dae1363dbc38ee7ff` |
| D03 | \[...\] | 99–102 | `2b84abc09895034579f4bd0f73debc2773b1c2c698916cb1e6739913b020abd7` |
| D04 | \[...\] | 110–124 | `eea86b33f7d30f8f83f20dde7f4d5698baf4a0b201e874e1201ef2928765de33` |
| D05 | \[...\] | 126–129 | `00e6eee736834991e3f8de3993cd4c6b3c155a305f5dbbd69e93438fe9b18d7f` |
| D06 | \[...\] | 136–139 | `6b71bf3e6003f935f251666d2c356fb6678ce316f7ea01ff00be5e04c860c0aa` |
| D07 | \[...\] | 154–157 | `4acf09ceb9aaae612e2c65a2ffac55882bb6fa8446c560137012600c5210eba9` |
| D08 | \[...\] | 159–162 | `e0158c02a58ca526ec7d5bd0bded8bd19e5d5fa2d4f7fd7f55901bd981092649` |
| D09 | \[...\] | 165–172 | `38ab1d44c60dfdf31a5302b95468c171b775944da313c94efdba189ff3730ef2` |
| D10 | \[...\] | 179–186 | `1e6717212e67f9319e32965de9394de46cdf3f1681c17e4947fd0ec109b9df9f` |
| D11 | \[...\] | 203–207 | `fb876ac215827e6c0064f3c8789d69d7ffd395dac467f1a97165b7074d059cf7` |
| D12 | \[...\] | 243–248 | `764a5824020bdd9d5d8462a9b26d8723650dda0f758f1cf02f77ca60d21999b2` |
| D13 | \[...\] | 309–311 | `8a052529aa50412fc439e37c3fd4538293483e10211d548ea5ae474716c704c7` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `pdfsubject={Exhaustive finite separation-key theorem},`
- TeX line 51: `\((\ell,k,d_{\rm nat})\) is not a row key for the \(2988\)-row frozen`
- TeX line 53: `over native keys.  We now solve the finite addressing problem exactly.`
- TeX line 78: `\noindent\textbf{Keywords:} fixed shift; finite archive; separation`
- TeX line 93: `\section{The finite addressing question}`
- TeX line 257: `\section{What ''minimal'' does and does not mean}`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:dictionary` → `../main.tex#L128` (existing project target or original TeX label line).
- Link relocation: `#eq:min-key` → `../main.tex#L156` (existing project target or original TeX label line).
- Link relocation: `#eq:injective` → `../main.tex#L161` (existing project target or original TeX label line).
- Link relocation: `#eq:injective-counts` → `../main.tex#L171` (existing project target or original TeX label line).
- Link relocation: `#thm:minimal-key` → `../main.tex#L151` (existing project target or original TeX label line).
- Link relocation: `#eq:min-key` → `../main.tex#L156` (existing project target or original TeX label line).
- Link relocation: `#thm:minimal-key` → `../main.tex#L151` (existing project target or original TeX label line).
- Link relocation: `#eq:injective` → `../main.tex#L161` (existing project target or original TeX label line).
