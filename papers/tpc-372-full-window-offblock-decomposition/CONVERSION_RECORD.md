# TPC-372 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `180a850a6f08a77eeae10d841f8c867af78c9528ee5b61089c7f54199307340d`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `006b35a0a1170cbfc9e5601066518bb481519b116683a47fea33e1681d59838f`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `0c98d7cddb4014e3c9d8ada9262d067eaf57b1bc0f3d40bf930ca82c1c1b42f2`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Motivation and frozen panel` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Operator and decomposition` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `Finite certification` | 73 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 93 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and limits` | 128 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `25` before writing and `25` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `4d4c7d4cacc79a3f4edacd52944cfbbc3e13725e22cdea44141ee60bf5e4cee9`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 52–56 | `853a2e7d3405aa5cee102032a976038bde03584d57d2a551caaf159a93e4e042` |
| D02 | \[...\] | 58–63 | `3bf841f9c3f4cbcecef55e76a4f72c865110c0f2e2ba95a80cd2dab453bd3563` |
| D03 | \[...\] | 66–68 | `bb0da242614725cd7ba549d35c86ed61b672ed342a46e326e6a003ef2675c086` |
| D04 | \[...\] | 77–81 | `8ea3852c839f4ab86d0746b8fcc2468abf396b82fd13b97aec489d76459b9638` |
| D05 | \[...\] | 113–117 | `f9df2668c29e594cba49e253bfa9819a098f4882630015107ab6bba72aa03f05` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 10: `\title{A common-normalization block/off-block decomposition of a finite\newline`
- TeX line 22: `We decompose the finite full-window operator from a count-2048 prime-shell`
- TeX line 29: `a finite sum/coherence obstruction and removes the normalization ambiguity of`
- TeX line 30: `an independently normalized short-block audit.  It does not prove causal`
- TeX line 71: `checked separately and does not select a panel row.`
- TeX line 73: `\section{Finite certification}`
- TeX line 75: `The decomposition identity is an exact finite entrywise identity.  For finite`
- TeX line 82: `The geometry is a finite sum of rational squares, and the Schur and Frobenius`
- TeX line 83: `quantities are independent finite envelopes for the spectral norm.`
- TeX line 100: `\caption{Finite component census.}`
- TeX line 126: `does not alter the beta=2 interpretation.`
- TeX line 130: `The result proves a finite necessity statement: on the six beta=2 failure`
- TeX line 132: `is required to bridge the diagonal norm to the full norm.  It does not prove`
- TeX line 139: `TPC372_DECOMPOSITION_IDENTITY = NUMERICALLY_CERTIFIED_FINITE`
- TeX line 140: `TPC372_OFF_BLOCK_NECESSITY = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 141: `TPC372_CROSS_BLOCK_CAUSALITY = OPEN`
- TeX line 144: `TPC372_FULL_GATE_B = OPEN`
- TeX line 148: `No source-uniform arithmetic \(L^2\) estimate, growing operator bound,`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:components` → `main.tex#L101` (existing project target or original TeX label line).
