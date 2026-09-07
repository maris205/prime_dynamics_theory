# TPC-294 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `7bba57e68d04514ee33ab2192a507a1f4edfebab`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `df418f158d275944ff1e668463d0d1ae885ac4c1dfaf4291aa68ad8434bf2122`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `73ffe8dade054710795a5d8af528f58810e1861f6e474053cee43ee183629e8b`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `5663a4943fb99b1fd6de7f83e4bdf1dcb673cc65be242c2d55d41ec2da055ff6`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `bc140dc3e868cdcc0164125cff8b86f60e2aacfa1035eb545a09c897d21a9454`.
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
| `Position on the twin-prime route` | 41 | 1 | `HEADING_TEXT_MATCH` |
| `Physical shell` | 57 | 1 | `HEADING_TEXT_MATCH` |
| `Weighted sign quotient` | 80 | 2 | `HEADING_TEXT_MATCH` |
| `Exact finite optimization` | 111 | 2 | `HEADING_TEXT_MATCH` |
| `Finite protocol and atlas` | 148 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and route boundary` | 210 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility and conclusion` | 232 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 250 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Post-document material begins at TeX line 252; suffix SHA-256 `1a5adb5c91a9dcdb41bb0ef68ce6bfcd6abd15ebe76771f80229ef1199e9d25f`. Retained as literal code, not interpreted as manuscript prose or counted as document math nodes.
- Pandoc math-node sequence: `61` before writing and `61` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `bc20ba8c25eff26326558594b132102d2f08d7582563d269593e79f499c3e4f5`.
- Source theorem/proof environment starts: theorem at TeX line 89, proof at TeX line 99, theorem at TeX line 122, proof at TeX line 128.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 62–66 | `a641d953a37284c10446dcf660c55e3b027e135132e489b2ff3d09a4ad996782` |
| D02 | \[...\] | 68–71 | `7bf26faa1f7a694abbe30d59293002d32056fca79e9fbac76dc1d60940e5d2ee` |
| D03 | \[...\] | 73–77 | `acb29a6117749e7f6981fee9ca8c2fbf677a006c467b16c11aac878b6ad038ba` |
| D04 | \[...\] | 83–86 | `fe366cb5d24e198ad2d3f1e374796cea692b10dc1f6c05ace1ac92ea01b2504b` |
| D05 | \[...\] | 91–95 | `be71faadd5dda1f9c0be0691d7d149f24daffc44b0824872652af959f64c2b9f` |
| D06 | \[...\] | 115–118 | `7c07f016b9037268ce3ec974cc671d4da597735a496519e1cf67916be0f93298` |
| D07 | \[...\] | 139–143 | `0b7e7bfa7f3cc8a9bfc4d1c2fe30a67b56dcd91e339a3c0d97dfb5b98a20f416` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 15: `\title{Magnitude-Weighted Signed Rayleigh Cancellation in Finite Prime Shells}`
- TeX line 27: `unit edge.  That sign layer can identify compatible cuts, but it does not`
- TeX line 32: `sign reversal, and certify the resulting finite atlas with exact rational`
- TeX line 36: `rows.  The result is a finite weighted structural diagnostic: source-image`
- TeX line 38: `twin-prime endpoint remain open.`
- TeX line 55: `the two optimizers directly rather than identifying them by assumption.`
- TeX line 72: `For a finite prime shell $S=\{q:Q<q\le 2Q\}$, define the exact Gram matrix`
- TeX line 111: `\section{Exact finite optimization}`
- TeX line 122: `\begin{theorem}[Global finite sign search]`
- TeX line 145: `source-coordinate-first physical accumulation, so the certificate does not`
- TeX line 148: `\section{Finite protocol and atlas}`
- TeX line 159: `\caption{Global finite audit on the inherited grid.}`
- TeX line 212: `The finite result closes a genuine missing branch of the map.  The`
- TeX line 214: `carried enough mass.  TPC-294 answers that finite question affirmatively for`
- TeX line 224: `$L^2$, Gate B, and the twin-prime endpoint open.`

## Conversion limitations

- Post-document source is retained in an explicit uninterpreted code block; its meaning and PDF inclusion are not inferred. See the formula-scope entry for provenance.
- 5 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:identity` → `main.tex#L94` (existing project target or original TeX label line).
- Link relocation: `#eq:identity` → `main.tex#L94` (existing project target or original TeX label line).
- Link relocation: `#tab:rows` → `main.tex#L184` (existing project target or original TeX label line).
