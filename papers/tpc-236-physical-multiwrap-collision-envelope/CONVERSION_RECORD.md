# TPC-236 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `a6d8106faf74f4f8126a97d8cbf9d1d7fd2988824bc275e967863c2881b727a8`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `eadc72995512a0ac8133619abdf09a1e83d94d3534a4afd1f07ed1065ba21d9b`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `f15343c55f1d9b5d1223cace822bfdb54ea2dee3e9ef76c3ef4df0aa51d85d6e`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `5d808f22cd9ff8cfd4821bb5162defeedc54e628f65a92dc83cfdec5dfa7fd36`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC235_239.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.
## Static TeX dependency provenance

All 9 manuscript-source files below match the declared source commit. Input order is preserved; no source file is rewritten or TeX executed.

| Original source | SHA-256 |
|---|---|
| [paper/main.tex](paper/main.tex) | `a6d8106faf74f4f8126a97d8cbf9d1d7fd2988824bc275e967863c2881b727a8` |
| [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) | `25f00b075fb61121ac3491d821b0cc34dac53586919fb0880d53f0ab232b3601` |
| [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) | `bc5a8c774c74cf0609f3063fbbffe2283e7f637e461d3f7da590d1669448f26b` |
| [paper/sections/2_gcd_fiber.tex](paper/sections/2_gcd_fiber.tex) | `7f575dcf78d0e19ff861a31cefe278fb0ada4c213b3d29cfdaec910a130c26a4` |
| [paper/sections/3_bessel.tex](paper/sections/3_bessel.tex) | `a5abc20d91a7c065f60ac7786ec617fb78e17f416bba94da8795f3a4c06ebe9b` |
| [paper/sections/4_triple_collision.tex](paper/sections/4_triple_collision.tex) | `ff3a0d098b50a2c7829051ab17693050d0bc00245f818b2bb4ad26048048539f` |
| [paper/sections/5_v59_ledger.tex](paper/sections/5_v59_ledger.tex) | `1e3b0d177c625fcf2f316cde7aa14fa68d1ce3e5a19acfd60152b058c5e68868` |
| [paper/sections/6_certificate.tex](paper/sections/6_certificate.tex) | `5dcbf1df3c9ae12e4c842d322a476252ea5512b37e1b814bb127467494573a25` |
| [paper/sections/7_conclusion.tex](paper/sections/7_conclusion.tex) | `899cb61107bdd8909f1a840357d7f99dbec90f58cd3a192c50486a4f2a0da154` |

