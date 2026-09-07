# TPC-344 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `e848dbf1895cb067bad6665654a7c992406bcf65`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `f3d1ee4880dd0c4507bd76ec40fdb3276abdda1fea25938f75222fbfba01212f`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `4611a08801629a53a8ff91fc250fe6347fe5416459cf3cfb4c79eedd67d3b634`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8e887b421271def1e1a74e8a4b9acd681b7b77810fff67356cf5b2b84083ada7`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC340_344.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 41 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen finite protocol` | 56 | 1 | `HEADING_TEXT_MATCH` |
| `Exact finite structure` | 90 | 2 | `HEADING_TEXT_MATCH` |
| `Audited finite readout` | 136 | 2 | `HEADING_TEXT_MATCH` |
| `Holdout and cross-fit tests` | 175 | 3 | `HEADING_TEXT_MATCH` |
| `Independent implementation and claim firewall` | 201 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and next question` | 239 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `66` before writing and `66` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `ac914073231066a6d1d2a3189a4adb2dbc7818ecb5ec55bb360af9cda1d55e4e`.
- Source theorem/proof environment starts: proposition at TeX line 92, proof at TeX line 107.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | align* | 59–64 | `f5bf7601d41b7e0547020d1c0dccfe2fa2bae09be42d3e9d5e4af4abc9692586` |
| D02 | \[...\] | 75–79 | `2ab98888225ee88275cb4f30c0bf5a77bc47d291c4774ae3cfa73b898661334c` |
| D03 | \[...\] | 95–98 | `da9b3ea9e4a1a58dc23d61da0cf3c18d3c32d5bd14a5fc886c455b0d18e3c478` |
| D04 | \[...\] | 101–104 | `41a38c60bb88e2be5cfa1609c55ad308305ad21247b68d0125ff82becad97934` |
| D05 | \[...\] | 109–112 | `50a072460ff0537e9ef7322a74188d669e6769779de11b593c477d21c681dee0` |
| D06 | \[...\] | 126–128 | `d30f30f497f5401f80702a44a5aa520d76ab9505f3564aa87bdaaa1010fd2c0b` |
| D07 | \[...\] | 188–191 | `ec3969886473979338947865e9bdc782f76bb59580a75cd3c677f0ec98c02e0b` |
| D08 | \[...\] | 193–196 | `a4ca851ce264582088575a4c3b703c493fddca8626f0cab68486a8d69af86e01` |
| D09 | \[...\] | 245–248 | `19e53fcb26a2f1922e4e52bc29051cc8cfe4e7c4c3da39e330796edc515a2d8e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 16: `A Finite Repair and Weighting Obstruction}`
- TeX line 26: `The preceding finite cross-panel audit found that one nuisance coefficient`
- TeX line 27: `vector does not fit two protocol-compatible twin-prime response panels.  We`
- TeX line 31: `one shared nuisance vector per panel.  On the locked six-row finite panel, its`
- TeX line 35: `$0.3759486734$--$0.6342934197$.  Thus the raw crossing is a finite,`
- TeX line 49: `All objects below are finite vectors generated by the repository's locked`
- TeX line 53: `particular, a finite fit is not a source-uniform estimate and does not pay any`
- TeX line 56: `\section{Frozen finite protocol}`
- TeX line 90: `\section{Exact finite structure}`
- TeX line 118: `The proposition is a finite change of coordinates.  It says exactly what the`
- TeX line 121: `It does not say that the two coefficient vectors are canonical or persist for`
- TeX line 124: `For any finite nuisance matrix $N$, let $P_N$ be the Euclidean orthogonal`
- TeX line 136: `\section{Audited finite readout}`
- TeX line 145: `\caption{Pooled finite projections and transfer diagnostics.}`
- TeX line 182: `the $0.40$ guard.  This is a finite out-of-sample diagnostic for the declared`
- TeX line 183: `control orbit, not a probability statement.`
- TeX line 198: `refuted on this finite pair.  These are prediction residuals, not orthogonal`
- TeX line 205: `does not import the producer: it uses the separately hash-locked reverse-shell`
- TeX line 220: `contrast span identity & proved exact finite declared model\\`
- TeX line 221: `raw contrast guard & numerically certified finite scoped pass\\`
- TeX line 224: `source-uniform arithmetic $L^2$ & open\\`
- TeX line 225: `uniform masked operator bound & open\\`
- TeX line 226: `full Route-B Gate B & open\\`
- TeX line 235: `not an official evaluator pass.  In particular, the finite raw crossing does`
- TeX line 249: `The next natural finite question is geometric: compute principal angles`
- TeX line 252: `artifact.  Until a source-uniform arithmetic theorem is supplied, all Route-B`
- TeX line 253: `and twin-prime gates remain open.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:main` → `main.tex#L146` (existing project target or original TeX label line).
- Link relocation: `#prop:contrast` → `main.tex#L93` (existing project target or original TeX label line).
