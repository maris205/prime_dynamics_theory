# TPC-405 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `b1b40518ea1714f301b23dd04ee1f893d9587982a2a2430fb8a747aad29f5656`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `18897725da4f6dd3d57c73c71aa69aeceec85e6bd4bacf3e6fabab79aaf2d423`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `3f00b1497f51b9c48b6910d0fc9799b6c773bf50e80da7c448a2403eb4793d91`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Scope and model` | 24 | 1 | `HEADING_TEXT_MATCH` |
| `\hspace{0.2em}Uniform adjacent-entry theorem` | 54 | 2 | `HEADING_TEXT_MATCH` |
| `\hspace{0.2em}Exact scale ladder` | 83 | 2 | `HEADING_TEXT_MATCH` |
| `\hspace{0.2em}Route boundary` | 109 | 2 | `HEADING_TEXT_MATCH` |
| `Reproduction` | 134 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `47` before writing and `47` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `dfaf3a971f96a5ae92b27c9b5a78ec1538e679f439da6638d67bc6b6fab3cda3`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 28–31 | `a0267afd43ac1a8ac0f516adee5ebc3a8250569d0301d3cb3bbf81600a6c4eec` |
| D02 | \[...\] | 36–40 | `e37520e2e9c8b8ab2f593857f1eca73bb047f1fbd1a9ea90ea74c2953d41922b` |
| D03 | \[...\] | 42–46 | `d0784cc0e0cea79422d343d5efef4be2924c89cb9a7f6e4bec505aca19bb272e` |
| D04 | \[...\] | 48–51 | `9c119ebd91e6db6134d9b9fb345e9b6efff4fff31c4562348c9d2f8a76a5085e` |
| D05 | \[...\] | 58–61 | `cb5598082793d77cda21ed1874300e6065f5e21c16be6d5c378d7b6ea112c33f` |
| D06 | \[...\] | 65–67 | `1ac4edab811037af8866ce30345aafca7d3be43ba1c630773886deac15c320e5` |
| D07 | \[...\] | 70–75 | `db4c5e2d46978db6dcd09db0e549b9ac01b27379d8b21d15ba8f65dfbd89b2db` |
| D08 | \[...\] | 78–80 | `36b91a1ae4b1371d5fd90b00428cca8b8b48ab42a5c0bcee6fecd80abfaba8c1` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 12: `deletion profile but tested only four finite configurations.  We prove the`
- TeX line 18: `multiplicities, while its decimal scale ladder is recorded only as a finite`
- TeX line 19: `numerical observation.  This is a uniform bound for one synthetic proxy entry,`
- TeX line 20: `not a bound on the complete operator and not an arithmetic or twin-prime`
- TeX line 32: `The origin may be chosen above any prescribed lower bound.  The half-open`
- TeX line 52: `Here $H$ is the kernel height of the proxy; it is not the physical $h_0$.`
- TeX line 54: `\section{\hspace{0.2em}Uniform adjacent-entry theorem}`
- TeX line 111: `narrow.  It bounds one adjacent entry of a selected-prime synthetic CRT`
- TeX line 112: `proxy.  It does not control the complete prime shell, unselected primes,`
- TeX line 113: `arbitrary origins, the arithmetic sign source, or the physical $h_0$.`
- TeX line 114: `Accordingly it does not pay an arithmetic $L^2$ estimate, fixed-power`
- TeX line 116: `an upper bound for this entry is not a full operator-norm estimate.`
- TeX line 121: `uniform proxy-entry bound & \texttt{PROVED\_UNIFORM}\\`
- TeX line 122: `finite rational certificate & \texttt{PROVED\_EXACT\_FINITE}\\`
- TeX line 124: `full normalized operator theorem & \texttt{OPEN}\\`
- TeX line 126: `Route-A / Route-B / twin-prime result & \texttt{OPEN} / \texttt{OPEN} / \texttt{NONE}\\`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.
