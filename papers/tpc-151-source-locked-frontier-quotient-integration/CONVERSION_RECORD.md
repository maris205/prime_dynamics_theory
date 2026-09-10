# TPC-151 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `6492a93eb6c701964a26a4ae1abad0099a42ca227a989da607ca32469fd3135b`.
- Bibliography: [references.bib](references.bib), SHA-256 `166d7c8fc11420025e0135ba4553a568a9a0863a02ce8003d7490537c0d1df79`.
- Preserved PDF: [tpc-151-source-locked-frontier-quotient-integration.pdf](tpc-151-source-locked-frontier-quotient-integration.pdf), SHA-256 `cbd1e1d8eca4bfe16a471d0bbc174711c4016b76327cf69be8cb6ff3e1c94bad`; 6 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `62ec51a9c96d3fab6205b860a40dbfb03d38dc53733e5b6a5133ce7a5efccad5`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC150_152.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The two inherited openings` | 113 | 1 | `HEADING_TEXT_MATCH` |
| `Canonical source locking` | 142 | 2 | `HEADING_TEXT_MATCH` |
| `The occurrence lift and four-map contract` | 182 | 2 | `HEADING_TEXT_MATCH` |
| `A real actual-core arithmetic corridor` | 278 | 3 | `HEADING_TEXT_MATCH` |
| `Route cells and the first missing antichain` | 318 | 4 | `HEADING_TEXT_MATCH` |
| `H9 and the split endpoint` | 347 | 4 | `HEADING_TEXT_MATCH` |
| `Source-locked integration theorem` | 383 | 4 | `HEADING_TEXT_MATCH` |
| `Deterministic audit` | 423 | 5 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 461 | 6 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 474 | 6 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `70` before writing and `70` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `18`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `cd04298a1e3e7212c948ae2bca4792e26eda62e636f0289f47df0c1a1a9cf99d`.
- Source theorem/proof environment starts: definition at TeX line 149, theorem at TeX line 163, proof at TeX line 174, definition at TeX line 201, proposition at TeX line 267, proposition at TeX line 298, definition at TeX line 333, proposition at TeX line 369, theorem at TeX line 385, proof at TeX line 403, corollary at TeX line 417.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 66–70 | `02865ed7d4f73181498abe93131c542fa2540dcb5ecfcd0b6896b5940d99bfb7` |
| D02 | \[...\] | 77–80 | `86af7150d94b0517e7b1671c119f27e71959006a97b0a44729c3f12a7aac9e73` |
| D03 | \[...\] | 116–119 | `262b00c058c624fb3c535483c9a87a27118a7462f00ff0eccf4a7f06b07bd7a7` |
| D04 | \[...\] | 125–128 | `1748ca5f728c498275d9fc0efd1d6aef3f35dd696854f3009453dfc6391472d4` |
| D05 | \[...\] | 135–137 | `01199e6f8901edc19e443de6d626c92b6040911b0d8b8aa5f436642b8098abf9` |
| D06 | \[...\] | 186–189 | `36b6f4a14d875b0bd0f0d24b7eaf46fb202bc0ac5c4931f22c416810c47dd7cd` |
| D07 | \[...\] | 203–205 | `7bac781cfdc268eae549248af0fdf2a44b4be66d18ab7d61109c198c07ae70c1` |
| D08 | \[...\] | 211–213 | `6687e7f2e672ae517df84917fbef2505acab0e2ba8bbe31e6bbbb8fa1b1be13f` |
| D09 | \[...\] | 225–227 | `5880532de8633b138b573d0cf4ee3cfb29e1777d918ea148563c6a95afbb8340` |
| D10 | \[...\] | 234–236 | `b97547caeb7cc11bf464e3b2f977a929ece1f3bea91a98a365fe0198bef383dc` |
| D11 | \[...\] | 244–248 | `61c6a74112b749876705c7fc2a4cc675a135b43bf98a6f27f4f83b89887156bc` |
| D12 | \[...\] | 250–259 | `7c354d3d4b8bc341d709b92649dfe578dc09875dda2fcd8166fdf95dfa26cf98` |
| D13 | \[...\] | 271–273 | `2166002b9294a7dc49962dccba5398f02c87c395d6178383dbbc643996db78b4` |
| D14 | \[...\] | 281–283 | `bfe956e84afc0f6888748b860052456e4dd41152b07ba008f58a3fef6a8a592e` |
| D15 | \[...\] | 285–287 | `b9f4305dfc95ef310b351384599d5da5f8fa8f940934d9044b82c19fe9c8ef99` |
| D16 | equation | 289–292 | `1ad75f5a83788d4947de51d70b7f19e5f83ad63f4a99ef214b836f5404857e2f` |
| D17 | \[...\] | 301–304 | `43c5ff40315808f76eac8a7316445224d795e3923783f64eed86edae4f24bdfa` |
| D18 | \[...\] | 357–364 | `328788f9dc9f40f2f9ba4f82411d66b5dbf97faa8fac8a494c60df97ce033956` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 36: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 37: `\newcommand{\Bhard}{B_{h_0,\delta}}`
- TeX line 56: `TPC-143--150 pursue the two openings left by the MVP4 audit.`
- TeX line 105: `The identity \(P_{h_0}^{\rm cut}=I\) is not a downstream`
- TeX line 107: `actual M\"obius core is not an all-prefix physical saving and has`
- TeX line 113: `\section{The two inherited openings}`
- TeX line 129: `where ETO denotes \texttt{ELIGIBLE\_TAIL\_OPEN} and FUM denotes`
- TeX line 130: `\texttt{FRONTIER\_UNMAPPED}.  The frozen finite sample contains`
- TeX line 154: `canonical content digests.  The bundle does not contain its own hash.`
- TeX line 160: `No collision-resistance assumption is used as a mathematical`
- TeX line 178: `The hash is not a logical edge and therefore supplies no theorem`
- TeX line 188: `\qquad P_{h_0}^{\rm cut}=I`
- TeX line 197: `This is a current-schema route obstruction, not a theorem that the`
- TeX line 239: `of the predicate ''shift equals \(h_0\).''  Thus`
- TeX line 240: `\(P_{h_0}^{\rm cut}=I\) cannot be substituted for a downstream`
- TeX line 262: `a theorem-backed disposition of every eligible-tail-open path:`
- TeX line 264: `class in one finite sample cannot discharge this second clause.`
- TeX line 274: `All actual \(Q_D,Q_Z,G,P_{h_0}^{\rm down}\) totality and intertwining`
- TeX line 306: `core and almost-scale scope.  It is not a theorem on the full`
- TeX line 311: `\eqref{eq:quotient} a synthetic model would discard a real arithmetic`
- TeX line 327: `The route list is a declared collection of tested cells, not a theorem`
- TeX line 343: `missing prerequisite and does not pretend that incomparable missing`
- TeX line 365: `The first may remain open at the arithmetic frontier; the second must`
- TeX line 376: `and determinant reserve is not a physical token.`
- TeX line 419: `actual-core arithmetic \(\Lone\) progress.  Neither is fixed-\(h_0\)`
- TeX line 443: `\item \(P_{h_0}^{\rm cut}\) used as the downstream selector;`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 8 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:quotient` → `../main.tex#L291` (existing project target or original TeX label line).
- Link relocation: `#prop:pointer` → `../main.tex#L268` (existing project target or original TeX label line).
