# TPC-221 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `2e1dce655ca118c7a41cb09b7dbddc1163cfebcd0f0c456fb319f9325b7018f6`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `d475668bce2decd3f92f7cb062b4447789647b497eeb076a0ce673dddafb90ee`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `515366712de8ff57de30fd725b1a83b5102994141980dd1d166c9778b4db4cf1`.
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
| `The collision object` | 37 | 1 | `HEADING_TEXT_MATCH` |
| `Exact PSD energy and Schur control` | 73 | 2 | `HEADING_TEXT_MATCH` |
| `A literal saturation of the absolute envelope` | 131 | 2 | `HEADING_TEXT_MATCH` |
| `Certificate and route position` | 163 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 195 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 202 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `67` before writing and `67` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `12`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `895645278d5a58cfe7687738d73173a9dbbd8e2eed1384dd8a89f6d3bffdb011`.
- Source theorem/proof environment starts: theorem at TeX line 75, proof at TeX line 86, theorem at TeX line 93, proof at TeX line 111, theorem at TeX line 133, proof at TeX line 148.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 43–47 | `1ed82974359ba69fa7725a64202378230f9b5d68168b53b67b545b9990bf892a` |
| D02 | \[...\] | 49–53 | `eb2dbd0f4a28c019bfc27cefd287d27d83bf72e8f9bf9e742d719b743e19f810` |
| D03 | \[...\] | 56–60 | `ef6cea7b5a9e14ea78f87fd0ed57c917f309fbfe4abee743183130dc58538d67` |
| D04 | \[...\] | 62–69 | `e44772fb2566142725f3e2ab462ffb922d9944bbfd683e93cd106ad9b292a1c5` |
| D05 | \[...\] | 78–83 | `037480fb736b031d632c369ce6b1d791564eae3117f2c9ed2620351c75002fcc` |
| D06 | \[...\] | 95–102 | `36bcae605648bff9b9158e1ee999f7842dd25bb384dacda8371a45c2919b62ca` |
| D07 | \[...\] | 104–108 | `b5de43e2aa50427bb4e995798262ddd714030c8463bdae27b5e70636a660a10f` |
| D08 | \[...\] | 113–117 | `b43a4b3741bfe13cee70ce25f0a53f55103dc364ecf2bf6d7712177f6f225eae` |
| D09 | \[...\] | 120–122 | `c96dca3b98a46ea9ab62962ca6d7967365d65245d313d012bc2e44e182edbb14` |
| D10 | \[...\] | 135–137 | `c65ca1e68c4925fa68f4894c2713c36b3c1d0197c67d2c7b105603ad5788ac45` |
| D11 | \[...\] | 139–142 | `a501135614572684241aebc4dab516f1971a9abd83d300a6ac360d5f4e2399f8` |
| D12 | \[...\] | 189–193 | `86c25b9a4a2a7757caa675ed2b2cce1a0bf8426fbd1c2fead9a9e5309f48731b` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 23: `collision Gram, but leaves open how much an absolute collision estimate can save.  This`
- TeX line 24: `paper supplies the next exact layer.  The row Gram is positive semidefinite, its weighted`
- TeX line 27: `finite saturation: with $h=5$, $H=500$, constant profile, and primes`
- TeX line 54: `Let $\mathcal Q$ be a finite active prime set and regard $B_q$ as a vector indexed by`
- TeX line 70: `where $w_{h,m,q}=\psi(Hm/(hq))$.  Thus the matrix is not an abstract covariance`
- TeX line 76: `The matrix $\G_h=(\G_h(q,q'))_{q,q'\in\mathcal Q}$ is Hermitian positive semidefinite.`
- TeX line 90: `$AA^{*}$ is Hermitian positive semidefinite.`
- TeX line 133: `\begin{theorem}[Finite aligned obstruction]`
- TeX line 158: `This is a literal finite saturation, not an arbitrary PSD counterexample.  It proves a`
- TeX line 160: `cannot guarantee a saving below the q-cardinality factor uniformly over the literal class.`
- TeX line 161: `It does not say that the same alignment survives in a growing prime window.`
- TeX line 167: `fixture.  The exact finite summary is:`
- TeX line 192: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 200: `than merely count collision edges.  Twin-prime reassembly remains open.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
