# TPC-175 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `4c554cdb7d3d6b23080cd3730c0b9845ffb9819ded243b42f0e3d4efec73902f`.
- Bibliography: [references.bib](references.bib), SHA-256 `6e5c69ecff953312a83366f805d8ae5692d708a8b6a35927223e51665853bf22`.
- Preserved PDF: [tpc-175-declared-corpus-local-edge-family.pdf](tpc-175-declared-corpus-local-edge-family.pdf), SHA-256 `5fd6fc4bd0c16caa7ca50b201c02115989b869a1acc04c6fdc8be3ffbef13ed4`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `1e97052ac9023849a41a912f701ae4ce10b9f8d9829b3ba38dab4903a080ad5d`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC175_179.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Admissible universe` | 53 | 1 | `HEADING_TEXT_MATCH` |
| `Scoped empty-family theorem` | 73 | 1 | `HEADING_TEXT_MATCH` |
| `Coverage and gluing state` | 105 | 2 | `HEADING_TEXT_MATCH` |
| `H1 consequence and dynamic route` | 130 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall` | 152 | 2 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 162 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `24` before writing and `24` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `3`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `863c85882a7d108ea39a52a8e88d10d9d4151e5f97b1b5182f65c4f32b9053ef`.
- Source theorem/proof environment starts: definition at TeX line 59, theorem at TeX line 75, proof at TeX line 86, proposition at TeX line 94, proof at TeX line 99.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 77–81 | `976ac0184869002c2e1067e1d9b215543da1bb9ff86db9a9ee978784cc5e0590` |
| D02 | \[...\] | 109–122 | `e1d261c40f6e0f9af6836d023147977b20fbaaf9b2681bae029d07325cde7038` |
| D03 | \[...\] | 133–135 | `8e57704e390671ea204fbb701b15516ea83a3f448a03a7c94d384a9af39edda2` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 37: `TPC-174 proves a finite witness-verifier interface, but its only positive`
- TeX line 38: `fixture is synthetic \(\Lzero\) and its production witness is absent.  We`
- TeX line 69: `Synthetic fixtures, shadow rows, archive addresses, formal gluing`
- TeX line 100: `The admissible universe explicitly quantifies only over the finite`
- TeX line 107: `The finite production archive has \(2988\) cut rows.  Since`
- TeX line 124: `TPC-165 assumes a nonempty local row family over every cut in a declared`
- TeX line 125: `cover \citep{WangTPC165}.  The empty family does not satisfy that hypothesis.`
- TeX line 154: `This is a scoped \(\Lone\) empty-inventory/maximality theorem with finite`
- TeX line 157: `representation, fixed-\(h_0\) edge theorem, named fixed phase, positive`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#def:edge` → `../main.tex#L59` (existing project target or original TeX label line).
- Link relocation: `#def:edge` → `../main.tex#L59` (existing project target or original TeX label line).
- Link relocation: `#eq:empty` → `../main.tex#L80` (existing project target or original TeX label line).
- Link relocation: `#eq:coverage` → `../main.tex#L121` (existing project target or original TeX label line).
