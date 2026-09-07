# TPC-324 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `88c46824c79e9c202a698cf4db36fcaf98260537`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `15f3cf28a447323e8375da11c42534d5411588b83621d4331d1d5a2516f848af`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `fc9476d9320ed5a2297e8247730ef6e65fd07222f22f3b430d574b0c0a9daccb`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `fce6bdb222763178199ba28b375e31e913c8e4c4483f8dbc3cec55816e8ffb57`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8f525ffcb7ca3dc57a712ccbc67686cbed7a5c25b385e2f460eea98d861455a6`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC320_324.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 41 | 1 | `HEADING_TEXT_MATCH` |
| `Literal block family` | 57 | 1 | `HEADING_TEXT_MATCH` |
| `An exact covariance control` | 92 | 2 | `HEADING_TEXT_MATCH` |
| `Frozen holdout protocol` | 123 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 153 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and firewall` | 192 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and next route` | 211 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 221 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `54` before writing and `54` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a8c98a2a3a8c73631ea533aef24a09bf4494dd57b1cfc156361257341d7e3609`.
- Source theorem/proof environment starts: proposition at TeX line 97, proof at TeX line 109.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 61–66 | `41fcfcd722358032226d53b290d07d2ef0b3a416e92c1bc6a8cd73c2773a585b` |
| D02 | \[...\] | 68–71 | `41257765f1c3551ea7a7452d0569cba295c5ae137914ec7967fef7299a6e5cd5` |
| D03 | equation | 73–79 | `75a023f3a7e5e53f90b66f649cd371413da727ec1b542bfe367408147efb2069` |
| D04 | \[...\] | 81–83 | `baf2d8b4580d45a2a62a2558780a47975537a2dffe13ed6d99fcaf617b4a26aa` |
| D05 | \[...\] | 85–87 | `3b240bb1ef74597327351acec135a2b2c0dd13b2bcd58b704b7d7f35a9ca29d0` |
| D06 | \[...\] | 101–105 | `d384989be3e1e0edb9ebc169c77d18275e50f0d6fc6fe37c3ebcf0b7f7f16c74` |
| D07 | \[...\] | 177–179 | `52fd350cf4a563af47da962b4ac158353bf87b99281f45c1dd89ed80bbd978ca` |
| D08 | \[...\] | 202–204 | `4e18fa2da7bf2899c08244b17517815daf9d07253c23093d1aa284869e41b7a2` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 26: `We test whether the finite trace-normalized spectral-profile`
- TeX line 36: `finite, independently replayed source-location replication; it supplies no`
- TeX line 53: `The conclusion is deliberately finite.  In particular, ''replication''`
- TeX line 59: `For a finite interval $I\subset\mathbb Z$, $p\in\PP_Q$ and $s\in\{1,2\}$,`
- TeX line 90: `usual finite majorization convention \cite{marshall2011,bhatia1997}.`
- TeX line 120: `an exact reusable control, not a reason to identify the two panels with the`
- TeX line 162: `\caption{Finite profile census on the two holdouts.}`
- TeX line 183: `coordinate still crosses the direct baseline.  The finite alternative-law`
- TeX line 197: `obstruction is equally important: replication of a finite profile pattern`
- TeX line 198: `does not provide a source-native arithmetic representation of the signs.`
- TeX line 203: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE\_SOURCE\_LOCATION\_HOLDOUT\_REPLICATION}.`
- TeX line 205: `It earns no fixed-power credit.  A uniform scale theorem, canonical`
- TeX line 207: `payment, and the twin-prime endpoint remain open.  The Session-named`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:block` → `main.tex#L65` (existing project target or original TeX label line).
- Link relocation: `#tab:panels` → `main.tex#L134` (existing project target or original TeX label line).
- Link relocation: `#tab:census` → `main.tex#L163` (existing project target or original TeX label line).
