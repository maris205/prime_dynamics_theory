# TPC-259 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `d1683c8f96ae1b86f2f9fcb9ba8318c9e1aaf3f6`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `657c1a3b86ceaf978dd9d40dd6c4d5540da5e27aee745f72bb39fbe7550fef0f`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `978467b31a799d112bb997d99423cbe144319b0b9a65da2f12dac774a34f2a42`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `50dee6b618644829c4b5c17e1f9b7f390021a092848b419c17a319743f051788`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `83ec8d8f3444c0258656c10eefcd0f4428ba01f2793185c5d00a0475ff67651a`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC255_259.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Problem and claim boundary` | 59 | 1 | `HEADING_TEXT_MATCH` |
| `One clock, four blocks, and the frozen null direction` | 83 | 1 | `HEADING_TEXT_MATCH` |
| `Four-block control of the literal hybrid residual` | 152 | 2 | `HEADING_TEXT_MATCH` |
| `Exact signed-coupling split` | 206 | 3 | `HEADING_TEXT_MATCH` |
| `Conditional rate and the residual obstruction` | 266 | 4 | `HEADING_TEXT_MATCH` |
| `Route evaluation` | 314 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility and epistemic labels` | 333 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 349 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `107` before writing and `107` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `32`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `9f25ae0459b5a665baa44cf025f00e542f67b716c9e814694e996bf4e4e32692`.
- Source theorem/proof environment starts: lemma at TeX line 122, proof at TeX line 129, theorem at TeX line 168, proof at TeX line 177, remark at TeX line 200, proposition at TeX line 217, proof at TeX line 227, theorem at TeX line 237, proof at TeX line 247, proposition at TeX line 287, proof at TeX line 297.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 41–43 | `e705e4f259973810978959f172763ac4ccb8d4ed006b3b3c7aecd668c5726763` |
| D02 | \[...\] | 45–49 | `1857f01350a9a2eb0728e85029ba586f9a2b4973d3fcfb9ca06e41875522d054` |
| D03 | equation | 63–65 | `6850fd4dd6cad6e1243e013d74f33576c47c8d368b11ec6264ca93cae5cbe14b` |
| D04 | \[...\] | 77–79 | `853ea63d77d910256d25e6dc32bea4a4f018efe1459a9d49b8d786f49124bec9` |
| D05 | equation | 86–89 | `2f04f5190bb4f93a6dd5edbef45c685f70fad99fa98ec0f45aae283668111a68` |
| D06 | equation | 92–95 | `cc3f456dead01d10c0732d64254dbceb96160903197a216eb027af48f7b72d47` |
| D07 | \[...\] | 100–103 | `0a537e129c816811472970c86d0c09312db5adb599374e8c43068355035e0ce7` |
| D08 | equation | 105–107 | `6f665d98dc630f4f1391060fb1856544460e646f122c8f983d63931d6b00ac02` |
| D09 | equation | 113–116 | `5c3ef35e248c88fe6525a05e813c96b4405b6f83ecd4a5b6507cc56644059c79` |
| D10 | equation | 118–120 | `10d5d04c1a8574e2295ee1606678283bad185c9a505d9cf6be60cc47323fa35b` |
| D11 | \[...\] | 131–133 | `a111aa046c9d52af92de4190806a4ee92393167191bd798237fd206b5cc68015` |
| D12 | equation | 141–143 | `a926a633e8cd1b4a01af191dbc8d21a502eff6666d620d81e65e3ede722fed5d` |
| D13 | equation | 145–147 | `929fe2442b0990f4dad53e2ed0550bc3111f1d61fab1a6851aa930ce27f73913` |
| D14 | equation | 155–158 | `5bedb583f5d6aca09a3434d63110aa8302c89767554e4d91ccf6e5476cbfaffa` |
| D15 | equation | 161–165 | `dc8ad41c9490c7f0f5a2b51ff31c7027207e4d11bfc2be0afc4f6095c048d37b` |
| D16 | equation | 170–173 | `6ae3fa96a5c5b295b0d391b72746563b2233e0b022f30d7baf37d3bd1f6d111d` |
| D17 | equation | 180–182 | `f397db5686012dced313cf4ab225b83f31b033d7d7a6843759188c8f99e0ec36` |
| D18 | \[...\] | 184–188 | `103bdecb0b3a2c2834519a200d1f9de1fd15720834920097f23c4a2463c0710b` |
| D19 | \[...\] | 192–195 | `70fae5196f97409cc49176e1f2ed1181151da33f9e47afefacd4252567ac5408` |
| D20 | equation | 209–213 | `ecf9d2c975e12e1fb6adf25e56e1916d850017ef157fdc3392080935c7bdba92` |
| D21 | equation | 219–224 | `2fc701d7230fee6a09b163599b7f9efe41d4b6221acbbc7d373e37dd4e6dc1f0` |
| D22 | \[...\] | 230–233 | `ce32ba58730745ed3c8aca81924d9708aaa56be2d3c7db8a5b88652f7d42f822` |
| D23 | equation | 240–244 | `4c091c8f4c029461fbd7b2c14c86822148aeefde94d58b8ff90b555f345f35f0` |
| D24 | \[...\] | 250–254 | `1e9604eaa62006741ad95b7f20e7106b4d32893b376e3d551384c306a5a8bdd8` |
| D25 | equation | 260–262 | `cc90b3955d03b5a3c4980fde04872ebd01d100e4192354add46638f0392ab652` |
| D26 | \[...\] | 270–273 | `a74fdccdfe951f44a29f338c9a78a07c7efaecc27ac28df99908415e3938df4d` |
| D27 | equation | 275–280 | `9cefeced2d94223ca3db51900c922cc066b5ea85fe646ceb4ca56509229af119` |
| D28 | \[...\] | 290–294 | `915fed5f3d6bf0421d8acc300f6ad2843195ff58b3c4b4b7e3a18bdf06dbac6b` |
| D29 | \[...\] | 299–302 | `b566594246fdb0f2e2d92011262f94ece1cc872a9b28eeb148963ebf6518177a` |
| D30 | \[...\] | 324–329 | `bb4df708dfc6265fe5589dc17fc511cd7630dc3db9efa336e5f1a465d2104ee1` |
| D31 | \[...\] | 341–343 | `9eb17d59a89870b880aff52e313be3af4b852414d27c8b67019f98eed050a43c` |
| D32 | \[...\] | 344–346 | `ba258367aab56af02149ac83476c09f306645294aeb33ce1389b9d5aa4276b13` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 53: `residual remains open, and an exact zero-diagonal finite witness shows that`
- TeX line 154: `Fix a finite admissible \(K\) and write`
- TeX line 174: `The implied constant is not uniform in \(M\) or \(K\).`
- TeX line 201: `The theorem means: first freeze finite \(K\), then choose fixed \(M\), then`
- TeX line 202: `take \(x\ge x_0(M,K)\).  Arbitrary fixed logarithmic saving does not imply`
- TeX line 215: `is purely finite-dimensional and requires no symmetry of \(A_x\).`
- TeX line 218: `For every finite clock,`
- TeX line 283: `\texttt{CONDITIONAL\_THEOREM}, not an unconditional fixed-power claim.`
- TeX line 285: `The open residual cannot be controlled by projection algebra alone.`
- TeX line 287: `\begin{proposition}[Exact synthetic non-promotion witness]\label{prop:witness}`
- TeX line 310: `prime shell, and it does not refute any arithmetic estimate.  It refutes only`
- TeX line 319: `general zero-diagonal scalar.  The next open theorem is therefore to estimate`
- TeX line 338: `that replace the residual status \texttt{OPEN} by a theorem, and a stress`
- TeX line 340: `Finite checks receive no prime-asymptotic proof credit.  The maximum status is`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:fullscalar` → `main.tex#L64` (existing project target or original TeX label line).
- Link relocation: `#eq:null` → `main.tex#L119` (existing project target or original TeX label line).
- Link relocation: `#eq:tpc258` → `main.tex#L146` (existing project target or original TeX label line).
- Link relocation: `#eq:maximal` → `main.tex#L164` (existing project target or original TeX label line).
- Link relocation: `#eq:blocksum` → `main.tex#L181` (existing project target or original TeX label line).
- Link relocation: `#eq:null` → `main.tex#L119` (existing project target or original TeX label line).
- Link relocation: `#eq:w-null` → `main.tex#L172` (existing project target or original TeX label line).
- Link relocation: `#eq:projection` → `main.tex#L212` (existing project target or original TeX label line).
- Link relocation: `#eq:split` → `main.tex#L223` (existing project target or original TeX label line).
- Link relocation: `#eq:split` → `main.tex#L223` (existing project target or original TeX label line).
- Link relocation: `#eq:tpc258` → `main.tex#L146` (existing project target or original TeX label line).
- Link relocation: `#thm:w-null` → `main.tex#L168` (existing project target or original TeX label line).
- Link relocation: `#eq:main` → `main.tex#L243` (existing project target or original TeX label line).
- Link relocation: `#eq:fullscalar` → `main.tex#L64` (existing project target or original TeX label line).
- Link relocation: `#thm:w-null` → `main.tex#L168` (existing project target or original TeX label line).
- Link relocation: `#eq:conditional` → `main.tex#L279` (existing project target or original TeX label line).
- Link relocation: `#eq:main` → `main.tex#L243` (existing project target or original TeX label line).
- Link relocation: `#eq:residual` → `main.tex#L261` (existing project target or original TeX label line).
