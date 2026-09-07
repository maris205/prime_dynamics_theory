# TPC-299 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `aa6a797b49ed462881998abf696440d164a0f74c`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `80214f05736a9e33a3d1530c88171e28a995e2d28e9e9d71d118fb04e9be7d1b`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `6ec9ade4c15d2ecbfed25c1ae636c25069ee1f38db99a9aba41bef6d815a6544`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `20bc9e1108440691dc4ea569709ade268164eef5efefe90ea67e7047aed71272`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `bbd2f51ff321c21c2216c02b4a0378c19faece2eb1f2b1b873d5490cff182463`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC295_299.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Position on the route` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `Finite physical map and literal source family` | 68 | 1 | `HEADING_TEXT_MATCH` |
| `Exact budget frontier` | 117 | 2 | `HEADING_TEXT_MATCH` |
| `Finite audit` | 208 | 3 | `HEADING_TEXT_MATCH` |
| `Validation and interpretation` | 275 | 3 | `HEADING_TEXT_MATCH` |
| `Claim boundary and conclusion` | 296 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 318 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 335 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `103` before writing and `103` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `16`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `fe9a6292d2a3e450b328519178c32b43bfd766c700e5d8efd3857397067748ee`.
- Source theorem/proof environment starts: remark at TeX line 111, theorem at TeX line 129, proof at TeX line 147, proposition at TeX line 169, proof at TeX line 178, proposition at TeX line 194, proof at TeX line 202.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 31–35 | `44d4f106f090e4974a413fa2d4c48a80469e520106fbba5d2c6d9b71bf1fe7ed` |
| D02 | \[...\] | 73–77 | `a2851ac3c41dcea256177d66d09266d39b638a9d6a590ab81d2cc7aad11d31f1` |
| D03 | \[...\] | 78–81 | `8c1ac78af2ed8da20983febfc9f30c78a64fde8ea182fcca3a200bd9b6685a70` |
| D04 | \[...\] | 86–88 | `fb36ac65f8f2589791a8bd36085e5fbeba62c7ed4dec0d04136bcb4444708989` |
| D05 | \[...\] | 90–96 | `2d002d5789f0e635e88a0bc5ec7574d10374fddc602599b5ab107a64a5f24de5` |
| D06 | \[...\] | 99–101 | `fb4103a91877c1755c0e8c91a339800fd71fe9ce8ac96097b54ccbaac019de39` |
| D07 | \[...\] | 104–106 | `cc8b678593d6eef835d5ef7f6e13de6f43914fd4b119cdf2629c0c2a42ca729c` |
| D08 | \[...\] | 120–125 | `0da5440ac7114d6e9d3d1f7912e3d0dbf6376719492f149c5e107df68e7558a3` |
| D09 | \[...\] | 132–134 | `afc509e351a63f07567db3f9d4070b385037f6fb6390257d821df981f464575b` |
| D10 | \[...\] | 138–141 | `c3d96da2c101565e314a801527be129afc026f68ed80571c2d98dea7f25f08eb` |
| D11 | \[...\] | 149–152 | `0a1ec60f5afdb98eb8ec6991c8fb54b110e3b21f30a69ea00d95cd947fa7c0d6` |
| D12 | \[...\] | 158–160 | `cda2ab9749ebdd6d3c30955cb3966730d950725ca1c542e7711df8d972c09355` |
| D13 | \[...\] | 182–186 | `d0197b81c3ddc52d264167730d4a416d78a741e96b3e3851bdeaccc4f2522869` |
| D14 | \[...\] | 187–190 | `870085b68d54ee60706e4e066737f7208193aa2433d07fe8890ef132ac2c6450` |
| D15 | \[...\] | 196–198 | `0a7927bcdc9948f8d1f211ab2b009f1bd11fc7b8fcf1c987812641bc82d676c8` |
| D16 | \[...\] | 306–312 | `5c93202720b3729c8d7e9663a7182cac241025beef42c318a6015bd6b3158eab` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 17: `for Finite Twin-Prime Shells}`
- TeX line 29: `becomes geometrically expressive, but it does not measure the source norm`
- TeX line 44: `are finite restricted-profile diagnostics: no growing budget theorem,`
- TeX line 51: `The current finite prime-shell line separates three questions that are easy`
- TeX line 53: `correlation map can be onto on the finite grid \cite{tpc295}.  TPC-296`
- TeX line 63: `does not imply a small source norm when the profile columns are correlated.`
- TeX line 64: `Conversely, a finite full-rank image can hide a large source budget behind`
- TeX line 68: `\section{Finite physical map and literal source family}`
- TeX line 108: `minimum, unit-edge max-cut, and all-positive vectors below are finite target`
- TeX line 112: `The word literal refers to the displayed finite cutoff formula.  It does`
- TeX line 113: `not assert that this 17-element family is complete, uniform in the shell`
- TeX line 129: `\begin{theorem}[Finite native budget frontier]`
- TeX line 130: `Suppose $M=U^{\mathsf T}U$ is positive definite and $V=A^{\mathsf T}U$.`
- TeX line 170: `For $\lambda>0$, $V^{\mathsf T}V+\lambda M$ is positive definite.  Along`
- TeX line 199: `whenever the right-hand side is finite.`
- TeX line 208: `\section{Finite audit}`
- TeX line 222: `a declared finite normalization, not an asymptotic scale law.`
- TeX line 227: `\caption{TPC-299 finite budget census.}`
- TeX line 273: `the displayed finite thresholds.`
- TeX line 287: `The finite result closes a specific ambiguity in the previous dimension`
- TeX line 288: `ladder.  The final prefix may be surjective on a finite shell, but that`
- TeX line 289: `surjectivity does not imply a cheap native source.  In the registered grid,`
- TeX line 293: `not a statement about the unrestricted ambient source map or about every`
- TeX line 298: `The KKT, feasibility, ridge-path, and nesting statements are exact finite`
- TeX line 300: `declared literal cutoff ladder, finite rows, frozen physical operator,`
- TeX line 301: `normalization, and target controls.  They do not establish uniform profile`
- TeX line 314: `the source-side definition and to check whether this finite budget gap has`
- TeX line 315: `any uniform shadow.  That is an open question, not a conclusion of this`

## Conversion limitations

- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:frontier` → `main.tex#L124` (existing project target or original TeX label line).
