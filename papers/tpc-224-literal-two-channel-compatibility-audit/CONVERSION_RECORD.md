# TPC-224 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `a89975ddbd8d57982fe25f06a807e4c9cfdba641b57d812a5cfefaeaf16025d5`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `5d7de82d845d8fd9bc2d40669cbb01074225c32b36f73f4f917200f2a29adb7f`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `8eb3c0420de387d2f58326a301655ba5ae6fe9600cc8f0cf74ead80f5084fac7`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `6c553eae6407a3539ed0d75ccd1350249b0b4f23fbc61b77ac59e131734cd374`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC220_224.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Why compatibility is the next bridge` | 61 | 1 | `HEADING_TEXT_MATCH` |
| `The common literal coefficient family` | 95 | 2 | `HEADING_TEXT_MATCH` |
| `Sharp common-vector theorem` | 130 | 2 | `HEADING_TEXT_MATCH` |
| `Literal growth audit` | 187 | 3 | `HEADING_TEXT_MATCH` |
| `Route evaluation and relation to TPC-223` | 259 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 290 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 304 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `89` before writing and `89` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `14`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `2ad79bf0139f0819d7e53d56bcf90933684a04de7e94e822393319e4bc63a2a4`.
- Source theorem/proof environment starts: theorem at TeX line 132, proof at TeX line 150, remark at TeX line 179.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 41–44 | `e548d17109cba2df9a556eea4e815e49804632066fc1eed20c9365c5f37f72b0` |
| D02 | align | 81–85 | `c7e580ec179bd6915c796adfa4ab2374e096e2e13fc84c0bfba903a57d79b78f` |
| D03 | equation | 100–106 | `6f64e601450e8ba6e2b552738e598b359378a7cdd15524010ebf215893d82406` |
| D04 | equation | 108–112 | `81e49b593e303dd45b5c92168a0d4d8fe657537486fe4c20b8a1cc26eb4bc985` |
| D05 | \[...\] | 122–125 | `a30097787c9bd5d673fea63531fd66c98824e98c4948a81c78573079ee45df7a` |
| D06 | equation | 137–140 | `ebaaf39592195e3effb987d77b40918cc62ba7441ebe27db3a44c8aa90c96335` |
| D07 | equation | 142–145 | `f38d7dbbbb4839ef673ba39d1b0366ee95f7616194fca1ab4b9066ab75338654` |
| D08 | \[...\] | 154–158 | `066ed8a9129017e73f728679509ebf800e9c193fee8ccc36af9b7bc7ee0ef9ba` |
| D09 | \[...\] | 162–164 | `6b10b8e299be63ddc42c7fcc73c0f52df98da838cde4df462215664b81aad80f` |
| D10 | \[...\] | 170–174 | `fb4a87aa21e88eb86c4f2bdf1b18bc0eafe4402cff63070a44755b303702e1b2` |
| D11 | \[...\] | 192–195 | `f8542140ea79b0d67ae25f7766b1a50e3a69027485f2e9452c3ad2046c284a9e` |
| D12 | \[...\] | 263–265 | `84645f7bdfd71912159dcf19705f66709ea7882cd954061e8919ffbd7fb5409e` |
| D13 | \[...\] | 270–274 | `2920df8fcfc5b11bc0585c6be933654db0dfc38304f95b0c502536b73272fe6c` |
| D14 | \[...\] | 279–285 | `1cdf07249b135a81bb557b61dedd8031c8ded0ea7176e459b215841693e7870b` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 47: `all three quantities.  Nine finite growing source-surrogate scales pass the`
- TeX line 53: `open.`
- TeX line 58: `The finite Hilbert theorem is unconditional algebra.  The two finite clocks`
- TeX line 59: `are explicitly modeling choices and are not an asymptotic prime theorem.`
- TeX line 74: `an exponent ledger but can change a finite quadratic form by a fixed factor or`
- TeX line 90: `The claim boundary is deliberate.  A finite vector identity is not an AP`
- TeX line 92: `scales, and we do not replace the V46 source clock by the finite clocks used`
- TeX line 113: `where $\mathcal F$ is the finite set of active $(h,a)$ coordinates.  The`
- TeX line 120: `packet-space reassembly.  If $T_I$ denotes the common finite-window synthesis`
- TeX line 127: `Thus the theorem is stable under a common physical window; it does not assume`
- TeX line 134: `For any finite $\Qset$ of size $P$, any positive integer $J$, and any vectors`
- TeX line 152: `$\sum_jV_j$ and $\sum_qU_q$.  Cauchy--Schwarz in the two finite label spaces`
- TeX line 179: `\begin{remark}[What the theorem does and does not compile]`
- TeX line 182: `of $x$ to an exponent ledger.  It does not prove bounds for either $\Eap$ or`
- TeX line 189: `The exact certificate has two named experiments.  The first is a finite`
- TeX line 254: `The stress result is an obstruction to a normalization shortcut, not a lower`
- TeX line 268: `identification condition, not a hidden theorem.  In particular, the current`
- TeX line 282: `\texttt{AP=OPEN},\quad \texttt{POLARIZED=OPEN}\\`
- TeX line 283: `\texttt{L2=NONE},\quad \texttt{FULL\_GATE\_B=OPEN}`
- TeX line 288: `finite-window synthesis, zero/nonunit terms, and normalization.`
- TeX line 292: `TPC-224 converts a vague compatibility requirement into a sharp finite theorem.`
- TeX line 299: `finite modeling choices, not a replacement for the V46 asymptotic clock.  No`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:ap` → `main.tex#L82` (existing project target or original TeX label line).
- Link relocation: `#eq:pol` → `main.tex#L83` (existing project target or original TeX label line).
- Link relocation: `#eq:ap` → `main.tex#L82` (existing project target or original TeX label line).
- Link relocation: `#eq:all` → `main.tex#L84` (existing project target or original TeX label line).
- Link relocation: `#eq:sharp` → `main.tex#L144` (existing project target or original TeX label line).
- Link relocation: `#eq:directional` → `main.tex#L139` (existing project target or original TeX label line).
- Link relocation: `#eq:sharp` → `main.tex#L144` (existing project target or original TeX label line).
- Link relocation: `#eq:sharp` → `main.tex#L144` (existing project target or original TeX label line).
- Link relocation: `#tab:source` → `main.tex#L227` (existing project target or original TeX label line).
