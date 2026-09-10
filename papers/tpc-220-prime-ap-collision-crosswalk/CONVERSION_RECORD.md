# TPC-220 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `032a02e63065c0e75efa2937431a768b87b4932ac95a8338ad7a99f89e5c5b73`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `29e47519e51a2802828c90d20d8d025893f83472af69a265461929964facec24`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `44797270eff179884f446d2f3bfef0b63f4446da9809abafdec24f9f9f0e943e`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC220_224.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `From the transverse ledger to arithmetic coordinates` | 37 | 1 | `HEADING_TEXT_MATCH` |
| `Exact weighted prime-AP crosswalk` | 66 | 2 | `HEADING_TEXT_MATCH` |
| `The multiplicative collision Gram` | 98 | 2 | `HEADING_TEXT_MATCH` |
| `Finite collision audit` | 140 | 3 | `HEADING_TEXT_MATCH` |
| `Route position` | 164 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 177 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 186 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `49` before writing and `49` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `12`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `093f619a90da59f548f8d7603047f9bf33ee6cb2950938113a40cf1bb1cd471a`.
- Source theorem/proof environment starts: theorem at TeX line 68, proof at TeX line 83, theorem at TeX line 108, proof at TeX line 125.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 40–42 | `e1f773a88f7ca5c29176825ee4167352b25f82cd36ca6e81d387fcd4a2d572b2` |
| D02 | \[...\] | 48–52 | `1ed82974359ba69fa7725a64202378230f9b5d68168b53b67b545b9990bf892a` |
| D03 | \[...\] | 54–56 | `e1e3aa72e3a09f3c1fb87531e2630fb9fd148f5516cb092d9c4bef4ab5073f2c` |
| D04 | \[...\] | 58–62 | `2b7823817057fbcb6f6b70ae15c5b67b1e427a915cf2ed07f2e6b6c1c3448120` |
| D05 | \[...\] | 70–74 | `32be5d450e8385165aac26ff14d5d1a3c40c0f2a87b4905e17d504660c75692f` |
| D06 | \[...\] | 76–79 | `ee1d982c8bc6a318a30161505a0e4724e1982606ad1d72d2ad368f0cab125340` |
| D07 | \[...\] | 85–89 | `5ff375b79a21581cea412cbcbc2a3a0a0ccc9d238eb3b736e80eaea64ab3da3d` |
| D08 | \[...\] | 101–105 | `a4475254c3316c83b553c0ff87f31a958b043fba54dc60bab12e705e2410934f` |
| D09 | align* | 110–117 | `db583ae0f1c0e08ef2f1f0d5c6868baf1d2b93097ea80e3a7c2e76e313e26c75` |
| D10 | \[...\] | 119–122 | `c204dc2f75892a9707f1022144e8c150b431e0ff24d0d6b2ace0726e0ede47ea` |
| D11 | \[...\] | 128–130 | `a6d8d9a1a1fa323a1db14d518e84834ac859783d546b173e032d94d3075b317b` |
| D12 | \[...\] | 169–173 | `0d6d288285fcfcc87659562238af20f38ab87890f34c0ad3d097f369c9388f61` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 23: `sub-$P$ prime-shell estimate, but it does not yet express that quantity in arithmetic`
- TeX line 30: `profiles.  No estimate for primes in progressions and no arithmetic $L^2$ advance is`
- TeX line 90: `Insert this equivalence into (1), multiply by $\lambda_q$, and interchange the finite`
- TeX line 95: `Equation (2) is not an average-prime approximation.  It is a weighted AP incidence`
- TeX line 137: `large-sieve lift.  The off-diagonal is not a formal error: it is the explicit graph of`
- TeX line 140: `\section{Finite collision audit}`
- TeX line 153: `object & finite scope & status\\`
- TeX line 172: `\texttt{FULL\_GATE\_B}=\texttt{OPEN}.`
- TeX line 189: `2026.  This is an internal source lock, not an external theorem citation.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
