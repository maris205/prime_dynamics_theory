# TPC-169 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `1790ad09df28c3e5f3a3b3bc556f745204edcc7df15c3614a05bda19817f475c`.
- Bibliography: [references.bib](references.bib), SHA-256 `53730c763b25c828157cb1ff9a52d364b5571cde643df2e1d250d5637449410f`.
- Preserved PDF: [tpc-169-maximal-prefix-phase-metric.pdf](tpc-169-maximal-prefix-phase-metric.pdf), SHA-256 `9e5432e3fafa1c63f5b75f3abaae18f62c7063391ea5b0a2bba4036153d6fa3d`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `3d497f1e06e4091e36316bb0f7ce87bfb260566546e678ac92267d7001ec4b1e`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC165_169.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Ordered fiber prefixes` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `The dyadic maximal lemma` | 92 | 2 | `HEADING_TEXT_MATCH` |
| `One phase set for all actual-core endpoints` | 134 | 2 | `HEADING_TEXT_MATCH` |
| `Power envelope and exact status` | 186 | 3 | `HEADING_TEXT_MATCH` |
| `Relation to the atomic endpoint barrier` | 216 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducible audit` | 236 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 248 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 259 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `50` before writing and `50` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `17`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a089e78fd055f4b516a336306adaec5ab8aa2203e13ec424f02ebd85bc30afc6`.
- Source theorem/proof environment starts: theorem at TeX line 94, proof at TeX line 106, theorem at TeX line 136, proof at TeX line 157, corollary at TeX line 167, proof at TeX line 176.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 67–70 | `85f1ffda949135dc90830709c7d7ece8da14db5e51206693c978ba3a3c2c05a1` |
| D02 | \[...\] | 73–75 | `f1c70ec41d271e458e852fd28e2da42818313c069e5cc75103a2eb9ccf5e52f2` |
| D03 | equation | 77–80 | `5b6b354b6ae551bd47bd84f06fac3eb7ff75e9fc5c16fdeb7dff2c1bde7759c8` |
| D04 | \[...\] | 82–85 | `65578ec55c39fb5e69dbd5d1e6b07bac86f1fffa02ca12ca189f90a8d1a72e52` |
| D05 | \[...\] | 87–90 | `28d87b385db4c1b44b28a629425f8137243409fb070029369d25cdcbf2dde57a` |
| D06 | equation | 96–103 | `aee172ae5b31eab98c59a1ae320b47fd3c9a8af8268b8ef781a270dccaea9dcf` |
| D07 | \[...\] | 116–119 | `89e6542b591fd65d0377647ab5682e2ee6cf00061ecc8de99810896a92ee55a9` |
| D08 | \[...\] | 122–126 | `ceeef887a070ad756dcca854b1b21e0223ec02c2fc35e5833c2af8a1f44b55a3` |
| D09 | equation | 138–146 | `21a3e45ba7d02812731e2e381961108328705e678ed1802c8273a38a82056cc5` |
| D10 | equation | 148–154 | `67a37e0eee5f22bad326a2619a85023e2f66f906229cf936bcea2b04ebcec62f` |
| D11 | \[...\] | 160–163 | `4af17142aac3bc0293dbfbe23f10518b0fb914ae1c9f24ab7760b91fe194316b` |
| D12 | equation | 170–173 | `1b2e02c2291bb35917149f7c2e4b700115398755a13ae73a4080c38e5015b341` |
| D13 | \[...\] | 189–192 | `fee21ef24d85aba88092b70dfc8186c35622757cce8aaeb5915a342eb861ec52` |
| D14 | equation | 194–198 | `30610b53b2d7cd046904ea6d4be29c80077361cc1c161df94061b048098439b6` |
| D15 | \[...\] | 201–204 | `b07f2be552b4f42648381e556a30ee93267c2e023995c6b632108e000a304082` |
| D16 | \[...\] | 205–212 | `5b9a8d984cf6a76e066de9336d6622784e32b660d19264da8966e34183c7d2bd` |
| D17 | \[...\] | 222–229 | `d92a4557d29f02e3238efd4289b28b821d42d5334e23e953c87a08e4d950321c` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 37: `variation atom exactly at its selected endpoint.  We open a different`
- TeX line 43: `endpoint but averaged in phase; it does not control a specified phase`
- TeX line 58: `exceptional set of additive phases.  The result does not imply`
- TeX line 60: `TPC-159 scale shadow by phase averaging is not a physical endpoint`
- TeX line 94: `\begin{theorem}[Finite dyadic maximal Parseval]\label{thm:abstract}`
- TeX line 130: `This is the finite dyadic maximal argument commonly associated with`
- TeX line 183: `scale shadow of TPC-159 \citep{WangTPC159}.  It does not assert that`
- TeX line 231: `\(\mathsf{O161.bad\_endpoint\_pointwise\_core}\).  It does not close`
- TeX line 241: `It evaluates the maximal function on a finite Fourier grid as an`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:abstract` → `../main.tex#L102` (existing project target or original TeX label line).
- Link relocation: `#thm:abstract` → `../main.tex#L94` (existing project target or original TeX label line).
- Link relocation: `#eq:count` → `../main.tex#L79` (existing project target or original TeX label line).
- Link relocation: `#eq:measure` → `../main.tex#L153` (existing project target or original TeX label line).
- Link relocation: `#eq:measure` → `../main.tex#L153` (existing project target or original TeX label line).
- Link relocation: `#eq:measure` → `../main.tex#L153` (existing project target or original TeX label line).
- Link relocation: `#cor:shell` → `../main.tex#L167` (existing project target or original TeX label line).
- Link relocation: `#eq:measure` → `../main.tex#L153` (existing project target or original TeX label line).
