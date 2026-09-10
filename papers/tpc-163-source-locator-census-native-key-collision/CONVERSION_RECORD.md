# TPC-163 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `bf4f6df7eba4b7f6161834d4830c08bd5063376f4556ba0a52dcddeae8fe48d1`.
- Bibliography: [references.bib](references.bib), SHA-256 `9212211058c11dac9fe196102f3adea0eb281c74b82310088f9105c6f708eeb0`.
- Preserved PDF: [tpc-163-source-locator-census-native-key-collision.pdf](tpc-163-source-locator-census-native-key-collision.pdf), SHA-256 `f5d6991e91262bb85b1102fe02be870f2af124c5cfd956666c3d6dfdb192248a`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `408919d227f48bc25ce4b4a053664a26fb4ddd0f652c9ac34b8cec7b8acf445b`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC160_164.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Why a source census is now necessary` | 100 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen corpus and evidence contract` | 127 | 2 | `HEADING_TEXT_MATCH` |
| `Exact source-locator census` | 187 | 3 | `HEADING_TEXT_MATCH` |
| `Native-key collision obstruction` | 268 | 4 | `HEADING_TEXT_MATCH` |
| `What the two theorems jointly imply` | 342 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducible certificate` | 377 | 5 | `HEADING_TEXT_MATCH` |
| `Next forced object` | 402 | 5 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 416 | 5 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 428 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `47` before writing and `47` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `18`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `73aaf16055a0516a76939bc8b2a227612631a9d384741447980d3c2a29ae611a`.
- Source theorem/proof environment starts: definition at TeX line 129, definition at TeX line 145, definition at TeX line 167, theorem at TeX line 189, proof at TeX line 215, remark at TeX line 247, remark at TeX line 254, theorem at TeX line 278, proof at TeX line 308, proposition at TeX line 324, proof at TeX line 334, corollary at TeX line 363, proof at TeX line 371.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 71–73 | `3347fa7cb9ef3c68e6e36ec9d310b12eb2aca3cbe3027c034b178aa13e9c4a88` |
| D02 | \[...\] | 112–115 | `aff681ebf1ddefe5f30cddff6212bc42bdabc55f1837b4defc7cb946bfa1e644` |
| D03 | \[...\] | 169–182 | `920d1819bb964e75bbf91f3e388b019ccea52c8a670041b312fa0dc8f95dce9d` |
| D04 | \[...\] | 195–197 | `40f97c4b25e58141820b368723f1719e47be36ff9222f20fe791eae0cac8ef17` |
| D05 | \[...\] | 201–203 | `2e59ce46ef88338a9d3325cc4c921455416461da277c22e7674fcf1f78abf68e` |
| D06 | \[...\] | 209–212 | `7ed7a885cbd11f7271cc3d0fb804cf8ef6442e1b90e24ab2b5225754efd64592` |
| D07 | \[...\] | 220–224 | `7ae060840a9874e8046e5c2bab3fda75560105a2e44207247d3fd06fe02b7a84` |
| D08 | \[...\] | 257–259 | `53f863fb0d9bb1ec7de40da9de2ff732b40f3d5e221b43f9d758ee473081dd80` |
| D09 | \[...\] | 261–263 | `c81205229b458b6b46d710703976abc8c2028961fe37edf43314ed312fcafc1c` |
| D10 | \[...\] | 272–274 | `0016118e7dcfefd8417f0d9161826d90e74a4ceb7c85f6b417834ecd149e7a3a` |
| D11 | \[...\] | 280–283 | `3270cfdfaa312ed988fb166e86ff08036abbb1165444d6883548cdf357314fc1` |
| D12 | \[...\] | 285–295 | `2f2e1d95cab5d141ec5f203d397f5271f34b03a57ba0bb5f7f4674b44454d13e` |
| D13 | \[...\] | 297–304 | `53c02cbbae685433d9cc13098e13aaa3683c4c48abb079a189d91b705beab208` |
| D14 | \[...\] | 312–315 | `35d708d18d91af6bab512bab9e53b7189fd80f01c45e8f648669c22b687f5845` |
| D15 | \[...\] | 318–320 | `675187788466e85f81109a4f5aa0eb765ad9b862f6e8dafc44390da6fca20349` |
| D16 | \[...\] | 327–329 | `7794fdc945d93a6fdc84c4886bd915922932c19dccd1e4d764c8156cb299b56b` |
| D17 | \[...\] | 345–355 | `d7bba0e5a9eff5049005c44ee0cc28c14685aa8b7ef9238194e1441df46f813f` |
| D18 | \[...\] | 407–410 | `1fdfbe3716dea22171da16bafcf3197c283d06bcf38aad9cb5a480550da1d5e5` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 35: `\newcommand{\ETO}{\textnormal{\textsc{eligible-tail-open}}}`
- TeX line 74: `Consequently the native triple is not a row key for this archive.`
- TeX line 77: `the frozen corpus is not a nonexistence theorem for actual`
- TeX line 93: `corpus and its archive keys.  It does not prove that actual`
- TeX line 106: `it does not construct such a completion.  TPC-154 constructs two`
- TeX line 109: `theorem-backed route open \citep{WangTPC154}.  TPC-155 supplies a typed`
- TeX line 141: `digest.  A digest is an integrity assertion only; it does not confer`
- TeX line 161: `The derivation tree is intentionally modest.  It is not a proof`
- TeX line 176: `Q_D,\ Q_Z,\ G,\ P_{h_0},\\`
- TeX line 247: `\begin{remark}[Mapped census, not a future-schema scanner]`
- TeX line 249: `fields of \(\Csrc\).  The program does not generically discover`
- TeX line 265: `universe, which is neither assumed nor proved.`
- TeX line 305: `In particular, \(\Nkey\) is not a row key for the frozen archive.`
- TeX line 339: `synthetic or actual-occurrence witness.`
- TeX line 359: `open.  The second`
- TeX line 399: `then runs the same validators.  It does not merely store expected`
- TeX line 406: `finite question:`
- TeX line 411: `This is an exhaustive finite-key problem, not yet an actual`
- TeX line 422: `time, the paper preserves the correct open-world boundary: new`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 5 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#def:admissible` → `../main.tex#L145` (existing project target or original TeX label line).
- Link relocation: `#def:classes` → `../main.tex#L167` (existing project target or original TeX label line).
- Link relocation: `#eq:shadow-map` → `../main.tex#L223` (existing project target or original TeX label line).
- Link relocation: `#eq:first-missing` → `../main.tex#L114` (existing project target or original TeX label line).
- Link relocation: `#eq:zero-edges` → `../main.tex#L211` (existing project target or original TeX label line).
- Link relocation: `#eq:native-key` → `../main.tex#L282` (existing project target or original TeX label line).
- Link relocation: `#eq:distribution` → `../main.tex#L294` (existing project target or original TeX label line).
- Link relocation: `#thm:collision` → `../main.tex#L278` (existing project target or original TeX label line).
