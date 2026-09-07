# TPC-334 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ba1fb3efe59e51e62f64f4dcb607bd390b4b4062`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `e1f41abbb6164e2e2765240cbd83246f0473e8bb81d927eb14bfb50181c1d79a`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `9df5253f498c64db219704c6dc9ed06d78fb5c10f22a513b099791a8d50af85d`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `5ec70204ea42a1fa123e4c075a16a1b614c924b7643291e8496c7dad1a902093`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC330_334.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 35 | 1 | `HEADING_TEXT_MATCH` |
| `Declared finite source` | 51 | 1 | `HEADING_TEXT_MATCH` |
| `Exact support partition` | 75 | 2 | `HEADING_TEXT_MATCH` |
| `Protocol and finite certificate` | 97 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 117 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and firewall` | 159 | 3 | `HEADING_TEXT_MATCH` |
| `Next question` | 188 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `48` before writing and `48` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `11`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `75396bd39d22309ae7debb5d2f911ed872645b6a905baa84e7bb5f92f2bdcf69`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 38–40 | `f81d6521f6385319fa06838fcfcf489184b2238703b33899dcdb9ea2cccff63e` |
| D02 | \[...\] | 54–56 | `ef00deb1077ad608cf8719ca830a5278889cb260b18a0c1c71d2acd970398f30` |
| D03 | equation | 58–62 | `da8a161d13ac8a162227563a1a45e9c5d1ffad5596a4af4137da1e269dfbf825` |
| D04 | \[...\] | 68–71 | `a01cce3c77052e830feaf24d948b8282ffbd530e3b01308223226cf758730e15` |
| D05 | align* | 80–84 | `0f3ab5a027ad35c6c602681e25e692567d585f8a6d685bd291bc28a21f2e0ea1` |
| D06 | \[...\] | 86–88 | `6478749b808edbe41c3b94bff7bfb2e508067bc7f89c079460d3bb1d9aca6c5e` |
| D07 | equation | 90–92 | `4ec924a46cdcea5ad475f76e1424d8f87a9dc1d392c6a4f431e09ddfbf09fdc5` |
| D08 | \[...\] | 105–107 | `85cf4f97c14e243747adc7adaf39a817ea026e13ebf9268765feecac51e62739` |
| D09 | \[...\] | 139–142 | `75274392a0b9a4c1131d91036fec5b4ec185b902628dbc53a01a8b6237d1f828` |
| D10 | \[...\] | 144–147 | `3af4e4927b1fc09fa477db7825d31fc865142c9c308507604801b11796e8b8c5` |
| D11 | \[...\] | 178–183 | `149cbffc2de2ddc69adfc9b91dce5e6d9e2c1db863debeaba5777340e9588053` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 11: `\title{Cross-Term Support in a Finite Twin-Prime Source Model\\`
- TeX line 21: `The preceding source-polarization audit found a substantial finite cross term`
- TeX line 29: `at most $0.2865191\%$.  This is a finite support obstruction to using the raw`
- TeX line 42: `cancellation on six finite windows.  Its next clue was to determine whether`
- TeX line 48: `coordinates are relevant to the finite source norm, but they are not twin`
- TeX line 49: `primes.  We therefore report masses, not a prime-pair theorem.`
- TeX line 51: `\section{Declared finite source}`
- TeX line 57: `The source is the parent-locked finite model`
- TeX line 63: `Here $\Lambda(p^k)=\log p$ and is zero otherwise.  The finite comparison`
- TeX line 67: `The cross term is the finite sum`
- TeX line 89: `Then finite additivity gives`
- TeX line 97: `\section{Protocol and finite certificate}`
- TeX line 109: `only a finite additivity check.`
- TeX line 112: `and reverse finite-tail product order.  A stress suite mutates row geometry,`
- TeX line 114: `are rejected.  These controls establish a finite certificate, not a global`
- TeX line 152: `The finite observation is therefore specific and useful: the raw source`
- TeX line 155: `prime.  This does not say that the twin class is unimportant in a different`
- TeX line 169: `\item \texttt{PROVED\_EXACT\_FINITE}: the support implication and additive`
- TeX line 171: `\item \texttt{NUMERICALLY\_CERTIFIED\_FINITE}: six rows, four categories,`
- TeX line 174: `\item \texttt{OPEN}: a twin-isolated source theorem, source-uniform $L^2$,`
- TeX line 181: `\texttt{FULL\_GATE\_B=OPEN},\qquad`
- TeX line 185: `checkout; the local Bridge-B check is fail-closed and not an official route`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#eq:source` → `main.tex#L58` (existing project target or original TeX label line).
- Link relocation: `#tab:range` → `main.tex#L124` (existing project target or original TeX label line).
- Link relocation: `#eq:partition` → `main.tex#L90` (existing project target or original TeX label line).
