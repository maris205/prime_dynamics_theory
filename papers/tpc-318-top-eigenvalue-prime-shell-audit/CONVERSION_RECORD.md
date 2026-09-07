# TPC-318 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `b9723facc6f4c261e20e0d86513230e5351dfe4d`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `a426d9cf0d3e32510ef41bed3136789702136521f2f95d5cbf5c1fe31b7a380c`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `42f99d170e6443f414a45223c4aaf3f544af347e5faae333bad7270e67fdbb70`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `001dc6af0c6b0200711676a29b598fd56d35d185100adfeb9d5e3c4f65bcf98d`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC315_319.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim ceiling` | 43 | 1 | `HEADING_TEXT_MATCH` |
| `The frozen operator` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `Finite error model` | 100 | 2 | `HEADING_TEXT_MATCH` |
| `Certificate and independent replay` | 128 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 150 | 2 | `HEADING_TEXT_MATCH` |
| `What the result does and does not buy` | 210 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion and next question` | 226 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 244 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `51` before writing and `51` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `ba7e4805addcf5c58db44076440939c8ff87d66ac24cd95e0c742a49e051c2fb`.
- Source theorem/proof environment starts: proposition at TeX line 83, proof at TeX line 91.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 67–70 | `eb12608e55acfffe74fc2baf7b7f871cea3b52d77bfe1a19e74d218a79664579` |
| D02 | equation | 72–77 | `9368c84b614e34367c292ef1c220b10b1cb6ea784ab94f988aec3610d3a049ec` |
| D03 | \[...\] | 86–89 | `2e6ca9851a01fc9e51f87034c0298367973585517bf1f7289308f33940e06838` |
| D04 | \[...\] | 109–112 | `0d20be4636ed4c754bcf33851a67f34996da409005da4d5cdb79c97bf29346ed` |
| D05 | equation | 116–119 | `1d1799683e79473014950484bd027f11b0dc1c668e18031bbd71d87396713726` |
| D06 | \[...\] | 132–136 | `e0439f654bcef69dec9aedcae39c0ad10afcc790c36fec36d9ef5813f017c9c9` |
| D07 | \[...\] | 234–240 | `eff77052ec1b1e2db4ce9bf5b4ab23aee4e9b7dcce8bbc77fa9e42d9cd705d36` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 15: `\title{Finite Top-Eigenvalue Readout for a Literal Prime--Shell Operator}`
- TeX line 26: `The preceding TPC-317 study replaced a finite Frobenius envelope by the`
- TeX line 29: `open.  We compute that top eigenvalue directly on the same locked operator,`
- TeX line 33: `rows are enclosed by finite numerical intervals and all 16 adjacent-scale`
- TeX line 34: `comparisons are strictly decreasing.  The corresponding finite log-base-two`
- TeX line 38: `single leading eigenvector is not a stable arithmetic channel on these panels.`
- TeX line 39: `The result is a finite numerical certificate, not an asymptotic estimate,`
- TeX line 46: `reassembled with a power saving.  TPC-316 supplied the full finite operator but`
- TeX line 50: `finite trend.  This is a diagnostic question about one fixed dynamical-system`
- TeX line 51: `family, not a replacement for the missing arithmetic theorem.`
- TeX line 55: `\item the PSD and perturbation statements below are exact finite linear algebra;`
- TeX line 57: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE} under a declared error model;`
- TeX line 58: `\item the normalized trend, the finite slopes, and the gap census are`
- TeX line 61: `twin-prime conclusion remain open.`
- TeX line 83: `\begin{proposition}[finite PSD and trace-power facts]`
- TeX line 84: `For every finite row, $G$ is positive semidefinite.  If its eigenvalues are`
- TeX line 92: `The identity $G=A^*A$ gives positive semidefiniteness.  The first inequality`
- TeX line 100: `\section{Finite error model}`
- TeX line 123: `The resulting interval is a finite numerical enclosure under this model.  It`
- TeX line 124: `is not a formal theorem about every floating-point implementation; that is why`
- TeX line 126: `finite matrix theory \cite{weyl,hj}.`
- TeX line 139: `matrix guard, and an outward decimal pad.  The independent checker does not`
- TeX line 179: `finite base-two slopes range from $-0.9972377$ to $-0.4238528$.  Thus the`
- TeX line 181: `upper envelope on these finite panels.`
- TeX line 185: `\caption{Finite slope and eigengap diagnostics.}`
- TeX line 207: `$0.01$; the global minimum is $0.0017043531$.  This is not a numerical failure:`
- TeX line 210: `\section{What the result does and does not buy}`
- TeX line 214: `$N\Lambda_{Q,s}(X)$.  Adding the source-count exponent shifts each finite`
- TeX line 216: `range approximately from $0.0027623$ to $0.5761472$.  The finite data do not`
- TeX line 217: `pay a uniform source-to-output power saving under either convention.`
- TeX line 223: `these.  In particular, the 16 finite decreases cannot be used as a fixed-power`
- TeX line 228: `The direct finite spectral readout closes the local question left by TPC-317:`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:chain` → `main.tex#L88` (existing project target or original TeX label line).
- Link relocation: `#eq:entry` → `main.tex#L76` (existing project target or original TeX label line).
- Link relocation: `#tab:top` → `main.tex#L159` (existing project target or original TeX label line).
- Link relocation: `#eq:normalized` → `main.tex#L135` (existing project target or original TeX label line).
