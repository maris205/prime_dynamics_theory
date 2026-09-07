# TPC-345 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `1de1964aa411aa631587da690524beadf1127d3c`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `13647baa6e68db156fd5553fac66085b580a3d3570a0a55bc173657f77331b87`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `9778f1b4829bbfd5a530c6d391571e97dd3320369c04c330e467c4132b652989`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `523ad985fc70d2f4daea70c11f691728198d4b4653314e04c1cf0fe2bbc947b1`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC345_349.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 43 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen finite protocol` | 59 | 1 | `HEADING_TEXT_MATCH` |
| `Finite Grassmann geometry` | 90 | 2 | `HEADING_TEXT_MATCH` |
| `Certified readout` | 145 | 3 | `HEADING_TEXT_MATCH` |
| `Coordinate and control robustness` | 188 | 3 | `HEADING_TEXT_MATCH` |
| `Independent certification and claim firewall` | 219 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion and next question` | 257 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `75` before writing and `75` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `d1d7cc91800a0b37a1a8d273067caf1ce750803238202bf55f5418b26cb79b17`.
- Source theorem/proof environment starts: proposition at TeX line 103, proof at TeX line 110, proposition at TeX line 122, proof at TeX line 130.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | align* | 62–67 | `5a2524a981cd1397221660396e8fcaa8b995e1facc3ffcc0222bac6b37f317a3` |
| D02 | \[...\] | 77–84 | `edc4238bba2275cad8e601b89602a9fe2002cd5e4e0d0ea9f9abb7457d982d0b` |
| D03 | \[...\] | 93–95 | `f64d19711f8da3cfad9f62cf251af19ab6f9058fa926396e4d218508aa9cfda0` |
| D04 | \[...\] | 112–115 | `a1ccc5f8a5d1cea05cdd12ce3080bfe8f6097dc10ad99739ac461e0c20cc70d1` |
| D05 | \[...\] | 125–127 | `8b6f6bf7895a248f4ce296b924832153f8ae8d98f268109808ae320d690bc5ef` |
| D06 | \[...\] | 138–140 | `b109fd90b1ac5151ce663fb304305d7d55d3160dbe6083c3d9d81b55b8a8f28c` |
| D07 | \[...\] | 180–183 | `44a78db8ddbc87d8d8b97edfc929d87efd8ff08942d60593f0d74b49f58b444d` |
| D08 | \[...\] | 192–194 | `64bb8040a3168cdbaba4526a0ed92e075ae0778d755d60d2a5bd872bf6ec0105` |
| D09 | \[...\] | 268–275 | `da0f86b7260b6e7cb6438e728238038c139a0ccba4a23df2741b18756aa23b1f` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 15: `\title{Principal Angles of Two Finite Nuisance Panels:\\`
- TeX line 26: `The preceding finite panel-contrast audit found a narrow raw-weighted`
- TeX line 39: `transverse separation.  This is a finite geometric obstruction only; it`
- TeX line 40: `provides no arithmetic, asymptotic, Route-A/Route-B, or twin-prime result.`
- TeX line 52: `All objects in this paper are finite vectors generated by the repository's`
- TeX line 54: `nuisance name declared masks and response vectors; they are not an arithmetic`
- TeX line 55: `decomposition.  In particular, a principal angle between two finite`
- TeX line 56: `response subspaces is not a source-uniform estimate and does not pay any`
- TeX line 59: `\section{Frozen finite protocol}`
- TeX line 90: `\section{Finite Grassmann geometry}`
- TeX line 105: `The singular values of $Q_1^TQ_2$ depend only on the two finite column`
- TeX line 122: `\begin{proposition}[finite projection identity]`
- TeX line 124: `For every finite target $Y$ and orthogonal projector $P$,`
- TeX line 137: `we record the finite residual retention`
- TeX line 142: `$\rho<0.30$.  This is a declared finite diagnostic, not a theorem about`
- TeX line 153: `\caption{Main finite Grassmann geometry and cross-panel transfer.}`
- TeX line 173: `and both second cosines are below $0.20$.  Thus the finite geometry has one`
- TeX line 175: `direction is not a numerical zero: it corresponds to angles near $85.4$`
- TeX line 199: `coordinate-invariance proposition, not a claim that the finite spaces are`
- TeX line 214: `directions below $0.30$, it is refuted in both finite weightings.  These`
- TeX line 223: `checker does not import the producer.  It uses a separately hash-locked`
- TeX line 237: `principal-angle definition and invariance & proved exact finite model\\`
- TeX line 238: `projection/Pythagorean identity & proved exact finite model\\`
- TeX line 239: `raw dominant alignment and transverse separation & numerically certified finite scoped\\`
- TeX line 240: `leave-one-control-out transverse separation & numerically certified finite scoped\\`
- TeX line 243: `source-uniform arithmetic $L^2$ & open\\`
- TeX line 244: `uniform masked operator bound & open\\`
- TeX line 245: `full Route-B Gate B & open\\`
- TeX line 254: `and cannot be called an official evaluator pass.  No finite principal-angle`
- TeX line 259: `The TPC-344 panel-adaptive repair has a clear finite geometric profile: one`
- TeX line 276: `The next minimal question is a finite no-go or freeze test: determine whether`
- TeX line 278: `class or merely overfits these locked panels.  Until a source-uniform`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:geometry` → `main.tex#L154` (existing project target or original TeX label line).
- Link relocation: `#prop:projection` → `main.tex#L123` (existing project target or original TeX label line).
