# TPC-143 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `4965d5ad640999fda1be2a75b82dabdbb2cef6ad17df770fa2e53fc08b2e9627`.
- Bibliography: [references.bib](references.bib), SHA-256 `62a6b6445db63e5dbe1e138dc371458c979b5f724ff96870a1c475e9d47decc9`.
- Preserved PDF: [tpc-143-frontier-occurrence-lift-contract.pdf](tpc-143-frontier-occurrence-lift-contract.pdf), SHA-256 `a4a633964f1d4eabb7ba04d35d81caebfb43f5784108772a00618052b22e4000`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2b1110933a55a04b400b5a1f9e5cac98782b3dc1dfc22f5c98c1e511d69e2d94`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC143_146.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The exact point reached by the cut archive` | 81 | 1 | `HEADING_TEXT_MATCH` |
| `The missing occurrence lift` | 125 | 2 | `HEADING_TEXT_MATCH` |
| `Field descent and nonidentifiability` | 204 | 3 | `HEADING_TEXT_MATCH` |
| `What the cut shift field does prove` | 280 | 3 | `HEADING_TEXT_MATCH` |
| `Executable field obligations` | 306 | 4 | `HEADING_TEXT_MATCH` |
| `Claim boundary and next object` | 370 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 396 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `79` before writing and `79` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `55fd3e9085dc28e94c286397588c9ced45d451232291630cc9e926d370abc744`.
- Source theorem/proof environment starts: definition at TeX line 111, definition at TeX line 127, definition at TeX line 143, proposition at TeX line 165, proof at TeX line 196, theorem at TeX line 217, proof at TeX line 231, proposition at TeX line 239, proof at TeX line 246, remark at TeX line 273, theorem at TeX line 285, proof at TeX line 295, theorem at TeX line 372.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 59–62 | `ecc4649fc03160c1287f0150959b226484136364db4604ae4c102492d92487ca` |
| D02 | \[...\] | 84–86 | `800d6b6912f8690c6f200cb7e2c0a5010d5496d354f12615dba648fb4065804d` |
| D03 | \[...\] | 90–92 | `396393f3d488fd3ba779c2ffefcf639f3c8d54e2358fbcd6103b06552bea9490` |
| D04 | \[...\] | 96–99 | `8045ddd1fd29da431ee7538f5ce5d8607aa040ce529c551ab62ea323bb356d22` |
| D05 | \[...\] | 145–147 | `87f28fa0e3fe731403b53cf7d3fd463d9234879d0b83c616a7256c5ba4269e1c` |
| D06 | equation | 151–154 | `3e80cd40f8285aa805920bb6ccedce2d5f430d0f99379cb680426a185b0fc2d6` |
| D07 | \[...\] | 170–180 | `7a48e35dfaec3d2593dcdc134c6c6e739192f00e5ca0178dfdeca6a10543cafd` |
| D08 | equation | 182–187 | `b228afeded5412339b823b2f9075277142fdd503eb2fb046c79a50d17869a99a` |
| D09 | \[...\] | 211–213 | `2506ea215a0a86ac4b3a1d399ee9bbc96c62e1071c8aa1b31318ea959c77dbf1` |
| D10 | \[...\] | 251–254 | `1bccdeacdd9bd411de1686654f8b8d2a59825dfbee113160ef522f6a926003dc` |
| D11 | \[...\] | 288–290 | `ac740a2be204d4cc6d12de8bece92a8341c94566d2af80aaee12648161ddfbf0` |
| D12 | \[...\] | 334–338 | `70b43c5dab85d575e2ad3c0ed959b5e92e383b97fbab4bae4ba526a3a45d2026` |
| D13 | \[...\] | 375–378 | `460f5c266b691c7a5e57b3d6888a71823f111735f52b27fea977fca170e66e6d` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 56: `path but does not yet reach the canonical determinant, ordered`
- TeX line 68: `therefore exactly \(P_{h_0}^{\rm cut}=I\), but determinant bins,`
- TeX line 74: `The committed finite sample has \(2988\) frontier paths and no`
- TeX line 75: `eligible-tail path; that finite emptiness is not promoted to`
- TeX line 85: `\mathfrak s=(X,h_0,Q,U,V,W_{\rm id},\nu_{\rm phys})`
- TeX line 94: `They stand for eligible-prefix-soft, eligible-tail-open and`
- TeX line 106: `multiplier expression, \(h_0\), and physical normalization.`
- TeX line 121: `such as \(r_Q(\ell k+h_0)\) may vanish.  Conversely, an unevaluated`
- TeX line 122: `coefficient is not an exact-zero certificate.  We therefore retain`
- TeX line 156: `\(h_0\), and \(\nu_{\rm phys}\) on every nonzero edge.`
- TeX line 160: `reconstruction.  Hence \(L_X\) is not assumed to be a function.  Its`
- TeX line 163: `identity, not a bound on the associated arithmetic scalar.`
- TeX line 249: `forgotten cut record and \(h_0=2,j=1\), two completion records may`
- TeX line 260: `Likewise the present schema does not constrain an outer affine key,`
- TeX line 266: `current schema-completion class.  It is not a mathematical`
- TeX line 275: `downstream maps from the present JSON labels alone.  It does not stop`
- TeX line 276: `a new analytic or algebraic construction of \(L_X\), and it does not`
- TeX line 282: `Let \(P_{h_0}^{\rm cut}\) be the coordinate selector on cut rows whose`
- TeX line 283: `stored shift is the prescribed \(h_0\).`
- TeX line 289: `\boxed{P_{h_0}^{\rm cut}=I.}`
- TeX line 296: `TPC-136 proves metadata intertwining for \(h_0\) from every native`
- TeX line 298: `prescribed \(h_0\), so every cut row is selected.`
- TeX line 303: `selectors \citep{WangTPC123,WangTPC125}.  Copying \(h_0\) into the`
- TeX line 339: `This census describes one finite sample at \(X=512\).  Since the`
- TeX line 351: `& \(\PROVED_{\Lone}\) & \(P_{h_0}^{\rm cut}=I\).\\`
- TeX line 354: `\(Q_D,Q_Z,G,P_{h_0}^{\rm down}\)`
- TeX line 365: `occurrence edge, and promotion of \(P_{h_0}^{\rm cut}\) to a`
- TeX line 380: `while the selected occurrence-augmented route remains open.`
- TeX line 389: `matrix \(L_X\), not a collection of labels detached from their`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:conservation` → `../main.tex#L153` (existing project target or original TeX label line).
- Link relocation: `#eq:conservation` → `../main.tex#L153` (existing project target or original TeX label line).
- Link relocation: `#thm:descent` → `../main.tex#L218` (existing project target or original TeX label line).
