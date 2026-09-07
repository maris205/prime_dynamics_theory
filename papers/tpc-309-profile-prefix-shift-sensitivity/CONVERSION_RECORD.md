# TPC-309 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ed725e6537012bd17a32d061d9d8e6dd3b253613`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `d898866c746655920bd4297508a1ed4f593ae7a0113b3b87fdb040a7a57454c6`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `bc7d055c705d3ba332be5aba710a5baf04215d99a9d96f21abc820b51255617c`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `057d7ca591a0806b1dc7aa74cf52850b12cd7b1049ec9e75246e9c4d80bdd5d3`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `50e195e54a70d2f567cce508055f5bec8ec212757d5031c40fa6de3cb4aad9ae`.
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
| `Question and frozen parent object` | 41 | 1 | `HEADING_TEXT_MATCH` |
| `Finite protocol and exact algebra` | 84 | 2 | `HEADING_TEXT_MATCH` |
| `Numerical implementation` | 158 | 3 | `HEADING_TEXT_MATCH` |
| `Results` | 177 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and route status` | 244 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 274 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 286 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `88` before writing and `88` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `f121ff8017e7c458a591cb42d34ec1d2f7e9d7a708f444323010558d63f55e93`.
- Source theorem/proof environment starts: proposition at TeX line 116, proof at TeX line 123, proposition at TeX line 131, proof at TeX line 142, remark at TeX line 151.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 62–64 | `bdbbfa88af30508c06cf728f6189fca70b4fb492cace598a372b44702d9076ff` |
| D02 | \[...\] | 70–72 | `5f5ab63594011f1227e0e1851fbbf4ccd9fee4e846927c54829ea6e8171d1cce` |
| D03 | \[...\] | 74–80 | `4a526daae185afe81bd695c85bb43088201843ea46da8b8d057b97ab532f1410` |
| D04 | \[...\] | 92–94 | `1567095e7f589018383bc5cd935398033aa39c33a3260d7c03dfa59fa419cb77` |
| D05 | \[...\] | 103–107 | `a254a051ccf960111aeb26ef15c616c2c465e9c709933a1e7479f8355d2dab4b` |
| D06 | \[...\] | 109–112 | `5600446c67d563f8574d0efc6cc3dd9ba3ff97cbcb414df9de07e84eb9d2d247` |
| D07 | \[...\] | 134–136 | `95faa81de877d703d9abdfa8fdf6a71c510e10e2fc01cb8d83d56ba971d6304c` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 21: `The finite common-ambient holdout of TPC-308 used one ordered source-profile`
- TeX line 29: `The exact finite protocol gives three source-backed windows, while a producer`
- TeX line 35: `BASE retain one each.  Thus the location and persistence of the finite`
- TeX line 37: `finite model-selection obstruction, not a causal, asymptotic, arithmetic, or`
- TeX line 48: `depend on the selected finite source-profile prefix?`
- TeX line 84: `\section{Finite protocol and exact algebra}`
- TeX line 102: `prediction $y$, define the finite completion ball and its loss envelope by`
- TeX line 116: `\begin{proposition}[Finite window and prefix facts]`
- TeX line 131: `\begin{proposition}[Finite completion and ratio facts]`
- TeX line 139: `and denominators are positive, (4) contains every finite completion ratio.`
- TeX line 152: `The completion ball is an adversarial finite diagnostic, not a probability`
- TeX line 170: `The standalone checker does not import the TPC-309 producer.  It reloads the`
- TeX line 175: `declared finite object, but not a directed-rounding certificate.`
- TeX line 234: `finite observation is therefore neither location-stable nor uniformly`
- TeX line 240: `This confirms that the result is a sensitivity statement about the finite`
- TeX line 246: `The strongest positive result is a reproducible finite protocol in which the`
- TeX line 251: `The natural open theorem would require a profile-independent preference or a`
- TeX line 258: `from TPC-302; changing profile coordinates does not cure that leakage.`
- TeX line 259: `\item The three windows are a finite modeling choice, not an asymptotic family`
- TeX line 260: `and not a probability distribution.`
- TeX line 263: `\item No arithmetic $L^2$ estimate, fixed-power credit, uniform growing budget,`
- TeX line 279: `in the project directory.  All empirical statements above are finite`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:agreement` → `main.tex#L188` (existing project target or original TeX label line).
