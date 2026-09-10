# TPC-168 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `40291c3cf00d844d6a4cdd3dca0efa382b410b0de0a6b387912e81505610998f`.
- Bibliography: [references.bib](references.bib), SHA-256 `cba1215f67da776d5ecec5d1239df91781347454a8716b31dd8e921817320479`.
- Preserved PDF: [tpc-168-separated-phase-registry-sieve.pdf](tpc-168-separated-phase-registry-sieve.pdf), SHA-256 `564de462e7bf0e2224a8b24505f68ac186a1aae520b1eaf3fee8f1c23799202c`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `ccf6c5ad52d3ad25a53ce95273f233c2071073a3e0695ec810cb0e56faf74957`.
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
| `A separated sampling inequality` | 62 | 1 | `HEADING_TEXT_MATCH` |
| `The determinant-two registry theorem` | 116 | 2 | `HEADING_TEXT_MATCH` |
| `The selector firewall` | 199 | 3 | `HEADING_TEXT_MATCH` |
| `Route decision and next object` | 231 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducible audit` | 248 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 258 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 270 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `59` before writing and `59` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `18`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `bcb046d83c8a932f6a5455fd10dd589a113b150a472ee3d66fab2509884c5c68`.
- Source theorem/proof environment starts: theorem at TeX line 75, proof at TeX line 88, corollary at TeX line 134, proof at TeX line 146, corollary at TeX line 151, proof at TeX line 169, proposition at TeX line 201, proof at TeX line 207.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 65–68 | `e92d1e23d67ef50beac322602d6b584866ef008fe87184664ef9f7144be39b28` |
| D02 | \[...\] | 71–73 | `3be8713821f055e0b958c52e3dda69ad73a36ee7a833395b84be50af72d98a3b` |
| D03 | equation | 78–85 | `16c4d3644a67978488dbdc1e240ec8b8030833210919e95a2ec3cd9c0a52ac9d` |
| D04 | \[...\] | 92–94 | `0db259d55cf9ece817c2de9967bf1ef0b8bbeab7dc4b5cde1fcc829c0b06b17d` |
| D05 | \[...\] | 97–101 | `175c8bc16587f956cfaca826fb475078c74411d0f13c0538261c59319dfa41dd` |
| D06 | \[...\] | 103–107 | `3b7a3fe96edcdf903e8d8d43f5b5c3dd533097269c5dcc9cdb71a11b048f0da3` |
| D07 | \[...\] | 119–122 | `85f1ffda949135dc90830709c7d7ece8da14db5e51206693c978ba3a3c2c05a1` |
| D08 | \[...\] | 123–126 | `95687979fd73ff90dff7052c2836d34c8abdb0b1e985ee333687fb7bd697a463` |
| D09 | \[...\] | 128–130 | `5dc379d095f79dabb63bd68182de2ece32ecac17a83c15067d9dca14e6db7f60` |
| D10 | equation | 137–143 | `6c9b1c2a811ee0f8aa6be5d336895628ffd241088227fc59ac5be777d69c07d4` |
| D11 | \[...\] | 153–155 | `6705ce7d77401c01e91fe0453ae7751cc0de78ec8df1866164f99d156b75c7c4` |
| D12 | equation | 157–163 | `fb9b9dc39b556af4a36b80eb3dbf2681c11e527540f0667861c80a36cd6ea2d6` |
| D13 | \[...\] | 173–175 | `3e98bfe071c22032b388b4912915c7d65d4c21e2eb3a0c27fad0b881a59da0a7` |
| D14 | \[...\] | 180–182 | `850e28d6100569424d5a568317c6eeace3e218b35d46cb5644cc961b716da6bd` |
| D15 | \[...\] | 184–187 | `ecc510ea05ab2ace7dc94e4856f565b94d70bb497287b80c6512b88970dbd872` |
| D16 | \[...\] | 188–195 | `bb4d3055b04df52b38420e2bacd43512cd9b467969711c4d4f85bbabe7096779` |
| D17 | \[...\] | 210–213 | `0e655b4e76d47d80954c2df45fffb0459ab1f3b1aab00f1c6fe6b5e04ba7d2dc` |
| D18 | \[...\] | 219–223 | `98e2bde78cc80de76e90f17b29e17d0b22ac46b9ff143e0129e49abbc51c1a42` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 24: `A Finite Large-Sieve Gate and a Selector Firewall}}`
- TeX line 37: `continuous statement to arbitrary finite separated phase registries.`
- TeX line 40: `\(\delta^{-1}+4\pi(L-1)\).  For a quasi-uniform registry of at least`
- TeX line 43: `why density-one registry control does not identify one distinguished`
- TeX line 44: `production phase.  Thus the finite-registry route genuinely advances,`
- TeX line 45: `but the original pointwise phase node remains open.`
- TeX line 49: `large sieve; additive phase; finite registry; selector firewall;`
- TeX line 56: `finite registry.  It does not prove that a named production phase is`
- TeX line 58: `sampling implication and is not a lower bound for the literal`
- TeX line 69: `A finite set \(\{\alpha_1,\ldots,\alpha_M\}\subset\T\) is`
- TeX line 75: `\begin{theorem}[Elementary finite phase sieve]\label{thm:sampling}`
- TeX line 151: `\begin{corollary}[Quasi-uniform registry density]\label{cor:density}`
- TeX line 186: `PHASE\_METRIC\_FINITE\_REGISTRY}.`
- TeX line 197: `uniform pointwise estimate.`
- TeX line 201: `\begin{proposition}[Density does not select]\label{prop:selector}`
- TeX line 202: `There are quasi-uniform registries and coefficient sequences for`
- TeX line 209: `\(\alpha_r=r/L\).  Finite Fourier orthogonality gives`
- TeX line 226: `coefficient-blind selection inference.  It does not say that any`
- TeX line 234: `\citep{WangTPC167}; TPC-168 now supplies finite separated-registry`
- TeX line 246: `therefore remains open rather than stopped.`
- TeX line 251: `\eqref{eq:sampling} and \eqref{eq:count} on a nonuniform separated`
- TeX line 266: `average.  TPC-169 turns to the other open door and asks whether one`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:sampling` → `../main.tex#L84` (existing project target or original TeX label line).
- Link relocation: `#thm:sampling` → `../main.tex#L75` (existing project target or original TeX label line).
- Link relocation: `#thm:sampling` → `../main.tex#L75` (existing project target or original TeX label line).
- Link relocation: `#eq:count` → `../main.tex#L142` (existing project target or original TeX label line).
- Link relocation: `#prop:selector` → `../main.tex#L201` (existing project target or original TeX label line).
- Link relocation: `#eq:sampling` → `../main.tex#L84` (existing project target or original TeX label line).
- Link relocation: `#eq:count` → `../main.tex#L142` (existing project target or original TeX label line).
- Link relocation: `#prop:selector` → `../main.tex#L201` (existing project target or original TeX label line).
