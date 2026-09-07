# TPC-357 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `f780ea0c90b7f9a6a967d53692bafc4c7f53d0afca87e102daf60e5c2dbf44ae`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `345786a6afa27cd87f278a79d38cfa763126c34200bfa3b1708021ae8f0000fe`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `ac834868b62a630e4636fc3cdfbeae3596e9b128816c7b5f440731b9181f53f0`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `a7e6b0c9dc6dc2bd19f61a8bed7da8ff204b94f9ccbe7cd049451c1af29564c7`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 42 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator model` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `Exact envelopes and numerical protocol` | 92 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 128 | 2 | `HEADING_TEXT_MATCH` |
| `Independent controls` | 187 | 3 | `HEADING_TEXT_MATCH` |
| `Claim firewall and conclusion` | 204 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 223 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `46` before writing and `46` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `bf82abfe91ecdf53d94ef9d109b3dec7bbc1ba18803588d1d4f1385d2303b2e0`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 69–74 | `3da2905b24cdceb1e722d9cf26e62d9706bb73d4436f07bc35587088e21a38c5` |
| D02 | equation | 76–81 | `bc8ddef1a51c10bbf66dee1b1dadbbfb54a971f350be4e5cd9f28f0fccc8d71d` |
| D03 | equation | 83–87 | `393fac2e8f76845962f4a83665ecbf09c70f0a546c97582a481b35c553b3b018` |
| D04 | equation | 97–101 | `13e9ae72340721b5d3fee4961b35c309d1c10ac871b632973d18222a9ff796d4` |
| D05 | equation | 103–106 | `45caa19a9d2b70bc8e9e9a22aaff4671d606fa0af0892d1ae7e82bd1b4f2f5f2` |
| D06 | \[...\] | 111–113 | `8c6a0cc3950e5e5eb4d69e5c16b448c34870bc9d98e59f95db95fab50fad4d36` |
| D07 | equation | 158–161 | `051d2910615ee3f166ec280b305daa134e2c2bd0c2b64cff1d02bcbe3a94efc2` |
| D08 | \[...\] | 173–175 | `82623c434cebc366f9da5b2f9489ad2526db3d3f36bbffc378887bd1bcb1a131` |
| D09 | \[...\] | 177–180 | `9b0034d3a1c798fb1d67362089d5d1421a887e94b72670522867232eb709054a` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{A Finite Operator-Norm Scale Ladder\\`
- TeX line 25: `We perform a finite operator-level audit of the position-aware congruence`
- TeX line 30: `the exact finite Schur row-sum and Frobenius envelopes, giving 288 law-level`
- TeX line 35: `1542.7455490253569.  These are finite scoped certificates, not uniform`
- TeX line 39: `operator bound and every arithmetic Route-B gate remain open.`
- TeX line 48: `said about operator size along a longer finite count ladder once those origins`
- TeX line 53: `on a preferred sign law.  Second, a finite spectral readout and an exact norm`
- TeX line 56: `for the all-plus subfamily.  Nothing below asserts an estimate uniform in the`
- TeX line 64: `\section{Finite operator model}`
- TeX line 88: `The finite replay checks $G_u>0$ on every row.  The four declared laws are`
- TeX line 94: `For a finite real symmetric matrix $T$, symmetry gives`
- TeX line 107: `These are exact finite inequalities.  They do not say that $S(T)$ or`
- TeX line 108: `$\lVert T\rVert_F$ stays bounded when the finite model changes.`
- TeX line 131: `The all-plus raw operator has a much larger finite scale than its normalized`
- TeX line 164: `values obey both finite envelopes whenever a spectral value is recorded;`
- TeX line 184: `nonmonotonicity are compatible: boundedness on four finite counts is not a`
- TeX line 192: `does not import the TPC-357 producer.  It reconstructs the prime sieve,`
- TeX line 206: `The exact contribution is the finite norm envelope~\eqref{eq:schur}--`
- TeX line 210: `finite diagnostic for the TPC-355 preconditioner.`
- TeX line 214: `finite cap nor the Schur envelope controls a growing origin or interval.  We`
- TeX line 215: `therefore assign zero fixed-power credit.  A source-uniform masked $L^2$`
- TeX line 217: `remain open.  The next experiment should attack the finite spectral cap on a`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.

- Link relocation: `#tab:envelopes` → `main.tex#L139` (existing project target or original TeX label line).
- Link relocation: `#eq:schur` → `main.tex#L100` (existing project target or original TeX label line).
- Link relocation: `#eq:frob` → `main.tex#L105` (existing project target or original TeX label line).
