# TPC-384 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `30f23e31aafb8793f25e8992b6a8de0f8e1b8e9eb8b7c5e084288e483f1e2c08`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `f8fe10a8f9a2051c636a759d34baa855dfcdbd345085ac47b18261ad43920ac1`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `274ce1a1e29a13dfaef37eec93e657628afaedbb43483e66c9b2798e58b485dd`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and frozen protocol` | 28 | 1 | `HEADING_TEXT_MATCH` |
| `Matrix construction` | 53 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 75 | 2 | `HEADING_TEXT_MATCH` |
| `Verification and claim boundary` | 119 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `41` before writing and `41` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `881e4fd14f94e1f05b09ff96ee4b204bdf18a1aa70abf6f42dd5b6b8e2086624`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 35–37 | `b1dfca083d2a5c4815155707aee19afeb045ad3ef08159ec2486901290aeddc3` |
| D02 | \[...\] | 46–48 | `d80a8c9ccfc12567613e1dbbe5d57cbbca265f951d1dc69ebffa10d07a86a738` |
| D03 | \[...\] | 57–61 | `a1de2dcfc5dd5e15142b63e106687d849473c46df9206f3ad23e8fb7178c4a1d` |
| D04 | \[...\] | 65–68 | `bf9a25ffbcb045506dda115220ef4454052d4a6f245d9bd313b9143d6cacef59` |
| D05 | \[...\] | 112–115 | `52fd734dfbe76add1a4e53c0af849a40f2a43e8f5677c495181962935b4d52aa` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{TPC-384: A Finite Bandwidth--Normalization Phase Diagram}`
- TeX line 19: `288-row finite phase diagram has law-dependent origin stability.  For the`
- TeX line 23: `the narrowest bandwidth.  These are finite model-relative observations; no`
- TeX line 31: `preserve a finite all-plus origin shape while moving its absolute scale.  The`
- TeX line 92: `All 288 rows are below both fixed finite caps.  This does not imply an`
- TeX line 116: `for \(c=0,1,2,3\), respectively.  The upward sequence is a finite numerical`
- TeX line 117: `observation, not a claim of monotonicity beyond the four declared points.`
- TeX line 135: `selection and coordinate separation & PROVED / FINITE\\`
- TeX line 136: `288-row bandwidth phase diagram & NUMERICALLY CERTIFIED / FINITE\\`
- TeX line 137: `origin-spread and calibration census & NUMERICALLY CERTIFIED / FINITE\\`
- TeX line 138: `bandwidth monotonicity & OPEN\\`
- TeX line 139: `source-valid normalization and growing bound & OPEN\\`
- TeX line 140: `arithmetic \(L^2\), fixed power, Route-B & NO CREDIT / OPEN\\`
- TeX line 146: `The next finite question is a response-blind origin holdout at the bandwidths`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
