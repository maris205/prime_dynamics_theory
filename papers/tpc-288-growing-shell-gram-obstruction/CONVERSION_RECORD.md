# TPC-288 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `c9f2a3559e421cb10eaf51c1268a03b838c5ed68`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `b3388ea64ffcd995992a5c56396ef66d5c0a4363d5c8d85499bb2d096203e3ea`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `7dbc958f5357e30ea0312beb9c14721b439d9622e3a546fc52658f17b95b808c`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `0bd3f34243e66ffb258a1fb4805728cf39771d6d3a7933b98ae12d951757c364`; 7 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `73f03a38666c5d52777dd7f6704171e1e36bd21e4de01cc8c15030ac458cabd9`.
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
| `Question and scope` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `The literal physical components` | 86 | 2 | `HEADING_TEXT_MATCH` |
| `Exact identities and the spectral object` | 137 | 2 | `HEADING_TEXT_MATCH` |
| `Finite growth and control design` | 223 | 3 | `HEADING_TEXT_MATCH` |
| `Certificate construction` | 258 | 4 | `HEADING_TEXT_MATCH` |
| `Results` | 297 | 4 | `HEADING_TEXT_MATCH` |
| `What full rank does and does not say` | 362 | 5 | `HEADING_TEXT_MATCH` |
| `The obstruction and the route consequence` | 382 | 6 | `HEADING_TEXT_MATCH` |
| `Verification and claim firewall` | 411 | 6 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 448 | 1, 6 | `UNMAPPED_OR_AMBIGUOUS` |
| `Reproduction record` | 464 | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `References (external bibliography)` | 487 | 7 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `109` before writing and `109` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `19`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `204ff4080255d7d76ff4aa8dd0e71c5964ccb17187c491a1f5f7964271278a27`.
- Source theorem/proof environment starts: remark at TeX line 130, theorem at TeX line 139, proof at TeX line 149, lemma at TeX line 164, proof at TeX line 176, proposition at TeX line 199, proof at TeX line 207.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 89–94 | `6c3be08277f10a80b64c26e3e6f87d0e0e5c289b729e0d7360fff141c70adcab` |
| D02 | equation | 96–99 | `73d23ef40566374cb119cd4c81077599bc37816d2d25c7615e4fe95a7ee02246` |
| D03 | equation | 101–104 | `6b98651d77ff05549510e6018359e0c53de272dc461d04b27fd0a38c78d42de5` |
| D04 | equation | 107–111 | `20fd7322f741eff1559d0c044dc3a6e13ae1011d5eedeab3f54ac0e0274b5d7f` |
| D05 | equation | 113–117 | `2762cf2f5cc84db0b99ad556ebb1543d936fa9afc1a12a1a383dfed7f6009146` |
| D06 | equation | 121–126 | `bd01bea857a085ed257aba66ec27235972d2c9c5e6e263dfc68c6c9d9a6d5d7b` |
| D07 | equation | 141–146 | `1900002cd156d5a4cbefcb467e78571774e2d1a5c8f66c7198bfef3a619298d7` |
| D08 | equation | 158–162 | `9b27ac71083b48aff31f783c3888c8a2145bf0a5124f41087d8022db9ed58a48` |
| D09 | equation | 167–173 | `bb3d08c5602e4c2ac384c193121b20e73f0cabaa2abe658e6c8930546f2c9551` |
| D10 | equation* | 178–181 | `c124d01cf48be0dd148e83c068c7d9885e937bb83ccb2b3d9434457f4ca44e16` |
| D11 | equation | 189–194 | `cfa58d98b9a95f8588b1fc33c9f8bb5c0964d5e990c358082369b5df7934e830` |
| D12 | equation | 215–218 | `0b0996b82c5997eecf3caaf51dfa27ba25e321d67f019c0b8c7a7e9796850b95` |
| D13 | align | 264–269 | `a1770402b64ee5e27b43d694ad94de1017be41c2a5c98c4fe032d430aac67e47` |
| D14 | equation | 271–277 | `b213bacb54297b1653b4d92a983d3a83a7ba85a0c0e7e122cb17fb8e0dd8569a` |
| D15 | equation | 279–282 | `0a57b04ab32382128b5260d353c3d03e1e09de48d023f5521bbb920ccc7dffc8` |
| D16 | equation | 286–290 | `4ce18257ce51f9dda0926c3fe5a9eaf85026ec21c8739e78b50cad3a0a3efdc6` |
| D17 | equation* | 325–328 | `fe97adf76b182dee6f25c9c33ead2069e127a86727d4d5f17faefd71e5d8c374` |
| D18 | equation* | 375–378 | `db283bed44ac8305a60e030b53f991acc60da5b5bddd91f53d4a2aa77f97b093` |
| D19 | equation | 385–388 | `c424960b6512f50314b87757c0df4b203de7606471bec79dff457f71f294057a` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 21: `A Finite Gram and Full-Rank Obstruction}`
- TeX line 31: `The preceding finite prime-shell ledger found substantial cancellation after`
- TeX line 37: `Finite regrouping, the Gram energy identity, and positive semidefiniteness`
- TeX line 44: `be promoted to physical $L^2$ decay.  The result is a finite obstruction and`
- TeX line 61: `On the same literal operator, does finite shell growth turn scalar`
- TeX line 72: `\item exact finite identities for shell regrouping, scalar attachment,`
- TeX line 74: `\item a two-axis finite probe: a scale/shell path reaching 17 prime`
- TeX line 78: `\item a finite scalar--energy obstruction in 13 rows, with exact rational`
- TeX line 82: `The paper is deliberately classified as a finite Route-B structural audit.`
- TeX line 83: `The words ''full rank'' and ''positive spectrum'' refer to the finite objects`
- TeX line 105: `Given a finite shell $\shell$, define the prime component matrix and its`
- TeX line 118: `The finite shell used in a row is $\shell_Q=\{q:Q<q\leq2Q,\ q$ prime$\}$.`
- TeX line 139: `\begin{theorem}[finite shell and attachment additivity]`
- TeX line 140: `For every finite shell $\shell$ and source vector $\beta$,`
- TeX line 150: `The first identity is the definition of the finite aggregate.  Multiplying`
- TeX line 153: `the second identity gives the third.  No limiting or infinite rearrangement`
- TeX line 165: `The matrix $G$ is real symmetric positive semidefinite.  If $\one_{\shell}$`
- TeX line 182: `This proves positive semidefiniteness and symmetry.  The trace is the sum of`
- TeX line 199: `\begin{proposition}[finite modular spectral witness]`
- TeX line 203: `positive semidefinite and has full modular rank, all of its real eigenvalues`
- TeX line 210: `A full-rank real positive semidefinite matrix has no zero eigenvalue, so all`
- TeX line 223: `\section{Finite growth and control design}`
- TeX line 251: `The $R_C^+$ column is an interval upper bound, not a floating-point estimate`
- TeX line 283: `Thus $R_C^+<1/10$ is a finite certified cancellation event.`
- TeX line 292: `modulo $p=1\,000\,000\,007$ and row-reduced.  On the finite grid all`
- TeX line 299: `The full finite audit is summarized in Table~\ref{tab:summary}.`
- TeX line 304: `\caption{TPC-288 finite certificate summary.}`
- TeX line 312: `Strictly positive finite Gram spectra & 34 & 34\\`
- TeX line 362: `\subsection{What full rank does and does not say}`
- TeX line 364: `The modular witnesses show that all 34 finite output Grams have rational rank`
- TeX line 366: `finite Gram spectrum.  The six aggregate matrix witnesses show the analogous`
- TeX line 371: `They do not imply a lower bound uniform in $N$ or $Q$, and they do not imply`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:A` → `main.tex#L110` (existing project target or original TeX label line).
- Link relocation: `#eq:L` → `main.tex#L125` (existing project target or original TeX label line).
- Link relocation: `#eq:add` → `main.tex#L145` (existing project target or original TeX label line).
- Link relocation: `#eq:energy` → `main.tex#L172` (existing project target or original TeX label line).
- Link relocation: `#eq:energy` → `main.tex#L172` (existing project target or original TeX label line).
- Link relocation: `#tab:path` → `main.tex#L234` (existing project target or original TeX label line).
- Link relocation: `#tab:summary` → `main.tex#L305` (existing project target or original TeX label line).
