# TPC-261 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `bdc7bb8c00508788363faa2db8691f1128ab3d3e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `d1b1b2c273a36631d8df9adbf740bd64a58e0fd016e9ef4fdb720deb988f6b19`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `8ce652fc1eac4b7423162e206636eeaa52abb8291d48aee83413fce4a1ef63c6`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `3a94a25c98555ef757e6eaf5e3f5fdf6655c38353cccb34c3159cded207e8138`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC260_264.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Scope and motivation` | 48 | 1 | `HEADING_TEXT_MATCH` |
| `Endpoint normalization` | 78 | 2 | `HEADING_TEXT_MATCH` |
| `The strict budget compiler` | 111 | 2 | `HEADING_TEXT_MATCH` |
| `The logarithmic firewall` | 174 | 3 | `HEADING_TEXT_MATCH` |
| `A scaled four-packet obstruction` | 200 | 3 | `HEADING_TEXT_MATCH` |
| `Current route and the minimum sufficient theorem` | 251 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 292 | 5 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 307 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `95` before writing and `95` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a9b5d675f7f3ee454553b59ca4dae7681935fc6aaa38ab3016210b2ca2affdb9`.
- Source theorem/proof environment starts: definition at TeX line 101, theorem at TeX line 113, proof at TeX line 131, theorem at TeX line 176, proof at TeX line 186, theorem at TeX line 213, proof at TeX line 226, corollary at TeX line 261.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 81–85 | `467b21a812a5a2738400281711dd1776f37aa801f4f60f6f1cd1bf2db35f5f22` |
| D02 | equation | 87–90 | `677488da315d2d2a883923d7c8a3f66b73009100a6dfb8a633183079bc37c379` |
| D03 | equation | 104–108 | `b4106c1eb9aca9a69267ba06b62121f552c8fb1b1823554b69c17231b4300806` |
| D04 | equation | 117–121 | `669c3427b2c59afc99d5e6af46848b0dbab49648fd913950ef020eda0ccd6ee9` |
| D05 | equation | 123–126 | `28310d244ff1f8063bf2ea50a4832974450f9086b32cb22c5ae14eb73584afe8` |
| D06 | align* | 134–139 | `7e8f9b5517816079ce08e1da70daf83580094d912682a0e0ec1d04417fc0ac42` |
| D07 | equation | 178–181 | `b2c662a0a006ed2016f481c229dd7b9a4ce3781c7f83a077f032ab4f7ac25dfe` |
| D08 | equation | 206–211 | `b7ea3c92478e0579c5f198f54762931318323e37fa2fbf7eda483189295ceff1` |
| D09 | equation | 217–221 | `3fb3040315eab3475cb126020d5bc6c1dbb966d028ace9e7fee13e622077842b` |
| D10 | equation | 241–246 | `27ab1b11911299245ea06f6daf5d271d242925956069c117d7ebc426363efedd` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 35: `endpoint arithmetic into an exact finite-lane budget.  The current baseline is`
- TeX line 38: `$\lambda_j$, the effective credit is $\sigma_j=\delta_j-\lambda_j$ and a finite`
- TeX line 43: `full energies $16x^{5/3}$ and $0$.  This is a structural synthetic obstruction,`
- TeX line 44: `not a prime-shell counterexample: the literal mode-zero or signed cross-Gram`
- TeX line 45: `estimate remains open.`
- TeX line 69: `\item a strict finite-lane endpoint compiler with a sharp $1/400$ threshold;`
- TeX line 96: `Let $\mathcal L$ be a finite set of lanes.  A lane may represent a packet,`
- TeX line 113: `\begin{theorem}[finite-lane endpoint compiler]`
- TeX line 114: `Let $\mathcal L$ be finite and nonempty.  Suppose that for every $j\in\mathcal L$`
- TeX line 128: `if $\sigma<\Delta_*$, the power ledger does not close.`
- TeX line 140: `Thus every term in the finite sum is $O(x^{E_*-\eta/2})$, and the sum has the`
- TeX line 146: `The theorem is a compiler, not an estimate of any particular lane.  Its main`
- TeX line 171: `$1/48-1/400=11/600$, but it is not a global credit until a transfer theorem`
- TeX line 190: `choose an $\varepsilon<\delta$ and obtain a uniform comparison with`
- TeX line 198: `and it does not estimate the orthogonal residual left by TPC-259.`
- TeX line 235: `The witness is the TPC-260 finite construction with its amplitude scaled to the`
- TeX line 236: `baseline exponent.  It is a structural synthetic family, not a sequence of`
- TeX line 238: `statement, not a proof that the literal route is impossible.`
- TeX line 256: `marginals.  These facts are compatible: a local gap is not a global saving, and`
- TeX line 265: `normalization losses, is sufficient to close the finite-lane endpoint compiler.`
- TeX line 284: `Scaled witness & exact structural synthetic certificate\\`
- TeX line 285: `Literal mode-zero estimate & open\\`
- TeX line 286: `Arithmetic $L^2$ / full Gate B & none / open\\`
- TeX line 296: `credit, not an isolated logarithm or a local exponent.  The scaled TPC-260`
- TeX line 301: `conclusion remain open.`
- TeX line 304: `a stress audit.  They verify the finite algebra and claim firewall only; no`
- TeX line 305: `finite computation is treated as asymptotic evidence.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:logpower` → `main.tex#L180` (existing project target or original TeX label line).
- Link relocation: `#eq:logpower` → `main.tex#L180` (existing project target or original TeX label line).
- Link relocation: `#eq:scaled` → `main.tex#L210` (existing project target or original TeX label line).
- Link relocation: `#eq:scaled-energy` → `main.tex#L220` (existing project target or original TeX label line).
