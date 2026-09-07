# TPC-404 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `17e93382e57dd23b9fe81092d7e3c25101f54ec6cb7d678453a5d77f51cc1079`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `53270221556d460152d98e4befe03a4633ba559f86150b3552783bb48e89fb83`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `33006c166710cf515bb5f9cdd5bc1f773fe0dcbbfea2da6d3ae07240670cc6e1`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and finite model` | 25 | 1 | `HEADING_TEXT_MATCH` |
| `Exact local identities` | 48 | 1 | `HEADING_TEXT_MATCH` |
| `Certificate and observations` | 70 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and route boundary` | 95 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 124 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `34` before writing and `34` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `f6927b0c05fdd9b3c23f59ff4e8f532976de9eebdd8500a65d22fb63be6e2917`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 31–35 | `7f5b49de945d2398052000de68b4c1f4be985d50e34757aadb6b215085079cd4` |
| D02 | \[...\] | 37–40 | `58a1d42dcae227c87c654f7518fbd5fd89e6f95752700340652a2fba1f739b23` |
| D03 | \[...\] | 42–45 | `ea50ba1c53fd9815d602a63fc0a1a8a57c75bb8a9333570dd5c9804144f144d8` |
| D04 | \[...\] | 51–53 | `6a1c5b756a5e090b0e42aed15c292ec11176a82fcc07e44c636f4bd429852f62` |
| D05 | \[...\] | 57–59 | `e7f69d44e8b09ecadea2ea056b63454866a0b7d64649972e11ddb306af8ed8aa` |
| D06 | \[...\] | 61–63 | `3bb6bd4f510ee3ac81fdbf78d3f80f9095bd11bef675951ba21fb9b46496b192` |
| D07 | \[...\] | 65–68 | `86d9c0ee3f9ed75eca89fcdec2a3b62e09bf0411cc03c7b83a53a2cace076785` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 11: `TPC-403 produced a large raw adjacent coefficient in a finite CRT-origin`
- TeX line 14: `normalization.  For the same alternating synthetic profile we prove exact`
- TeX line 15: `finite formulas for the two local diagonal energies and the adjacent`
- TeX line 21: `this finite audit.  No normalized growing theorem, arithmetic sign law,`
- TeX line 25: `\section{Question and finite model}`
- TeX line 46: `All statements in this paper concern the declared finite profile.`
- TeX line 93: `records the finite scale of the exact rational certificate.`
- TeX line 99: `both endpoints.  In the four tested finite configurations this normalization`
- TeX line 100: `is of stable small size, not a growing obstruction.  This is a useful negative`
- TeX line 103: `not an upper bound on the full normalized operator norm.`
- TeX line 105: `The arithmetic signs of the source remain unidentified.  No arithmetic $L^2$`
- TeX line 115: `local identities & \texttt{PROVED\_EXACT\_FINITE}\\`
- TeX line 116: `finite decimal values & \texttt{NUMERICAL\_OBSERVATION}\\`
- TeX line 117: `normalized growing theorem & \texttt{OPEN}\\`
- TeX line 119: `Route-B / twin-prime result & \texttt{OPEN} / \texttt{NONE}\\`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
