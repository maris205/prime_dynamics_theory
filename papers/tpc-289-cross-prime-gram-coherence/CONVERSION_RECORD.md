# TPC-289 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `c9f2a3559e421cb10eaf51c1268a03b838c5ed68`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `afd690feeb8026ef60dce047997e1b749bb8d9d96a4fc012453298e2badd4fcb`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `cfe1cda5e41742aadd0c24557466bd1c3dd73a28e0ec0722ceccde4af701eedb`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `4a6965c5e2bcb7ad8199dad87c75250912d31220e5e8c7ba9c8c2c2bd55785ca`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `7a07bb709169a78498939beeeeccf9035d543a369814c17cb1822fdf3a28a37d`.
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
| `Position on the route map` | 53 | 1 | `HEADING_TEXT_MATCH` |
| `The frozen physical model` | 69 | 1 | `HEADING_TEXT_MATCH` |
| `Exact coherence structure` | 111 | 2 | `HEADING_TEXT_MATCH` |
| `Finite protocol` | 168 | 3 | `HEADING_TEXT_MATCH` |
| `Results: a finite sign/coherence phase diagram` | 194 | 3 | `HEADING_TEXT_MATCH` |
| `What is and is not established` | 249 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility and claim firewall` | 270 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 290 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `79` before writing and `79` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `15`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `5f8245e33a5bc3d1da3d920178647103a93b15c975fdfd1a3ebb989d925c8940`.
- Source theorem/proof environment starts: lemma at TeX line 113, proof at TeX line 121, proposition at TeX line 131, proof at TeX line 147, remark at TeX line 161.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 74–77 | `531d74da7b4e844abfeb77aeaaeb9b27dddd77946f4f27e21fd6b00e80d81106` |
| D02 | \[...\] | 79–83 | `33f24fb0dec303fcd24fe7c5990dba2cbe94c3f676879966ade0c1bd459a2fc0` |
| D03 | \[...\] | 85–88 | `7d39acba837e27b87a8032f6ad82fdc943b2bf26483b1f7630ef6b3ee7231c56` |
| D04 | \[...\] | 90–93 | `95cfbb434e9dac7ace37cc02784f543ce999c27003a09e3f4ff8ba9c6b7136f6` |
| D05 | \[...\] | 98–100 | `4bf3c16c418635134af613038291ee1c066b4a220cb40363fe70459f46d593d6` |
| D06 | equation | 104–108 | `31f7b6062c71cd35391395d34804957a4ca3df400ad01a4a7b08a73b741be072` |
| D07 | equation | 115–118 | `c5380e824f6634afd8b94b36676de46c9ae3a35559b339873337e83dc9ff391f` |
| D08 | \[...\] | 123–126 | `f335c529c21eda8bdae7c6e19246c32ed1da9832bb425b3fa010cafdb807bd6c` |
| D09 | \[...\] | 134–138 | `40010f55c05676b6cb8564e191d1243082d1aa742babc3256fff1e3a5a4d229a` |
| D10 | equation | 140–144 | `ce64f600ba71e57cde5301e8a1fd5d32c5668409c203537d24c4f9aeac064293` |
| D11 | \[...\] | 150–152 | `1322e681050e6f61856d4d93d0ecfdf11d77c2a06fb61eaf5daed8c2db598ce7` |
| D12 | \[...\] | 155–158 | `205c0109398b871b53ddbcaf44d130ab90c38dbcc6da764eb151c2e89045b23a` |
| D13 | \[...\] | 179–182 | `1ba2d4eca69bcdd8c7f2da30ce902fb7158d9630ac2b8c6e55ae238bc5300517` |
| D14 | \[...\] | 231–233 | `9e81a540b711257b49b3c21af98389be54bcd207a995528c143a6b6e35866525` |
| D15 | \[...\] | 255–258 | `eac8ae184be5fad19f7db582a0e5dcf89593d0042ed4963246af1648452c80ce` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 21: `Twin-Prime Dynamics: A Finite Phase Diagram\\`
- TeX line 33: `The preceding finite shell study found a potentially misleading combination:`
- TeX line 42: `finite scan of 18 rows and 1,380 unordered pairs then separates two regimes.`
- TeX line 45: `$1.37\times 10^{-7}$.  Conversely, eight late-shell rows satisfy the finite`
- TeX line 48: `a finite sign/coherence phase diagram and a precise obstruction to promoting`
- TeX line 49: `late-shell behavior to a uniform growing-shell theorem; it is not an`
- TeX line 57: `the finite physical operator into prime components and documented scalar`
- TeX line 60: `a finite growth/control grid \cite{tpc288}.  Its central warning was that a`
- TeX line 61: `small scalar attachment is not an $L^2$ saving.`
- TeX line 66: `finite.  The distinction between exact identities, finite numerical`
- TeX line 67: `certificates, and open asymptotic gates is maintained throughout.`
- TeX line 89: `For a finite shell $S$ write`
- TeX line 114: `For every finite shell, $G$ is positive semidefinite.  If $d_q,d_r>0$, then`
- TeX line 148: `The positivity assumption selects the positive square-root branch in the`
- TeX line 162: `The proposition is a finite vector lemma, not a claim that its hypotheses`
- TeX line 168: `\section{Finite protocol}`
- TeX line 178: `exact energy ratio in \eqref{eq:energy}.  The finite ''strong block'' test uses`
- TeX line 194: `\section{Results: a finite sign/coherence phase diagram}`
- TeX line 244: `finite certificate also finds two exact groups in which the three cutoff`
- TeX line 246: `this is a warning that these finite controls should not be counted as an`
- TeX line 254: `it refutes the tempting uniform rule`
- TeX line 260: `amplification does not require pairwise positivity either.`
- TeX line 262: `The result is therefore an obstruction paper on the route map, not a proof or`
- TeX line 264: `growing-shell bound, a uniform theorem over literal sources, an arithmetic`
- TeX line 268: `source class admits a uniform coherence estimate.`
- TeX line 279: `FINITE: 17/18 positive rows; 3 negative pairs in one row`
- TeX line 280: `FINITE: 8-row eta=3/5, delta=4/5 strong block; 18/18 R_E > 1`
- TeX line 281: `OPEN: source-restricted/growing-shell coherence and arithmetic L2`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:cauchy` → `main.tex#L117` (existing project target or original TeX label line).
- Link relocation: `#eq:energy` → `main.tex#L107` (existing project target or original TeX label line).
- Link relocation: `#eq:cauchy` → `main.tex#L117` (existing project target or original TeX label line).
- Link relocation: `#eq:energy` → `main.tex#L107` (existing project target or original TeX label line).
- Link relocation: `#tab:representative` → `main.tex#L223` (existing project target or original TeX label line).
- Link relocation: `#eq:hypotheses` → `main.tex#L137` (existing project target or original TeX label line).
