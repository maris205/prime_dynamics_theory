# TPC-286 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `c9f2a3559e421cb10eaf51c1268a03b838c5ed68`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `8acfd84925fe1b671e5586f4c2b2e03a7b5707066ca49daff139bd8cfe00811e`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `b2382f9a70241ced0f5d3f953c3bbb8c3376d7f73beaf1afbb34edabcd6d255d`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `ad00c667c963df04567d62af741d8f07d536d1186a53a685e3df87fa998c7efe`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8714eb029a07aa2a225f4d762eb62ed1d309d55bcc112b40ab5e06d1bfc9d664`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC285_289.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Motivation and contribution` | 51 | 1 | `HEADING_TEXT_MATCH` |
| `The frozen finite operator` | 83 | 2 | `HEADING_TEXT_MATCH` |
| `Exact diagonal split` | 128 | 2 | `HEADING_TEXT_MATCH` |
| `The registered 72-row ledger` | 183 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and route consequence` | 261 | 4 | `HEADING_TEXT_MATCH` |
| `Verification, limitations, and conclusion` | 290 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility details` | 322 | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `References (external bibliography)` | 354 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `74` before writing and `74` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `16`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `c0b1641fdf21670f2aab10fd6f50be6cead4e8d5de2be08b40ba9624c881c47c`.
- Source theorem/proof environment starts: theorem at TeX line 130, proof at TeX line 151, remark at TeX line 175.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 87–92 | `c39ea12afa4c1a8a50db9bfcc28cbc60f8fdf7564156a931a397a740c9bb50b0` |
| D02 | equation | 94–97 | `438051733b9f837c1a449778fb5b7403dc03f1f5dbe1b78a2e28cf51ca22991d` |
| D03 | equation | 99–102 | `ec9592d833ed627752521114c5d127054e358a39ea5fa07d3f757aaa49d329c1` |
| D04 | align | 105–112 | `97016ceb27a116fb50ae8dffbeaa221091a354bb8e3e6f25cd217ac247f0b29e` |
| D05 | equation | 118–122 | `4c351945f0288acf4d14a211cdef8b88266008a0d931b4ba25a7e5e863015992` |
| D06 | equation | 134–138 | `637ce5e523bfec213c2d6f23c0630ebb3b9e2a0c7ad1696edb0d2d23de1b4b78` |
| D07 | equation | 140–143 | `2fdb4ecbc1665a494f4cbcfdfe6dfdb4271a1e10c73ead7b923deada1fb87e67` |
| D08 | equation | 145–148 | `7dc16f70b83d1fd4fcf54fe897ae5c867fd6d07d74055452a0aa50b3bacb38ae` |
| D09 | equation | 154–158 | `4507cd4b5383cea02a4e849b505d438f9232a440c4c709270ee28355087e51cd` |
| D10 | equation | 162–166 | `cceaf4c445ee10016a535e09e3b33a3054026cb9f1c1937d71c614a28485f78b` |
| D11 | equation | 168–171 | `63574c07d2b9588ade15020938b52eafb47abd0053486cc6fc43b4a4cd1e9c6c` |
| D12 | equation | 186–190 | `1bb78a5bbed186edc676ed53785b831196112b45418ae648a65407f963aa8aaf` |
| D13 | equation | 229–232 | `e6aec195ed7a24b9de0944119b9db7618f0c9e805dc7cb53cd3be89bfed9c20a` |
| D14 | equation | 266–270 | `e4de0e7bc85d8579aaaedfd6fd085c2e9465aae61cf76b883e1edb2556d634cd` |
| D15 | \[...\] | 312–316 | `77381ec8f23bcce7e1ffb311df392290e9dbd00f5e285667ef49e59fe4d625bd` |
| D16 | \[...\] | 327–329 | `f9c46c8fca6dedaa7578a24042472ebc9fa971be5b0d9479a8609599300cf8a1` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 31: `The previous finite control atlas found sign changes in the literal source`
- TeX line 33: `analysis found a tempting low-rank factorization that does not survive the`
- TeX line 35: `finite prime shell we define a diagonal-including output, an explicit`
- TeX line 36: `diagonal correction, and the physical deleted-diagonal output.  A finite-sum`
- TeX line 44: `strictly larger certified absolute magnitude in 21 rows.  These are finite`
- TeX line 54: `finite source profile.  TPC-284 showed that six natural schedule controls can`
- TeX line 55: `change the sign of the resulting scalar attachment on a registered finite`
- TeX line 60: `question: how much of the finite sensitivity is carried by the diagonal term`
- TeX line 63: `This paper answers that question at the level supported by the frozen finite`
- TeX line 71: `the finite route;`
- TeX line 74: `\item a sharpened route obstruction: finite diagonal sensitivity is real,`
- TeX line 75: `but it does not by itself settle growing-scale cancellation.`
- TeX line 83: `\section{The frozen finite operator}`
- TeX line 85: `Let $I$ be a finite interval of integer indices and let $q$ be an odd prime.`
- TeX line 103: `For a finite shell $\mathcal S_Q=\{q:Q<q\leq2Q,\ q\text{ prime}\}$ and a`
- TeX line 113: `The first sum includes the $t=u$ terms; the second one does not.`
- TeX line 115: `The scalar used in the finite certificates is the four-block projected`
- TeX line 131: `For every finite $I$, finite prime shell $\mathcal S_Q$, source vector $\beta$,`
- TeX line 161: `diagonal summand from each finite full sum consequently gives`
- TeX line 172: `All sums are finite, so no convergence or rearrangement theorem is required.`
- TeX line 179: `operator.  It does not say that the diagonal correction dominates for every`
- TeX line 195: `from the finite operator certificate~\cite{tpc268}.`
- TeX line 206: `\caption{TPC-286 finite component census.  Every component interval is`
- TeX line 259: `operator.  The table is descriptive of the registered finite family only.`
- TeX line 271: `The finite ledger shows why this term cannot be silently absorbed into a`
- TeX line 278: `separate it before estimating any norm.  Second, the finite evidence does not`
- TeX line 280: `finite row may cancel across primes, and the 15 sign flips do not constitute a`
- TeX line 286: `of the full-rank physical blocks, or a uniform bound for the explicit diagonal`
- TeX line 303: `finite modeling choice; the interval ledger has no moving-order theorem; the`
- TeX line 304: `diagonal dominance counts have no asymptotic extrapolation; and no arithmetic`
- TeX line 310: `physical prime-shell operators and certifies its finite sensitivity on all 72`
- TeX line 317: `The next open theorem is signed full-shell cancellation after this split.`

## Conversion limitations

- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:full` → `main.tex#L108` (existing project target or original TeX label line).
- Link relocation: `#eq:physical` → `main.tex#L111` (existing project target or original TeX label line).
- Link relocation: `#eq:block` → `main.tex#L91` (existing project target or original TeX label line).
- Link relocation: `#eq:full` → `main.tex#L108` (existing project target or original TeX label line).
- Link relocation: `#eq:diag-output` → `main.tex#L137` (existing project target or original TeX label line).
- Link relocation: `#eq:attachment` → `main.tex#L121` (existing project target or original TeX label line).
- Link relocation: `#tab:census` → `main.tex#L208` (existing project target or original TeX label line).
- Link relocation: `#tab:controls` → `main.tex#L239` (existing project target or original TeX label line).
- Link relocation: `#eq:baselines` → `main.tex#L189` (existing project target or original TeX label line).
