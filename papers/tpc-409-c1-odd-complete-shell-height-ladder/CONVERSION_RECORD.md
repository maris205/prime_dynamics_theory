# TPC-409 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `a28d0391f7e521318511a612753a3c25f6ebdc5a9ce16829d7cb2a55e7af2f26`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `bbc9004ea119da875e9285429e908915f6bfc76b4fa0077fde0c9b7b10bfbe7a`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `dad823a14814b3655517e421137092f5e535ad4ca5d42d892a7a130eaa8f06b2`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Odd-shell height ladder` | 23 | 1 | `HEADING_TEXT_MATCH` |
| `Finite height theorem` | 44 | 1 | `HEADING_TEXT_MATCH` |
| `\,Exact certificate and observations` | 65 | 2 | `HEADING_TEXT_MATCH` |
| `\,Route boundary` | 82 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 91 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `41` before writing and `41` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `f82bbac5598563266688c7b20024a9218d5034240bd23e50f4b0648def968511`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 27–30 | `a158af3c9c0d6e46f31e83fa7b4577bb61ec4821a3777b9cf0b3c88b96039925` |
| D02 | \[...\] | 33–37 | `54395d2c81a7466f172d9ec79e8e17cee6c7ee22a345b9106982a7bd340f316a` |
| D03 | \[...\] | 39–41 | `7b100f808d18d4052eeded8e2aca476db7e047c1abb646590cb246ebb1f82299` |
| D04 | \[...\] | 47–50 | `c4c41246e68f9ca6a849094f1019e90a8a389b29dcc13808e6bc634e4fab417b` |
| D05 | \[...\] | 57–60 | `d2ccf0d987f5d6bb5cbc347cf7df6f6fc9ef71d7038327e42b71ba419b277058` |
| D06 | \[...\] | 68–76 | `3857ae3550b3a5bbfb6a8f5de60df0cfd3f1a5951c251a2305da40b43695ca94` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 19: `replay verify all four rows.  This remains a finite synthetic proxy result,`
- TeX line 20: `with no arithmetic or twin-prime conclusion.`
- TeX line 42: `The height $H$ is a proxy parameter, not the physical $h_0$.`
- TeX line 44: `\section{Finite height theorem}`
- TeX line 67: `rational arithmetic.  The resulting finite observations are`
- TeX line 78: `squares; it is not an asymptotic fit.  The independent checker reconstructs`
- TeX line 83: `This is a finite four-height result for one synthetic adjacent normalized`
- TeX line 84: `proxy entry.  It is not a full normalized operator estimate, physical`
- TeX line 85: `$h_0$ theorem, arithmetic sign or $L^2$ theorem, fixed-power saving,`
- TeX line 87: `status is \texttt{PROVED\_EXACT\_FINITE\_ODD\_COMPLETE\_SHELL\_HEIGHT\_LADDER};`
- TeX line 89: `is \texttt{OPEN}.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
