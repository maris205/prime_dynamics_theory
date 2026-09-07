# TPC-287 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `c9f2a3559e421cb10eaf51c1268a03b838c5ed68`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `cb23c6378bfb52e3ddcd196a0041cfe37d9f8b38d11bd623c577a6653450f3a7`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `6a4f4eef4864f112e5c88a360f71e86669062ec4e1fa158286227ea3a0256790`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `d7d637e4b5deaeb413b0b195ce9665907f1c0bd000f3d06703f7b13643fa9ab7`; 7 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2316abfa9956323f39bb9072c969e957dcec757fb4a80608297f29045f8c2c86`.
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
| `Question and contribution` | 51 | 1 | `HEADING_TEXT_MATCH` |
| `The physical prime components` | 85 | 2 | `HEADING_TEXT_MATCH` |
| `Exact shell additivity` | 133 | 2 | `HEADING_TEXT_MATCH` |
| `A certified retention envelope` | 169 | 3 | `HEADING_TEXT_MATCH` |
| `Declared ladder and finite protocol` | 212 | 3 | `HEADING_TEXT_MATCH` |
| `Results: cancellation depth and sensitivity` | 261 | 4 | `HEADING_TEXT_MATCH` |
| `What this settles, and what it does not` | 336 | 5 | `HEADING_TEXT_MATCH` |
| `Verification and claim firewall` | 370 | 6 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 404 | 6 | `HEADING_TEXT_MATCH` |
| `Reproduction record` | 420 | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |
| `References (external bibliography)` | 443 | 7 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `99` before writing and `99` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `16`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `17bf9997b69dab9d609a792b4193cfeb7d9834e8b8115c2b2477984ae729c575`.
- Source theorem/proof environment starts: theorem at TeX line 135, proof at TeX line 150, remark at TeX line 162, proposition at TeX line 183, proof at TeX line 191.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 88–93 | `6a9cbd9a1721ac5314fc41462677584cf863d74e1e633b3ea6c6920c53bd4a4c` |
| D02 | equation | 95–98 | `89cc79f73c4c37b4ecd0ce0fd035ca6007fd943a6bd3879795c56f230f45c7e9` |
| D03 | equation | 100–103 | `bef9cd11e442abf50a7fa2b1f2ab9f6bafa4dc639a895294e1313b6d6c26e212` |
| D04 | equation | 106–110 | `b07da88f63efafd6ab87cbc9da5124e158e08d826d2a02b4b638facd47968fd8` |
| D05 | equation | 112–115 | `91f5e7042c17a41bd38da905d12bdc2e7c0aa93a613c1af1ffa6a0a586f0cc85` |
| D06 | equation | 122–126 | `aeb230e823428c9d746172375faa43630b0b1bed70fc76be37e2c3650aacb0ad` |
| D07 | equation | 139–142 | `e2335ec7d0694a71d2f8868c8f518691bac9f83a9203bfd2150bcc98ed367bbb` |
| D08 | equation | 144–147 | `a494e594455cf57989f66385e9aa4df71bef1885b50e11809173d086cb4b1162` |
| D09 | equation* | 155–158 | `62c1b3bb6221b23c2236442c57e9b294e2bb83c13b930a0811409fbd02fa2b78` |
| D10 | align | 175–181 | `4aa21ed2e438eba131e2fc5d169e0879e0f961a61e2c5a88fad751bbd643964c` |
| D11 | equation | 185–188 | `f91e9386d294d05c77d06df3937f7dd58eb67ffbd67762926e71811e878c60d6` |
| D12 | \[...\] | 193–195 | `217f680d83bec0392fb1ea1a6b52f0f954d2063f4a6054addea910c0d6b21621` |
| D13 | \[...\] | 198–201 | `84f2df888112bef2d1747469abcdb7102315c9f60b73a29ca19202161f8a0d6b` |
| D14 | equation | 239–243 | `1bb78a5bbed186edc676ed53785b831196112b45418ae648a65407f963aa8aaf` |
| D15 | \[...\] | 248–250 | `3e9cede0cce62c07f9ea2c8f51cef173c3d3232a58e149cc00b0471436acccad` |
| D16 | \[...\] | 340–346 | `99b2a920eedd6b6b52c54b4974e8eca4341fd42eb3984a209cda194e663e94dc` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 21: `A Finite Signed Component Ledger for the Physical Operator}`
- TeX line 34: `finite shell we define one physical off-diagonal component per prime and prove`
- TeX line 44: `finite cancellation-depth diagnostic and an exact reusable decomposition, not`
- TeX line 45: `an asymptotic saving.  The principal obstruction is now precise: the finite`
- TeX line 46: `ladder has no canonical growing-shell measure, so uniform cancellation under`
- TeX line 47: `growing shells and source controls remains open.  No fixed-power credit, Gate-B`
- TeX line 54: `a finite source profile.  A preceding control atlas showed that small changes`
- TeX line 62: `deep is that cancellation on a controlled finite ladder?}`
- TeX line 68: `finite-shell additivity theorem;`
- TeX line 75: `\item a route obstruction identifying the next missing theorem: uniform`
- TeX line 79: `The distinction between exact structure and finite evidence is essential.  We`
- TeX line 82: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE} for the ledger counts.  The declared`
- TeX line 83: `ladder is a modeling choice, not an asymptotic sampling rule.`
- TeX line 87: `Let $I$ be a finite interval of integers and let $q$ be an odd prime.  Put`
- TeX line 104: `For a finite shell $\shell_Q=\{q:Q<q\leq 2Q,\ q\text{ prime}\}$ and a`
- TeX line 119: `The scalar attachment is the same finite interface used by the earlier`
- TeX line 131: `interval arithmetic in the finite audit.`
- TeX line 135: `\begin{theorem}[finite component decomposition]`
- TeX line 136: `For every finite $I$ and finite prime set $\shell$, every source vector $\beta$,`
- TeX line 152: `of \eqref{eq:output-add}.  The resulting sum is exactly the defining finite`
- TeX line 153: `double sum for $g_{\shell}(u)$.  Since both $I$ and $\shell$ are finite, no`
- TeX line 166: `majorant.  It does not provide a bound for the signed sum.`
- TeX line 173: `$J_{\shell}=[\ell_{\shell},u_{\shell}]$.  Assume each $J_q$ is separated from`
- TeX line 184: `Under the stated enclosure and sign-separation assumptions,`
- TeX line 209: `intervals.  Thus a small $r^+$ is useful finite evidence of cancellation, but`
- TeX line 210: `not a limiting proportion or a norm estimate.`
- TeX line 212: `\section{Declared ladder and finite protocol}`
- TeX line 263: `The headline finite census is in Table~\ref{tab:aggregate}.  All 336`
- TeX line 272: `\caption{Aggregate TPC-287 finite certificate.}`
- TeX line 296: `three- and four-prime rows are the most active part of this finite ladder;`
- TeX line 299: `information: shell cardinality alone is not a proxy for asymptotic gain.`
- TeX line 323: `ratio is retained in the JSON certificate).  This is a strong finite`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:component` → `main.tex#L109` (existing project target or original TeX label line).
- Link relocation: `#eq:shell` → `main.tex#L114` (existing project target or original TeX label line).
- Link relocation: `#eq:component` → `main.tex#L109` (existing project target or original TeX label line).
- Link relocation: `#eq:output-add` → `main.tex#L141` (existing project target or original TeX label line).
- Link relocation: `#eq:retention` → `main.tex#L187` (existing project target or original TeX label line).
- Link relocation: `#tab:ladder` → `main.tex#L222` (existing project target or original TeX label line).
- Link relocation: `#tab:aggregate` → `main.tex#L273` (existing project target or original TeX label line).
- Link relocation: `#tab:size` → `main.tex#L305` (existing project target or original TeX label line).
- Link relocation: `#tab:aggregate` → `main.tex#L273` (existing project target or original TeX label line).
- Link relocation: `#tab:size` → `main.tex#L305` (existing project target or original TeX label line).
