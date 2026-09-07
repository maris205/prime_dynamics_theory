# TPC-280 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `928077a9bd66c38f38bd0a9ee65d7b903ff25814`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `4889234c04316333aecdf027c733d6199acd9c705c04184cc762d1a156665ee6`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `caa86b7f5890ef5911edcaf8ee4bc2d3c9f3360655479860c121e9c4301c7b3c`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `dd48180fbe6907466377f39cefbe1c2d33ae39ff32dd625de88426cee8c65e65`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `4a144102d088205c9015217dfb2bf040a82e759a99622721bbd45616887bda2b`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC280_284.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The source interface` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `The two-term compiler` | 70 | 2 | `HEADING_TEXT_MATCH` |
| `Margin and endpoint accounting` | 112 | 2 | `HEADING_TEXT_MATCH` |
| `Sharpness and the leakage obstruction` | 159 | 3 | `HEADING_TEXT_MATCH` |
| `Exact fixtures and parent transfer` | 187 | 3 | `HEADING_TEXT_MATCH` |
| `Route consequence and claim firewall` | 226 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 255 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `90` before writing and `90` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `12`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `690d726c2df6d6af0967b7137907ed22af18b76d6c3ce081b51bf752f1442bec`.
- Source theorem/proof environment starts: theorem at TeX line 72, proof at TeX line 96, corollary at TeX line 123, proof at TeX line 141, proposition at TeX line 161, proof at TeX line 174.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 28–30 | `f988ae32931c34ca3a514377d24fbbeb99b7dc2c8a0a7077ec8cbc9b465b99af` |
| D02 | \[...\] | 32–36 | `80a3244ce31dbd08cf465166a52b74649945f108ad722fcb0e1ad7fc62cdcda5` |
| D03 | equation | 58–62 | `601b2939e27241a4b4841608a63b11a0eb37470d1e0184aa09819d73596ef208` |
| D04 | \[...\] | 74–77 | `590a914e8bdbbc8813f5f71f397869d31cf7bcd3c26f4eb0aa9da10d4fe2d3ac` |
| D05 | align | 79–84 | `97406c7be78610921ff11b93b3f43769c83c37a8e15eb169e605516ae540fd8b` |
| D06 | align | 86–92 | `063b502f47717fbd7dcaa9566c45ccda285eae0c235b042ffb7c56cba8ea2e69` |
| D07 | equation | 115–118 | `fe12e11b3d561865747c0822bbcb3ce175c86b332385cbb32b3b396ba945b843` |
| D08 | equation | 125–129 | `8d8f8dd5b430ec26f988b2ce53956dfb1e7b79a76ad3d7c0d940815ca8c1e416` |
| D09 | equation | 131–134 | `f2491678368dc6f4273172d429ce650bd42e3049fab22b3c948216fee70d3242` |
| D10 | \[...\] | 136–138 | `4277e3b8e64ba5a4ed8844537b9631a89031d928ac6ef6ed9a9e98fbe8fe84e4` |
| D11 | equation | 151–154 | `3151ce42560d351a602663afd0bbb6c4b312c9c4d4ab02ea093ebb023e900008` |
| D12 | \[...\] | 164–167 | `1419a62dab6e93698a50c7bce745af2dc8fc96290f276d1018e1ed1d8ef95b06` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 26: `open how a non-multiplicative error should be charged.  We prove a conditional`
- TeX line 46: `certified.  No arithmetic $L^2$ estimate or twin-prime conclusion is claimed.`
- TeX line 57: `absolute scale.  We therefore assume`
- TeX line 73: `Assume \eqref{eq:raw} and set`
- TeX line 106: `The two-term form is the useful one at finite scales: it retains the crossover`
- TeX line 120: `Equation \eqref{eq:margin-identity} is an interface assumption for this`
- TeX line 121: `compiler, not a new arithmetic estimate.`
- TeX line 184: `The equality family is an information-model adversary, not a claim that the`
- TeX line 222: `eight positive-deficit and four negative-deficit rows.  This finite census`
- TeX line 223: `validates the coordinate interface; it does not assert that the literal source`
- TeX line 228: `The new result is a conditional compiler, not an arithmetic payment.  To use`
- TeX line 231: `the leakage term.  In particular, the theorem does not convert a finite table`
- TeX line 242: `finite rational fixtures and parent transfer & \textsc{numerically certified}\\`
- TeX line 243: `literal growing source decomposition & \textsc{open}\\`
- TeX line 244: `arithmetic $L^2$ / full Gate B & \textsc{open}\\`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:raw` → `main.tex#L61` (existing project target or original TeX label line).
- Link relocation: `#eq:raw` → `main.tex#L61` (existing project target or original TeX label line).
- Link relocation: `#eq:two-term` → `main.tex#L81` (existing project target or original TeX label line).
- Link relocation: `#eq:collapsed` → `main.tex#L83` (existing project target or original TeX label line).
- Link relocation: `#eq:gain-two` → `main.tex#L89` (existing project target or original TeX label line).
- Link relocation: `#eq:gain-collapsed` → `main.tex#L91` (existing project target or original TeX label line).
- Link relocation: `#eq:raw` → `main.tex#L61` (existing project target or original TeX label line).
- Link relocation: `#eq:margin-identity` → `main.tex#L117` (existing project target or original TeX label line).
- Link relocation: `#eq:margin-identity` → `main.tex#L117` (existing project target or original TeX label line).
- Link relocation: `#eq:margin-identity` → `main.tex#L117` (existing project target or original TeX label line).
- Link relocation: `#eq:collapsed` → `main.tex#L83` (existing project target or original TeX label line).
- Link relocation: `#eq:margin-collapsed` → `main.tex#L133` (existing project target or original TeX label line).
- Link relocation: `#eq:two-term` → `main.tex#L81` (existing project target or original TeX label line).
- Link relocation: `#eq:gain-two` → `main.tex#L89` (existing project target or original TeX label line).
- Link relocation: `#tab:budget` → `main.tex#L209` (existing project target or original TeX label line).
- Link relocation: `#eq:two-term` → `main.tex#L81` (existing project target or original TeX label line).
- Link relocation: `#eq:collapsed` → `main.tex#L83` (existing project target or original TeX label line).
- Link relocation: `#eq:margin-two` → `main.tex#L128` (existing project target or original TeX label line).
- Link relocation: `#eq:endpoint` → `main.tex#L153` (existing project target or original TeX label line).
- Link relocation: `#eq:raw` → `main.tex#L61` (existing project target or original TeX label line).
