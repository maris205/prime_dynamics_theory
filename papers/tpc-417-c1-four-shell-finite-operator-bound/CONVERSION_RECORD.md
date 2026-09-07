# TPC-417 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `f92f1bd23b6c5738216ebbb91f1336f133346e4c3e3f28333ba0d560ec0fb780`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `7484892d443c4115bbb7329ac9408d4aec3aef7fd46da83136f1acd5faa9e842`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `87b771b925f208782a6acde77f210d8add4b6c991bef72046113fe4ef92104c3`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Finite model` | 20 | 1 | `HEADING_TEXT_MATCH` |
| `Exact matrix identities` | 29 | 1 | `HEADING_TEXT_MATCH` |
| `Bound` | 45 | 2 | `HEADING_TEXT_MATCH` |
| `Scope and audit` | 62 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 77 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `42` before writing and `42` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a4875acd1dde9509721fe73ceb4588eac0485e1d9bcaa13d2b89ec35893a7670`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 31–34 | `18052ab3b3833cdfa78f31da46321ef9aa9d54554d131583931dc13446413936` |
| D02 | \[...\] | 36–38 | `e7867b0d238f1939079545024a632e049ba19dee049dec89757dbcc6c1ab1709` |
| D03 | \[...\] | 40–44 | `5d947628f4c3841540513e28260cbac951ec1dcb588b7daed92a5e48313958ab` |
| D04 | \[...\] | 49–51 | `eb82948b02d9819a5cd7e9b279119e18d78e090f837958cb6c98f100110ccece` |
| D05 | \[...\] | 56–58 | `c65ae0735ce8347b41af7905f6c5684dd3007c61f4bd8198cff08fed1cd574ca` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 4: `\title{TPC-417: A Finite Full-Operator Bound for the Four-Shell C1 Proxy}`
- TeX line 10: `finite window matrix.  For four complete prime shells and each of`
- TeX line 13: `finite, explicit bound is obtained:`
- TeX line 16: `$75483$ primes.  This is a finite synthetic-operator theorem only: it does`
- TeX line 20: `\section{Finite model}`
- TeX line 59: `The star certificate records the exact Cauchy--Schwarz envelope, not an exact`
- TeX line 67: `modes.  The result is a full finite matrix bound for the declared synthetic`
- TeX line 68: `proxy, not a bound uniform in growing $H,Q,N$ and not a statement about the`
- TeX line 71: `finite full matrix bound & \texttt{PROVED\_EXACT\_FINITE}\\`
- TeX line 72: `growing operator theorem & \texttt{OPEN}\\`
- TeX line 73: `physical $h_0$/arithmetic sign & \texttt{OPEN}\\`
- TeX line 75: `Route-B / twin-prime result & \texttt{OPEN} / \texttt{NONE}\\\bottomrule`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
