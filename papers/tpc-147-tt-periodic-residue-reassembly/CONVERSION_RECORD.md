# TPC-147 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `30214b03d162e1398648cd129e14de016dbf78c52f33a486e1ff826415175d98`.
- Bibliography: [references.bib](references.bib), SHA-256 `995ffc8e28b39578828d8b4fddd285bb309b5130db9d7eab9672265da456e9ec`.
- Preserved PDF: [tpc-147-tt-periodic-residue-reassembly.pdf](tpc-147-tt-periodic-residue-reassembly.pdf), SHA-256 `7cc1327585910ecfe4001ce5978b95ca7f0d77607d9e4fec13c583149b6236c1`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `0e2aaad5c9e30055579bb913a4f860e46194cc53110cfe13a87cf6504e680761`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC147_149.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The exact source contract` | 75 | 1 | `HEADING_TEXT_MATCH` |
| `An exact periodic residue partition` | 131 | 2 | `HEADING_TEXT_MATCH` |
| `Periodic reassembly without a census loss` | 165 | 2 | `HEADING_TEXT_MATCH` |
| `What is and is not an \texorpdfstring{\(\ell^1\)}{l1} cost` | 227 | 3 | `HEADING_TEXT_MATCH` |
| `Certificate and claim boundary` | 262 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 303 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `85` before writing and `85` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `14`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `906499c5fa3bcc6a1bc7f8d599f2e1efa7e872c66ebb5f8d85309672866000b3`.
- Source theorem/proof environment starts: remark at TeX line 121, lemma at TeX line 140, proof at TeX line 155, theorem at TeX line 167, proof at TeX line 191, corollary at TeX line 213, proposition at TeX line 246, proof at TeX line 254.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 81–83 | `710c85ef9df8e6d43f0feafe878c185b80799ad09bc4c8b7ee8a8ae02f717481` |
| D02 | equation | 85–88 | `acdf59a30d1e9b43220560f5df5b41403d421ec62f8e1763f79bcb49f7523d5f` |
| D03 | \[...\] | 93–95 | `41ac25282855ba668c0296e661b845e820b2824a85892f64c1c523c6b1443cc2` |
| D04 | equation | 97–101 | `e7f74325191fa72fa9f3e6d09884aafa01bc91e1e398ca7f6545a704166b5918` |
| D05 | \[...\] | 103–107 | `35eb61b49094a6352a955d516cf4b018c5ab9493538bdf1edd9eaf67e8e1d912` |
| D06 | equation | 109–116 | `410a89dab9162de5a9acfb8a5b7e53ee88fbf48a6a1c4b3bf6d15d577673957b` |
| D07 | \[...\] | 135–137 | `eb7da2190048fc7f7c14bb627141fe5156d00993363fd52d5e76b8cb6ca3216e` |
| D08 | equation | 143–150 | `520c4f3ac1cab2103172194cdd7e50691ea0de03b07582f781dfaa5add0882c3` |
| D09 | equation | 171–174 | `37d33639e4dccb0b554d958206b29d6763e532cc9861b89ba2647ee2820f84c9` |
| D10 | align | 178–187 | `83e159468bcbabdc16795a9224e3782f7d6b05e605215700b130b307711e7937` |
| D11 | \[...\] | 198–200 | `e240f295f16f4f6cb6ea58b98c0ce8b48cf1cebaee2975c4b1a31effc9a08ae6` |
| D12 | \[...\] | 203–207 | `64b25bf07aea2f6e4ba0a7120faf679d57622c77d8cdd5aa68612199b2da0104` |
| D13 | equation | 230–233 | `b2545c2f45556a7e7e5a6ddc64fc87a16a4b782134feb332dbd502a735062e9c` |
| D14 | \[...\] | 237–241 | `6391e6ad32cf6e8d911948fa1566bed180c7cc964e5c7e8dbfa9690c61cfc373` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 38: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 55: `uniform in the congruence modulus, residue and two shifts after its`
- TeX line 67: `reassembly.  It does not remove an outer coefficient-mass loss and`
- TeX line 68: `does not cover a nonperiodic physical multiplier, a generic additive`
- TeX line 71: `arithmetic interface, not positive \(\Ltwo\), not an \(X\)-power`
- TeX line 72: `saving and not a prime-pair statement.`
- TeX line 118: `uniform in these parameters.  The normalization \(W/N\) is part of`
- TeX line 142: `For every finitely supported sequence \(F(n)\),`
- TeX line 162: `This is a pathwise partition, not a scalar replacement by a periodic`
- TeX line 169: `Assume the hypotheses of \eqref{eq:source} for fixed \(g_1,g_2\).`
- TeX line 208: `Multiplication by \(Q/N\) proves \eqref{eq:periodic}.  Uniformity of`
- TeX line 215: `Any finite product of bounded periodic masks may be combined into`
- TeX line 227: `\section{What is and is not an \texorpdfstring{\(\ell^1\)}{l1} cost}`
- TeX line 234: `It does not say that every finite decomposition has no cost.  If`
- TeX line 243: `splitting a nonperiodic multiplier into unrelated pieces does not`
- TeX line 269: `prefixes.  These are finite consistency checks, not numerical`
- TeX line 284: `\(\OPEN\); not in the theorem.\\`
- TeX line 286: `\(\OPEN\); no implication.\\`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:exception` → `../main.tex#L100` (existing project target or original TeX label line).
- Link relocation: `#eq:source` → `../main.tex#L115` (existing project target or original TeX label line).
- Link relocation: `#lem:partition` → `../main.tex#L141` (existing project target or original TeX label line).
- Link relocation: `#eq:source` → `../main.tex#L115` (existing project target or original TeX label line).
- Link relocation: `#eq:periodic` → `../main.tex#L186` (existing project target or original TeX label line).
- Link relocation: `#eq:height` → `../main.tex#L173` (existing project target or original TeX label line).
- Link relocation: `#thm:periodic` → `../main.tex#L168` (existing project target or original TeX label line).
- Link relocation: `#thm:periodic` → `../main.tex#L168` (existing project target or original TeX label line).
- Link relocation: `#eq:density-cancel` → `../main.tex#L232` (existing project target or original TeX label line).
- Link relocation: `#eq:exception` → `../main.tex#L100` (existing project target or original TeX label line).
- Link relocation: `#eq:periodic` → `../main.tex#L186` (existing project target or original TeX label line).
- Link relocation: `#eq:density-cancel` → `../main.tex#L232` (existing project target or original TeX label line).
- Link relocation: `#eq:source` → `../main.tex#L115` (existing project target or original TeX label line).
