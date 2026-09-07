# TPC-255 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `d1683c8f96ae1b86f2f9fcb9ba8318c9e1aaf3f6`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `372f84d7b590d0f927a75b603fa7b62b3e15ad1ef04c01aac6c4892e418278f1`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `63573811e67fb865b9ff83c87d668271058b0cb60d0e4807cc6c637196342c56`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `0a1c608ec09ef53ebc928269b877c54a8ee7574c1ba607ede890a64fb4c1dd66`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `623e0a01f3ce53195a30b94656f553eb142b9c2525ae695a4ef4dd472ee54983`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC255_259.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Frozen operator and ordered-rank test` | 44 | 1 | `HEADING_TEXT_MATCH` |
| `Complete row and exact adjoint decomposition` | 78 | 1 | `HEADING_TEXT_MATCH` |
| `The literal beta pairing and the returned shell coefficient` | 140 | 2 | `HEADING_TEXT_MATCH` |
| `Unit-mask and normalization firewalls` | 175 | 3 | `HEADING_TEXT_MATCH` |
| `Finite validation and adversarial controls` | 195 | 3 | `HEADING_TEXT_MATCH` |
| `Route status` | 231 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 276 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `89` before writing and `89` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `23`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `dbc10a3a2dda38355cf7b69adaca8147d46dbb70f43ff574b11f8612dfc63931`.
- Source theorem/proof environment starts: theorem at TeX line 94, proof at TeX line 116.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 47–50 | `6907ebdeddf3933db3d691da93b8f989ac0abbc5d2cbab0acd214c85d33ad54d` |
| D02 | equation | 51–55 | `d47130fdf59b5791922aba2434bf99499a077047aaa054027835eb6acc023402` |
| D03 | equation | 58–61 | `08a71882ae557176d2d301060a75badca755fb9705fd05d27622884fdf4ccdf4` |
| D04 | equation | 66–69 | `5a1e66867f68e335771a6f8ca3bd0434ed9324263d6ddc93b395a269f1a07979` |
| D05 | equation | 70–73 | `4f2baba01d7dea2cd5bf7800f08b4b1e9270e325df0d70e382113a6ed4159dc2` |
| D06 | equation | 81–84 | `ad0495d365937d3d0cdd95f2003e538853c25520f69c91f1a6f0effc2f19ce96` |
| D07 | align | 86–91 | `cad47e0f3b405ee4da2defc840e55e7b6446142c9d3279051ffc5d0619110b32` |
| D08 | align | 96–100 | `0ad43b7a8bc1e8cdf60da40183cab0e4528cca2c30b60c3c90fa810b4936fe0b` |
| D09 | equation | 103–106 | `6c633f106dd7400f6a131b75fc4635f896cf1bd502a8eb495a6d59ddd112a81d` |
| D10 | equation | 108–113 | `9ed4d1ee1d1d21c3b9263b61280d66aa3bf15b2bacfe42ca317429b2649f6341` |
| D11 | \[...\] | 119–122 | `35ac061b477b4eb091dd0f1f429de9a25a40027ae5406f0be343b081837fa2d4` |
| D12 | \[...\] | 133–135 | `d40f0362392efd712516655e2aa5bc369c57f16ab8ca8395311e6a0dbf56ef9c` |
| D13 | equation | 144–146 | `83898db4666ad23f2a7db2b817c5d0480a1bdbdb0ab6c5d8db56f88cdbff2ccd` |
| D14 | align | 149–155 | `ce1f90fe3804d1ac05fe0387e4696f1aa5ebffb7647f992162f1da5d35ae3f24` |
| D15 | equation | 157–160 | `22831f2d167e5377298cc29ce0f125427c8381ef249ffd8dae0666e36527f3b3` |
| D16 | equation | 162–164 | `b600e4eaaa674c35b844c90fa52c506cbc14e43dd178206ba5d51b5e594a4c9d` |
| D17 | equation | 166–170 | `8ef414244ae2c278d13139d1af7bf1027299e432f973960d9e822f945cdb99bc` |
| D18 | equation | 178–181 | `f8cc63c228153ab13c825eeab20074830b473404ac95f829eaa683d4a014d5b0` |
| D19 | equation | 183–186 | `93031c565fcda31ca9157d351222ca00bdcc783c9e395137460c719dc72f653c` |
| D20 | \[...\] | 206–208 | `91f3b2766fe6a3014c94ac1eb93043a082af48ec1503e143b71c4593475a7ce5` |
| D21 | \[...\] | 237–239 | `0a30cfc753778d41c787dd3aa1a85e80d5da7342a6cd840c8346e250c83b3e5e` |
| D22 | \[...\] | 240–243 | `b975ad020020afaf8a8590bde9484179ad85649f9de7453012763b136a9262c3` |
| D23 | \[...\] | 262–267 | `74890378df6ea4b71c69d83fd90ca28be531d2ff25741071b6f8193e9f69ea24` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 33: `$H>2Q$.  This does not annihilate the physical row: deleting its diagonal`
- TeX line 38: `result is an exact normal form for $\ip{\zm}{\Ax\beta}$, not an estimate.  In`
- TeX line 41: `families reproduce the finite algebra but are not asymptotic evidence.`
- TeX line 65: `Write $I_x=\{n_1<\cdots<n_N\}$, assume $N\geq2$, and put`
- TeX line 131: `assuming that $K_H$ is even or real.  When $q\leq2Q<H$, every nonzero dual`
- TeX line 173: `normal form, not an estimate.`
- TeX line 195: `\section{Finite validation and adversarial controls}`
- TeX line 197: `The executable certificate is deliberately finite and exact.  Its primary`
- TeX line 225: `is supported by the frozen Poisson theorem, not inferred from the finite`
- TeX line 251: `adjoint Haar form without an evenness or self-adjointness assumption.  What`
- TeX line 260: `\paragraph{Reusable compiler and open theorem.}`
- TeX line 268: `The open theorem is a signed estimate for \eqref{eq:scalar} after the`
- TeX line 273: `and the twin-prime problem open.`

