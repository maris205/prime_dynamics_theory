# TPC-378 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `60ea54a85c5604c7f58c65c958129b152c0246d2fc6762387c74bc4f0c6cb884`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `99de4db9d0b1c94b2ff7341a4f1bc50b9cb54a30a42c35fbd22fde7b5e954217`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `13244357a6f8a3ce86dd59793b6ad9096fff65ce111ef701e047b74b7d00c40c`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 34 | 1 | `HEADING_TEXT_MATCH` |
| `Finite object and exact identities` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `Predeclared cross-holdout protocol` | 79 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 100 | 2 | `HEADING_TEXT_MATCH` |
| `Independent audit` | 146 | 2 | `HEADING_TEXT_MATCH` |
| `Limitations and route decision` | 163 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 181 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `48` before writing and `48` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `28911a4aacc2b6bb15023265b62207c93bb417c03ff5a20c4c3679e81520f0d0`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 52–57 | `6bf5d91f3017d3972b4a0a8c0bca402a1e8d3b7b9bed75d2e6f41519f7c4f54f` |
| D02 | \[...\] | 59–63 | `654d09d2538c9765c0bb7d4bb52f47394bd7882a674667c8ed78e7880b9be637` |
| D03 | \[...\] | 65–68 | `5a4518ae33090f60dd41c2e72c109e69a13a632a1dc116f9675bbd05b817da3a` |
| D04 | \[...\] | 73–76 | `ebb744238d0e8f0c2f0c9e90224f5e7faf60725acbcb1eb5c27a6ce85846a396` |
| D05 | \[...\] | 82–84 | `438808fdcefc65e94463e7f04cf3e6001d9c2916dc61e2cf38c1810e485860b8` |
| D06 | \[...\] | 126–129 | `fa93d78dc59e4b5c273eb0077d70625673d90bc81f6f5e5a645306f9225706c7` |
| D07 | \[...\] | 137–141 | `4e216386df7e573d8a742ddb1ce619a7ef48dde3e0bdfd9364351b162740e5a1` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 21: `TPC-377 found that a finite $c=1$ prime-shell band retained its high-$Q$`
- TeX line 29: `$0.98046528117382914$.  This is finite response-blind support-transfer`
- TeX line 30: `evidence only; it does not prove origin or scale uniformity, an asymptotic`
- TeX line 36: `The recent TPC line has isolated a recurring finite signature: after`
- TeX line 44: `All statements in this paper concern the declared finite panel.  In`
- TeX line 45: `particular, a coordinate-disjoint sample is not an origin-uniform theorem,`
- TeX line 46: `and a shared left endpoint between two finite counts is not a growing`
- TeX line 49: `\section{Finite object and exact identities}`
- TeX line 69: `The geometry is a finite sum of nonnegative rational squares.  The exact`
- TeX line 77: `These are exact finite identities, not uniform estimates.`
- TeX line 104: `independent random samples; they are the fixed finite protocol above.`
- TeX line 149: `JSON certificate.  A separate checker does not import the TPC-378 producer:`
- TeX line 161: `and not an official evaluator verdict.`
- TeX line 165: `The finite transfer does not prove origin uniformity, window-scale`
- TeX line 166: `uniformity, spectral-magnitude stability, cross-block causality, source`
- TeX line 168: `source-uniform arithmetic $L^2$ estimate.  It pays no fixed-power credit:`
- TeX line 170: `\texttt{FULL\_GATE\_B = OPEN}.  There is no Route-B reassembly and no`
- TeX line 178: `common band/tail Rayleigh audit.  The next finite question is`
- TeX line 183: `TPC-378 closes the finite origin/scale cross-holdout proposed by TPC-377:`
- TeX line 185: `It strengthens the empirical map of the finite model while leaving every`
- TeX line 186: `arithmetic and growing-operator gate open.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:profile` → `main.tex#L109` (existing project target or original TeX label line).
