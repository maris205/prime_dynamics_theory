# TPC-377 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `03db7fc8f3e6255c887e2b58795ce997b214aad7838c07e9cfb8ab0debec9eb9`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `0a487ec51afbaedc34d3efc793db719fc59a00a44a0114ab2dc3dead393acb64`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `ebe8550e2038bd11d467c0fc372930fad7f794949c50c997d2236c3381418273`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 35 | 1 | `HEADING_TEXT_MATCH` |
| `Finite object and exact identities` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `Predeclared scale protocol` | 80 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 104 | 2 | `HEADING_TEXT_MATCH` |
| `Independent audit and limitations` | 148 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion and next question` | 165 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `46` before writing and `46` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `593ef7effd246a91a75a2abeded8af48b6ca31eb480efdd3fd6454dbeb716ccd`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 52–57 | `6bf5d91f3017d3972b4a0a8c0bca402a1e8d3b7b9bed75d2e6f41519f7c4f54f` |
| D02 | \[...\] | 59–63 | `ac6741ca8a835f9a251c4ac05fe97ef012a27b674be30aa233bfd1867156867f` |
| D03 | \[...\] | 66–69 | `df8f176d42dca2219ae8086a493d961ffd253baba6172dd9244c0246917c518c` |
| D04 | \[...\] | 73–76 | `ebb744238d0e8f0c2f0c9e90224f5e7faf60725acbcb1eb5c27a6ce85846a396` |
| D05 | \[...\] | 83–85 | `77b5db4f22852a431fec41b23d3c0d63e05a64dabd812ee656a952bf367fec23` |
| D06 | \[...\] | 87–91 | `053746b9acf1baea2200e3704fd016643417bf15a1045151c8e618ed4ecf544c` |
| D07 | \[...\] | 98–100 | `866073899cf8ee5d35cd44d480c0f4e1e65314507e81fdde66d6ad12cf179b33` |
| D08 | \[...\] | 139–143 | `d08c5553ea24c71761a0d8feae855298c428857b521db15fc4b7ae083453c9c9` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 13: `{\Large\bf A Finite Window-Scale Holdout for the $c=1$ Prime-Shell Band}\\[5pt]`
- TeX line 21: `TPC-376 moved the first finite bandwidth cutoff matching a high-$Q$ failure`
- TeX line 29: `$0.93760019185559207$ to $0.98047323365759775$. This is a finite`
- TeX line 30: `nested-prefix scale audit. It does not establish a growing operator bound,`
- TeX line 31: `origin or window uniformity, source-uniform arithmetic $L^2$, a power`
- TeX line 37: `The preceding finite audits found a recurring high-$Q$ all-plus signature in`
- TeX line 39: `$c=1$ as the first member of a finite list reproducing that support, and`
- TeX line 44: `The word scale is deliberately finite here. For each origin, the three`
- TeX line 49: `\section{Finite object and exact identities}`
- TeX line 70: `The geometry is a finite sum of nonnegative rational squares. Thus the`
- TeX line 77: `These are exact finite identities. They do not provide a bound uniform in`
- TeX line 112: `\caption{Band spectral ranges and finite failure census.}`
- TeX line 134: `whereas the two high-$Q$ ranges increase. This separates the finite`
- TeX line 153: `eigensystems. A mutation suite tests protocol, schema, finite-audit, and`
- TeX line 159: `The result is not an origin-uniform statement, a window-scale-uniform`
- TeX line 161: `normalization, a growing masked-operator estimate, or a source-uniform`
- TeX line 167: `Within the declared finite ladder, the $c=1$ band preserves the parent`
- TeX line 171: `each count keep the asymptotic interpretation open.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:profile` → `main.tex#L113` (existing project target or original TeX label line).
