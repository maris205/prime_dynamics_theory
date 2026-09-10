# TPC-172 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `17991bbcd072cedab101c95d3924bbff035aee06e6b41a3d19febdebd9af39a6`.
- Bibliography: [references.bib](references.bib), SHA-256 `c4c02014a8dd900ddf5fe11eb0afe5702d2b462371c741b6879d699532669734`.
- Preserved PDF: [tpc-172-mvp7-occurrence-phase-atomic-route-decision.pdf](tpc-172-mvp7-occurrence-phase-atomic-route-decision.pdf), SHA-256 `8bbf582d6c3bb9f50c34d600d4e35d19c7731b8348a32d7a67f6d3a84003dc70`; 6 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `7c90690ba64f18df310ca109915f523d9b27c02695da780e6f773334a6f6c693`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC170_174.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Imported state` | 88 | 1 | `HEADING_TEXT_MATCH` |
| `Six-axis projection` | 140 | 2 | `HEADING_TEXT_MATCH` |
| `Two route families` | 196 | 2 | `HEADING_TEXT_MATCH` |
| `Evidence modes` | 245 | 3 | `HEADING_TEXT_MATCH` |
| `Endpoint V4 classifier state` | 269 | 3 | `HEADING_TEXT_MATCH` |
| `Ordered classifier` | 318 | 4 | `HEADING_TEXT_MATCH` |
| `MVP7 decision` | 376 | 5 | `HEADING_TEXT_MATCH` |
| `Mutation audit and next decisions` | 425 | 5 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 447 | 5 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 461 | 6 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `65` before writing and `65` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `15`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `c652038daa56f4ffa8d5ce94a898d3f93ef1c7347e700f5b65f7e7c9f47eee2d`.
- Source theorem/proof environment starts: proposition at TeX line 174, proof at TeX line 186, definition at TeX line 227, definition at TeX line 305, definition at TeX line 324, theorem at TeX line 354, proof at TeX line 366, theorem at TeX line 378, proof at TeX line 397, corollary at TeX line 414.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 77–79 | `c94ab2e962dfc392ad043ec1e1ffc4d489645bf3ebcf45c8cc418fb5401763ba` |
| D02 | \[...\] | 96–108 | `68fa911179bd94e0e408f1ea0424cf129f9af4944ad576b282cb2c0cd2aaba1d` |
| D03 | \[...\] | 113–118 | `4d0e04babd45cfd8fea2c3868f1742add760df58496c545b8c9e32d49fdbecc1` |
| D04 | \[...\] | 124–132 | `2795e16c20bd41a8504ff2948ce4f1b662423f33993792b4d07423550cef3a2e` |
| D05 | \[...\] | 143–147 | `ef6a4b6971677e214903f8b5141bf786ebf64b19a2bc9b12f07357503f5d354a` |
| D06 | \[...\] | 151–169 | `349ae86cfb5c08125b010a061b657cf7722ae8039984c9372b891b9c41a1f5b4` |
| D07 | \[...\] | 177–180 | `deb2dcb9f3957dfc720e321d432d4aa512f115f83d5ddeb90adca7a7ccc43956` |
| D08 | \[...\] | 202–207 | `8463c04d07ba57f9c9c72cb528051ece3f2010031faffe4ae145d7ff5f8324a1` |
| D09 | \[...\] | 215–224 | `6f440088d67e812ab63b34204e28f1d80784b330911ea2df8fd37c23c68940ba` |
| D10 | \[...\] | 260–263 | `84b4408cb62fe1298a831a3e5b53f430135897ac467b676a43e5cd91fc5866b1` |
| D11 | \[...\] | 290–294 | `6df2e1416f5250c984a3ccb2aeabf822c1fdabdc526585e32fad5b1ec4481234` |
| D12 | \[...\] | 297–301 | `88ae4ad841e8e4a3d49ec7d71846cc527ebebd3cb47c806575ec8d0ca43e33c5` |
| D13 | \[...\] | 327–335 | `b6e8d06f02ab87543a4d1e02c182c2892fa4e2dc521798eb2e928ae80c178d4d` |
| D14 | \[...\] | 357–362 | `60a5c2340261f6cf2fde4ec2273332514a1ec7b0d6949b8e4e2da3036deefb6d` |
| D15 | \[...\] | 381–391 | `a911789bb82aa86fdcd2286dd65a1c4b7f7bbbf00bb567ee15ea0e3d97f247b9` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 36: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 64: `does not reach a named physical phase.`
- TeX line 71: `method cell; it does not stop the direct fixed-phase twist or the`
- TeX line 110: `declared obligation order.  It does not replace the other six.`
- TeX line 114: `\mathcal F_{\rm open}`
- TeX line 117: `\tag{2}\label{eq:open}`
- TeX line 119: `The sets in \eqref{eq:blockers} and \eqref{eq:open} are disjoint in`
- TeX line 120: `both status and role.  A missing artifact and an open theorem target`
- TeX line 156: `\text{actual fixed-}h_0\text{ packet}\\`
- TeX line 181: `It does not stop a source-backed metric-to-fixed-atom bridge, a`
- TeX line 259: `\(\mathsf{SYNTHETIC\_REACHABILITY}\) mode.  Its records carry`
- TeX line 261: `\mathsf{NONE\_SYNTHETIC\_REACHABILITY\_ONLY}`
- TeX line 262: `\tag{9}\label{eq:synthetic}`
- TeX line 265: `finite classifier logic reaches each verdict; they prove no`
- TeX line 274: `\item fixed physical \(h_0=2\);`
- TeX line 316: `and does not have the named-atom quantifier.`
- TeX line 331: `\NT,\quad\AF,\quad\OPEN`
- TeX line 350: `\item \(\OPEN\): every other valid state.`
- TeX line 360: `\STOPR,\quad\NT,\quad\AF,\quad\OPEN.`
- TeX line 363: `Every result is reached by a finite typed regression state.`
- TeX line 369: `unique first true predicate exists.  The synthetic suite supplies one`
- TeX line 370: `separate assumed-predicate state for each valid verdict and one`
- TeX line 372: `firewall \eqref{eq:synthetic} prevents these reachability witnesses`
- TeX line 393: `pointwise arithmetic targets \eqref{eq:open} remain parent-ready`
- TeX line 394: `\(\OPEN\).`
- TeX line 404: `before \(\AF\) or \(\OPEN\).`
- TeX line 435: `an \(\OPEN/\NT\) frontier merge; a positive named-atom exponent`
- TeX line 445: `method cell, the other remains open.`
- TeX line 453: `remaining gap is now a sharp quantifier interface, not an unspecified`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:blockers` → `../main.tex#L107` (existing project target or original TeX label line).
- Link relocation: `#eq:open` → `../main.tex#L117` (existing project target or original TeX label line).
- Link relocation: `#eq:projection` → `../main.tex#L168` (existing project target or original TeX label line).
- Link relocation: `#eq:methods` → `../main.tex#L223` (existing project target or original TeX label line).
- Link relocation: `#def:reroute` → `../main.tex#L228` (existing project target or original TeX label line).
- Link relocation: `#def:AF` → `../main.tex#L306` (existing project target or original TeX label line).
- Link relocation: `#eq:order` → `../main.tex#L334` (existing project target or original TeX label line).
- Link relocation: `#eq:synthetic` → `../main.tex#L262` (existing project target or original TeX label line).
- Link relocation: `#eq:blockers` → `../main.tex#L107` (existing project target or original TeX label line).
- Link relocation: `#eq:open` → `../main.tex#L117` (existing project target or original TeX label line).
- Link relocation: `#eq:blockers` → `../main.tex#L107` (existing project target or original TeX label line).
- Link relocation: `#eq:projection` → `../main.tex#L168` (existing project target or original TeX label line).
- Link relocation: `#eq:sigmas` → `../main.tex#L300` (existing project target or original TeX label line).
- Link relocation: `#eq:blockers` → `../main.tex#L107` (existing project target or original TeX label line).
