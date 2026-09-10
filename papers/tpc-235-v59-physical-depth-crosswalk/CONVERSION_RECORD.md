# TPC-235 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `3e30690df581ce6e78cb41b359cd5dba819475ddd7170f04d9c64655ee271b34`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `eadc72995512a0ac8133619abdf09a1e83d94d3534a4afd1f07ed1065ba21d9b`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `81b203d78fc26fd826b4a8bcaecdec1da6d334c8ef2234edece614a3471dee39`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `186b8aa4da639e077a7f83821addced6a5b4716f623ccdb03657045dc8fc0ecc`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC235_239.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 8 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `3e30690df581ce6e78cb41b359cd5dba819475ddd7170f04d9c64655ee271b34` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `4a96553e1e4261b6c6fbd027c0b362bebb4644291cae9091450c0e7d34e16bbb` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `5149b9aa33f9bbe9807487fc4d855bf5db27848f973c952fa4d86bc5496922f5` |
| [paper/sections/2_physical_crosswalk.tex](paper/sections/2_physical_crosswalk.tex) | `8375103c582c220a0429f5afc559e91d5fb62155afe0527675e3f9b54e97be7a` |
| [paper/sections/3_single_clock.tex](paper/sections/3_single_clock.tex) | `b1e0523609423613144a753798cf97b561253f296fef59b02e4de8e644f7e92a` |
| [paper/sections/4_polarization.tex](paper/sections/4_polarization.tex) | `7b97f7d2cbe0fc8fdbae78cfc7a6732b421d161010b007eec8f1e2f199a320f3` |
| [paper/sections/5_certificate.tex](paper/sections/5_certificate.tex) | `59539031ca39ea5168752d7b3680aab93b9d172bbf51130b87a2d24b5f07953f` |
| [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) | `47a75f15ebcef8baf34df2c8b16ce0b58c6111ea2c36a7dd36011bec7736ee8f` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L20](paper/main.tex#L20) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L21](paper/main.tex#L21) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L22](paper/main.tex#L22) | `\input{sections/2_physical_crosswalk}` | [paper/sections/2_physical_crosswalk.tex](paper/sections/2_physical_crosswalk.tex) |
| [paper/main.tex:L23](paper/main.tex#L23) | `\input{sections/3_single_clock}` | [paper/sections/3_single_clock.tex](paper/sections/3_single_clock.tex) |
| [paper/main.tex:L24](paper/main.tex#L24) | `\input{sections/4_polarization}` | [paper/sections/4_polarization.tex](paper/sections/4_polarization.tex) |
| [paper/main.tex:L25](paper/main.tex#L25) | `\input{sections/5_certificate}` | [paper/sections/5_certificate.tex](paper/sections/5_certificate.tex) |
| [paper/main.tex:L26](paper/main.tex#L26) | `\input{sections/6_conclusion}` | [paper/sections/6_conclusion.tex](paper/sections/6_conclusion.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `The exact physical-depth crosswalk` | [paper/sections/2_physical_crosswalk.tex:L1](paper/sections/2_physical_crosswalk.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `The single-clock compatibility obstruction` | [paper/sections/3_single_clock.tex:L1](paper/sections/3_single_clock.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Packet normalization and polarization` | [paper/sections/4_polarization.tex:L1](paper/sections/4_polarization.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Exact reproduction and the next compiler` | [paper/sections/5_certificate.tex:L1](paper/sections/5_certificate.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/6_conclusion.tex:L1](paper/sections/6_conclusion.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | [paper/main.tex:L28](paper/main.tex#L28) | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `76` before writing and `76` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `11`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b13c341fee342a8cc27c17caa913100192d09966b71ed09f13b93f2d49ee803e`.
- Source theorem/proof environment starts: theorem at [paper/sections/2_physical_crosswalk.tex:L23](paper/sections/2_physical_crosswalk.tex#L23), proof at [paper/sections/2_physical_crosswalk.tex:L38](paper/sections/2_physical_crosswalk.tex#L38), corollary at [paper/sections/2_physical_crosswalk.tex:L45](paper/sections/2_physical_crosswalk.tex#L45), proof at [paper/sections/2_physical_crosswalk.tex:L54](paper/sections/2_physical_crosswalk.tex#L54), theorem at [paper/sections/3_single_clock.tex:L7](paper/sections/3_single_clock.tex#L7), proof at [paper/sections/3_single_clock.tex:L15](paper/sections/3_single_clock.tex#L15), proposition at [paper/sections/4_polarization.tex:L11](paper/sections/4_polarization.tex#L11), proof at [paper/sections/4_polarization.tex:L18](paper/sections/4_polarization.tex#L18).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/2_physical_crosswalk.tex:L4](paper/sections/2_physical_crosswalk.tex#L4) – [paper/sections/2_physical_crosswalk.tex:L6](paper/sections/2_physical_crosswalk.tex#L6) | `453277f3460328cea3cf7b9fb211c315c1483682fa67b40e6b641a32bc30d21d` |
| D02 | equation | [paper/sections/2_physical_crosswalk.tex:L8](paper/sections/2_physical_crosswalk.tex#L8) – [paper/sections/2_physical_crosswalk.tex:L13](paper/sections/2_physical_crosswalk.tex#L13) | `417073e42d21d7ef5d059b08c660fdac3a8372e3c8a2ccccaedd1e5eea6bee36` |
| D03 | equation | [paper/sections/2_physical_crosswalk.tex:L15](paper/sections/2_physical_crosswalk.tex#L15) – [paper/sections/2_physical_crosswalk.tex:L19](paper/sections/2_physical_crosswalk.tex#L19) | `2cf8ad5112697ac52c7773bc4e137d146f8e4f93e548221ad5e1639c3a2c31a4` |
| D04 | \[...\] | [paper/sections/2_physical_crosswalk.tex:L25](paper/sections/2_physical_crosswalk.tex#L25) – [paper/sections/2_physical_crosswalk.tex:L27](paper/sections/2_physical_crosswalk.tex#L27) | `933646278e9d0bc0bb90b32039c8371c18c957a1a3553cbea756a1f51f8b4118` |
| D05 | equation | [paper/sections/2_physical_crosswalk.tex:L29](paper/sections/2_physical_crosswalk.tex#L29) – [paper/sections/2_physical_crosswalk.tex:L34](paper/sections/2_physical_crosswalk.tex#L34) | `5b6d0a9369098c024e436f12db32ffe32fcaa66acd6a2dccc8e31e6315daf85f` |
| D06 | \[...\] | [paper/sections/2_physical_crosswalk.tex:L47](paper/sections/2_physical_crosswalk.tex#L47) – [paper/sections/2_physical_crosswalk.tex:L49](paper/sections/2_physical_crosswalk.tex#L49) | `c680190f65851947ca7f1be96f46ba01a2074ba26ed2f023ef6383f0ae920c6c` |
| D07 | equation | [paper/sections/3_single_clock.tex:L10](paper/sections/3_single_clock.tex#L10) – [paper/sections/3_single_clock.tex:L12](paper/sections/3_single_clock.tex#L12) | `363cbbdb22c24a8a1da4e84ce7e3c4e040651199b68daf928c7c3b252330cebd` |
| D08 | equation | [paper/sections/3_single_clock.tex:L23](paper/sections/3_single_clock.tex#L23) – [paper/sections/3_single_clock.tex:L25](paper/sections/3_single_clock.tex#L25) | `3c1ec061b4650a4e386d35e67380b6c826607e0b449182b787c5e3c0b7f6ffa2` |
| D09 | equation | [paper/sections/4_polarization.tex:L5](paper/sections/4_polarization.tex#L5) – [paper/sections/4_polarization.tex:L8](paper/sections/4_polarization.tex#L8) | `2130a51b637370e244a27ea7bc8a67166f875f8fa8e7d3e4a479983b8150c43c` |
| D10 | \[...\] | [paper/sections/5_certificate.tex:L5](paper/sections/5_certificate.tex#L5) – [paper/sections/5_certificate.tex:L9](paper/sections/5_certificate.tex#L9) | `a1414adb94150d8e48b8de968c6be36e4a25db75047011fdcf82a57c0fa49631` |
| D11 | \[...\] | [paper/sections/5_certificate.tex:L22](paper/sections/5_certificate.tex#L22) – [paper/sections/5_certificate.tex:L24](paper/sections/5_certificate.tex#L24) | `e3e4e8ad2efd219ad2a6cdf5e9fc3a9129e93a92113440136f790a9fa986903b` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/0_abstract.tex:L16](paper/sections/0_abstract.tex#L16): `claims no arithmetic cancellation or Gate-B estimate.`
- [paper/sections/1_introduction.tex:L3](paper/sections/1_introduction.tex#L3): `Finite model clocks are useful only when their parameters can be traced back to the`
- [paper/sections/1_introduction.tex:L6](paper/sections/1_introduction.tex#L6): `theorems and a depth-uniform Bessel estimate after row normalization.  Those results`
- [paper/sections/1_introduction.tex:L7](paper/sections/1_introduction.tex#L7): `are internally correct, but two transfer questions remained open: whether one modeled`
- [paper/sections/2_physical_crosswalk.tex:L21](paper/sections/2_physical_crosswalk.tex#L21): `is not an innocent change of coordinates.`
- [paper/sections/2_physical_crosswalk.tex:L59](paper/sections/2_physical_crosswalk.tex#L59): `The final count is a geometric grid count only.  It does not assert that every`
- [paper/sections/3_single_clock.tex:L28](paper/sections/3_single_clock.tex#L28): `makes its multiplier depth too small by the same factor.  This is not a constant-loss`
- [paper/sections/3_single_clock.tex:L32](paper/sections/3_single_clock.tex#L32): `Theorem~\ref{thm:compatibility} does not invalidate the modeled clock as an abstract`
- [paper/sections/5_certificate.tex:L3](paper/sections/5_certificate.tex#L3): `The finite certificate evaluates a rational fixture with`
- [paper/sections/5_certificate.tex:L16](paper/sections/5_certificate.tex#L16): `profile scales, and packet rules.  Its exact finite-record digest is`
- [paper/sections/6_conclusion.tex:L10](paper/sections/6_conclusion.tex#L10): `transform, then analyze collisions at the true ratio $Q^2/H=x^{1/96}$.  No arithmetic`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:physical-row` → `sections/2_physical_crosswalk.tex#L12` (existing project target or original TeX label line).
- Link relocation: `#eq:compatibility` → `sections/3_single_clock.tex#L11` (existing project target or original TeX label line).
- Link relocation: `#eq:clock-gap` → `sections/3_single_clock.tex#L24` (existing project target or original TeX label line).
- Link relocation: `#thm:compatibility` → `sections/3_single_clock.tex#L7` (existing project target or original TeX label line).
- Link relocation: `#eq:polarization` → `sections/4_polarization.tex#L7` (existing project target or original TeX label line).
- Link relocation: `#eq:polarization` → `sections/4_polarization.tex#L7` (existing project target or original TeX label line).
- Link relocation: `#eq:full-source` → `sections/2_physical_crosswalk.tex#L18` (existing project target or original TeX label line).
