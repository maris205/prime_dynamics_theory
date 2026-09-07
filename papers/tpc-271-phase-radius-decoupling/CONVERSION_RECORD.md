# TPC-271 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `6be994e34a06fda0de2ed0bcaa42ff3db716ffef`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `7bfe4df4bb1975e48638164628ff4fd86cad52d83734e110095a21ad40cbf417`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `eb62e2304285ad8e2b0a87a4e05027642fa72a203c89f6cb13a8a0b44489e967`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `df4790236bedb4a2ed74122008725a4886df389baa002a6784f17db33b04e9e0`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC270_274.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Position and claim firewall` | 48 | 1 | `HEADING_TEXT_MATCH` |
| `Projected residual coordinates` | 65 | 1 | `HEADING_TEXT_MATCH` |
| `Exact lane factorization` | 82 | 2 | `HEADING_TEXT_MATCH` |
| `Certified finite result` | 110 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and limits` | 160 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 177 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 187 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `54` before writing and `54` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `9bff9130a5299284edb76419447e06a1c5c5c7cd455c9137f9fbdd6d15d69257`.
- Source theorem/proof environment starts: lemma at TeX line 92, theorem at TeX line 136.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 58–60 | `7c3507e9c3685d65a14861fade61bbe09d497321d376071306da5f310ad1118b` |
| D02 | \[...\] | 69–73 | `c00cbe910e9a0b8c25bab0ed653cf69fc3452041328b67cf4db5f8def18ded29` |
| D03 | \[...\] | 75–78 | `3506b4b80298c92be3dd3d634ccb3e91fa3dc00446eba124b1e0c464bb818820` |
| D04 | \[...\] | 85–90 | `8680d18dc8a33a0da7fbf790af7f57c73b4c7b3f477202c86af71e550954fae8` |
| D05 | \[...\] | 94–99 | `6cb0efe32e6e0b5763fbe78e32c4d816319b72a985a7aeb4bfc79402b9285511` |
| D06 | \[...\] | 113–116 | `f53a7b4b982352fe9898ad8feb4ec7ab1965fa5a4bf10e07f0537487c97e3fde` |
| D07 | \[...\] | 140–143 | `f5b5f7b1c6c675fe75424a732c17d483e438769c9ce8bfe040811aeaadfb9804` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 21: `\title{Phase--Radius Decoupling in a Finite V59 Residual}`
- TeX line 31: `TPC-270 found a strong finite variation in an endpoint-normalized residual`
- TeX line 39: `lane attribution, and phase alignment.  On the registered TPC-269 finite`
- TeX line 44: `numerically certified finite phase--radius decoupling audit, not an asymptotic`
- TeX line 50: `The TPC chain studies a literal finite V59 physical operator containing the`
- TeX line 55: `and found a finite DROP--RISE--RISE--DROP pattern.`
- TeX line 59: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE\_PHASE\_RADIUS\_DECOUPLING\_AUDIT}.`
- TeX line 61: `The word ''finite'' is essential: the registered rows are a diagnostic`
- TeX line 62: `interface, not a proved asymptotic sequence.  No finite ratio is promoted to a`
- TeX line 68: `contrasts.  On each finite row put`
- TeX line 84: `The algebraic number $N^{5/3}$ is unnecessary at finite scale.  Define`
- TeX line 92: `\begin{lemma}[finite identities]`
- TeX line 110: `\section{Certified finite result}`
- TeX line 136: `\begin{theorem}[finite phase--radius decoupling]`
- TeX line 151: `phase label is unchanged.  This is an attribution statement about the finite`
- TeX line 152: `registry, not a claim that phase and radius are statistically independent.`
- TeX line 171: `uniform source-level sequence; the phase sign does not establish an eventual`
- TeX line 173: `$R_N\ll N^{5/3-\delta}$; and the radius product is not an arithmetic $L^2$`
- TeX line 175: `credit is zero and full Gate B remains open.`
- TeX line 179: `TPC-271 adds a joint coordinate system to the TPC-267--270 finite chain.  The`
- TeX line 181: `finite phase--radius decoupling: negative-real scalar phase persists while the`
- TeX line 183: `The next source-level task is a uniform signed-phase estimate coupled to an`
- TeX line 195: `L. Wang, ''Cross-scale endpoint-normalized radius in a finite V59 residual,''`

## Conversion limitations

- 4 whitespace separator(s) inserted after inline math before numeric prose to preserve dollar-delimiter parsing; formulas and original TeX are unchanged.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
