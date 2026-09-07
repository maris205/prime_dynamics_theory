# TPC-319 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `b9723facc6f4c261e20e0d86513230e5351dfe4d`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `834adec8a42a75455bea1c52016405a46740253f12b44a42d85cec54ebeaf01c`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `10689366eaa2358e38b7dbe9df0da8e03309b0544f028adbe4e3bc3a049ee433`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `809928e1cf3b6afd414093d30880168689acbee7d43bc593faa946e990c2998d`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC315_319.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Motivation and scope` | 41 | 1 | `HEADING_TEXT_MATCH` |
| `The frozen finite operator` | 56 | 1 | `HEADING_TEXT_MATCH` |
| `The normalization firewall` | 91 | 2 | `HEADING_TEXT_MATCH` |
| `Certified finite protocol` | 113 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 149 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and limitations` | 183 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 199 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 208 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `65` before writing and `65` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `9e95b5148c1fc75cd0d381ffe1b15b31de4e4d06aa536b4265d2c861f1d47813`.
- Source theorem/proof environment starts: proposition at TeX line 76, proof at TeX line 84, theorem at TeX line 95, proof at TeX line 105.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 60–65 | `3af391dda1f7076eab449557b6eb510219181ce42a1f824acc38dcf47d163fb0` |
| D02 | \[...\] | 69–73 | `a8cbae68505f66d8777eca513ed791993dd2076e626006602d0eb626c8f4a152` |
| D03 | \[...\] | 78–81 | `837ccc5c414720db4d52aefe6acbf38cb3de273445bd091bfd2c52dd0c8861cf` |
| D04 | equation | 98–101 | `ed71f57b31c74f7801408039beebf48bd09d56f66c1d68e1d8d55294abedd1a5` |
| D05 | \[...\] | 122–124 | `eaeb6e2f937fe41274394223b975f1feda24ef724d33f8384bfc1948490ea682` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 26: `We continue a finite spectral audit of a deleted-diagonal, centered prime--shell`
- TeX line 33: `dual-path finite interval audit, while all 80 unnormalized comparisons are`
- TeX line 37: `result is a useful normalization firewall and a finite cluster diagnostic, not`
- TeX line 43: `The working operator is a literal finite model for a prime-shell component of`
- TeX line 44: `the twin-prime route.  Earlier finite releases successively compared a`
- TeX line 47: `second one, a single eigenvector is not a canonical object.  Moreover, a`
- TeX line 56: `\section{The frozen finite operator}`
- TeX line 76: `\begin{proposition}[finite Ky Fan principle]`
- TeX line 93: `The finite scale comparison has an elementary but decisive algebraic constraint.`
- TeX line 108: `Equation~\eqref{eq:flip} is not an asymptotic estimate.  Its role here is to`
- TeX line 109: `prevent a finite normalized plot from being misread as a power saving.  A`
- TeX line 113: `\section{Certified finite protocol}`
- TeX line 121: `and the finite Weyl estimate`
- TeX line 126: `Weyl to each of the $k$ eigenvalues.  All claims below concern this finite`
- TeX line 132: `\caption{Finite cluster audit.  Gap means`
- TeX line 177: `top eigenvalue is not uniformly isolated: ten of 24 rows have a top/second`
- TeX line 178: `gap below one percent.  Enlarging the cluster does not remove all small edge`
- TeX line 181: `not a stable canonical surrogate on this panel.`
- TeX line 186: `energy captured by a rank-$k$ subspace, and the finite certificate tracks this`
- TeX line 189: `finite transition.  This blocks credit for a growing arithmetic power saving.`
- TeX line 191: `Several gates remain open.  The calculation does not prove a uniform law as`
- TeX line 194: `locked finite engine rather than an external physical holdout.  The`
- TeX line 202: `but the resulting finite data makes the normalization issue impossible to`
- TeX line 219: `L. Wang, \emph{Finite Top-Eigenvalue Readout for a Literal Prime--Shell Operator},`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:kernel` → `main.tex#L64` (existing project target or original TeX label line).
- Link relocation: `#eq:flip` → `main.tex#L100` (existing project target or original TeX label line).
- Link relocation: `#tab:clusters` → `main.tex#L146` (existing project target or original TeX label line).
