# TPC-215 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `9873c210d3a4d1fe3b319c304c76bf985de8e1f9ae90d945d040b27aa4874028`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `56d740c2842364aa1fef24eb46ad3f8404d89251e9dfc03768e74fcda065d2bf`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `b8d83a1afdceb6ce505d399b8f0ab98a222131742f7b9c0f98366ee07159da1b`; 8 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `3adca97f3f091d6b8051ff99b2667a75b79d50b22e57a66a91a9e1cbd77945c8`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC215_219.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | 72 | 1 | `HEADING_TEXT_MATCH` |
| `Literal source lock and the emitter` | 116 | 2 | `HEADING_TEXT_MATCH` |
| `Activation and the short quotient` | 170 | 3 | `HEADING_TEXT_MATCH` |
| `A deterministic coefficient majorant` | 239 | 3 | `HEADING_TEXT_MATCH` |
| `From rows to the complete-period Gram` | 318 | 4 | `HEADING_TEXT_MATCH` |
| `A sharp top-shell obstruction` | 408 | 6 | `HEADING_TEXT_MATCH` |
| `Finite exact certificate` | 439 | 6 | `HEADING_TEXT_MATCH` |
| `Route evaluation and open arithmetic` | 506 | 7 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 549 | 7 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 564 | 8 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `166` before writing and `166` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `36`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `fc495f84842e4b14480b0029863a45c901f99eb997be9f714ac85964e5dd043f`.
- Source theorem/proof environment starts: remark at TeX line 163, lemma at TeX line 172, proof at TeX line 183, lemma at TeX line 195, proof at TeX line 213, remark at TeX line 232, lemma at TeX line 249, proof at TeX line 260, corollary at TeX line 287, proof at TeX line 304, lemma at TeX line 328, proof at TeX line 337, theorem at TeX line 368, proof at TeX line 380, remark at TeX line 400, proposition at TeX line 410, proof at TeX line 420.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 77–80 | `051f305bd3e1750759bf9c2530662feb79d07399ea09692212fe97978dea2a4e` |
| D02 | equation | 87–90 | `5c0985f3eb1dc1df178c4300aa3daa8ef72ef47da50a876d6c5b3154080a8b50` |
| D03 | equation | 120–125 | `08c36185328f2a1c21047f5597362d416eb429cdd7de71225ecae50daefc1779` |
| D04 | equation | 127–131 | `efd28c00303383e4a09fb78dbcb061bffa8d1c277ea2915e1f3648b17b59a18e` |
| D05 | equation | 133–136 | `9a168b6682ed1cceccd761ee4806c6c6858cf4125194e47adf272215f2e5e5f3` |
| D06 | equation | 142–149 | `5732d45a649c04e4f16580bc5ebd898ef2a0c7fff655c614a773fdf8179abcc6` |
| D07 | equation | 154–158 | `6c945fbb412cc4554442c85d70cab345eb511d9322a1ef67f2f8b22fe7bf1d0e` |
| D08 | equation | 175–179 | `3e1f709c04ff5ac70dfe79f7635fe9bf145727a79d3a1ba0f428595178278c82` |
| D09 | \[...\] | 186–188 | `7f62fbea2c597017fd6a04318272c88b04410f7111d10d1189b33a55bcabf9a5` |
| D10 | equation | 198–203 | `f6e41cc20231e8c3ca4715bd2d6d18456e8a39038034e4b5963dfe8dd1ea535b` |
| D11 | equation | 205–210 | `0dfa702bb5c1499c80bd13a80ad1972556346a78efabe349424b42fb40e3de2c` |
| D12 | \[...\] | 220–222 | `0a48cd552957ceb7bda7a17c8de8414483a47e2a516a2c0e34ad25a45034e60b` |
| D13 | \[...\] | 224–228 | `40f6af953d6548de57847c03d2db749ca6a41b2ea5063da4227263808fcde9e6` |
| D14 | equation | 242–245 | `9b9d995991797a62066d381435adcd0c8ac89e746235008006905eaa1ebdb89f` |
| D15 | equation | 252–257 | `acf46da88d09ae49cb26078ae0d896e242ed59bc6202d20499bd1a92edc28f4e` |
| D16 | equation | 262–265 | `d747ff062974189f3b3a5943c7aef0fc4aefa6f48cc9e21f919c873fad7f32ba` |
| D17 | align | 267–275 | `11300c1506de0dca370b5af7e3c3fd13b453ce56b3d536c5cb5e65b4792be86b` |
| D18 | equation | 281–285 | `b4a2234771a97b328eac23f3e999986bd213f7b6ec756659d63fc4fc4614baeb` |
| D19 | equation | 290–294 | `dfad7d94146b9027ecd59ba51f591aea4672800dcf7c1e03e618558175e2e889` |
| D20 | equation | 296–301 | `5d5723f3c7d47e6d262f6e3265d41a76a03823190b85b04947564bad887b2650` |
| D21 | \[...\] | 311–314 | `d9624665fb7b1adc2dfc0facf4f0d069e11cb3f224c7895a89231ed5005287f2` |
| D22 | equation | 321–324 | `c8e7c36ae1a7fc8e6ecd98295f012c104ed5a569fe233b27b5c4b92a1ef2b9b8` |
| D23 | equation | 331–334 | `e28b478718170ae991bf7fb8be10affe87e4f2911abbbbdfc302389a19148b04` |
| D24 | \[...\] | 339–342 | `4e34cbd8ed8454d72ec57948039fa10811aa779b9ca7efa470eaa1e2f921c0d6` |
| D25 | equation | 351–354 | `da980933b5ecf99effe8765b98245d44cdaacae07d9b4c4023fbe23718711828` |
| D26 | align | 356–366 | `6356f9846b9049142ee4574e944bc21ad00f314d17b1690947b42bc309fc0351` |
| D27 | equation | 371–375 | `f7a7caef1ae0fc3650ffe86501400925d538fba2bb4393a8c98b1d3e3508d4c8` |
| D28 | equation | 382–385 | `12e23fb9c3fd4106112cf85de6ced8f13cc7273fa8c0d62e60ac6466634bfc2e` |
| D29 | align | 388–395 | `a1c49d9565f4d12754dcbc8cd9ea6ab3fff4b8ae65034fe0cfce95de6e224d1c` |
| D30 | equation | 413–417 | `031fe582ebb77766febddd490ffee8e0f6a93599fcf636f71811cfe9c8a3a391` |
| D31 | equation | 429–433 | `bcec20d4a9cb662c6326a794bfac624cb6c1f8b1caee6b9d7da9500fa81cb8c2` |
| D32 | equation | 443–447 | `30be624fe84e7f4a91e5b3aa1316d185c6b8d740f7f31803f742b8630915ac64` |
| D33 | equation | 457–460 | `ba22b52181ab8053c6050753c0045205c4e33f4e0b0d7bbb13daff59590479ec` |
| D34 | equation | 492–497 | `c500add325a4eb08f1e625e50620cc9b5ae46eee5328478558912b6fb9619cc1` |
| D35 | equation | 509–514 | `6821043cb7fbfe234e3f3815305786f6796067ceae8c21177bcf0a6d28e0e32f` |
| D36 | equation* | 534–545 | `b236d79a15a520ab31f52e9aa26c6831d463bb09fd4093dfad5d538abe730184` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 60: `is not a saving theorem: every active denominator in $U/2<h\le U$ has`
- TeX line 62: `energy, finite-window off-frequency Gram, prime-shell reassembly, arithmetic`
- TeX line 63: `$L^2$, and twin-prime endpoint remain open.`
- TeX line 69: `scales.  Finite decimal ratios are numerical observations only.  No`
- TeX line 82: `so different divisor blocks are not an orthogonal direct sum`
- TeX line 280: `Define the source-locked uniform factor`
- TeX line 289: `Uniformly over all active reduced denominators,`
- TeX line 355: `for a finite realization of the transition band, and define`
- TeX line 386: `Corollary~\ref{cor:subpower} and a finite rearrangement of nonnegative terms`
- TeX line 400: `\begin{remark}[what the theorem does and does not remove]`
- TeX line 402: `additional fixed-power cost beyond the divisor direct sum.  It does not bound`
- TeX line 403: `\(\Edir\) at the natural arithmetic scale.  It also does not replace the`
- TeX line 404: `finite physical interval by a complete period: off-frequency terms that`
- TeX line 428: `uniform rowwise estimate of the form`
- TeX line 434: `based only on cluster coefficients.  It does not refute a global saving that`
- TeX line 435: `uses the size or distribution of $N_h$, finite-window oscillation, prime-shell`
- TeX line 439: `\section{Finite exact certificate}`
- TeX line 442: `divisor family to a full finite band:`
- TeX line 448: `The finite band consists of all squarefree $2<d\le35$ coprime to the three`
- TeX line 450: `$U<Q$, makes every finite inverse legal.  All emitter entries and row-norm`
- TeX line 461: `The largest realized quotient is $10$, below the uniform integer bound`
- TeX line 483: `\caption{Finite coefficient diagnostics.  The majorant is deliberately`
- TeX line 491: `by real-logarithm evaluation, the whole finite cluster and direct energies are`
- TeX line 496: `\label{eq:finite-ratio}`
- TeX line 498: `Equation \eqref{eq:finite-ratio} is a reproduction diagnostic, not evidence`
- TeX line 503: `active rows across three finite configurations and verifies that deleting the`
- TeX line 506: `\section{Route evaluation and open arithmetic}`
- TeX line 524: `\item \textbf{Finite physical interval.}  Complete-period orthogonality`
- TeX line 539: `\texttt{UNIFORM\_ROWWISE\_POWER\_SAVING} &=`
- TeX line 558: `top shell simultaneously proves that no uniform rowwise saving can come from`
- TeX line 560: `physical direct-sum row energy before reintroducing finite-window cross`

