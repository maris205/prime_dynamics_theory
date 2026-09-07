# TPC-291 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `7bba57e68d04514ee33ab2192a507a1f4edfebab`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `ffc735fcf29ec6c027f7c76cb7f2387e3b422f3ebe37309a06997e419b546a16`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `41b9560cfed8b34e9544bde1b0fccff95d596e4cd6affb1be4ebb5329ef6ec45`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `4dc2b6a201ebee6eb17bdb33c55d44787ef8f1b4015bb05cbcb23de4c2c4b420`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `79feebf1d97bdad9c4606d8d27129f2e35ec56c3f4102a6d999e33ef9e687175`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC290_294.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Position on the twin-prime route` | 54 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen physical model` | 74 | 1 | `HEADING_TEXT_MATCH` |
| `Exact two-prime cancellation compiler` | 99 | 2 | `HEADING_TEXT_MATCH` |
| `Finite protocol` | 169 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 186 | 3 | `HEADING_TEXT_MATCH` |
| `Global census` | 188 | 3 | `HEADING_TEXT_MATCH` |
| `Representative rows` | 222 | 3 | `HEADING_TEXT_MATCH` |
| `The exceptional sign-flip row` | 255 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and claim firewall` | 273 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility and conclusion` | 299 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 322 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `77` before writing and `77` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `11`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `5c516dcc85ff572912f3c3bddd6928e34ff163c373937979bb2281bc5ca58841`.
- Source theorem/proof environment starts: lemma at TeX line 104, proof at TeX line 118, proposition at TeX line 128, proof at TeX line 138, corollary at TeX line 149, proof at TeX line 156, remark at TeX line 162.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 36–40 | `cde00bc28a9c5754e3ee21facc2ac2e32c9a46a521fb82315678ccaea4e46bfb` |
| D02 | \[...\] | 79–83 | `a641d953a37284c10446dcf660c55e3b027e135132e489b2ff3d09a4ad996782` |
| D03 | \[...\] | 85–88 | `7bf26faa1f7a694abbe30d59293002d32056fca79e9fbac76dc1d60940e5d2ee` |
| D04 | \[...\] | 90–94 | `c1e0e22e75ac3f6635b8b3b5845c4d6bda84d552d0adc96c858f371c3e8ff93c` |
| D05 | \[...\] | 107–109 | `93f17188ceec8e47be28f62d249030dcc01c91ed6133f6b43ad512ef9f63a54c` |
| D06 | equation | 111–115 | `3ff3f36f0a86832216d40e61cf7b28ca15440ad1e42ecd5e4d3812ee5b14d107` |
| D07 | \[...\] | 120–122 | `9dfb1f154d574ffae2f29c79294ca7895f420da40dde9f4643b5f750f2e04c77` |
| D08 | equation | 130–135 | `42c73d485da998478ccef49b50aeaf435515ab1cf0e8f05e32e0c0a83ba9dff9` |
| D09 | \[...\] | 141–144 | `2a930dcde9da248cd90701977b498cd5f6c8b89f907452955eeaf2f240b848a2` |
| D10 | \[...\] | 259–261 | `9e81a540b711257b49b3c21af98389be54bcd207a995528c143a6b6e35866525` |
| D11 | \[...\] | 263–266 | `f4d90221ae0a818d165c27faad6b60a6120ad9502b2b1fdf71042aac8bd3959e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 19: `a Finite Coherence-to-Cancellation Atlas}`
- TeX line 59: `produces a positive-semidefinite source-output Gram object whose finite`
- TeX line 76: `Let $I=I_N$ be the finite integer interval and let $\beta$ be the frozen`
- TeX line 163: `Equation~\eqref{eq:schur} is a two-dimensional statement.  It does not say`
- TeX line 169: `\section{Finite protocol}`
- TeX line 181: `The finite thresholds are $1/2$, $1/4$, and $1/10$ for the residual, and`
- TeX line 197: `\caption{Finite pairwise census on the declared 18-row grid.}`
- TeX line 217: `Thus high coherence is common in this finite probe, but its sign is almost`
- TeX line 251: `largest coherence is therefore a real finite cancellation opportunity in the`
- TeX line 267: `Consequently these three negative pairs are precisely the finite`
- TeX line 271: `it does not yet provide a diffuse or growing-shell mechanism.`
- TeX line 284: `\item Pairwise optimality does not compose automatically.  A multi-prime`
- TeX line 290: `Rayleigh compiler.  The strongest finite numerical claim is the complete`
- TeX line 291: `1,380-pair coherence-to-cancellation atlas.  The following remain open:`

## Conversion limitations

- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:rayleigh` → `main.tex#L134` (existing project target or original TeX label line).
- Link relocation: `#eq:schur` → `main.tex#L114` (existing project target or original TeX label line).
- Link relocation: `#tab:rows` → `main.tex#L233` (existing project target or original TeX label line).
