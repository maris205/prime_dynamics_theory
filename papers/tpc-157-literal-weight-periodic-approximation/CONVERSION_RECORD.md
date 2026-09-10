# TPC-157 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `29aab509cb95fa24b19f23f67552021b805afefc1d11db95eb4ef58a1ae982c9`.
- Bibliography: [references.bib](references.bib), SHA-256 `b48c2f3ec8a1aeec3dde0a0fa45bf59a81d03025c0493a7acbc80741316c9190`.
- Preserved PDF: [tpc-157-literal-weight-periodic-approximation.pdf](tpc-157-literal-weight-periodic-approximation.pdf), SHA-256 `542abe9631c535aea0df758204a92a811d341dedfe9929483a6a739ed19e902d`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `89073f578f2273325b4d8534764159ad3cfc02b68c388e7a6164c15bc56dd33d`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC157_159.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The inherited periodic corridor` | 63 | 1 | `HEADING_TEXT_MATCH` |
| `The literal-weight interface` | 102 | 2 | `HEADING_TEXT_MATCH` |
| `Residue-fiber error optimization` | 163 | 2 | `HEADING_TEXT_MATCH` |
| `Products, phases and precise limitations` | 207 | 3 | `HEADING_TEXT_MATCH` |
| `Audit and progress classification` | 227 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 250 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 261 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `47` before writing and `47` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `16`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `15d457915e6986ecab3d128171e49d7f487dd0cfd300b24a253200849d55729b`.
- Source theorem/proof environment starts: theorem at TeX line 81, definition at TeX line 104, theorem at TeX line 117, proof at TeX line 128, corollary at TeX line 144, remark at TeX line 157, proposition at TeX line 170, proof at TeX line 185, proposition at TeX line 209.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 66–69 | `92d214601ec75b4fc5550fa02793b7cd098269cc4ed042dac9cbc6aa3ff75904` |
| D02 | \[...\] | 71–74 | `f156a8f484ecb49fa25af9acd52c92ad7d8dc67a301840244ac346c6d6a87639` |
| D03 | \[...\] | 75–77 | `66872ac96d3fa2e4684feb63a515444bee270751befc0957df17c22a6be52b81` |
| D04 | \[...\] | 85–88 | `ef7f70f4a62c432fdef37a518b5c524623502104862ad485783a3161ff4c3acf` |
| D05 | equation | 92–96 | `5b6baabe0b6cea45ca034c98d7f64aa47a344b8c8df3dcfed95d3893f7c019d9` |
| D06 | equation | 106–114 | `009c077ed274fb544726a6f196d8429ea383cfef2be2534d8f0168a7b274dd36` |
| D07 | equation | 119–124 | `f2bdd8801b1ab811540f228780bdc5649cdfeb59a5afdfae9e19ae3a660aa9b5` |
| D08 | \[...\] | 130–135 | `26c30b00dac144ffddeafed606d599dd79d26fb2bdc92921b81f4fbf6e766b34` |
| D09 | \[...\] | 138–140 | `3cdc32e34f3d224906a24ade59418dcf8c773f22b8325fd45be48aa1f9b784ca` |
| D10 | \[...\] | 148–152 | `8ba56dbe41d9c46ca176d03ef850d0f524478d5831f77bd1647ac325ad2b7253` |
| D11 | \[...\] | 166–168 | `8c6f82cfbbf33dc6454ec9f92f68433004330a93480e735fede5353433367029` |
| D12 | \[...\] | 172–177 | `d44677e7c16736e0362c3639c211eecb70648d2abb7aeee37ad22510737132c6` |
| D13 | \[...\] | 180–182 | `58d14c37590836f625c5862be46da685d297d7474635c7899a4ebd28f15df2c4` |
| D14 | \[...\] | 188–193 | `4747305ef6a0d31032e9f95a6c68b34321ddf5416642614fbc95a4671a32bf1c` |
| D15 | \[...\] | 199–203 | `6f27ea88a52d53ec38e1427d9256e46c18644e847fb460867a9a08f586ca6010` |
| D16 | \[...\] | 214–217 | `af53633cf87a32229ce19531ad8f4e5de0abd96116da5f33c14b97349361c59f` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 37: `multiplier on a literal two-M\"obius core, uniformly outside one`
- TeX line 57: `once a multiplier \(w\) is supplied.  It does not construct the`
- TeX line 100: `after seeing \(w\) does not require a union over its values.`
- TeX line 158: `The corollary is an implication, not a claim that the current`
- TeX line 204: `Thus the interface is finite and auditable whenever literal values of`
- TeX line 223: `\cref{thm:main} treats one interval \((N,2N]\); it does not convert`
- TeX line 258: `does not answer that question by schema, numerics or notation.`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#thm:149` → `../main.tex#L81` (existing project target or original TeX label line).
- Link relocation: `#thm:149` → `../main.tex#L81` (existing project target or original TeX label line).
- Link relocation: `#eq:periodic` → `../main.tex#L95` (existing project target or original TeX label line).
- Link relocation: `#thm:149` → `../main.tex#L81` (existing project target or original TeX label line).
- Link relocation: `#thm:main` → `../main.tex#L117` (existing project target or original TeX label line).
