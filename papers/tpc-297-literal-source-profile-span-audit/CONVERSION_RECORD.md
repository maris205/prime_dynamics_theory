# TPC-297 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `aa6a797b49ed462881998abf696440d164a0f74c`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `9744a8e238c695adb82b583a68e86821161940c6d933f56832ef9ac2b4ca35e4`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `b9c95d6d96325709fc8a93b524e9892a2c886bf52c882f2e5cbbe241150602c4`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `2d0464d77a0ecea6b178b635d01190de4950b220426749f13e1205cb39964950`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `3bf1674c87cee21e13b88d98540c061d672dc780620d2232cf8e0db947333f87`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC295_299.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Position on the route` | 45 | 1 | `HEADING_TEXT_MATCH` |
| `Literal source family and physical map` | 61 | 1 | `HEADING_TEXT_MATCH` |
| `Exact restricted projection theorem` | 97 | 2 | `HEADING_TEXT_MATCH` |
| `Finite audit` | 142 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and obstruction` | 207 | 3 | `HEADING_TEXT_MATCH` |
| `Claim boundary and conclusion` | 224 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 243 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 258 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `66` before writing and `66` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `db1d1d6cba392dda603d04e26f8ea4723a0456e619a09229acb9611ac9a7cae4`.
- Source theorem/proof environment starts: remark at TeX line 91, theorem at TeX line 99, proof at TeX line 111, proposition at TeX line 123, proof at TeX line 130.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 64–68 | `a3e0919870fbab6604c0165a3317cdeb9bc576e0e9f4ec3ad6a40d9c0ac83fd3` |
| D02 | \[...\] | 70–72 | `ca6e407013e5e8dd026eac3bb69375ec904c5af4f2836baa13e304f0ac5f3ae0` |
| D03 | \[...\] | 75–81 | `969c28da3970181f2f28e2b9263cce1b40c231f934b4142826f8d27f6540329e` |
| D04 | \[...\] | 83–86 | `84d2b62ad7529bf29619116c578e484525efb74eb384f85aa69d5b77ff07d9c4` |
| D05 | \[...\] | 102–106 | `e3d3f2b7f792d78fb7d729141ccb594f1206cb8a6f46854aa9e354110785efd4` |
| D06 | \[...\] | 116–118 | `8b34f9460b228ee1851b608679cf4a2169c87f344338feb514f3549720ece56f` |
| D07 | \[...\] | 136–138 | `246762ecb3546635cb73012a6af3f7635298f6f93d1d09ee5257dd98f9367c9d` |
| D08 | \[...\] | 234–239 | `e5368f81c80feaa3d9bb05fff702f504cfd7c8f784d633a9ade417e04783f0da` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 17: `for Finite Twin-Prime Shells}`
- TeX line 28: `TPC-296 showed that unrestricted finite source witnesses can be cheap while`
- TeX line 40: `on all 17 larger shells.  This is a finite profile-dimension obstruction,`
- TeX line 41: `not an asymptotic theorem: arithmetic $L^2$, fixed-power credit, Gate B, and`
- TeX line 42: `the twin-prime endpoint remain open.`
- TeX line 47: `The finite prime-shell line has now separated three questions.  TPC-294`
- TeX line 48: `found the physical weighted sign optimum, TPC-295 showed that every finite`
- TeX line 56: `ray and captures a positive control target, but it does not capture the`
- TeX line 59: `profile, without pretending that the finite family exhausts it.`
- TeX line 92: `The notation ''literal'' describes the finite formula and its source-side`
- TeX line 93: `origin.  It does not assert that the four cutoffs are the complete admissible`
- TeX line 112: `The vector $P_Vb$ is the unique closest point to $b$ in the finite`
- TeX line 139: `The theorem is exact over the reals; the finite certificate uses rational`
- TeX line 142: `\section{Finite audit}`
- TeX line 150: `The independent replay uses source-first accumulation and does not import`
- TeX line 156: `\caption{TPC-297 finite profile-span headline.}`
- TeX line 209: `This finite experiment changes the geometry of the route in a useful way.`
- TeX line 218: `source profile.  A finite rank-four result also does not say that the native`
- TeX line 227: `counts are numerically certified finite observations under a declared`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:projection` → `main.tex#L105` (existing project target or original TeX label line).
- Link relocation: `#tab:representative` → `main.tex#L183` (existing project target or original TeX label line).
