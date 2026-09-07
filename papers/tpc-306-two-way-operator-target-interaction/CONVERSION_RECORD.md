# TPC-306 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ed725e6537012bd17a32d061d9d8e6dd3b253613`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `5d87da1cb344f6986484d6361ce6323034de8f69ed4314271b1587868e2e9945`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `20f1a625d07697dc595cce6d168701f3054c351a3f84955f568e8cebdbb37774`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `c8e1d7ed6b5d00afebf0c4c7ef6b3334b98eb87075be47cf0e682362ac87ea54`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `db1b1fac7e2242488e78fd1051b110d99067868d4b02ac126b45d162e4687d2f`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC305_309.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `From a target swap to a two-way table` | 33 | 1 | `HEADING_TEXT_MATCH` |
| `Effects and exact decomposition` | 60 | 1 | `HEADING_TEXT_MATCH` |
| `Finite certificate` | 110 | 2 | `HEADING_TEXT_MATCH` |
| `What this does and does not identify` | 165 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility and next question` | 186 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 196 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `59` before writing and `59` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `e8057422853805feb50c46676f853f108e601889c8555c6b1d6167e6c72f98df`.
- Source theorem/proof environment starts: proposition at TeX line 78, proof at TeX line 86, proposition at TeX line 97, proof at TeX line 101.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 48–54 | `2230f0a03d81239a9e298432ef26a748bdd27e42304c06521ec7332e172dccbe` |
| D02 | \[...\] | 64–67 | `c0498108935d5f66e04fb68ef442b61e31fef1f378ff0943e20500c60030e9f7` |
| D03 | \[...\] | 70–74 | `e86ba6d826add77c7ece4eb5a9626a176308f4cb7b979d127f45bc27d78a92bb` |
| D04 | \[...\] | 80–82 | `9852d1a0750cc02f29561d7e17f806200aee79110d9e73104acac99c069e071a` |
| D05 | \[...\] | 89–91 | `ea8a5f381f72e88b74c8604059c43bca9b422cd995cfcfbc42b7f362c633f6be` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 29: `dominant.  The finite diagnostic quantifies, but does not remove, the`
- TeX line 44: `We retain exactly the TPC-305 finite data: two kernel exponents, three`
- TeX line 108: `main preferences.  This terminology is algebraic; it is not a causal claim.`
- TeX line 110: `\section{Finite certificate}`
- TeX line 114: `checker does not import this producer: it replays the logarithms with`
- TeX line 162: `upper endpoint is below $0.64$.  Thus the finite atlas has a visible gap`
- TeX line 165: `\section{What this does and does not identify}`
- TeX line 177: `to their row.  Consequently the table is not a balanced intervention on a`
- TeX line 181: `The decomposition also supplies no arithmetic $L^2$ estimate, fixed power`
- TeX line 193: `made that the finite orientation persists as $Q$ or $N$ grows.`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:pair` → `main.tex#L125` (existing project target or original TeX label line).
- Link relocation: `#tab:central` → `main.tex#L144` (existing project target or original TeX label line).
