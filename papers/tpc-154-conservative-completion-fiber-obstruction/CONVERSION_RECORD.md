# TPC-154 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `28bf9b9b1d868e8fd8e8126e689fa05b332f701177b5eb80a9fc6ce597e28097`.
- Bibliography: [references.bib](references.bib), SHA-256 `421d27a402c47202679c2dfcf4f9a9a3ba417870e1c773c10444fc0e9515db8b`.
- Preserved PDF: [tpc-154-conservative-completion-fiber-obstruction.pdf](tpc-154-conservative-completion-fiber-obstruction.pdf), SHA-256 `6609f8b96d20f5baa7ff55b40d63def6b95a111ae839436fd7b893b40ce5ca85`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `d34e2219758fa8ef01fc087b683454430cf82ac990a6a4edba91d43959e24636`.
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
| `Question and scope` | 79 | 1 | `HEADING_TEXT_MATCH` |
| `The free conservative completion class` | 105 | 1 | `HEADING_TEXT_MATCH` |
| `Two inequivalent completions` | 163 | 2 | `HEADING_TEXT_MATCH` |
| `What is and is not identifiable` | 226 | 3 | `HEADING_TEXT_MATCH` |
| `The exact negative theorem` | 270 | 3 | `HEADING_TEXT_MATCH` |
| `Why this does not prove impossibility` | 299 | 4 | `HEADING_TEXT_MATCH` |
| `Executable certificate` | 331 | 4 | `HEADING_TEXT_MATCH` |
| `Kill criteria and next object` | 384 | 5 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 410 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `70` before writing and `70` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `2f8f5d3d96afd6e4f7212c01513595a95162d3d68a2308f85f6b2199efe187b9`.
- Source theorem/proof environment starts: definition at TeX line 107, definition at TeX line 122, proposition at TeX line 138, proof at TeX line 148, definition at TeX line 165, definition at TeX line 173, definition at TeX line 190, theorem at TeX line 201, proof at TeX line 211, corollary at TeX line 232, proof at TeX line 238, proposition at TeX line 243, proof at TeX line 258, theorem at TeX line 272, proof at TeX line 285, remark at TeX line 292, proposition at TeX line 307, proof at TeX line 318.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 82–85 | `d7ace512b113d73d86ca021a2963d93705d73526407bd18998f4916049a6e95e` |
| D02 | equation | 111–114 | `dd4018a4046e57d44a9e2d38fae6c5ff6b2bddb68cc0cdac9000dccf7fd8eee8` |
| D03 | \[...\] | 124–126 | `3586390d6c75e4ee88e36c12315b40a733d6b30c11d77a77a4ec6d413cd18152` |
| D04 | \[...\] | 128–132 | `81217e05a98ba6a7cfa8957610021317e797330c6aca1ae7c050297f66a5d2d8` |
| D05 | \[...\] | 141–145 | `9b75395b56ad108cab0c740c676dc3b179af25d4ff3279b67ff6d8b372e61d89` |
| D06 | \[...\] | 150–153 | `d07892d77f229eee49681a9abb896639a5f75b823d86e0524099085c1c101319` |
| D07 | \[...\] | 167–169 | `ce2f324375dfde61b8a24f40d89178f839f7c6e1d73adc640f93f60a75addc1e` |
| D08 | \[...\] | 175–179 | `7402ebf3c61af159c1faf7b08c1428489c3f89f29c6c686a07f5ac403aca4025` |
| D09 | \[...\] | 195–197 | `124d64d6ae870fa55642da5653d8d2a327cdd18e18ebd5405e65088b87add2aa` |
| D10 | \[...\] | 205–207 | `a37f3cf75e0d731054dea0c4942600dd3a3accc9c7beef6a5dee091e0133223a` |
| D11 | \[...\] | 215–217 | `8a00519393b241e52664c4dfd56c42d21a1a0f8c565c286be2207fe92bcf5073` |
| D12 | \[...\] | 278–282 | `d7e2825a827b0bd28b6d30b6f7d666b0fdadf4d913f56c1066e0102495f1f5ec` |
| D13 | \[...\] | 342–349 | `176ecc31359323cf86c5227b906d4b4b83733abd7494167be3506b4c9fab8061` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 74: `route open.  A deterministic certificate verifies the obstruction on`
- TeX line 75: `all \(2988\) production fibers and on one separately marked synthetic`
- TeX line 101: `present artifacts.  It is not a statement that the mathematical`
- TeX line 108: `For \(u=\iota(c)\in\Ocut\), a finite formal completion is a nonempty`
- TeX line 116: `tuple, source \(h_0\), physical normalization and formal-support role`
- TeX line 160: `interface and does not add an unarchived actual-support, canonical`
- TeX line 223: `elementary.  It does not depend on cancellation between different`
- TeX line 232: `\begin{corollary}[Branch count does not descend]`
- TeX line 243: `\begin{proposition}[Downstream provenance does not descend]`
- TeX line 294: `Such a convention is not a theorem-backed recovery of the actual`
- TeX line 299: `\section{Why this does not prove impossibility}`
- TeX line 309: `\Cref{thm:obstruction} does not imply:`
- TeX line 347: `\text{synthetic L0 ETO}&1&(1,2).`
- TeX line 352: `unique.  The synthetic ETO fiber remains outside the production`
- TeX line 355: `Each edge contains the source native tuple, source \(h_0\), physical`
- TeX line 359: `synthetic-ETO omission, a cross-fiber edge, nonconservative weights,`
- TeX line 360: `native/\(h_0\)/normalization drift, missing parent or stage data,`
- TeX line 361: `active-support or actual-provenance promotion, an assumed`
- TeX line 378: `Selected augmented route & Open & Not stopped by the formal`
- TeX line 396: `eligible-tail-open and frontier-unmapped source.  It must include`
- TeX line 403: `estimate, positive fixed-\(h_0\) \(\Ltwo\) saving, endpoint below`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:column` → `../main.tex#L113` (existing project target or original TeX label line).
- Link relocation: `#prop:forget` → `../main.tex#L139` (existing project target or original TeX label line).
- Link relocation: `#prop:labels` → `../main.tex#L244` (existing project target or original TeX label line).
- Link relocation: `#cor:branch` → `../main.tex#L233` (existing project target or original TeX label line).
- Link relocation: `#prop:labels` → `../main.tex#L244` (existing project target or original TeX label line).
- Link relocation: `#thm:obstruction` → `../main.tex#L273` (existing project target or original TeX label line).
