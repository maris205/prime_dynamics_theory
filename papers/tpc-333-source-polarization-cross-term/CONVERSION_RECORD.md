# TPC-333 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ba1fb3efe59e51e62f64f4dcb607bd390b4b4062`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `6f30022aef04cb077816dac2043991e46291017c011a556cc0452dd00bfd05cd`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `26151898fe19ac90e4d68a83b2386cc44c50bff495e31d2580f42b1192c7c3cb`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `835f3f8057ae62881605c06f55ec6d0ab5c3ac65831044e8e047acd347e2a608`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8c422a215253767e6c0e9801421704851f7be15316ceea1375c5d1ed7484db9f`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC330_334.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Motivation and claim boundary` | 38 | 1 | `HEADING_TEXT_MATCH` |
| `Finite source model` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `Polarization ledger` | 86 | 2 | `HEADING_TEXT_MATCH` |
| `Protocol and exact anchor` | 110 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 137 | 2 | `HEADING_TEXT_MATCH` |
| `What the ledger does and does not prove` | 181 | 3 | `HEADING_TEXT_MATCH` |
| `Next question` | 213 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 223 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `40` before writing and `40` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `11`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `309f113e8d977a62839a9b5f7309b27351bac16d77a8da9d2ed01d9f4f99ae08`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 25–27 | `d9d6eb5a83d7d9e6310eb4c5fe15010029e9ce77373528009ca88c40dee12072` |
| D02 | \[...\] | 67–69 | `ef00deb1077ad608cf8719ca830a5278889cb260b18a0c1c71d2acd970398f30` |
| D03 | equation | 71–75 | `1274a6bc2ab4c256fd7a4c6e2c92dc0857139ab2feabcc9ab454e9ccfb68e590` |
| D04 | equation | 90–93 | `0d722a5bc5c2f8c68304b758845ec577dc38bed5b456eda1d6ee58751f015a54` |
| D05 | \[...\] | 95–99 | `0b5882cb0dbbdb3753ae29f1041ecc60c4fd97a58d2a25dfb292aa590e7780d2` |
| D06 | equation | 101–105 | `e7ab328a82899ac806a989e20af6a5d18b43ae501f7f78d003ad95068895febd` |
| D07 | \[...\] | 123–126 | `ff6cfa9ec910ef7e56d57b387f68884ef07568830a8a92be4eabd08ba5035746` |
| D08 | \[...\] | 128–132 | `71fc7f206fbc2203d16ba850d3c190612eca3832ef37130ba953314b8bf04cb6` |
| D09 | \[...\] | 162–165 | `e93d73c34348443443f4d61e83dd6032e7c67a92e0614de6d506fd157803c5cb` |
| D10 | \[...\] | 167–170 | `758c226e7cb15d184c4af02cd225f7a2fc9266b713eba04842d81c811c4ebbcf` |
| D11 | \[...\] | 203–208 | `149cbffc2de2ddc69adfc9b91dce5e6d9e2c1db863debeaba5777340e9588053` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 12: `\large in a Finite Twin-Prime Signed-Gram Model}`
- TeX line 33: `finite panel.  An independent reverse-factorization replay and mutation`
- TeX line 34: `stress suite verify the ledger.  This is a finite source diagnostic, not a`
- TeX line 35: `source-uniform estimate, power saving, or twin-prime theorem.`
- TeX line 40: `The session's dynamical twin-prime route uses a finite source vector of the`
- TeX line 49: `the polarization identity on a new finite source ensemble and test two`
- TeX line 58: `The finite data reject both readings only for the declared windows and model;`
- TeX line 64: `\section{Finite source model}`
- TeX line 70: `The source is the parent-locked finite model`
- TeX line 76: `Here $\Lambda(p^k)=\log p$ and is zero away from prime powers.  The finite`
- TeX line 81: `The symbols in \eqref{eq:source} are therefore a declared finite numerical`
- TeX line 82: `model, not an assertion that a truncated comparison is an exact global`
- TeX line 88: `For finite real vectors $a,b$, symmetry and bilinearity of the Euclidean`
- TeX line 107: `positive-definite correlation coefficient and need not lie in $[0,1]$ in an`
- TeX line 108: `arbitrary model; the interval observed here is a finite result.`
- TeX line 117: `reverse order for the finite tail product.  It does not import the producer's`
- TeX line 134: `anchor proves the finite algebra and does not pretend to be a prime-density`
- TeX line 171: `These numbers describe finite-dimensional inclusions, not a convergence`
- TeX line 181: `\section{What the ledger does and does not prove}`
- TeX line 186: `obstruction is equally clear: finite source polarization is in a mixed`
- TeX line 188: `replacement for a future uniform estimate.`
- TeX line 192: `\item \texttt{PROVED\_EXACT\_FINITE}: \eqref{eq:polarization} and`
- TeX line 194: `\item \texttt{NUMERICALLY\_CERTIFIED\_FINITE}: six rows, four scale pairs,`
- TeX line 197: `finite panel;`
- TeX line 198: `\item \texttt{OPEN}: a source-uniform arithmetic $L^2$ bound, support`
- TeX line 206: `\texttt{FULL\_GATE\_B=OPEN},\qquad`
- TeX line 211: `test, not an official evaluator pass.`
- TeX line 215: `The cross term is substantial, but its numerical value alone does not say`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.

- Link relocation: `#eq:source` → `main.tex#L71` (existing project target or original TeX label line).
- Link relocation: `#eq:polarization` → `main.tex#L90` (existing project target or original TeX label line).
- Link relocation: `#tab:range` → `main.tex#L144` (existing project target or original TeX label line).
- Link relocation: `#eq:polarization` → `main.tex#L90` (existing project target or original TeX label line).
- Link relocation: `#eq:complement` → `main.tex#L101` (existing project target or original TeX label line).
