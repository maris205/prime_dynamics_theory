# TPC-213 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `76f28d5036db2c51c4e58ec0e626e3528f1701149b9f20196043eaf2834683ec`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `2baf751079ef2e6ecadb6b27c5b4a38b3209a978276ac597c74372c227cd3ed4`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `cd08c66735932dc3e49b9175fffa7ded60fd0c62f5bbf25b862f71d8ac94eda2`; 6 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `fd5e413a64ce58f6f568c647dd8899e3a93a4a412eb459845f9b181ca0790f21`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC210_214.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | 67 | 1 | `HEADING_TEXT_MATCH` |
| `The common-source physical operator` | 122 | 2 | `HEADING_TEXT_MATCH` |
| `Residue lifts and transforms` | 124 | 2 | `HEADING_TEXT_MATCH` |
| `The residue-lift cross blocks` | 206 | 3 | `HEADING_TEXT_MATCH` |
| `The emitter pullback Gram` | 246 | 4 | `HEADING_TEXT_MATCH` |
| `Exact finite certificate` | 314 | 4 | `HEADING_TEXT_MATCH` |
| `Fixture and checks` | 316 | 4 | `HEADING_TEXT_MATCH` |
| `Interpretation` | 382 | 5 | `HEADING_TEXT_MATCH` |
| `Route evaluation and limitations` | 393 | 5 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 429 | 6 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 445 | 6 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `121` before writing and `121` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `15`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b3ada1615055b809d60754cce39aec4efe2d26d162318d6f1d193f6fe8be1d3f`.
- Source theorem/proof environment starts: theorem at TeX line 163, proof at TeX line 180, remark at TeX line 199, proposition at TeX line 211, proof at TeX line 223, corollary at TeX line 232, theorem at TeX line 251, proof at TeX line 263, theorem at TeX line 270, proof at TeX line 283, corollary at TeX line 292, proof at TeX line 300, remark at TeX line 307.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 72–77 | `eceeaa6afa92c07314a9a24e6ceae8b8dcdcfced26d4809f16d0cd417b37fafa` |
| D02 | equation | 79–85 | `cfe0c51d35c9f05ea3c8ca0a77b246c1d35555ba19dd0518779c1f7f28731d64` |
| D03 | equation | 128–132 | `af1f96ead6e1ada3fb83580eb17edc98f5a4f36c8217c4d38ebea41d9b770df7` |
| D04 | equation | 134–138 | `1933d7981df8f76e6b3472ba6e381bc7f9f205eb94a5d2d107bc3c3f390dc0ee` |
| D05 | equation | 144–148 | `e6e8529f5e0474fdaf109bb8eeeef56808cbf48eb3abcf9c8be0de7679fa4eca` |
| D06 | equation | 156–159 | `9590bed587e36b46c76ba6a4246332d41439d11b7c09c38cf15db8c2ba0629eb` |
| D07 | equation | 167–172 | `fe191353de3057d47886e99824e17c2c4cb608b64f314e32c3770e2ee372f179` |
| D08 | equation | 174–177 | `33eeb330e3fe88447d491aab57dfbae613a3655fe1c675b4b3b6ed98a6deab98` |
| D09 | align* | 182–186 | `4c25b661c44cfaf2e3cc97be242433f69d9f47d4d1b80b5baa83fcc25cc20cfa` |
| D10 | equation* | 189–194 | `87af01722ac99e22f5c97381537184286da737c5ad3357b86b35de46afb5da30` |
| D11 | equation | 215–220 | `7ce798521bbf6498f472e88b5307db4ee743f5cf2ade7eadedc87b5dfe6b021e` |
| D12 | equation | 254–260 | `e0a2dd8a998f5a42bb9c1367ebef225df113e2de8705ccfe443df6f44dcc5470` |
| D13 | equation | 273–278 | `f21010d2fab4583aa6be05db13c61e0192db3edb2f4491511efc34bc35c1f3ea` |
| D14 | \[...\] | 319–321 | `259fb63ddc7ac97ba42b71b40fffcd96627d09cf2eb09f478c709f4f8062bb75` |
| D15 | equation | 374–378 | `5cfcd68315fe3c8853b442162edc95d5cf4f88e2db98d31be96381cb9fedbaef` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 49: `finite coupling map.  A residue lift sends a common source on a finite support`
- TeX line 60: `Gate B, and arithmetic $L^2$ credit remain open.`
- TeX line 65: `No arithmetic advance, fixed-atom credit, or strict $1/400$ payment is claimed.`
- TeX line 92: `obstruction, but it deliberately leaves open whether the literal residuals`
- TeX line 102: `This paper answers that operator question.  Let $\UU$ be a finite set of`
- TeX line 106: `pulled-back kernels, not an orthogonal sum.  The cross-divisor Gram is governed`
- TeX line 109: `The results are structural and finite.  They make no claim about the shifted`
- TeX line 118: `\item a finite certificate showing nonzero nested-divisor cross terms and`
- TeX line 126: `Let $\Dd$ be a finite family of positive moduli and let $\UU$ be a finite set`
- TeX line 142: `For each $d\in\Dd$, let $A_d(r)$ be any finite complex emitter row and define`
- TeX line 150: `assumed in the following identities.`
- TeX line 165: `For finite $\UU$, $\Dd$, source $v$, corrections $b_d$, and emitter rows`
- TeX line 188: `All sums are finite, so interchanging their order gives`
- TeX line 201: `finite analogue of the V46 $\Delta_{d,z}$ correction and cannot be silently`
- TeX line 241: `residue lifts to one common sequence.  In a finite family containing a maximal`
- TeX line 251: `\begin{theorem}[finite-interval pullback Gram]`
- TeX line 253: `For any finite support $\UU$ and any $d,e\in\Dd$,`
- TeX line 265: `$K_e$.  The resulting sum is finite, so the order of summation may be`
- TeX line 266: `interchanged.  The inner sum is precisely the finite exponential sum displayed`
- TeX line 307: `\begin{remark}[what the theorem does not say]`
- TeX line 314: `\section{Exact finite certificate}`
- TeX line 324: `divisor, and the finite corridor satisfies $2|m|<d$ on all nonempty rows.`
- TeX line 325: `The profile correction is the literal finite product difference`
- TeX line 329: `zero frequency occupancy $0$ because the finite corridor excludes $|m|\geq d$.`
- TeX line 348: `$47-35=12$ linear dependencies.  This is a finite rank statement, not a`
- TeX line 380: `including rational $\ell^2$ norms, and does not use floating-point comparison.`
- TeX line 384: `The fixture supplies the missing interface theorem at the finite algebraic`
- TeX line 396: `carrier, not a dynamical spectral family.  On Route B, the structural threshold`
- TeX line 404: `frequency-intersection Gram & \texttt{PROVED\_EXACT\_FINITE} \\`
- TeX line 406: `literal V46 asymptotic Gram bound & \texttt{OPEN} \\`
- TeX line 407: `prime-shell reassembly & \texttt{OPEN} \\`
- TeX line 415: `$\psi=1$ and omits the logarithmic scalar in order to keep the finite Gram`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:emitter` → `main.tex#L84` (existing project target or original TeX label line).
- Link relocation: `#eq:residual-vector` → `main.tex#L158` (existing project target or original TeX label line).
- Link relocation: `#eq:dft` → `main.tex#L137` (existing project target or original TeX label line).
- Link relocation: `#eq:pullback-identity` → `main.tex#L171` (existing project target or original TeX label line).
- Link relocation: `#eq:pullback-identity` → `main.tex#L171` (existing project target or original TeX label line).
- Link relocation: `#eq:crt-cross` → `main.tex#L219` (existing project target or original TeX label line).
- Link relocation: `#eq:pullback-kernel` → `main.tex#L147` (existing project target or original TeX label line).
- Link relocation: `#eq:general-gram` → `main.tex#L259` (existing project target or original TeX label line).
- Link relocation: `#eq:general-gram` → `main.tex#L259` (existing project target or original TeX label line).
- Link relocation: `#eq:general-gram` → `main.tex#L259` (existing project target or original TeX label line).
- Link relocation: `#eq:frequency-gram` → `main.tex#L277` (existing project target or original TeX label line).
- Link relocation: `#thm:frequency-gram` → `main.tex#L271` (existing project target or original TeX label line).
- Link relocation: `#tab:emitter` → `main.tex#L333` (existing project target or original TeX label line).
- Link relocation: `#thm:frequency-gram` → `main.tex#L271` (existing project target or original TeX label line).
- Link relocation: `#thm:general-gram` → `main.tex#L252` (existing project target or original TeX label line).
- Link relocation: `#eq:pullback-identity` → `main.tex#L171` (existing project target or original TeX label line).
