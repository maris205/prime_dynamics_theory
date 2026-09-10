# TPC-156 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `19ca4cba08d88a34ac01b06364acb45309f4b1eca612c65c408131e3b4c4834c`.
- Bibliography: [references.bib](references.bib), SHA-256 `b0cc42ee564399dc1041a3b927ce0f7384666c05c2b5ef8db19643be93099e99`.
- Preserved PDF: [tpc-156-h1-occurrence-crosswalk-route-decision.pdf](tpc-156-h1-occurrence-crosswalk-route-decision.pdf), SHA-256 `81fff95cd04b1056a4322889d0c4046cd0183b951af81d69850a5f1f89b2f876`; 6 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `587eab3648eed00b5ffc486ebb6ba0080a029b7e83b535355478121b7d815679`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC153_156.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The exact imported state` | 115 | 1 | `HEADING_TEXT_MATCH` |
| `The theorem-backed crosswalk` | 185 | 2 | `HEADING_TEXT_MATCH` |
| `The typed H1 alternative` | 261 | 3 | `HEADING_TEXT_MATCH` |
| `Current route decision` | 338 | 4 | `HEADING_TEXT_MATCH` |
| `Scoped stops and kill criteria` | 404 | 5 | `HEADING_TEXT_MATCH` |
| `Executable source-locked audit` | 443 | 5 | `HEADING_TEXT_MATCH` |
| `Decision theorem and next analytic object` | 472 | 6 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 510 | 6 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `52` before writing and `52` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `19`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `0b9da661771d7a17e5c57568f78b520279a5c11202f3d321f1f693ca79e02732`.
- Source theorem/proof environment starts: definition at TeX line 187, definition at TeX line 238, remark at TeX line 253, definition at TeX line 274, definition at TeX line 293, theorem at TeX line 313, proof at TeX line 327, proposition at TeX line 340, proof at TeX line 360, theorem at TeX line 370, proof at TeX line 384, remark at TeX line 392, theorem at TeX line 474, corollary at TeX line 489.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 81–85 | `9ae210d970032f92fa10af8b8ce21906cd23e1912e2d300e8264f8fd39b0a85c` |
| D02 | \[...\] | 91–93 | `8c40c62b1ab31aaf1acc35e0d99c960742cfac7ca91285fba02962e1e2943d32` |
| D03 | \[...\] | 118–120 | `99f3b69bb6621e60eacb2461bcc119e37ddb2888920cf0a7cfc3b482e8b9de89` |
| D04 | \[...\] | 125–127 | `7e5fbea0923a9a52791bb6ebe09f22e0ebadef60eb816249db0b248d3ff36e03` |
| D05 | \[...\] | 133–135 | `222909617214fd2fba177ef0ebd3c6400cd6147c3951e3e4e05fbab14f6932fe` |
| D06 | \[...\] | 137–139 | `9298cd7abe5fb4fdb9a45812f4802f945fcfc577acbf4beab49d2e849a1b89dd` |
| D07 | \[...\] | 141–144 | `6c466825561333fc7511c3646648336d29420be6bf39240ae6c1cff9761d4646` |
| D08 | \[...\] | 152–154 | `c594206533f0200ad0d37c2405f36c73cef7c1e4d71f0458f419a1fb06cc5675` |
| D09 | equation | 157–160 | `f3fdfbefe57764c02f8a9f9b1961853a6838eb1f271239fc7feed7cf7b4b0cb3` |
| D10 | \[...\] | 178–182 | `1d53e871608e3bb736938d91b5ff0387af313f4801c42dee092b579257a5ce8a` |
| D11 | equation | 211–215 | `5a90b0f4d28942dbcb5bbd375f34ca0f450913c94a9813cd0921ced0b613a23f` |
| D12 | \[...\] | 266–270 | `993c81e94b895447e54f34c128621ea90ebd8a5964eea1e3a5b2dd9969dc7c86` |
| D13 | \[...\] | 277–285 | `fe988de809adc72f362a171fd3c61d25069f147ef4b463be4d94ea8668a0687b` |
| D14 | \[...\] | 296–302 | `6f7d2bfefa756d5e8b3e4bcfb35b4d80eb5335c5c7efb9415868aa2fd282066e` |
| D15 | \[...\] | 316–321 | `6b153775adba29453e147b369d104fa6ecfc9713f5085358b60ddbab10c81a35` |
| D16 | \[...\] | 343–355 | `15166a68215c74d1940045d9e4ca9db76f1e5b5713e76f4ca0e0b8bae8ca966a` |
| D17 | \[...\] | 374–379 | `68a77543cf079406fcf0cb8d016ada9ff38d31a974cd17db95d9f1e4cf6ff9d8` |
| D18 | \[...\] | 394–399 | `6910a6777febac1abcf2737faf537ea9fe6c375497bece477f9a98ea415f473a` |
| D19 | \[...\] | 478–480 | `87ffb834648a08788eafecb0c68e3e55477192d9e96ed9c9ff01787ebd28c5b8` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 37: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 62: `The complete native cut leaves two nonsoft classes: eligible-tail-open`
- TeX line 79: `path and a theorem-backed disposition of every eligible-tail-open`
- TeX line 89: `routes remain open.  The minimal missing node on the selected map`
- TeX line 95: `not a positive \(\Ltwo\), endpoint, prime-pair, or twin-prime result.`
- TeX line 107: `current-artifacts-only derivation; it is not an impossibility theorem`
- TeX line 122: `terminal tags mean \emph{eligible tail open} and`
- TeX line 124: `statement below quantifies over both classes.  The finite census`
- TeX line 128: `does not prove that \(\Ceto\) is asymptotically empty`
- TeX line 146: `dyadic multiplier, \(h_0\), physical normalization, weight source,`
- TeX line 162: `row-separated children are forgotten.  It does not determine those`
- TeX line 173: `TPC-155 then specifies a production witness contract.  Its synthetic`
- TeX line 190: `crosswalk supplies a finite nonempty row set \(\mathcal R_c\).  A row`
- TeX line 196: `\item the native tuple, \(h_0\), physical normalization, cut`
- TeX line 230: `the cut value \(h_0\) into a later record is not a proof that an`
- TeX line 291: `row-separated fixed-\(h_0\) test.`
- TeX line 357: `remain open.`
- TeX line 416: `& \(\NT\), open`
- TeX line 420: `& \(\NT\), open`
- TeX line 434: `parent or stage data lack a trusted source, if native, \(h_0\), or`
- TeX line 439: `\cref{def:scalarclause} is missing.  A finite ETO census is not a`
- TeX line 458: `\item scoped route stops and open alternatives; and`
- TeX line 465: `ETO-only route pass, finite-empty-ETO reasoning, an unsupported`
- TeX line 483: `occurrence-augmented map route remains open, with first missing object`
- TeX line 486: `open with both of its factors missing.`
- TeX line 493: `It does not establish a complete actual physical carrier or any`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 6 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:shadow` → `../main.tex#L159` (existing project target or original TeX label line).
- Link relocation: `#eq:column-conservation` → `../main.tex#L214` (existing project target or original TeX label line).
- Link relocation: `#eq:column-conservation` → `../main.tex#L214` (existing project target or original TeX label line).
- Link relocation: `#def:mapclause` → `../main.tex#L275` (existing project target or original TeX label line).
- Link relocation: `#def:scalarclause` → `../main.tex#L294` (existing project target or original TeX label line).
- Link relocation: `#thm:h1` → `../main.tex#L314` (existing project target or original TeX label line).
- Link relocation: `#def:crosswalk` → `../main.tex#L188` (existing project target or original TeX label line).
- Link relocation: `#def:scalarclause` → `../main.tex#L294` (existing project target or original TeX label line).
- Link relocation: `#def:crosswalk` → `../main.tex#L188` (existing project target or original TeX label line).
