# TPC-355 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `f220b9b21b044fb1ca15e16d98c4ca4b39d0898a1379f6179db6bbf7735bdb5c`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `0978499b12e6247e05c69e58bd59fe78ffcc337a44c466d060095683f8c851d6`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2b6b4d6d528bb408aa2a6023dcc78b894d8eb93e3a669493d68fce37d6f0c699`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 39 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator and normalization` | 55 | 1 | `HEADING_TEXT_MATCH` |
| `Exact finite identities` | 86 | 2 | `HEADING_TEXT_MATCH` |
| `Frozen protocol and audit` | 109 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 147 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and route status` | 214 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 240 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 252 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `57` before writing and `57` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `2e350272d34487bacd1b53af1a1be00221c4f1cbff8d4d8fae6a77b3a7173e06`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 60–65 | `641f59f0474a9729621ff11fbc44e9a41c788e9498043c6bff9e79b5e782dc90` |
| D02 | equation | 67–70 | `e6dd5d4038076fe4ff96c916b59c6e5dfc26b6c3f97aae0eec1cf4cd0cfa6ab0` |
| D03 | equation | 74–79 | `848f44d0c7ae82d52ee88c293f8d5249b82a698777e12134de64e8283cc6d8c2` |
| D04 | equation | 89–92 | `e0fa02a04b947429ab8f58127a3ff7b1f49ef2f1b6da2e9b9930fd602679f9d5` |
| D05 | equation | 94–98 | `0a7692d9933d5d592fc086e00997e8a99d2ceaa9592867f7d300614074794571` |
| D06 | equation | 100–105 | `889daddc0740b6c75f71f75d3867ee3136bf3620e4a2b8bff1e2469ab1bb8ebc` |
| D07 | \[...\] | 170–173 | `136691cfe74538e95c4a74dc4ad12aa692f44003e02a3fcabb557910615960ed` |
| D08 | \[...\] | 175–178 | `87994dc58b2140cbade499d6c803d3ecb7604482c7394da8ba1e8ce6bc7c685e` |
| D09 | \[...\] | 180–183 | `c8d23bbb70979cedc401cc616a4e5266ea5358357a096e57d63a50c99a090770` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 7: `\title{Position-Aware Mask-Energy Normalization for a Finite\`
- TeX line 23: `The preceding finite source/operator audit transferred positive operator`
- TeX line 32: `normalization, a finite reduction fraction of $0.3775498289$.  The repair is`
- TeX line 33: `not uniform: the all-plus mean drop becomes larger, and a fresh mod-4 row is`
- TeX line 34: `still negatively aligned.  We therefore record a finite partial repair and a`
- TeX line 35: `sharp obstruction, not an asymptotic arithmetic estimate or a twin-prime`
- TeX line 41: `TPC-353 attached the finite V59 residual`
- TeX line 51: `classified as either an exact finite identity, a declared finite model`
- TeX line 52: `statement, or a numerically certified finite observation.  No statement here`
- TeX line 55: `\section{Finite operator and normalization}`
- TeX line 57: `Let $I$ be a finite integer interval and let`
- TeX line 81: `independent of $e$, and it also does not use $\Lambda$, $b$, $\beta$, or an`
- TeX line 83: `defined.  It is a finite preconditioner, not a claimed uniformly bounded`
- TeX line 86: `\section{Exact finite identities}`
- TeX line 88: `For either $T=A_e$ or $T=A_e^\sharp$ and $\beta=L-b$, finite bilinearity gives`
- TeX line 99: `we have the exact finite relation $R_T=1-\kappa_T$.  Cauchy--Schwarz gives`
- TeX line 106: `The diagonal congruence changes the finite geometry on which these identities`
- TeX line 107: `are evaluated; it does not change their logical status.`
- TeX line 138: `648 rows in total.  The producer uses the finite V59 midpoint convention and`
- TeX line 140: `source and accumulates shells in reverse order; it does not import the`
- TeX line 150: `reduces the low-to-higher minimum drop, but does not reduce the corresponding`
- TeX line 186: `for a finite partial stabilization of the minimum, not a uniform lower-floor`
- TeX line 217: `inserted between a literal masked operator and the finite polarization`
- TeX line 218: `interface.  It makes the location of the finite obstruction more explicit:`
- TeX line 224: `\item the geometry diagonal and diagonal congruence are exact finite declared`
- TeX line 226: `\item polarization and its Cauchy envelope hold exactly for both finite`
- TeX line 230: `\item the all-plus minimum-floor reduction is a finite partial repair, while`
- TeX line 231: `mean repair and law-uniform alignment are scoped refuted.`
- TeX line 234: `No source-uniform arithmetic $L^2$ estimate, growing geometry bound,`
- TeX line 247: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE\_POSITION\_AWARE\_MASK\_ENERGY\_NORMALIZATION\_AUDIT}.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#eq:block` → `main.tex#L64` (existing project target or original TeX label line).
- Link relocation: `#tab:protocol` → `main.tex#L119` (existing project target or original TeX label line).
- Link relocation: `#tab:floor` → `main.tex#L156` (existing project target or original TeX label line).
