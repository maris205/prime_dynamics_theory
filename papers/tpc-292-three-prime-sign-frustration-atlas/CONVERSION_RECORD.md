# TPC-292 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `7bba57e68d04514ee33ab2192a507a1f4edfebab`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `76ff5c2f97c72e8bfb9a05bf126365130cca5f01cfd0d18f2006b3785e523add`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `867db1a104e68fb3fdb4f512f18505434970a2bc3c597180b33f867a618c1aa6`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `aee858d1bb32921a768af3b1a25670eaa0979b3744eb6b0ee9c34cd573628f15`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `14f762bc4bbbcc4cc41a1ae997d2efea7acdd77f284b8085a59243f65358e0e4`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC290_294.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Position on the twin-prime route` | 48 | 1 | `HEADING_TEXT_MATCH` |
| `Physical Gram model` | 65 | 1 | `HEADING_TEXT_MATCH` |
| `The compatibility theorem` | 89 | 2 | `HEADING_TEXT_MATCH` |
| `Three-vector Schur residual` | 124 | 2 | `HEADING_TEXT_MATCH` |
| `Exact finite protocol` | 158 | 2 | `HEADING_TEXT_MATCH` |
| `Finite atlas` | 174 | 1, 2, 3 | `UNMAPPED_OR_AMBIGUOUS` |
| `Interpretation and claim firewall` | 234 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility and conclusion` | 260 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 279 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `59` before writing and `59` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `f8520f4773d948eaa5e5ecdd177ba50ef03983814fb475402c52ed229a288fb6`.
- Source theorem/proof environment starts: theorem at TeX line 91, proof at TeX line 104, remark at TeX line 117, proposition at TeX line 126, proof at TeX line 137, corollary at TeX line 146.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 36–39 | `647a3d7689fea6870121bf0860c639bd59e6532a8c34e2c009888fa4c4d463ec` |
| D02 | \[...\] | 70–74 | `a641d953a37284c10446dcf660c55e3b027e135132e489b2ff3d09a4ad996782` |
| D03 | \[...\] | 76–79 | `7bf26faa1f7a694abbe30d59293002d32056fca79e9fbac76dc1d60940e5d2ee` |
| D04 | \[...\] | 81–84 | `977ad19ae809052c03670946bec8c65cc84549408fb167c933b749396273fec3` |
| D05 | \[...\] | 94–97 | `978869483022639d4661aa2f984df97246666035a56ebad202cdbb90f6d40f58` |
| D06 | \[...\] | 99–101 | `c4e2947f4909865148f86cd52cf5e614b771a93546df28460f05641704619866` |
| D07 | \[...\] | 111–114 | `2daf5df071fdf3b763b45f4d731764b1becf8a0f44b5ed383bd4bcd9df34fadc` |
| D08 | \[...\] | 129–134 | `5297b168cdef17bb91d606a029a221223ad0b61dd931fe7b40d8eae757159afb` |
| D09 | \[...\] | 164–166 | `2e87eb0fc165b3b73c31a5d5216cf682cd30c863996382ee7c78fe6528f9f66c` |
| D10 | \[...\] | 199–201 | `35df03285295f883bbcffbe55e3fd7831eedd3f70d4d10cad6930a3381b5cd97` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 42: `with positive normalized Gram volume in all 5,727 cases.  The finite atlas`
- TeX line 44: `does not establish a growing-shell compatibility theorem, an arithmetic`
- TeX line 62: `structural probe on the road map, not a claim that the finite grid represents`
- TeX line 120: `The theorem is a statement about a signed triangle; it does not optimize`
- TeX line 128: `$M=G_{(j,k),(j,k)}$ is positive definite.  Then`
- TeX line 149: `semidefiniteness of a Gram matrix, and is positive exactly when the three`
- TeX line 158: `\section{Exact finite protocol}`
- TeX line 174: `\section{Finite atlas}`
- TeX line 179: `\caption{Global exact-rational finite census.}`
- TeX line 231: `sign-frustrated triangle.  Geometric near-dependence therefore does not by`
- TeX line 236: `The finite experiment closes one uncertainty and exposes another.`
- TeX line 245: `\item The nine anti-alignable triangles are localized finite exceptions.  A`
- TeX line 252: `numerical claim is the complete finite atlas on the declared grid.  A`
- TeX line 255: `conclusion remain open.  The Session-named Route-A/Route-B evaluator files`

## Conversion limitations

- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
