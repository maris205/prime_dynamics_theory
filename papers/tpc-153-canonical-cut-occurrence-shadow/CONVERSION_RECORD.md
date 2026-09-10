# TPC-153 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `310086b540b3335bd9f71897ca9bb7e65637d53e8618c1873eb9e5d212474249`.
- Bibliography: [references.bib](references.bib), SHA-256 `4068256b805be2174d3e8a2880260a1da6477b887d664b33554fde228501fb02`.
- Preserved PDF: [tpc-153-canonical-cut-occurrence-shadow.pdf](tpc-153-canonical-cut-occurrence-shadow.pdf), SHA-256 `446d80ba8e892064c6389911f92adfd0f705692b6b12074e8843c12a8da04528`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8c689ec185e7a4ea9499777ed00d7499cd84402ee0a28e437fb9de4e56a2eae3`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC153_156.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The exact input` | 86 | 1 | `HEADING_TEXT_MATCH` |
| `The cut-occurrence shadow` | 132 | 2 | `HEADING_TEXT_MATCH` |
| `Exact reconnection with the soft rows` | 189 | 2 | `HEADING_TEXT_MATCH` |
| `Universal pushforward property` | 222 | 3 | `HEADING_TEXT_MATCH` |
| `What remains deliberately absent` | 281 | 3 | `HEADING_TEXT_MATCH` |
| `Executable finite certificate` | 318 | 4 | `HEADING_TEXT_MATCH` |
| `Kill criteria and next artifact` | 372 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 396 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `85` before writing and `85` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `16`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `2e8193c29c4f7e6cc6835da073b7fc7fa3d488a355a80203f7285d962ee5fca6`.
- Source theorem/proof environment starts: definition at TeX line 121, definition at TeX line 134, definition at TeX line 148, theorem at TeX line 159, proof at TeX line 172, remark at TeX line 181, proposition at TeX line 200, proof at TeX line 212, definition at TeX line 227, theorem at TeX line 247, proof at TeX line 258, corollary at TeX line 266, proposition at TeX line 298, proof at TeX line 311.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 65–69 | `944dbe4033cb8b059095ba44b5d3af083c37a3e31bcbf90597354f22ff228f6b` |
| D02 | \[...\] | 92–94 | `a2a09f78d71a0afb2da1aabf22c12645cd923c9227708cf3e0c425dec32060bf` |
| D03 | equation | 97–100 | `48ccdfa31a4035f974f3b68dd65c907bfd558bb03a98cde76fbaffbd071f4850` |
| D04 | \[...\] | 136–138 | `f020cd5728480549d6b052af4de118e4225a78a9239b7413324811dfb57ed804` |
| D05 | \[...\] | 140–142 | `56990ea461987be1dd25f71bfef7373c88f09d222d1fe912871f7a7979b15670` |
| D06 | equation | 150–154 | `9d9112aa8db4e8da9c53fd191eff302e7168f930f1fcd4e0665a82a71dc9881b` |
| D07 | equation | 163–166 | `cae1e9de33234f0e0d6616a2d81dede90bbfdfbe18d88406aeadb8e97980852d` |
| D08 | \[...\] | 193–198 | `cee1cd93f3ba4be7913862eb9e901a3977a617868f93372d779b087b9351c2a6` |
| D09 | equation | 203–208 | `5e6a3418391e0622571664d83c7c1b988fd4a0152d799204b50dd9f0b8240d9c` |
| D10 | \[...\] | 230–232 | `511160ca1543117ed94a06aeb81b3c208512e0bdaa8684874c02d2bb949c308d` |
| D11 | \[...\] | 236–238 | `e50869709f8435fd2befecfcf9aad17ce1b16919cdc777a2f7715f0b856ce4d2` |
| D12 | equation | 240–244 | `4a364fcb00f9e4b48a2b97289224b1f256b415861f47c8019dde63305bc92507` |
| D13 | equation | 250–253 | `a71012f899985eb1e5e5aa0f08d19f4e5d0fb55c3dab0db9bc7c054fe9e432a8` |
| D14 | \[...\] | 268–270 | `b6d5aa168b61a138d618aa9cfcc80db8318d7678438328c212d06736d5941ae5` |
| D15 | \[...\] | 332–336 | `7789e8f65bc76fecf4d95c455166aaaca951dc3abb042a0ffdff0356370347e5` |
| D16 | \[...\] | 345–348 | `966d29fcd000745a395bd659a8fe753e5cd6c3ff0bec1078958a52b40c61b38e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 61: `downstream occurrences.  The existing archive does not contain those`
- TeX line 70: `There is exactly one shadow row for every eligible-tail-open or`
- TeX line 78: `\(S_X\).  This universal property does not produce such a lift.`
- TeX line 81: `eligible-tail fixture is marked synthetic \(\mathrm{L0}\) only and`
- TeX line 83: `\(\mathrm{L1}\) progress, not a fixed-shift arithmetic saving.`
- TeX line 102: `finite fixture.  TPC-143 attaches an explicit lift obligation to`
- TeX line 110: `\item \(X,h_0,Q,U,V\), the weight-source identifier and physical`
- TeX line 145: `occurrence}; it is not an actual downstream occurrence.`
- TeX line 168: `\(h_0\), physical normalization, source path and formal-support`
- TeX line 185: `actual rows without changing the sourced column total.  It does not`
- TeX line 279: `not a construction of the missing lift.`
- TeX line 283: `The partial row reserves, but does not populate, the following field`
- TeX line 294: `does not give a row-level cut-to-stage-to-parent occurrence crosswalk`
- TeX line 318: `\section{Executable finite certificate}`
- TeX line 339: `relabeling, nonunit weight, \(h_0\) or normalization drift, active`
- TeX line 350: `marked \texttt{SYNTHETIC\_L0\_ONLY}.  It tests that the union`
- TeX line 367: `& Open & A theorem-backed external crosswalk may extend the shadow.\\`
- TeX line 376: `column sum differs from \(1\), or if native, \(h_0\), normalization`
- TeX line 383: `multipliers, native and \(h_0\) lineage, physical normalization,`
- TeX line 389: `fixed-\(h_0\) \(\Ltwo\) saving, endpoint below \(1/400\), prime-pair`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:shadow-conservation` → `../main.tex#L165` (existing project target or original TeX label line).
- Link relocation: `#eq:shadow-conservation` → `../main.tex#L165` (existing project target or original TeX label line).
- Link relocation: `#eq:universal` → `../main.tex#L252` (existing project target or original TeX label line).
- Link relocation: `#eq:fiber-conservation` → `../main.tex#L243` (existing project target or original TeX label line).
- Link relocation: `#eq:fiber-conservation` → `../main.tex#L243` (existing project target or original TeX label line).
- Link relocation: `#thm:universal` → `../main.tex#L248` (existing project target or original TeX label line).
- Link relocation: `#eq:shadow` → `../main.tex#L153` (existing project target or original TeX label line).
- Link relocation: `#eq:nonsoft-domain` → `../main.tex#L99` (existing project target or original TeX label line).