## Conversion limitations

- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:divisor-band` → `main.tex#L135` (existing project target or original TeX label line).
- Link relocation: `#eq:emitter` → `main.tex#L148` (existing project target or original TeX label line).
- Link relocation: `#eq:activation` → `main.tex#L178` (existing project target or original TeX label line).
- Link relocation: `#eq:activation` → `main.tex#L178` (existing project target or original TeX label line).
- Link relocation: `#eq:cluster-coefficient` → `main.tex#L89` (existing project target or original TeX label line).
- Link relocation: `#eq:normal-form` → `main.tex#L202` (existing project target or original TeX label line).
- Link relocation: `#lem:activation` → `main.tex#L173` (existing project target or original TeX label line).
- Link relocation: `#eq:quotient-bound` → `main.tex#L209` (existing project target or original TeX label line).
- Link relocation: `#lem:activation` → `main.tex#L173` (existing project target or original TeX label line).
- Link relocation: `#eq:triangle` → `main.tex#L274` (existing project target or original TeX label line).
- Link relocation: `#eq:anchor` → `main.tex#L264` (existing project target or original TeX label line).
- Link relocation: `#eq:row-majorant` → `main.tex#L256` (existing project target or original TeX label line).
- Link relocation: `#eq:row-majorant` → `main.tex#L256` (existing project target or original TeX label line).
- Link relocation: `#lem:activation` → `main.tex#L173` (existing project target or original TeX label line).
- Link relocation: `#eq:subpower-coefficient` → `main.tex#L293` (existing project target or original TeX label line).
- Link relocation: `#eq:explicit-Ax` → `main.tex#L300` (existing project target or original TeX label line).
- Link relocation: `#eq:scales` → `main.tex#L124` (existing project target or original TeX label line).
- Link relocation: `#eq:dilation` → `main.tex#L157` (existing project target or original TeX label line).
- Link relocation: `#eq:row-decomposition` → `main.tex#L333` (existing project target or original TeX label line).
- Link relocation: `#eq:Ax` → `main.tex#L284` (existing project target or original TeX label line).
- Link relocation: `#eq:explicit-Ax` → `main.tex#L300` (existing project target or original TeX label line).
- Link relocation: `#cor:subpower` → `main.tex#L288` (existing project target or original TeX label line).
- Link relocation: `#lem:row-decomposition` → `main.tex#L329` (existing project target or original TeX label line).
- Link relocation: `#eq:main` → `main.tex#L374` (existing project target or original TeX label line).
- Link relocation: `#eq:tpc214-factor` → `main.tex#L384` (existing project target or original TeX label line).
- Link relocation: `#lem:activation` → `main.tex#L173` (existing project target or original TeX label line).
- Link relocation: `#eq:cluster-coefficient` → `main.tex#L89` (existing project target or original TeX label line).
- Link relocation: `#eq:direct-mass` → `main.tex#L244` (existing project target or original TeX label line).
- Link relocation: `#prop:top-shell` → `main.tex#L411` (existing project target or original TeX label line).
- Link relocation: `#eq:top-shell` → `main.tex#L416` (existing project target or original TeX label line).
- Link relocation: `#tab:fixture` → `main.tex#L486` (existing project target or original TeX label line).
- Link relocation: `#eq:finite-ratio` → `main.tex#L496` (existing project target or original TeX label line).
- Link relocation: `#eq:route-change` → `main.tex#L513` (existing project target or original TeX label line).
