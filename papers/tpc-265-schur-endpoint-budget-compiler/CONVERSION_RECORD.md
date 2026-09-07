# TPC-265 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `524af4ad2c623e839511e915db5d85e6c41c7c9e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `6c4d7b94615f2a2727d20a13e70f373fa5095940c95874df68c5747e1255c0ed`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `e20b3f329f16c96f39789ab710b266cdc28f6e9214c680cf4905ead4506d55b1`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `87d9dff915d5fe5a4820bfa4c3701facadc82755ab145ba55e01a21d7d354176`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC265_269.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Scope and motivation` | 42 | 1 | `HEADING_TEXT_MATCH` |
| `Schur geometry as an endpoint set` | 77 | 2 | `HEADING_TEXT_MATCH` |
| `Sharp radial support` | 109 | 2 | `HEADING_TEXT_MATCH` |
| `The endpoint-budget compiler` | 151 | 3 | `HEADING_TEXT_MATCH` |
| `Logarithmic firewall and finite audit` | 192 | 3 | `HEADING_TEXT_MATCH` |
| `Claim firewall and route consequence` | 226 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 250 | 4 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 260 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `81` before writing and `81` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `14`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `377cf715df063035840ff0609f376e4fe8cdcf22adb8c477ca8c134fcfdce33f`.
- Source theorem/proof environment starts: remark at TeX line 102, theorem at TeX line 111, proof at TeX line 119, theorem at TeX line 128, proof at TeX line 140, theorem at TeX line 165, proof at TeX line 177.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 45–47 | `0cf45c86bc5a9c949a4ce70503ca762db2c4583aa1953864526e446c0c714da6` |
| D02 | \[...\] | 49–51 | `4e830d4919113aa79f3af2ae283042b343f1b732b77eab29a342964ed1bb5fac` |
| D03 | \[...\] | 53–55 | `17d375aee8ad3c62b2baab01ba1783eb2523ff43ac9c2c096128344e9dce7b96` |
| D04 | \[...\] | 80–82 | `d013381f0bfced336fd74a372082e2c013acd2949d6f59b49cff298fb287c42b` |
| D05 | equation | 85–88 | `88526e78cfcbf8ca241f6e1f456c4c5355e735d8bc980c58973817a4d99720f8` |
| D06 | \[...\] | 90–93 | `ba04fe1dbacb60e1b848383ad9943bf24c8c933a6c1c59d24e6cc703aa755288` |
| D07 | \[...\] | 96–98 | `b95b4e048d55d52376c0bf2ffeff765f2c10755cce74c7723fb694fe7a07cf0e` |
| D08 | align | 113–116 | `ac12618a3b7360e70e2382e81e6c4c60d732b723dc411b5c5e9810ceb5c59a52` |
| D09 | \[...\] | 130–132 | `483363e4bb29e7795621539d14f9dc900b3e39624210aaf4a69eff75da6eb7ff` |
| D10 | \[...\] | 133–137 | `477b8fbf43cd36d27fe3222230b3716b6e290bdf9be0247c94a101bb8ad08230` |
| D11 | \[...\] | 154–157 | `080f940b1e9376c885d8c195f142781ec1f7f85339bc192a0c5c68d8580923a8` |
| D12 | align | 159–163 | `5d1a6cf3fefe8a0a2b1364b8f4564d51c2c9b2241dd0c98d1bc76a590f3b6eff` |
| D13 | \[...\] | 167–171 | `f262022e0acd32f3adf674acf38e24ae2c0cda59366a2cfdceb383d3eccbcdcb` |
| D14 | \[...\] | 195–198 | `9ad344dc2aaf0832ea15116a02fbc2122f1e06d79bd9ef99a1d80b10c5a9e0af` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 31: `by the rank-three physical channel.  We now compile that finite geometry into`
- TeX line 38: `fixed-power credit.  This is an interface theorem and obstruction: it does not`
- TeX line 62: `The answer is not a new Cauchy estimate; it is an exact support calculation.`
- TeX line 75: `All conclusions about the literal V59 residual are explicitly left open.`
- TeX line 148: `uniform upper bound.  A phase theorem can change the feasible set, but it is`
- TeX line 149: `additional information rather than a consequence of positive semidefiniteness.`
- TeX line 192: `\section{Logarithmic firewall and finite audit}`
- TeX line 237: `Literal V59 radius and phase & \texttt{OPEN}\\`
- TeX line 238: `Arithmetic $L^2$ and full Gate B & \texttt{NONE / OPEN}\\`
- TeX line 245: `not a completed arithmetic bridge.  The next valid task is to estimate the`
- TeX line 258: `residual open.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:upper` → `main.tex#L114` (existing project target or original TeX label line).
- Link relocation: `#eq:lower` → `main.tex#L115` (existing project target or original TeX label line).
- Link relocation: `#eq:upper` → `main.tex#L114` (existing project target or original TeX label line).
- Link relocation: `#eq:strict` → `main.tex#L170` (existing project target or original TeX label line).
- Link relocation: `#eq:lanes` → `main.tex#L162` (existing project target or original TeX label line).
