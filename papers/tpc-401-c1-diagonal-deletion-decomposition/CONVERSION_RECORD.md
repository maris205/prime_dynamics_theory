# TPC-401 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `b3982c08680e5acb3f79e485fb6133e93680694d44e2ab8b7db9e48e977dd415`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `869023a983e2a82b05f8894e22be8f61ee29474b37539bf475e179566bfc9916`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `47b272c5120feb1b7399f5ea8f3d830f495fdaa0fe545a8ff6bbeb0a98ab61df`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 22 | 1 | `HEADING_TEXT_MATCH` |
| `Exact production-domain identity` | 33 | 1 | `HEADING_TEXT_MATCH` |
| `Geometry formula and finite audit` | 49 | 2 | `HEADING_TEXT_MATCH` |
| `Boundary counterexample` | 63 | 2 | `HEADING_TEXT_MATCH` |
| `Route ledger` | 70 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 84 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `36` before writing and `36` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `4`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a68094125cadb27458c8e405b12d69f1e1a7cea46782e889c54520acc6fbf481`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 27–29 | `0bbf2e1b3bf60ada0c595ae14dcd6806fb7a9974e805ae8f0c69166a2aa20be5` |
| D02 | \[...\] | 37–40 | `6efc46a8d32d3d80beeb64efe8080a5b8d806190fdf5791e7c06ed8efc69de70` |
| D03 | \[...\] | 44–46 | `7bd0cada5bd81a45aacfe6720de670fba75c2a18843279da120a1003c347d2ff` |
| D04 | \[...\] | 53–56 | `578e053caf8566d7fdc88090af9e218ecbb5467d90c47be5c2a704c2a4d198d1` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 4: `\title{TPC-401: An Exact Finite Diagonal-Deletion Decomposition for the C1 Panel}`
- TeX line 14: `$K_p=-a_p(D_pTD_p-D_p)$.  An exact finite audit over six TPC-400 origins and`
- TeX line 18: `finite algebraic result; it supplies no arithmetic $L^2$ estimate, asymptotic`
- TeX line 19: `uniformity, or twin-prime theorem.`
- TeX line 25: `responsible for that finite object.  We use the exact production parameters`
- TeX line 30: `All claims below are finite.  The synthetic sign laws used by the parent panel`
- TeX line 49: `\section{Geometry formula and finite audit}`
- TeX line 61: `mutation.  These are exact finite checks, not a growing estimate.`
- TeX line 67: `to that anchor.  The anchor is useful for checking other finite interpolation`
- TeX line 68: `identities, but it does not prove this decomposition.`
- TeX line 73: `production decomposition & \texttt{PROVED\_EXACT\_FINITE}\\`
- TeX line 75: `finite audit & \texttt{NUMERICAL\_OBSERVATION}\\`
- TeX line 78: `Route-B / twin-prime result & \texttt{OPEN} / \texttt{NONE}\\`
- TeX line 80: `The next finite question is the signed diagonal-deletion term audit.  A source`
- TeX line 81: `arithmetic sign law, uniform constants, an asymptotic operator bound, and the`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
