# TPC-385 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `38be1c1e548e17857c6ffbe502d1b0dc7255dc781b2442613d3ddbc12ac36d4b`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `33896b857d561aec2d93afe9060046a6a095b8d6c5e8c68d108eaada9a77180f`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `20d117a64ac00302515e30259d8a885ddba81f2b67672c56d44ae930a3d77154`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and finite object` | 39 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen protocol and certification` | 74 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 92 | 2 | `HEADING_TEXT_MATCH` |
| `Claim boundary and route status` | 121 | 2 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 141 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `43` before writing and `43` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a719579a36deeb4c3bab0f44f0b19e7058cc6f6769bec3bb185372f9beadc64d`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 49–53 | `8c5b6d998fd3755424a0196242ade657dd8c51667e5b44b165d60d9294c37cdf` |
| D02 | \[...\] | 55–57 | `9bb427399cb324e57115df53be56e863845130870691f11455caab3215414a42` |
| D03 | \[...\] | 60–64 | `2c458812b04960500986fc7ce32d02cde461fca35b0d310aba27f8da9bae31e9` |
| D04 | \[...\] | 66–70 | `061452866296fb4132688aee8f0f0f546ada6e077c7eddf4c3f6850d0c9fac45` |
| D05 | \[...\] | 83–85 | `81b0a0b779453f8ddd611754a1c60ef239c8120239e97a0a26c7041677a963b7` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 14: `\title{A Response-Blind Origin Holdout for a Finite\\`
- TeX line 25: `We test whether the high-bandwidth phase observed in the preceding finite`
- TeX line 34: `unstable at $Q=2048$.  This is a finite transfer certificate and a law-control`
- TeX line 35: `obstruction; it supplies no arithmetic $L^2$ estimate, power saving, or`
- TeX line 39: `\section{Question and finite object}`
- TeX line 95: `All 160 rows are below both finite metric caps.  The maximum holdout spread is`
- TeX line 98: `law-uniform.`
- TeX line 117: `a useful finite origin-holdout replication of the all-plus phase.  It does`
- TeX line 123: `The paid finite statements are:`
- TeX line 129: `\item \texttt{OPEN}: bandwidth monotonicity, law/origin/count uniformity,`
- TeX line 137: `evidence only.  The next finite clue is`
- TeX line 146: `and one BLAS/OpenMP thread; normal and optimized checker outputs are required`
- TeX line 148: `finite dynamical proxy and carries no twin-prime claim.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
