# TPC-347 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `1de1964aa411aa631587da690524beadf1127d3c`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `5653b8c46a72d44cb1bd78544437dceda86014a87930b34600a037585ab6b6ba`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `26013a2d20ff2665ae3fc6a73b5d9e228a261fd9f7c3395be1063cccc4999f2d`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `f8cf48ebba80fb742b946801bf7961be9f9266bee4b80388794e1a6536728c27`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC345_349.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 43 | 1 | `HEADING_TEXT_MATCH` |
| `Exact factorisation` | 71 | 1 | `HEADING_TEXT_MATCH` |
| `The unmasked Fourier interface` | 99 | 2 | `HEADING_TEXT_MATCH` |
| `Finite audit` | 142 | 2, 3 | `UNMAPPED_OR_AMBIGUOUS` |
| `Adversarial checks and claim boundary` | 183 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion and next question` | 222 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `75` before writing and `75` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `0ffa8048aa7977da91b51dcaf90a0844e5b6d9a4eeab3a50190685b68eac1ceb`.
- Source theorem/proof environment starts: proposition at TeX line 76, proof at TeX line 87, theorem at TeX line 110, proof at TeX line 124, remark at TeX line 213.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 53–59 | `1b844b14dd127baf2e38659b7bd0c88d82aa14028eae79d62d5f05445b60b580` |
| D02 | equation | 63–67 | `16c35fde39a39c96354726395f5f414314431f7ca5f3d52854cbc8478cfcdb20` |
| D03 | equation | 78–80 | `1f7d2d1a202d5037b22dc20df1fa41388f3e2368e1692b9e454232d05420761e` |
| D04 | equation | 82–84 | `141f3233c12e5fa58afe97d15ad7e0acd0d4a1f4446a4fe428de0ab8ceb6152f` |
| D05 | equation | 103–107 | `798ddc8a2734ad53219295cf703e14beb83e2b4db70f1f793992ddc09d55f4e8` |
| D06 | equation | 112–116 | `3b334cac895f3c07c1c8b372ac1fc69282758100c058eb803ebb7107ce7ac34d` |
| D07 | equation | 118–121 | `28165dec56f0872cb0046526871e5e13530fe1c36b1d3f10497f1d8d10679117` |
| D08 | equation | 134–137 | `09e17ccbca6d4b74f8d0fb9f0890958e5f53fa80dc7f1ab970b77853bb1cc2d4` |
| D09 | equation | 153–155 | `b210c9961900336d0445b3db6f6360eb609bf6e7565e2733aaae240601e31025` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 33: `the unmasked convolution on $\el(\mathbb Z)$, and a finite triangle envelope`
- TeX line 39: `interface and a finite obstruction to discarding the masks; it is not an`
- TeX line 45: `The recent finite route has repeatedly encountered a distinction between a`
- TeX line 47: `to the unresolved source-uniform $L^2$ question at the operator level.  The`
- TeX line 61: `$(K_pf)(u)=\sum_d k_p(d)f(u-d)$.  The physical finite matrix on an interval`
- TeX line 69: `finite table below must not be read as evidence for a twin-prime density.`
- TeX line 92: `\eqref{eq:defect}.  All sums over the shell are finite.`
- TeX line 117: `For every finite interval $I$,`
- TeX line 142: `\section{Finite audit}`
- TeX line 149: `finite sum uses $R=65536$ and the analytic tail in \eqref{eq:tail}.`
- TeX line 154: `\norm{A_I}\leq\norm{K_e}+\norm{D_I}_F. \label{eq:finitecertificate}`
- TeX line 161: `\caption{Summary of the 192-row finite spectral audit.}`
- TeX line 164: `quantity & certified finite readout \\`
- TeX line 180: `is not a monotone function of shell size or interval count: it is a diagnostic`
- TeX line 181: `of the masks and their placement, not a candidate exponent.`
- TeX line 201: `mask factorisation and defect identity & proved exact finite \\`
- TeX line 204: `192-row spectral replay & numerically certified finite \\`
- TeX line 206: `source-uniform arithmetic $L^2$ & open \\`
- TeX line 207: `fixed-power credit / Route-B Gate B & $0$ / open \\`
- TeX line 214: `The finite obstruction does not say that every possible mask estimate fails,`
- TeX line 216: `the current finite physical object is not faithfully represented by its`
- TeX line 227: `error.  The finite audit shows that this defect is sometimes substantial,`
- TeX line 230: `$L^2$ problem.  No arithmetic advance is claimed in this release.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:kernel` → `main.tex#L58` (existing project target or original TeX label line).
- Link relocation: `#eq:factor` → `main.tex#L79` (existing project target or original TeX label line).
- Link relocation: `#eq:physical` → `main.tex#L66` (existing project target or original TeX label line).
- Link relocation: `#eq:defect` → `main.tex#L83` (existing project target or original TeX label line).
- Link relocation: `#eq:symbol` → `main.tex#L106` (existing project target or original TeX label line).
- Link relocation: `#eq:fourierbound` → `main.tex#L115` (existing project target or original TeX label line).
- Link relocation: `#eq:tail` → `main.tex#L136` (existing project target or original TeX label line).
- Link relocation: `#eq:tail` → `main.tex#L136` (existing project target or original TeX label line).
