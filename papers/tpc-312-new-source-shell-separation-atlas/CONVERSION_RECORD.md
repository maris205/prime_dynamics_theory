# TPC-312 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `abdb8bfb644f8d81c8d74b6ac609d88d191b913b`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `e9df20182f024b8dc5a8ad38e1e260db0e19a5d5e858ae0fc2b4dc286e1e69e1`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `f62fda1d2053e690a8aa175b7813fee1f08b401f338fe6fb4854c5c803481415`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `0add7967ce34e5f15051c11189d0213562c6d422396f21270213bb16353a5531`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `da456689c29c79efb33adace5a3cf7ba9def727c199775ec42f441ba03760649`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC310_314.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and route position` | 40 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator and certificate` | 58 | 1 | `HEADING_TEXT_MATCH` |
| `Finite facts` | 87 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 130 | 2 | `HEADING_TEXT_MATCH` |
| `What this does and does not establish` | 170 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and next gate` | 188 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 207 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `45` before writing and `45` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `6cd6a2336e298898f5be9d2a81e43ecc288e524e4a6d05bb3c0edcd7e0c8c0a9`.
- Source theorem/proof environment starts: lemma at TeX line 89, proof at TeX line 95, proposition at TeX line 101, proof at TeX line 105, proposition at TeX line 112, proof at TeX line 123.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 61–64 | `23553f0fe3ea04c3df1ae565fd3f04d341df7e202bd5f35ee9b70641e4c165ce` |
| D02 | \[...\] | 66–71 | `e1d7af2ba7b0c6991175a07e6887ffaf315719ae4c0db00d4352bf02554da78d` |
| D03 | \[...\] | 73–77 | `16ae6674f76068f376b157d21c3e0878a0d9e1daa6adacb46dd5b89f88929701` |
| D04 | \[...\] | 91–93 | `ac89f8dc87031d59042984ef79a543af8e7485930366295a04c8c5e7a859a33d` |
| D05 | \[...\] | 115–119 | `757416cefefc6fa8896edf448b224d3f17e7d602bcb820acd6dc8b52e59baa8f` |
| D06 | \[...\] | 134–136 | `3d71cda722a6c870ee80be50bc391d4cb5330419da6c2653216932a9da19b466` |
| D07 | \[...\] | 163–165 | `58815c47876c03480c522430dd706ea5c6034e72594f119d97d243e8e965aa9a` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 13: `for a Finite Prime-Shell Diagnostic}`
- TeX line 24: `We move a finite Bridge-B diagnostic to eight previously unused physical rows.`
- TeX line 34: `The result is an exact finite source--shell atlas and a useful new obstruction:`
- TeX line 35: `the observed separation is reproducible inside the same engine, but it does not`
- TeX line 36: `provide external independence, a canonical weight law, a uniform asymptotic`
- TeX line 42: `The preceding releases progressively attacked finite-instability concerns in`
- TeX line 44: `showed that aggregation order changes the finite class, and TPC-311 found that`
- TeX line 55: `parameters within the same locked finite engine, not an externally collected`
- TeX line 58: `\section{Finite operator and certificate}`
- TeX line 85: `ratio digests.  It does not import the producer or TPC-288's output routine.`
- TeX line 87: `\section{Finite facts}`
- TeX line 96: `Expand the square and interchange the two finite sums.  This gives exactly`
- TeX line 101: `\begin{proposition}[Finite sign enumeration]`
- TeX line 112: `\begin{proposition}[Finite ordering statement]`
- TeX line 143: `\caption{Exact finite sign extrema, shown as decimal renderings.}`
- TeX line 167: `negative vector.  These facts are exact finite comparisons; the displayed`
- TeX line 170: `\section{What this does and does not establish}`
- TeX line 174: `new finite spine, cancellation and amplification separate in opposite`
- TeX line 183: `the same finite engine; ''new'' is not external independence.  Third, exact`
- TeX line 184: `finite ordering says nothing about a sequence of growing intervals or shells.`
- TeX line 193: `obstruction is equally clear: finite sign separation alone cannot choose an`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
