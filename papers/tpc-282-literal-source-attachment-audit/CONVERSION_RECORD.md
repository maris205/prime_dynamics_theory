# TPC-282 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `928077a9bd66c38f38bd0a9ee65d7b903ff25814`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `85b4183e583e1c37bb4168760d5b7c1a0cdaab530b3ab08b26b25a2108faf1ae`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `977258ddfdc91cac679c10108cfbc1569390abcb36a26f597c259e87686b9dec`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `3709d8acec4140561ef1a1432f2d92cffb12964bccdaa3d5f2836113f7d5f3a8`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `bdf4b173819af62e6c9cdb20204f76dcea9e894ff2c1c7428d39be513631e984`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC280_284.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 39 | 1 | `HEADING_TEXT_MATCH` |
| `Projection formula and attachment coefficient` | 76 | 2 | `HEADING_TEXT_MATCH` |
| `Finite source-lock result` | 116 | 2 | `HEADING_TEXT_MATCH` |
| `What the result does and does not buy` | 173 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility and claim firewall` | 195 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 210 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 220 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `57` before writing and `57` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `9bf88512c036e5cdda7e6077687c0fa1e6c17165f6c951f4ea7259e5b9ff9e2a`.
- Source theorem/proof environment starts: proposition at TeX line 88, proof at TeX line 102, theorem at TeX line 118, proof at TeX line 130.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 44–46 | `247b9caaa4fa69d2a0230fb783d46e5b3960336e9b981ba18bde65f2e014376f` |
| D02 | \[...\] | 49–51 | `6d238ed66ba7d47d6484086019a49ca968561b6b8714bd2a01ff54159cd31a0f` |
| D03 | equation | 61–66 | `3022a07cecc6ca9506cd6358db51d498daa5a3b419912ce18dca0f52ab393416` |
| D04 | \[...\] | 68–71 | `5edc095cbfaab1ff244021f1f8917be8d355889392a7d8f9f3348a8724b4a12e` |
| D05 | \[...\] | 80–83 | `34799f472513fcb783a9180f56d189498cd58f870c5676fab3a452cf809af6ff` |
| D06 | \[...\] | 90–93 | `41040f42f40b8f5371edb9af15dfa195cd24025a882791c2c14715fe62789708` |
| D07 | \[...\] | 96–99 | `bd44115ed0d9bd8be24eceb8556dfbd47379af4736e4925254150d10f0043213` |
| D08 | \[...\] | 124–127 | `915ae7d0dea8518710bbb6f164b7878ef9b93a5b07ac10cae0c2223f56b1a9ba` |
| D09 | \[...\] | 180–184 | `686830f876c72e02705854172dc503fb70f4f4f77a0614784748f7f844e6c9a8` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 27: `registered finite schedule without replacing the source by a model functional.`
- TeX line 34: `only about $3.36\times 10^{-5}$.  Thus the finite source lock is real but weak;`
- TeX line 35: `it supplies neither a uniform asymptotic nondegeneracy theorem nor fixed-power`
- TeX line 41: `The four-packet analysis records a source vector $\beta$, a literal finite`
- TeX line 47: `The arithmetic readout is not an arbitrary dual vector.  It is the actual`
- TeX line 52: `The purpose of this paper is to audit this scalar on the frozen finite source`
- TeX line 53: `chain.  It is not to infer a power law from a finite table.  The distinction is`
- TeX line 74: `literal prime-power weight minus the finite comparison profile.`
- TeX line 113: `side of zero.  This is a finite, reproducible predicate rather than an`
- TeX line 116: `\section{Finite source-lock result}`
- TeX line 168: `The row at $X=256$, exponent $2$, is not a typo: the finite source attachment`
- TeX line 169: `changes sign there.  A sign change does not invalidate the finite nonzero`
- TeX line 173: `\section{What the result does and does not buy}`
- TeX line 175: `The finite result resolves one ambiguity left by an abstract equal-norm`
- TeX line 177: `It does not resolve the uniform question.  In particular, the minimum of`
- TeX line 183: `\label{eq:open}`
- TeX line 185: `is proved here.  Such an inequality would have to be uniform on the same`
- TeX line 191: `certificate supplies finite evidence for that identification, but neither the`
- TeX line 193: `the arithmetic $L^2$ gate, fixed-power credit, and full Gate B remain open.`
- TeX line 206: `These checks establish a finite numerical certificate.  They do not turn a`
- TeX line 207: `finite source scan into a theorem uniform in $X$, and they do not claim a`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:operator` → `main.tex#L65` (existing project target or original TeX label line).
- Link relocation: `#tab:rows` → `main.tex#L147` (existing project target or original TeX label line).