| Parent input location | Preserved input command | Included source |
|---|---|---|
| [paper/main.tex:L20](paper/main.tex#L20) | `\input{sections/0_abstract}` | [paper/sections/0_abstract.tex](paper/sections/0_abstract.tex) |
| [paper/main.tex:L21](paper/main.tex#L21) | `\input{sections/1_introduction}` | [paper/sections/1_introduction.tex](paper/sections/1_introduction.tex) |
| [paper/main.tex:L22](paper/main.tex#L22) | `\input{sections/2_gcd_fiber}` | [paper/sections/2_gcd_fiber.tex](paper/sections/2_gcd_fiber.tex) |
| [paper/main.tex:L23](paper/main.tex#L23) | `\input{sections/3_bessel}` | [paper/sections/3_bessel.tex](paper/sections/3_bessel.tex) |
| [paper/main.tex:L24](paper/main.tex#L24) | `\input{sections/4_triple_collision}` | [paper/sections/4_triple_collision.tex](paper/sections/4_triple_collision.tex) |
| [paper/main.tex:L25](paper/main.tex#L25) | `\input{sections/5_v59_ledger}` | [paper/sections/5_v59_ledger.tex](paper/sections/5_v59_ledger.tex) |
| [paper/main.tex:L26](paper/main.tex#L26) | `\input{sections/6_certificate}` | [paper/sections/6_certificate.tex](paper/sections/6_certificate.tex) |
| [paper/main.tex:L27](paper/main.tex#L27) | `\input{sections/7_conclusion}` | [paper/sections/7_conclusion.tex](paper/sections/7_conclusion.tex) |


## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | [paper/sections/1_introduction.tex:L1](paper/sections/1_introduction.tex#L1) | 1 | `HEADING_TEXT_MATCH` |
| `The gcd-fiber collision theorem` | [paper/sections/2_gcd_fiber.tex:L1](paper/sections/2_gcd_fiber.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `An unnormalized weighted Bessel compiler` | [paper/sections/3_bessel.tex:L1](paper/sections/3_bessel.tex#L1) | 2 | `HEADING_TEXT_MATCH` |
| `Exact adversarial fixtures` | [paper/sections/4_triple_collision.tex:L1](paper/sections/4_triple_collision.tex#L1) | 3 | `HEADING_TEXT_MATCH` |
| `The V59 exponent ledger and remaining bridge` | [paper/sections/5_v59_ledger.tex:L1](paper/sections/5_v59_ledger.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Finite reproduction` | [paper/sections/6_certificate.tex:L1](paper/sections/6_certificate.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | [paper/sections/7_conclusion.tex:L1](paper/sections/7_conclusion.tex#L1) | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | [paper/main.tex:L29](paper/main.tex#L29) | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. Every source locator names the hashed original file and its original line; no expanded line is presented as a main.tex line. Raw display hashes cover the expanded block, which can span multiple linked source files.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `116` before writing and `116` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `16`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `526678b563d9472a6fd7eafa3fc68e56c27681778c2aeedcc7a6a5c6ae5f7fb8`.
- Source theorem/proof environment starts: lemma at [paper/sections/2_gcd_fiber.tex:L7](paper/sections/2_gcd_fiber.tex#L7), proof at [paper/sections/2_gcd_fiber.tex:L13](paper/sections/2_gcd_fiber.tex#L13), theorem at [paper/sections/2_gcd_fiber.tex:L27](paper/sections/2_gcd_fiber.tex#L27), proof at [paper/sections/2_gcd_fiber.tex:L39](paper/sections/2_gcd_fiber.tex#L39), corollary at [paper/sections/3_bessel.tex:L8](paper/sections/3_bessel.tex#L8), proof at [paper/sections/3_bessel.tex:L19](paper/sections/3_bessel.tex#L19).

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | [paper/sections/0_abstract.tex:L6](paper/sections/0_abstract.tex#L6) – [paper/sections/0_abstract.tex:L10](paper/sections/0_abstract.tex#L10) | `a60054e849bed30f904ee37bc452a0f88ae1321753e7fecfec993946ec350ae2` |
| D02 | equation | [paper/sections/1_introduction.tex:L4](paper/sections/1_introduction.tex#L4) – [paper/sections/1_introduction.tex:L9](paper/sections/1_introduction.tex#L9) | `c4fe412957220b570ea0738786bd59f22775eb2e20162db8fd002f357f289453` |
| D03 | \[...\] | [paper/sections/1_introduction.tex:L11](paper/sections/1_introduction.tex#L11) – [paper/sections/1_introduction.tex:L14](paper/sections/1_introduction.tex#L14) | `f4f14f15105aed9fdfe5c99db67edad1961435ae7676757570803a248d3b4883` |
| D04 | \[...\] | [paper/sections/2_gcd_fiber.tex:L15](paper/sections/2_gcd_fiber.tex#L15) – [paper/sections/2_gcd_fiber.tex:L17](paper/sections/2_gcd_fiber.tex#L17) | `099c801dec7f772a75292af0439da58a970cbeaa938a504d09030bc275bb85b4` |
| D05 | \[...\] | [paper/sections/2_gcd_fiber.tex:L22](paper/sections/2_gcd_fiber.tex#L22) – [paper/sections/2_gcd_fiber.tex:L24](paper/sections/2_gcd_fiber.tex#L24) | `c1b029f4a05a1dcd9ab2dc04bb76db9319d78ed12010ca2fb848942a2d639b1d` |
| D06 | equation | [paper/sections/2_gcd_fiber.tex:L30](paper/sections/2_gcd_fiber.tex#L30) – [paper/sections/2_gcd_fiber.tex:L36](paper/sections/2_gcd_fiber.tex#L36) | `9906c9f85982551f709ab345a06644bba07d56b44fc726d805561c5e2c8827df` |
| D07 | equation | [paper/sections/3_bessel.tex:L10](paper/sections/3_bessel.tex#L10) – [paper/sections/3_bessel.tex:L16](paper/sections/3_bessel.tex#L16) | `46955da4654d75407c391c4117db2977b93d3e4bdd4b55d2af91d160b87a9176` |
| D08 | equation | [paper/sections/3_bessel.tex:L28](paper/sections/3_bessel.tex#L28) – [paper/sections/3_bessel.tex:L32](paper/sections/3_bessel.tex#L32) | `c8314f15a7350d520506be9bfd331c39b9bf684b0e1752d72e9c8b7bf318446c` |
| D09 | \[...\] | [paper/sections/4_triple_collision.tex:L4](paper/sections/4_triple_collision.tex#L4) – [paper/sections/4_triple_collision.tex:L6](paper/sections/4_triple_collision.tex#L6) | `b3f74e16c12a884d06f56cc042331fcf6366b869618ac04ade5151be6935c16a` |
| D10 | \[...\] | [paper/sections/4_triple_collision.tex:L8](paper/sections/4_triple_collision.tex#L8) – [paper/sections/4_triple_collision.tex:L11](paper/sections/4_triple_collision.tex#L11) | `da939094931358aaa97ee356d606762b3f69686bd016453747ce8af13eff8f86` |
| D11 | \[...\] | [paper/sections/4_triple_collision.tex:L17](paper/sections/4_triple_collision.tex#L17) – [paper/sections/4_triple_collision.tex:L19](paper/sections/4_triple_collision.tex#L19) | `a74a536240c98a16dda22679ea96b9b5d1a7c6687b45342ae64fddf14a11ff6c` |
| D12 | equation | [paper/sections/4_triple_collision.tex:L26](paper/sections/4_triple_collision.tex#L26) – [paper/sections/4_triple_collision.tex:L29](paper/sections/4_triple_collision.tex#L29) | `c7b1544e1c4c78149e83d6d43335bd3f9804ada9fb3bf59cd2fa3358e9ca0fe0` |
| D13 | \[...\] | [paper/sections/5_v59_ledger.tex:L4](paper/sections/5_v59_ledger.tex#L4) – [paper/sections/5_v59_ledger.tex:L6](paper/sections/5_v59_ledger.tex#L6) | `453277f3460328cea3cf7b9fb211c315c1483682fa67b40e6b641a32bc30d21d` |
| D14 | align | [paper/sections/5_v59_ledger.tex:L8](paper/sections/5_v59_ledger.tex#L8) – [paper/sections/5_v59_ledger.tex:L11](paper/sections/5_v59_ledger.tex#L11) | `cce702fc79d46a825d7ddfe40ab7cc49e9e7907186c1781d3b67d989b6a84263` |
| D15 | equation | [paper/sections/5_v59_ledger.tex:L13](paper/sections/5_v59_ledger.tex#L13) – [paper/sections/5_v59_ledger.tex:L16](paper/sections/5_v59_ledger.tex#L16) | `333028a3c2999f26fd798628b978ce60268487224286063bf0c3c495c2298871` |
| D16 | \[...\] | [paper/sections/6_certificate.tex:L4](paper/sections/6_certificate.tex#L4) – [paper/sections/6_certificate.tex:L6](paper/sections/6_certificate.tex#L6) | `1a83ef27b31923839aa53f820cf4b99e6ebd44ffd15e7064f53337e9a870d025` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- [paper/sections/0_abstract.tex:L13](paper/sections/0_abstract.tex#L13): `bound.  At the V59 scales the sharper uniform loss is`
- [paper/sections/0_abstract.tex:L18](paper/sections/0_abstract.tex#L18): `cross-denominator rational-frequency reassembly and divisor-weight cancellation open.`
- [paper/sections/1_introduction.tex:L33](paper/sections/1_introduction.tex#L33): `denominators are not declared orthogonal on the physical finite window, and no`
- [paper/sections/2_gcd_fiber.tex:L46](paper/sections/2_gcd_fiber.tex#L46): `$h$, so the result is immediate.  Assume henceforth that $a\ne0$.`
- [paper/sections/2_gcd_fiber.tex:L56](paper/sections/2_gcd_fiber.tex#L56): `The reduced modulus $h/g$ is essential.  A finite counterexample to counting modulo`
- [paper/sections/3_bessel.tex:L6](paper/sections/3_bessel.tex#L6): `equality of amplitudes or row norms is assumed.`
- [paper/sections/3_bessel.tex:L23](paper/sections/3_bessel.tex#L23): `uniform bounds.`
- [paper/sections/4_triple_collision.tex:L13](paper/sections/4_triple_collision.tex#L13): `this is a literal finite floor model of the V59 exponent relations.`
- [paper/sections/4_triple_collision.tex:L23](paper/sections/4_triple_collision.tex#L23): `For uniform amplitudes let the three rows be $v_{113},v_{127},v_{193}$.  Each has`
- [paper/sections/4_triple_collision.tex:L31](paper/sections/4_triple_collision.tex#L31): `Bessel constant two in this class.  It is a finite structural obstruction, not an`
- [paper/sections/5_v59_ledger.tex:L12](paper/sections/5_v59_ledger.tex#L12): `Because $23/2400<1/96=25/2400$, the source-uniform factor is`
- [paper/sections/5_v59_ledger.tex:L21](paper/sections/5_v59_ledger.tex#L21): `ledger observation does not prove that every future reassembly must factor in that`
- [paper/sections/5_v59_ledger.tex:L25](paper/sections/5_v59_ledger.tex#L25): `More importantly, \eqref{eq:weighted-direct-sum} is not yet the physical finite-window`
- [paper/sections/5_v59_ledger.tex:L28](paper/sections/5_v59_ledger.tex#L28): `physical-fiber envelope with reduced-frequency regrouping and a finite-window large`
- [paper/sections/6_certificate.tex:L1](paper/sections/6_certificate.tex#L1): `\section{Finite reproduction}`
- [paper/sections/6_certificate.tex:L9](paper/sections/6_certificate.tex#L9): `gcd-fiber count and the uniform $8Q^2/H$ envelope.  The compilers independently rebuild`
- [paper/sections/6_certificate.tex:L14](paper/sections/6_certificate.tex#L14): `margin.  The exact finite-record digest is`
- [paper/sections/6_certificate.tex:L19](paper/sections/6_certificate.tex#L19): `These computations certify formulas and finite fixtures.  They are not numerical`
- [paper/sections/7_conclusion.tex:L9](paper/sections/7_conclusion.tex#L9): `The exact Q101 triple collision proves that multiplicity two does not survive the`
- [paper/sections/7_conclusion.tex:L12](paper/sections/7_conclusion.tex#L12): `discarding, the signed divisor coefficients.  No arithmetic cancellation, $L^2$`

## Conversion limitations

- Standalone literal TeX inputs were expanded in memory from the manuscript directory; all dependencies were checked against the source commit. Original-file/line links and an ordered dependency ledger are retained. This is not a TeX execution or a general conditional/dynamic-include interpreter.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:physical-row` → `sections/1_introduction.tex#L8` (existing project target or original TeX label line).
- Link relocation: `#lem:injectivity` → `sections/2_gcd_fiber.tex#L7` (existing project target or original TeX label line).
- Link relocation: `#sec:fixtures` → `sections/4_triple_collision.tex#L1` (existing project target or original TeX label line).
- Link relocation: `#eq:physical-row` → `sections/1_introduction.tex#L8` (existing project target or original TeX label line).
- Link relocation: `#eq:bessel` → `sections/3_bessel.tex#L15` (existing project target or original TeX label line).
- Link relocation: `#thm:gcd-envelope` → `sections/2_gcd_fiber.tex#L27` (existing project target or original TeX label line).
- Link relocation: `#eq:ratio-three` → `sections/4_triple_collision.tex#L28` (existing project target or original TeX label line).
- Link relocation: `#cor:bessel` → `sections/3_bessel.tex#L8` (existing project target or original TeX label line).
- Link relocation: `#eq:main-toll` → `sections/5_v59_ledger.tex#L9` (existing project target or original TeX label line).
- Link relocation: `#eq:weighted-direct-sum` → `sections/3_bessel.tex#L31` (existing project target or original TeX label line).
- Link relocation: `#eq:v59-toll` → `sections/5_v59_ledger.tex#L15` (existing project target or original TeX label line).
