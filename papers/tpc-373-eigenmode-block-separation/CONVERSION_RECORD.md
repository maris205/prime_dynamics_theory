# TPC-373 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `ba3c27dccae5233debb11d84634d5b3b2f91a41e6df71dd1abeb4c74ee4ce5e4`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `ffbb1ffdab58f1e5fe0a2db425698874b5d6b9ada1549b3be12d9e23f486e659`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `08ed00506280701e4ec5f62bdb97e8805c8b02f8fbe1b087aa809e97cf6dfde1`.
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
| `Operator and exact layer identity` | 51 | 1 | `HEADING_TEXT_MATCH` |
| `Certification` | 83 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 99 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and limits` | 149 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `30` before writing and `30` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `4`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `8aa9b7e65fb9c4723a4b9946f2bf77359855416a1a3fd6bd1acb5eacad20d0f7`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 54–58 | `853a2e7d3405aa5cee102032a976038bde03584d57d2a551caaf159a93e4e042` |
| D02 | \[...\] | 60–65 | `c8292a9cd002dc3fa01fc20c93bc0e093cb48abe05c8315ef6725761b7558e61` |
| D03 | \[...\] | 70–72 | `a3c9281d36ab18f8fe8318581bb2d118eeb24993619473c0ca8bfa4c8d45cc74` |
| D04 | \[...\] | 76–78 | `7df852569769f9065aa5ac6db45dbd25955a574b1fd0e543f4fc4faf85511dc4` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 10: `\title{Extremal-eigenmode separation by block distance in a finite\newline`
- TeX line 22: `We resolve the extremal eigenmode of a finite count-2048 prime-shell operator`
- TeX line 30: `percent.  This is a finite near-block signed-coherence certificate, not a`
- TeX line 31: `causal attribution, a uniform decay theorem, or a twin-prime consequence.`
- TeX line 75: `\(c_d=v^{\mathsf T}L_dv\).  Linearity gives the exact finite identity`
- TeX line 80: `\(|c_d|/\sum_e|c_e|\).  The latter is descriptive and is not a norm`
- TeX line 92: `\([1010346,1010359)\), at \(Q=4\) and shell \(\{5,7\}\), does not select a`
- TeX line 99: `\section{Finite results}`
- TeX line 106: `\caption{Finite full-panel census.}`
- TeX line 144: `spread across all block separations.  It has a stable finite near-block`
- TeX line 153: `not created by cancellation among block-distance terms.  It does not show`
- TeX line 155: `one data-dependent eigenvector is not an operator-norm bound for a truncated`
- TeX line 156: `band, and the panel supplies no origin-, window-, or shell-uniform decay law.`
- TeX line 157: `The next finite test is therefore a predeclared near-block band truncation,`
- TeX line 158: `not an asymptotic promotion.`
- TeX line 161: `TPC373_RAYLEIGH_PROFILE = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 162: `TPC373_CROSS_BLOCK_DECAY = OPEN`
- TeX line 163: `TPC373_CROSS_BLOCK_CAUSALITY = OPEN`
- TeX line 166: `TPC373_FULL_GATE_B = OPEN`
- TeX line 170: `No source-uniform arithmetic \(L^2\) estimate, growing operator bound,`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:census` → `main.tex#L107` (existing project target or original TeX label line).
- Link relocation: `#tab:layers` → `main.tex#L129` (existing project target or original TeX label line).
