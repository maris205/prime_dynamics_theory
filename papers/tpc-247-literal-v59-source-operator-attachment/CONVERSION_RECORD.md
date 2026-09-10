# TPC-247 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `08686c00ceded09d8d88779c28cc1c7c28946445f86ef5b0aebfe33baf8b93eb`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `c22353a450d4dabed33fd8f3ba962e2f14eb402103b8baf3a429e90c1d357267`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `f91abc64e8b6f4f4f9a478e2f78deccbf473c9dd2d587e7b4535f326d4fce959`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `5095f3c1597b9b673e4c14e6817fd2a7bdf2f300c16af3982f96a910744c0c39`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC245_249.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The source-attachment problem` | 40 | 1 | `HEADING_TEXT_MATCH` |
| `Literal source operator` | 68 | 2 | `HEADING_TEXT_MATCH` |
| `Exactly-once hard blocks` | 100 | 2 | `HEADING_TEXT_MATCH` |
| `Tagged covariance and its exact toll` | 136 | 3 | `HEADING_TEXT_MATCH` |
| `Certificate, route boundary, and conclusion` | 177 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 201 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `68` before writing and `68` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `df24cf9b483b10909ab13ee0c27c252bbaff37c1f33a70099128388d4c2cb2c0`.
- Source theorem/proof environment starts: proposition at TeX line 81, proof at TeX line 89, theorem at TeX line 108, proof at TeX line 118, theorem at TeX line 146, proof at TeX line 157.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 43–47 | `5aac5e380bddb44dbfacf8ef4b0bc2a77d44b10be31b287bcb01f5a922d6c33f` |
| D02 | equation | 71–75 | `2614f747789c262ff18596e1a38bcc7006fef1b0eec4adb43e655de0dd4c331c` |
| D03 | \[...\] | 83–85 | `9d94a4c1e6f670531bf65a47cd8e4f0105294b4e5ffd4d2a143d4d85b9415742` |
| D04 | \[...\] | 104–106 | `65f31e65a86a92c32409323bfeba6cbd18bfe6aad50f5b7da838e80c0ade2d0b` |
| D05 | equation | 110–113 | `39769b9aea120e293dd89977dddbf5bda41ff9c563e08840387da511f648cdbc` |
| D06 | \[...\] | 121–124 | `f9b55cc021ea137f2be3129af34a66405028916ba23f162e2627a74adddd1a2f` |
| D07 | \[...\] | 140–144 | `e7673ef86977a597218ecc33a005b393e15f5ef49220e342bdff6a4a8a79b915` |
| D08 | align | 148–152 | `f66fc847787e9d167f9686369de4e784c0dc0d52bf3d7c65cb1bfd3a87a3eacf` |
| D09 | \[...\] | 164–167 | `dbc80b1d8a877174f54dc2f735477dafcf84df32a5b5afaf64f0f55d545825e1` |
| D10 | \[...\] | 189–192 | `fe721036a6c35c22eb94af5bcde64d6a7899e164c564568f1685301a3b64df34` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 24: `attachment.  We construct such an attachment directly on the finite physical`
- TeX line 33: `physical-index attachment is exact but does not supply the norm-payable`
- TeX line 36: `the two norm failures.  No arithmetic $L^2$ estimate or twin-prime conclusion`
- TeX line 42: `The frozen V59 record reduces the open analytic gate to the scalar`
- TeX line 53: `sharp aggregate disk geometry, but explicitly assumes the relevant joint`
- TeX line 70: `Let $\mathcal H_x=\C^{I_x}$.  Define the finite matrix`
- TeX line 79: `does not alter the outer $q$, diagonal deletion, or kernel orientation.`
- TeX line 102: `Fix a finite disjoint partition $I_x=\bigsqcup_{b\in\mathcal B}I_b$ and let`
- TeX line 196: `open.  The next minimal problem is no longer whether a physical two-lane`

## Conversion limitations

- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:v59` → `main.tex#L46` (existing project target or original TeX label line).
- Link relocation: `#eq:v59` → `main.tex#L46` (existing project target or original TeX label line).
- Link relocation: `#eq:A` → `main.tex#L74` (existing project target or original TeX label line).
- Link relocation: `#eq:v59` → `main.tex#L46` (existing project target or original TeX label line).
- Link relocation: `#eq:v59` → `main.tex#L46` (existing project target or original TeX label line).
- Link relocation: `#eq:v59` → `main.tex#L46` (existing project target or original TeX label line).
- Link relocation: `#eq:block` → `main.tex#L112` (existing project target or original TeX label line).
- Link relocation: `#eq:bnorm` → `main.tex#L151` (existing project target or original TeX label line).
- Link relocation: `#eq:cov` → `main.tex#L149` (existing project target or original TeX label line).
- Link relocation: `#thm:block` → `main.tex#L108` (existing project target or original TeX label line).
- Link relocation: `#eq:wnorm` → `main.tex#L150` (existing project target or original TeX label line).
- Link relocation: `#eq:bnorm` → `main.tex#L151` (existing project target or original TeX label line).
