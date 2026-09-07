# TPC-328 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `b13909fddbffed372f43022d2cfaa2d7bdb1110e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `da4fecebf56bb36f30c40e7a50e1a135e203c8af0055c4b9242514f3e7c4d483`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `26151898fe19ac90e4d68a83b2386cc44c50bff495e31d2580f42b1192c7c3cb`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `e3661318a486105ace24b2c4444ad1f9b47ab1f6f0d476878a0469fbd607fe51`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `dd6ce710cf65f7c6c69c68224646202ae45fee06a1b16d1b8e06706a6be2aba9`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC325_329.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and contribution` | 41 | 1 | `HEADING_TEXT_MATCH` |
| `The literal finite object` | 65 | 1 | `HEADING_TEXT_MATCH` |
| `The source-native model` | 105 | 2 | `HEADING_TEXT_MATCH` |
| `Exact Gram decomposition` | 134 | 2 | `HEADING_TEXT_MATCH` |
| `Protocol and certificate` | 163 | 3 | `HEADING_TEXT_MATCH` |
| `Finite results` | 181 | 3 | `HEADING_TEXT_MATCH` |
| `Exact local anchor` | 227 | 4 | `HEADING_TEXT_MATCH` |
| `Interpretation and claim boundary` | 253 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 280 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 303 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `71` before writing and `71` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `16`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `ca86691dc82e8d57d4b4fdfef87fdfc54d94022ba787b753ccb57c7807499b08`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 68–70 | `ef00deb1077ad608cf8719ca830a5278889cb260b18a0c1c71d2acd970398f30` |
| D02 | \[...\] | 72–75 | `a2e4cfe7ae5c022dccad33784303f7d0206436a3eb0728f8791130851f1b7dc4` |
| D03 | equation | 78–83 | `1a022bc3c3cec12dce5730b515a465e05cb461152ff8803422d812fbb43e6e49` |
| D04 | \[...\] | 86–88 | `6dc68a973de60528f95115754d021b8052e31e6f1633b51dc797892274cee233` |
| D05 | align | 93–97 | `699da9d6106a0df5615f1361b523900b50cc21a2ea47ca77b6ebc2bd7f2bed66` |
| D06 | \[...\] | 99–101 | `cdd303101ac5dd754c6bacc7385f9195f3b1dace4fa388134941542a77561b13` |
| D07 | \[...\] | 108–114 | `2a2d8faf0f65de892e1f89a03446899ee8d6731329d17e94ccf4c5578e8c2bf0` |
| D08 | equation | 116–120 | `98c63623b171d576b6c5c69fd5822c54e9d71a291ce8d99b4d4181ba5f592907` |
| D09 | \[...\] | 122–125 | `a6d55c0a238532faae07ae21ab2a2782bd3987a891268bbeccaca9984eba359d` |
| D10 | equation | 139–143 | `7840a987cd1411327f562f025401d62160ac3351dff88b9fddf8d621e46d75fb` |
| D11 | \[...\] | 148–152 | `323a028607760d3268fa108c638ab407e350079adf8d2977da8ba61d7a56fd13` |
| D12 | \[...\] | 203–206 | `6c5ea19154641e527c7d813072b8aad41c7ecc59bb7d92237d70b2346aefaf0f` |
| D13 | \[...\] | 210–214 | `e2a1a83dcc23653e0deb41b34af15f8f00442b2d9eb68d28c848200bd59f038d` |
| D14 | \[...\] | 231–233 | `eda3a99dc7d9c3d59f62db92be5dc07585e639b5768c2132d632ef5b2e9b6b37` |
| D15 | \[...\] | 235–239 | `bb701095f5cb7158c2393f011edc685b3a2f5755dfbe2e2ecc44ba0029416a77` |
| D16 | \[...\] | 270–275 | `149cbffc2de2ddc69adfc9b91dce5e6d9e2c1db863debeaba5777340e9588053` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 14: `\title{Source-Native Arithmetic $L^2$ Cancellation and the Finite Signed-Gram Obstruction}`
- TeX line 22: `The finite prime-shell experiments in the preceding releases compared signed`
- TeX line 26: `centered prime-shell matrix to the finite V59 comparison residual`
- TeX line 27: `$\beta_o^{(2)}(t)=\Lambda(t+2)-b^{(2)}(t)$.  An exact finite Gram expansion`
- TeX line 35: `finite source-native $L^2$ cancellation atlas and a scoped obstruction to a`
- TeX line 36: `uniform contraction for the four declared laws.  It supplies no growing`
- TeX line 44: `recurring risk is that a stable-looking finite spectral readout may describe`
- TeX line 50: `The paper makes four finite contributions:`
- TeX line 57: `\item it records a non-vacuous finite obstruction: every declared sign law`
- TeX line 62: `All claims below are finite.  In particular, a row count is not a uniformity`
- TeX line 63: `quantifier and a ratio is not an asymptotic exponent.`
- TeX line 65: `\section{The literal finite object}`
- TeX line 92: `For a finite real vector $v=(v_t)_{t\in I_{o,N}}$, define`
- TeX line 102: `Thus $R_e<1$ and $R_e>1$ have an unambiguous finite meaning: negative and`
- TeX line 107: `The arithmetic vector is the finite V59 comparison model, with`
- TeX line 130: `float64 matrix replay.  This is a declared finite model and numerical`
- TeX line 131: `protocol.  It is not an identification theorem for an asymptotic twin-prime`
- TeX line 137: `For every finite interval, every finite family of matrices in`
- TeX line 146: `The finite matrix product is`
- TeX line 153: `The terms with $t=t'$ are exactly $D_e(v)$, and the remaining finite terms`
- TeX line 158: `finite trace bookkeeping are standard finite-dimensional matrix facts`
- TeX line 173: `The independent checker does not import the producer.  It constructs the`
- TeX line 176: `metrics.  The stress suite checks the finite identity with exact rational`
- TeX line 181: `\section{Finite results}`
- TeX line 188: `\caption{Guarded finite off-diagonal census.}`
- TeX line 216: `is not a zero-energy or unresolved-component artifact.`
- TeX line 218: `The row-level finite conclusion is deliberately narrow:`
- TeX line 221: `$E_e(\beta_o^{(2)})\leq D_e(\beta_o^{(2)})$ uniformly on the released panel.`
- TeX line 223: `The all-plus law nevertheless exhibits cancellation on a substantial finite`
- TeX line 250: `prime.  This is an exact finite anchor, not a statement about the density of`
- TeX line 256: `combined with an independently replayed source-native finite atlas.  The`
- TeX line 259: `uniform contraction only on the declared finite panel.`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.

- Link relocation: `#eq:block` → `main.tex#L78` (existing project target or original TeX label line).
- Link relocation: `#eq:gram` → `main.tex#L139` (existing project target or original TeX label line).
- Link relocation: `#tab:census` → `main.tex#L189` (existing project target or original TeX label line).
