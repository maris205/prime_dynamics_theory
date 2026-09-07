# TPC-374 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `88884da96fa89613f1d95d36589334ae4078dfac3453d2706e6d8f4e04e8656d`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `ce793883e6bae6f2f71dadb632f8cfb7b7bae85dc2eda6ae73787dcd91388cc3`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `e8a8b48ce657e8cace7fae6b908447a39a05aebb4a4e31c7d525a611bcd88059`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and frozen panel` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Operator and exact truncation identity` | 50 | 1 | `HEADING_TEXT_MATCH` |
| `Certification protocol` | 85 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 103 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and claim boundary` | 157 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `24` before writing and `24` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `1828c999a0dd7e66623908864b112ea653dec3a8fa141f3a1a08243930b0beab`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 53–57 | `f5db465b2dc6d087179609c0df2bf1c818213f06479a9448037c34e308600406` |
| D02 | \[...\] | 59–63 | `878d1ddaa175f9955ab8c9397f8427133ad8d82fdc26ba05578678d163508fb6` |
| D03 | \[...\] | 68–71 | `650dd2e62696ea558fec4ab5e2498ee34bf6e295f464191f74a49188c78e285a` |
| D04 | \[...\] | 73–75 | `576686aefce9ff2f878f6eabe377f72e2638b3060ae792c6f169475940061ff5` |
| D05 | \[...\] | 79–82 | `7ce5d5de8fb13b4c2047d517bc36702313a72b0a5b0f4d2859cfe4f096d60faf` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 8: `\title{A finite near-block band reproduces the spectral\newline`
- TeX line 29: `absolute Rayleigh fraction.  The result is a finite, independently replayed`
- TeX line 30: `near-block reduction; it is not a causality theorem, a bandwidth-uniform`
- TeX line 76: `entrywise on every finite row.  Both matrices are symmetric.  If \(v\) is`
- TeX line 83: `Equation (2) is an exact finite identity, not an attribution statement.`
- TeX line 97: `positive geometry and does not select a main-panel row.  Local Bridge-B`
- TeX line 111: `\caption{Finite cap census on the complete 18-row panel.}`
- TeX line 131: `so truncation is not a monotone norm-repair operation.`
- TeX line 153: `approximation theorem.  The finite eigensystem residual and norm checks are`
- TeX line 159: `The main positive result is an operator-level finite reproduction: a band`
- TeX line 162: `locates the finite excess in a near-block subspace at this partition scale.`
- TeX line 163: `It does not show that the near-block entries cause the excess.  In`
- TeX line 165: `operator-norm estimate for \(B_3\), and the small tail on this panel does not`
- TeX line 168: `The next finite question is bandwidth stability: test smaller predeclared`
- TeX line 173: `TPC374_BAND_REPLAY = NUMERICALLY_CERTIFIED_FINITE_18_ROWS`
- TeX line 174: `TPC374_BAND_FAILURE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 175: `TPC374_PARENT_FAILURE_REPRODUCTION = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 176: `TPC374_BAND_OPERATOR_UNIFORMITY = OPEN`
- TeX line 177: `TPC374_CROSS_BLOCK_CAUSALITY = OPEN`
- TeX line 180: `TPC374_FULL_GATE_B = OPEN`
- TeX line 184: `No source-uniform arithmetic $L^2$ estimate, growing operator bound,`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:census` → `main.tex#L112` (existing project target or original TeX label line).
