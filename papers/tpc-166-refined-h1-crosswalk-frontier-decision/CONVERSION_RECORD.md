# TPC-166 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `44795630be600a5eda175702748e0849632d3da878f65a6a59e95657a970a54f`.
- Bibliography: [references.bib](references.bib), SHA-256 `71f05b5e7a941f490daafb03345a0a7edcfd712e376d8c8e9c71a5efa7a5b78b`.
- Preserved PDF: [tpc-166-refined-h1-crosswalk-frontier-decision.pdf](tpc-166-refined-h1-crosswalk-frontier-decision.pdf), SHA-256 `3e731f75f6f9ddc372101c86ba45eaa1cdf4e8cfb8221ebcdc9f6741cafd2c65`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `826a887dc5d673da5cdffd3a59047df38a4953568e8dbcdb97e61f746396e681`.
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
| `Historical pointer versus current refinement` | 110 | 1 | `HEADING_TEXT_MATCH` |
| `The complete H1 envelope remains outside this refinement` | 140 | 2 | `HEADING_TEXT_MATCH` |
| `The refined production DAG` | 184 | 2 | `HEADING_TEXT_MATCH` |
| `Exact three-root frontier` | 227 | 3 | `HEADING_TEXT_MATCH` |
| `A selected pointer that preserves the antichain` | 287 | 3 | `HEADING_TEXT_MATCH` |
| `Production evidence and verdict` | 322 | 4 | `HEADING_TEXT_MATCH` |
| `Why TPC-162 is not rewritten` | 373 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducible DAG audit` | 391 | 4 | `HEADING_TEXT_MATCH` |
| `Next source-producing task` | 412 | 5 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 429 | 5 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 444 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `71` before writing and `71` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `16`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `0b278552653b465ff4f503c00cd1d366bd1b564f0c94a0cea70ce7aa270d177c`.
- Source theorem/proof environment starts: definition at TeX line 172, definition at TeX line 216, theorem at TeX line 229, proof at TeX line 243, remark at TeX line 268, corollary at TeX line 276, proof at TeX line 281, proposition at TeX line 298, proof at TeX line 304, theorem at TeX line 348, proof at TeX line 364.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 67–73 | `9705ce18e8095ff4c19ff9c79131574c661c423055d9e876293719dbff6b7821` |
| D02 | \[...\] | 113–115 | `28a2e144577eff51e80ea637300e29f99b30307ec38db3148c2f4234a3570b91` |
| D03 | \[...\] | 117–121 | `523ad793c77e7dbe8b4d5d2d7df9f4b6ee39005ae2de5bcf168afde29c218b21` |
| D04 | \[...\] | 143–147 | `82a728362c1a422a9b3f92705953712341f64848248ccebfe2ff8273c5a5b648` |
| D05 | \[...\] | 149–164 | `6b83bfc46b3654773740dbfa04a1d15fd7dc894c993089533a039e4e5ed39d4d` |
| D06 | \[...\] | 187–196 | `3e0b4477b4bf5a5626c7a564f65518c59ab690d6ab6d57f2cfa3f9b491adbedb` |
| D07 | \[...\] | 199–209 | `7a69a671f6578b3b24e268f67e81e85af8b59b15116e49a7ad48ab7d81e6ca02` |
| D08 | \[...\] | 233–238 | `6dca019b20b49b224ff8b693543658d33d046a8887052ccaec9749ec3f1029cc` |
| D09 | \[...\] | 245–248 | `bffa092f3facfedc95ab03577c883898b183ff80fc0a156f45818505c8728e83` |
| D10 | \[...\] | 252–256 | `db360a188bc8547aa7120bfab00edc95f22741a4e564542636559e60e7dfd821` |
| D11 | \[...\] | 290–293 | `68d15f923d67c2b3d1afe04f9ddd207f93b923411522979aa471c7cd694134a9` |
| D12 | \[...\] | 306–312 | `27e63944304f141699a9ba61f2ac03edc63709fe108796874a6105f9825fe962` |
| D13 | \[...\] | 325–329 | `c4cf5775594814aac548e7a6ad4555e74b2ab1cfa3a93a69842e41ca29cbb6a6` |
| D14 | \[...\] | 351–359 | `5648278a61ff039728e0fc66f207f03ae4cac7d160edc9aa6d757b927c9dc1e5` |
| D15 | \[...\] | 376–380 | `849decbae6e7504dfb9975baa7b0687a15cf3faceccd23cd2225a798ad746915` |
| D16 | \[...\] | 384–386 | `0ffec5ff7d5b24f121f62dd8f52fdeee0314a775fce493c4bb93105a6f3bd41e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 78: `and the finite gluing theorem of TPC-165 are proved supporting nodes,`
- TeX line 100: `This paper refines a frontier; it does not close it.  It does not`
- TeX line 168: `scalar-plus-ETO clause is a separate \(\NT\) route and is not a child`
- TeX line 211: `\(G_{165}\) is the proved finite typed gluing theorem.  The three`
- TeX line 217: `For a target \(H\) in a finite prerequisite DAG, take the ancestral`
- TeX line 224: `an earlier unresolved prerequisite is missing.  It does not choose`
- TeX line 277: `Proving any one member of \(\mathcal A_{166}\) does not, by the`
- TeX line 338: `finite typed gluing theorem & \(\PROVED\)\\`
- TeX line 368: `the formal gluing theorem leaves source augmentation open.  Thus the`
- TeX line 438: `open, the verdict remains \(\NT\), and the next constructive target`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 5 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:historical` → `../main.tex#L120` (existing project target or original TeX label line).
- Link relocation: `#eq:dag` → `../main.tex#L208` (existing project target or original TeX label line).
- Link relocation: `#eq:antichain` → `../main.tex#L237` (existing project target or original TeX label line).
- Link relocation: `#eq:full-h1` → `../main.tex#L163` (existing project target or original TeX label line).
- Link relocation: `#eq:dag` → `../main.tex#L208` (existing project target or original TeX label line).
- Link relocation: `#eq:selected` → `../main.tex#L292` (existing project target or original TeX label line).
- Link relocation: `#eq:antichain` → `../main.tex#L237` (existing project target or original TeX label line).
- Link relocation: `#eq:selected` → `../main.tex#L292` (existing project target or original TeX label line).
- Link relocation: `#eq:antichain` → `../main.tex#L237` (existing project target or original TeX label line).
- Link relocation: `#eq:full-h1` → `../main.tex#L163` (existing project target or original TeX label line).