## Conversion limitations

- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:full` → `main.tex#L99` (existing project target or original TeX label line).
- Link relocation: `#eq:j` → `main.tex#L90` (existing project target or original TeX label line).
- Link relocation: `#eq:jump` → `main.tex#L112` (existing project target or original TeX label line).
- Link relocation: `#eq:e` → `main.tex#L88` (existing project target or original TeX label line).
- Link relocation: `#eq:j` → `main.tex#L90` (existing project target or original TeX label line).
- Link relocation: `#thm:compiler` → `main.tex#L94` (existing project target or original TeX label line).
- Link relocation: `#eq:scalar` → `main.tex#L154` (existing project target or original TeX label line).
- Link relocation: `#eq:bq` → `main.tex#L169` (existing project target or original TeX label line).
- Link relocation: `#eq:operator` → `main.tex#L60` (existing project target or original TeX label line).
- Link relocation: `#eq:full` → `main.tex#L99` (existing project target or original TeX label line).
- Link relocation: `#thm:compiler` → `main.tex#L94` (existing project target or original TeX label line).
- Link relocation: `#eq:full` → `main.tex#L99` (existing project target or original TeX label line).
- Link relocation: `#eq:modes` → `main.tex#L185` (existing project target or original TeX label line).
- Link relocation: `#eq:scalar` → `main.tex#L154` (existing project target or original TeX label line).
- Link relocation: `#eq:bq` → `main.tex#L169` (existing project target or original TeX label line).
- Link relocation: `#eq:scalar` → `main.tex#L154` (existing project target or original TeX label line).
- Link relocation: `#eq:bq` → `main.tex#L169` (existing project target or original TeX label line).
