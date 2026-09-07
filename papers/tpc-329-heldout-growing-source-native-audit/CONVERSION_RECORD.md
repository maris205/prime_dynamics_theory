# TPC-329 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `b13909fddbffed372f43022d2cfaa2d7bdb1110e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `d6389a08871df9e5e1737c5ebebc812c900f97d2168766da0cba7353c3ef504c`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `26151898fe19ac90e4d68a83b2386cc44c50bff495e31d2580f42b1192c7c3cb`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `e2d25943949ff8d3a5878d127924948e42d640fff9b26a4f9a70f2857ecef3a9`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `09e40b0ca48d86b9cd97540e6fa6a0721880889c867b210f190a6021f8d96ce3`.
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
| `Question and contribution` | 40 | 1 | `HEADING_TEXT_MATCH` |
| `The literal finite object` | 65 | 1 | `HEADING_TEXT_MATCH` |
| `Source model and placement control` | 100 | 2 | `HEADING_TEXT_MATCH` |
| `Exact finite identities` | 132 | 2 | `HEADING_TEXT_MATCH` |
| `Certificate protocol` | 160 | 3 | `HEADING_TEXT_MATCH` |
| `Finite results` | 176 | 3 | `HEADING_TEXT_MATCH` |
| `Two-scale audit` | 211 | 3 | `HEADING_TEXT_MATCH` |
| `Exact local anchor` | 230 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and claim boundary` | 248 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 275 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 285 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `88` before writing and `88` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `18`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `10d2f612a18b04baceb7a211965d2f96b2d6ebe4efe74f8e2d97cba58dc58e05`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 54–56 | `e6823e4c47a927edcafcec1a388edbd5fa032aee742c72113e8c2d67d3b111de` |
| D02 | \[...\] | 68–70 | `ef00deb1077ad608cf8719ca830a5278889cb260b18a0c1c71d2acd970398f30` |
| D03 | \[...\] | 72–74 | `9cda7939c1f425097e58d032fae1256509f53d831660a262ff4bf5c98e4344bd` |
| D04 | equation | 77–82 | `52c52614efd7a3371466b6f7d6717a7dcb8e5d4edbfc44165f8cd713bf7b44c9` |
| D05 | \[...\] | 85–87 | `6dc68a973de60528f95115754d021b8052e31e6f1633b51dc797892274cee233` |
| D06 | align | 92–96 | `664d8b5000f6b03649040230d03063b125cb69077a511f26a0d2a73d9a3e6491` |
| D07 | \[...\] | 103–109 | `ff62ea1b9bbaf7f3e7eb5f575962b3dff9488c1620fa7dd84b65dd16ee5a0a53` |
| D08 | equation | 111–115 | `3e8a10210ea21f62bf39b52503ef1a2db588b01cf9b754d9987406d12a423fda` |
| D09 | \[...\] | 124–126 | `3cafcf5529414d3b71b8ed1ccf88b254170b1cee49cfed2ac4651d0496788fca` |
| D10 | \[...\] | 137–140 | `bcc8930e0ac924d0e75d9bca60f698e2953f9f9094afb09117b92b8a68abee3f` |
| D11 | \[...\] | 142–145 | `f36c38b71793f343a7f5366b37e548587d45a2b642328749e3274679bb406868` |
| D12 | \[...\] | 153–155 | `fd80b07624bc334e883a3860cc2ae475539f2844f3083efa51cd14c723d2d4ef` |
| D13 | \[...\] | 204–207 | `ef3c754b29106770ac733d762ad5f88c76405e2e082087e8248a58dce794f156` |
| D14 | \[...\] | 217–220 | `16d2e60fec1cb19097f5007984f7c74f3b4eb85393cbc6d26a30f995acb1bda4` |
| D15 | \[...\] | 221–225 | `c7dc7c755b39923548d68c4d77cb5fe322e1aecebfba9513c8d5c03231a9e3f4` |
| D16 | \[...\] | 234–236 | `eda3a99dc7d9c3d59f62db92be5dc07585e639b5768c2132d632ef5b2e9b6b37` |
| D17 | \[...\] | 238–242 | `b8512bf32b0772bd9c30ecfa3bcaca327ff340a4b801b5bf71f8076ab57e9add` |
| D18 | \[...\] | 265–270 | `7736e6284fec396d00a934e7675e9cacd86e0c103ce291e2ab35ca1498295716` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 22: `We test whether the source-native finite V59 residual used in the preceding`
- TeX line 26: `shell anchors, two kernel exponents, and four fixed sign laws.  The exact finite`
- TeX line 34: `finite numerical observations, not a growing arithmetic estimate.  The`
- TeX line 35: `principal contribution is a finite placement-sensitivity obstruction to reading`
- TeX line 43: `finite sign pattern can be misleading if it is tested at only one origin or if`
- TeX line 45: `attached the finite V59 residual to the operator.  We now make the smallest`
- TeX line 50: `The paper contributes four finite facts.  First, it provides a two-origin,`
- TeX line 52: `same exact source-coordinate Gram decomposition for every finite row.  Third,`
- TeX line 61: `Every statement below is finite.  A finite row count is not a uniformity`
- TeX line 62: `quantifier, and a growth factor between two scales is not an asymptotic`
- TeX line 65: `\section{The literal finite object}`
- TeX line 91: `For a finite vector $v=(v_t)_{t\in I_{o,N}}$, define`
- TeX line 102: `The source is the finite V59 comparison model`
- TeX line 129: `divisibility masks and distance kernel are not assumed to commute with an`
- TeX line 132: `\section{Exact finite identities}`
- TeX line 135: `The finite product expands as $C_ev=\sum_t v_tC_ee_t$.  Therefore, by`
- TeX line 146: `Hence $E_e(v)=D_e(v)+O_e(v)$ exactly for every finite vector.  No limiting`
- TeX line 147: `interchange or arithmetic estimate occurs in this step; this is the finite`
- TeX line 157: `Gram operator that is not part of the model.  The finite control therefore`
- TeX line 168: `The independent checker does not import the producer.  It rebuilds the source`
- TeX line 176: `\section{Finite results}`
- TeX line 208: `This rules out a zero-energy component as an explanation for the finite sign`
- TeX line 209: `contrast, but it does not create an arithmetic estimate.`
- TeX line 245: `recomputed.  The anchor is a finite arithmetic sanity check, not a claim`
- TeX line 250: `The strongest finite positive result is the held-out source-native replay plus`
- TeX line 256: `The following remain open or unpaid:`
- TeX line 258: `\item a source-uniform growing $L^2$ estimate for the actual residual;`
- TeX line 268: `\texttt{FULL\_GATE\_B=OPEN},\quad`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.

- Link relocation: `papers/tpc-329-heldout-growing-source-native-audit` → `..` (existing project target or original TeX label line).
