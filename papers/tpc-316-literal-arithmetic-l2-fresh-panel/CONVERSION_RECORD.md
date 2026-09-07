# TPC-316 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `b9723facc6f4c261e20e0d86513230e5351dfe4d`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `07cdbde2a949ad19c9c0382f00d3bdfe167f720752e31eb672e9dfd97abe6b69`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `89dcfcf9fce4d734d935af51675afff666605c94d9679ab2075efaf5f4b7ab38`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `20a8b9c3b9f47f9257f590d09f64985375550734af597932127963295f7cfae3`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `1b6f17c618aa65e5372e057827fc768a9460fbe549246c5e5af7c573fcb92bce`.
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
| `Question and route position` | 44 | 1 | `HEADING_TEXT_MATCH` |
| `The literal source operator` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `Two exact finite identities` | 102 | 2 | `HEADING_TEXT_MATCH` |
| `Exact protocol and finite results` | 188 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and route firewall` | 261 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and next gate` | 286 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 311 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `68` before writing and `68` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `14`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `6137a6c07d6a2a44e7b2bcf7a6e3849418fa4d63bcdc439664779c4e262f0be4`.
- Source theorem/proof environment starts: proposition at TeX line 104, proof at TeX line 116, lemma at TeX line 130, proof at TeX line 163.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 67–69 | `5436e15859f88756b13d4ff181fef21d096046c470d573aba6881d87156c65ef` |
| D02 | \[...\] | 71–73 | `2a67103ffcb1e42ecdac6420981225b11b68093b2fa07237585692fb4be34f44` |
| D03 | equation | 76–82 | `b476bcfe23504aac9b9e6fe9f49a9a39f86eba115abb8c7712e0339a291adca4` |
| D04 | equation | 84–91 | `6a48dd16fd25ef9e88920a063336e6d660314eea7faa96e0a1a2124d82ecb0ad` |
| D05 | equation | 106–113 | `6248be2acfaed587ced586e7dfc4291aa2644c5e8e9f647457bb84049e4d3b73` |
| D06 | \[...\] | 118–122 | `284516fc29ca6657d986061cfbaa640b0d06b7f4c6e7fe49fc6510147b620c03` |
| D07 | \[...\] | 133–136 | `e8668fc32fc29853b3d74408e66510eeead3d27397b5df6cafc162523e591ea7` |
| D08 | \[...\] | 139–146 | `abb51c588ef7a35373fa1bce68a60b2a65c3614ce63d62bb9106b820feeb9ebf` |
| D09 | equation | 148–154 | `6016b18746fb1a71242a00cc9056a73b6882f6f980dfcc0aec6129fe11ef98dc` |
| D10 | \[...\] | 156–160 | `2582af139bd3ffcecce4b2ab7e743edea3cf9ca64a5ca68b2b0594564494aaa7` |
| D11 | equation | 174–178 | `6e1cb1b4c79ddb261fc0ac2d818255780f2a0cb526a126f8674a8e5c378b1596` |
| D12 | equation | 180–183 | `5075a10c786aef039fb902703ae6a059f8a174fa6b27066804509446b082b9d7` |
| D13 | \[...\] | 194–198 | `cd36b2a41dc37dc0f1e405983372b762ccf55b08f1c5c0f0d0ce50e925ded1f3` |
| D14 | \[...\] | 289–292 | `23ffcd2004e5e57896dd372a69436bcc7cb386bfce3d76900ffc8b5ddc31c0af` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 14: `\title{A Literal Finite $L^2$ Envelope for the Fresh Prime--Shell Operator}`
- TeX line 25: `The preceding finite prime--shell audit left the source-level arithmetic`
- TeX line 26: `$L^2$ interface open.  We make that interface literal by treating the`
- TeX line 30: `finite Frobenius inequality gives`
- TeX line 39: `is a finite literal $L^2$ envelope and a scoped obstruction to using that`
- TeX line 40: `envelope as a decaying proxy.  It is not a growing operator-norm theorem,`
- TeX line 52: `What is the exact finite source-to-output operator behind the physical formula,`
- TeX line 59: `We answer it for the locked finite engine and keep the two-panel comparison`
- TeX line 60: `strictly finite.  In particular, a rising Frobenius envelope does not prove`
- TeX line 61: `that the true spectral norm rises, just as a finite upper bound cannot prove a`
- TeX line 98: `for the four anchors are $6,9,12,15$, so the output dimensions are finite and`
- TeX line 102: `\section{Two exact finite identities}`
- TeX line 105: `For every finite vector $\beta$,`
- TeX line 127: `The bound is useful only as an envelope.  It does not assert that the`
- TeX line 188: `\section{Exact protocol and finite results}`
- TeX line 206: `column is $U/L$, not a condition number for the true operator.`
- TeX line 212: `\caption{Fresh-panel exact finite sandwich.  Values are decimal views of`
- TeX line 259: `certified finite observation, not an asymptotic monotonicity statement.`
- TeX line 263: `The positive result is now concrete: the literal finite matrix, rather than a`
- TeX line 273: `Thus the immediate envelope gives no negative-power credit and does not`
- TeX line 274: `identify the scale of the true operator norm.  The result does not say that a`
- TeX line 280: `finite modeling choice, and no canonical weight law is selected.  The`
- TeX line 284: `zero, full Gate B is \texttt{OPEN}, and no twin-prime conclusion is claimed.`
- TeX line 288: `TPC-316 pays a finite literal $L^2$ interface:`
- TeX line 297: `from a conditional $L^2$ interface to a literal finite envelope, but stops`
- TeX line 306: `This manuscript is a finite diagnostic release by Liang Wang (HUST).  It does`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:matrix-entry` → `main.tex#L81` (existing project target or original TeX label line).
- Link relocation: `#eq:hs-count` → `main.tex#L153` (existing project target or original TeX label line).
- Link relocation: `#eq:hs-count` → `main.tex#L153` (existing project target or original TeX label line).
- Link relocation: `#tab:fresh` → `main.tex#L214` (existing project target or original TeX label line).
- Link relocation: `#tab:scale` → `main.tex#L241` (existing project target or original TeX label line).
