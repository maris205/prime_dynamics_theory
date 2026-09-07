# TPC-402 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `433061db39680b1040f6c8c91439f1318220673cb268b609b92331090c2cd00b`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `79b7a298a9cc6c718311be3eef43c7cd5578b9133c6364cd2fa3d9bf4056cdce`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `edc10c830bc4e4a9b3ff79e5bda3d2c176ef2a28ceb084c0ddf7d31f4765a917`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Setup and boundary` | 19 | 1 | `HEADING_TEXT_MATCH` |
| `Signed coefficient identity` | 27 | 1, 2 | `UNMAPPED_OR_AMBIGUOUS` |
| `Exact audit` | 44 | 2 | `HEADING_TEXT_MATCH` |
| `Anchor obstruction and route ledger` | 51 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 64 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `20` before writing and `20` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `4`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `170f9faf36c17b2fe36d381ab2c6e57a4b70490a3382db720faac2a7cc0f2aeb`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 22–24 | `0bbf2e1b3bf60ada0c595ae14dcd6806fb7a9974e805ae8f0c69166a2aa20be5` |
| D02 | \[...\] | 29–32 | `e77c23c5747ee07efd274cc97044ed72ecc116afbceba1dde035072850b0efdf` |
| D03 | \[...\] | 35–38 | `1ecf4549518ceaaa7049c3c3d123f9bd9b136f54026b90d6c1781fd53b655973` |
| D04 | \[...\] | 40–42 | `53d1618b84e046def6cc2ffe84f445b4066c14b5617eba6e446e010d9a990ce6` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 4: `\title{TPC-402: The Signed Diagonal-Deletion Coefficient in a Finite C1 Panel}`
- TeX line 9: `We continue the exact finite decomposition from TPC-401 and retain the endpoint`
- TeX line 16: `boundary counterexample.  No arithmetic sign identification or asymptotic`
- TeX line 26: `synthetic finite probes.  All claims here are finite.`
- TeX line 53: `The divisibility term is one, so the production identity does not apply.  The`
- TeX line 54: `finite result is therefore bounded by its hypotheses.`
- TeX line 57: `signed coefficient identity & \texttt{PROVED\_EXACT\_FINITE}\\`
- TeX line 58: `finite audit & \texttt{NUMERICAL\_OBSERVATION}\\`
- TeX line 59: `source sign identification & \texttt{OPEN}\\`
- TeX line 61: `Route-B / twin-prime result & \texttt{OPEN} / \texttt{NONE}\\`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
