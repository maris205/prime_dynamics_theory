# TPC-300 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `55240d2d7254cbf8bd7fc0b4755fa8f24254e424`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `f8bad634b4fec6b4a5863cda6c6f4c95b13502c160101ac2e5dfc70bd0f0e70c`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `28b8d77da3a715b6619a32c0a8c7c0f8c6c73b96a0cd44b83726af3532042390`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `a29fb8c20823a5994804e6e90369e1700f69d5a59487e5127bdbe8716c4c738f`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `d739f7f5e06a82a2c3d788dd9ed82b966206bf347781c004ef6746c9170e097e`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC300_304.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and finite setting` | 41 | 1 | `HEADING_TEXT_MATCH` |
| `Dual formula` | 69 | 2 | `HEADING_TEXT_MATCH` |
| `The reciprocal parameter correction` | 136 | 3 | `HEADING_TEXT_MATCH` |
| `Exact rational certificate compiler` | 151 | 3 | `HEADING_TEXT_MATCH` |
| `Finite audit` | 170 | 3 | `HEADING_TEXT_MATCH` |
| `What this does and does not close` | 204 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility and claim status` | 227 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 245 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `77` before writing and `77` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `18`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `ecb2574957a339a99d12ac691ef6912a2a02de3cba298ab513b1f66b72f2747a`.
- Source theorem/proof environment starts: theorem at TeX line 71, proof at TeX line 84, proposition at TeX line 112, proof at TeX line 124.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 28–31 | `923ef855928f1a233a4de5a3bfce0cc6834bbeb1f65801a560ad384b75ffeeb3` |
| D02 | \[...\] | 46–48 | `9ef5b7d64c77fe5849e8d0e6de76942cfd679a206aa6aadf56cd62edf071769c` |
| D03 | \[...\] | 50–52 | `2572eca309976c4bf1971263a5e9c509e541a897bddc986a9484bd41846a146b` |
| D04 | \[...\] | 60–65 | `0b2772c01836914ed13bda292dea15567839e52b7d7907790746941d8511f434` |
| D05 | \[...\] | 74–76 | `b6278738021035ffa001d004ec1c95d99dbb98cfe8a903796e1eee52e59f2c27` |
| D06 | \[...\] | 78–80 | `ad51f2d0dface216d090804e77d7429609c7e0fbf1e7e12a9a75998d75ca31de` |
| D07 | \[...\] | 86–88 | `60544e72305cac04fc27683eb88d4187006c680ce93e8f9bebfff14586f811cf` |
| D08 | \[...\] | 90–92 | `fda377db8bb3172ff495329b81870b05c1aa9870a4c7fcff51a4758a655219e1` |
| D09 | \[...\] | 94–97 | `86290e23aab6550b4f44af4867487553069dd330d9b8199f0dc8b52140670fd3` |
| D10 | \[...\] | 105–107 | `1ea9f03ad249eb7529284f65e77d727d9a2370ded62d7808e7693d58c6ffc078` |
| D11 | \[...\] | 114–116 | `d13d6b10ce1babde36afe177473f0a4cef4388dfacd63b4235d2c4e1239264cc` |
| D12 | \[...\] | 119–121 | `ee84171313978aad70b1898bfc986ae4329f4c2b366b50a7a20f52300884da0a` |
| D13 | \[...\] | 126–129 | `0f68495a266eac97b926d29c2e1854583b06da1a07850904c7d9493e0bfeec28` |
| D14 | \[...\] | 141–143 | `8f2694e1fc3f60c360c160509a094a9e99d6b506d5251d5e1ff9c63c19540e27` |
| D15 | \[...\] | 207–213 | `63c1bbfd02737619c3aacf347722b934e0746fc93db4aead5815b118dfcfd746` |
| D16 | \[...\] | 234–236 | `f1a1050510bd8ff410d3bf044cd0a93d048dcac659982de4558c0c7ce122877b` |
| D17 | \[...\] | 237–239 | `ed63a2ba405a9f3d170a7fbf39967335512fa0bfdb7c4235cd9acc0200dcbad8` |
| D18 | \[...\] | 240–242 | `195382d7d086cd8890f7850559afd7c24a6bfc034586f86ea4a4a41f5c6de28e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 22: `The preceding finite native-profile study measured the source norm required`
- TeX line 32: `At an active finite frontier this is equality.  We also isolate the`
- TeX line 38: `result is a finite structural certificate, not an asymptotic estimate.`
- TeX line 41: `\section{Question and finite setting}`
- TeX line 43: `The TPC-299 release \cite{tpc299} converted a finite profile-angle ladder`
- TeX line 56: `because it separates the finite convex calculation from the choice of a`
- TeX line 66: `The finite audit has 18 rows and 1,380 shell edges.  It is deliberately`
- TeX line 72: `Let $M\succ0$, let $V$ and $b$ be finite real data, let $R\geq0$, and let`
- TeX line 89: `Its quadratic part is positive definite.  Its unique minimizer satisfies`
- TeX line 109: `$\norm{e_\rho}=R$.  Thus the dual scalar is not an extra fitted statistic:`
- TeX line 147: `finite obstruction counts changes.  The distinction matters when comparing`
- TeX line 170: `\section{Finite audit}`
- TeX line 180: `\caption{TPC-300 finite rational dual atlas.}`
- TeX line 204: `\section{What this does and does not close}`
- TeX line 215: `does not trust the primal source coefficients as its final evidence.  The`
- TeX line 220: `The finite profile family, shell grid, target tolerance, and normalization`
- TeX line 225: `finite convention.`
- TeX line 235: `\texttt{PROVED\_EXACT\_FINITE\_NATIVE\_BUDGET\_DUALITY\_AND\_RECIPROCAL\_}`
- TeX line 238: `\texttt{MULTIPLIER\_CORRECTION\_PLUS\_NUMERICALLY\_CERTIFIED\_FINITE\_}`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:atlas` → `main.tex#L181` (existing project target or original TeX label line).
