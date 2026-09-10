# TPC-160 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `24a387f0dbd47b1ddd7815f524b8cb07093725b8359d8febb30c2825a90f177f`.
- Bibliography: [references.bib](references.bib), SHA-256 `947e7ea8ba8ab7f82292fce1e2b971a3adbd109f87d38d284fb57df9841497f8`.
- Preserved PDF: [tpc-160-exceptional-variation-abel-return.pdf](tpc-160-exceptional-variation-abel-return.pdf), SHA-256 `4d308f3fd94f236e265e6d21712843d494a39ec00ebca72ce6da5c349cef678c`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `879dfae073896dde3716ae329f4743ed273cc321b26153f9ce6d149ba02f3fa9`.
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
| `Ordered fiber and the bad set` | 65 | 1 | `HEADING_TEXT_MATCH` |
| `Exact Abel summation` | 94 | 2 | `HEADING_TEXT_MATCH` |
| `The weighted return` | 127 | 2 | `HEADING_TEXT_MATCH` |
| `The atomic all-prefix barrier` | 202 | 3 | `HEADING_TEXT_MATCH` |
| `Phase and ledger interactions` | 250 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 264 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 274 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `47` before writing and `47` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `23`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `0d82e8a023436feb94846c4dbe2afdca6762e09dd4e1d0bea19cb63cdd9286f4`.
- Source theorem/proof environment starts: lemma at TeX line 102, proof at TeX line 109, definition at TeX line 116, theorem at TeX line 135, proof at TeX line 150, corollary at TeX line 170, proposition at TeX line 209, proof at TeX line 222.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 68–71 | `f156a8f484ecb49fa25af9acd52c92ad7d8dc67a301840244ac346c6d6a87639` |
| D02 | \[...\] | 74–76 | `b3bfe3e5a6cb651fc5a148e053d35ee844d0d5bbe1bb405065fdc4b51055a983` |
| D03 | \[...\] | 78–81 | `5e67cf424b08ea616c57a2c89fb2be4ef2f50d75aa35185c4520f326e7e42c49` |
| D04 | \[...\] | 83–86 | `acface43cabd906fd2f904d83648ff1d683cbee525947a49535ce7c12cfe2f6b` |
| D05 | equation | 89–92 | `179424b5b81b3b488bb2f906ede6831be2e573e1d58d5f5940dfd781b5847d3b` |
| D06 | equation | 97–100 | `d7bdbbe94ed821b2125710895ca752eeb059576ac11946356e9df83503aa57bf` |
| D07 | equation | 103–106 | `3270ed74e848dbc592e5e3d9eed14472cc8e0cc6a19f717ba50984f82625482e` |
| D08 | \[...\] | 111–113 | `3ad1c41d4f9d163bc15c96d074ea8d50fa5dd24ce7adcfa0213ed63651103131` |
| D09 | \[...\] | 118–124 | `86c1b7f173c4865e16e6bc086fc84c7e051804b5545fb63737a3d1850e8d5569` |
| D10 | equation | 130–133 | `d61fd3e1019ecb6deb24508638470cb3d86b8f9c4d7827e3121a072fe514cdf8` |
| D11 | equation | 138–147 | `bc0a527b2eb570bf4c6cb5a526893a9291775aaf41a94655467d35fcf3b0e710` |
| D12 | \[...\] | 153–157 | `ebab76675c4111a07df892a27057fd0fbb59af4f38b8d806df22dceac0551fa4` |
| D13 | \[...\] | 159–161 | `2e2aedbdf73c3a39c4c006525ba31b2ac8175b3024eb972575579962657a070a` |
| D14 | \[...\] | 163–165 | `cbed52c7aebb0a13f2a5f4b13b186b664ca1aaebebf5a06355c88be3822b3b15` |
| D15 | \[...\] | 172–174 | `fa2808695d78cfb9e9dec7c1c62391c4258762c57109474d1fe2d8f607232a8a` |
| D16 | \[...\] | 177–180 | `4ca2f8a5faaeb4d46915dfd51ec06a57ec22f516bd2966e4b6372aa475f4fd47` |
| D17 | \[...\] | 182–184 | `9aea6a15d8fc8ccf6e249eed6cb3eefefdb7b91c80fd3e97a44bd097538505c9` |
| D18 | \[...\] | 186–188 | `152b77ae94fe45e9084c1bf59205870f6bc570767e9cd51c617be697273769b3` |
| D19 | \[...\] | 205–207 | `97cb90bdb638bfa61ced494f6a048eff2bea67d50f220ad7fea1934809821175` |
| D20 | \[...\] | 211–213 | `36d9c85be84220c2d0e3323834a2151aca65ff5b8a37bd84fd0c8ded72922a78` |
| D21 | equation | 215–219 | `81c1f3ebb5f283dd8fd92cc89ed38942e8240e655697ca7093acf3af6ff2a8df` |
| D22 | equation | 230–235 | `13329318955f823160ec4829b9842c1e34d4ab0f11aeb93668f5df6fd1ec82b3` |
| D23 | \[...\] | 240–243 | `5b2c6e6a85f9aa3b89a4d13908cb1de596d372d907933389590d0844d258f8b4` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 45: `Abel derivative is one atom, so uniform all-prefix control requires`
- TeX line 102: `\begin{lemma}[Finite Abel identity]\label{lem:abel}`
- TeX line 136: `Assume the determinant-two and period envelope of TPC-159 and`
- TeX line 198: `does not supply the literal \(w\), its variation, or the required`
- TeX line 228: `To obtain a uniform saving for all its step cutoffs from`
- TeX line 244: `does not change its continuous logarithmic measure, does not`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:abel` → `../main.tex#L105` (existing project target or original TeX label line).
- Link relocation: `#def:variation` → `../main.tex#L116` (existing project target or original TeX label line).
- Link relocation: `#eq:main` → `../main.tex#L146` (existing project target or original TeX label line).
- Link relocation: `#eq:difference` → `../main.tex#L99` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `../main.tex#L135` (existing project target or original TeX label line).
- Link relocation: `#eq:avoid` → `../main.tex#L234` (existing project target or original TeX label line).
