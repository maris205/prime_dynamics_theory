# TPC-359 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `3b68586a9b683c3578cb5da1806aae2df479c1d605cd5e4deac23a56fb501a7e`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `fd0789aa40d2b726859f8bffba381b3389be4bb1aa47eeba5335a4b775251c99`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `d5d07376dc728bb5d65081c626183cd12c69e0f132f64e74dae91eb0da5c329f`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [notes/route_evaluation.md](notes/route_evaluation.md), [experiments/protocol.md](experiments/protocol.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 37 | 1 | `HEADING_TEXT_MATCH` |
| `Literal operator and frozen selection` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `Finite inequalities` | 84 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 96 | 2 | `HEADING_TEXT_MATCH` |
| `Audits and proof package` | 141 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion and route status` | 157 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `43` before writing and `43` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `49f0453f90913e60750b6d4bbc134b8ecc7b0c833f4fe5f015a7f2389cbe02c8`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 52–57 | `463b07bcd825c9c5f39b96744a93bcec005dffec45306073985fcf5e93307670` |
| D02 | equation | 61–66 | `001f3c9d8c556a336f26f2d4ed6ce839ae0d095144f8c59993787e891a9a011c` |
| D03 | equation | 70–74 | `3e4234be5e7b2b456581183d4db1b2643da273f5a3e2341e06988ca4934f5fa6` |
| D04 | equation | 76–79 | `f40bd62fab0ecc7a5527e2fd68c4f3fb017a0b68c8e787bfed2aac39a8fdb1a6` |
| D05 | equation | 87–91 | `b348dfe88baddfdf6061bb1dde0d075d2117bcbc6cdb90f6b447adecdb1e5f8a` |
| D06 | equation | 120–125 | `b660c86469820ed005753ffdb30adbb10b3b1ab666cb47a906e66e5eda9d8c95` |
| D07 | \[...\] | 133–135 | `d522a37c684215002bd1778e204f059653d552035e50f7c5d50561e416f8c001` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 22: `We perform a hostile finite audit of a position-normalized literal`
- TeX line 29: `maximum is $0.6271657593674812$, both within the preceding finite caps; the`
- TeX line 30: `raw all-plus spectral maximum is $1542.7354827195263$.  This is a new finite`
- TeX line 31: `positive transfer under adversarial geometry selection.  It does not establish`
- TeX line 32: `an origin-uniform or growing bound: the normalized spectral ladder has 12`
- TeX line 33: `increases, 36 decreases, and 6 flats.  No arithmetic or twin-prime conclusion`
- TeX line 39: `The preceding fresh-origin audit transferred a finite normalized operator cap`
- TeX line 42: `The present experiment answers only this finite question.  It does not use the`
- TeX line 43: `V59 source response, does not select a sign law from data, and does not perform`
- TeX line 84: `\section{Finite inequalities}`
- TeX line 86: `For every finite real symmetric matrix $T$,`
- TeX line 92: `These are exact finite inequalities.  Positivity of every declared $G_u$ makes`
- TeX line 93: `the congruence in~\eqref{eq:norm} a well-defined finite real symmetric matrix.`
- TeX line 94: `None of these facts supplies a bound uniform in $x$ or $N$.`
- TeX line 127: `$0.62663944469203836$, respectively.  Thus both finite caps transfer within`
- TeX line 129: `$1542.7354827195263$, showing that the normalized comparison is not a claim`
- TeX line 136: `under guard $10^{-6}$.  In particular, the finite cap is compatible with`
- TeX line 139: `this is a selection diagnostic, not an asymptotic statistic.`
- TeX line 144: `selection ledger, parent locks, finite inequalities, transition census, and a`
- TeX line 153: `The strongest positive statement is therefore a numerically certified finite`
- TeX line 159: `TPC-359 strengthens finite evidence for the normalized operator cap under a`
- TeX line 160: `deliberately hostile geometry-only selection.  It does not pay an arithmetic`
- TeX line 161: `loss, establish source-uniform $L^2$, prove a growing masked-operator bound,`
- TeX line 167: `$\texttt{FULL\_GATE\_B=OPEN}$; the twin-prime result remains none.`

## Conversion limitations

- No PROOF_PACKAGE.md is present; no proof-package review is claimed.

- Link relocation: `#eq:norm` → `main.tex#L65` (existing project target or original TeX label line).
