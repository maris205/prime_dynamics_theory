# TPC-310 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `abdb8bfb644f8d81c8d74b6ac609d88d191b913b`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `21c8c39f65f089aaa31cdef3386219ab1ad7f8935a31a216132b62e7850a9754`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `c95f3c63334412ea0350baad1d007208c7f09672192bab0d1c865e8a4e859fc3`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `e3fb3fc8255e0663626429842bbf8450ca13aeb7f2c8f93322224e5a152fbbe5`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `0607e91dcbdea9f30269aadf90a63ba995764b3c2f011afcebf9b15fff506079`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC310_314.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and position on the route` | 41 | 1 | `HEADING_TEXT_MATCH` |
| `Finite protocol` | 61 | 1 | `HEADING_TEXT_MATCH` |
| `Finite algebra` | 97 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 145 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and obstruction` | 213 | 3 | `HEADING_TEXT_MATCH` |
| `Claim firewall and conclusion` | 231 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 259 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `70` before writing and `70` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `4`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `02d76286bbb16ad133d5793a2c508c411aea18ea359d23828f9dc5fef61d698b`.
- Source theorem/proof environment starts: lemma at TeX line 99, proof at TeX line 107, proposition at TeX line 113, proof at TeX line 117, proposition at TeX line 126, proof at TeX line 136.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 65–69 | `4d2167e18cca473a945a1a558caa229f609ef91b31512f8aa4b751a81209a034` |
| D02 | align | 79–89 | `f3c8adb87ab82b93cca45ab9e65afbd5617aebbab4557eedebd5afc6ab4c0742` |
| D03 | \[...\] | 102–105 | `897e202e03b9ab9e8acea1b315ad99f9286603b024230d31e331b6c917bac8fa` |
| D04 | \[...\] | 128–132 | `700013e1df246979346a8b128df9af25a27438b12d1185b69477039773760ae1` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 25: `We audit a finite common-ambient prime-shell holdout experiment under an`
- TeX line 31: `row ratios, and an equal-case geometric mean give different finite classes.  On`
- TeX line 35: `\([0.1993188213,0.8609189559]\) (right lower).  We prove the finite interval`
- TeX line 37: `row ratios.  The result is a scoped aggregation-order obstruction, not a causal,`
- TeX line 43: `The recent finite diagnostics separate increasingly precise sources of`
- TeX line 52: `answer matters before interpreting any finite preference as structural: a`
- TeX line 61: `\section{Finite protocol}`
- TeX line 93: `$1.1$, and unresolved otherwise.  The budget reference used only for a finite`
- TeX line 97: `\section{Finite algebra}`
- TeX line 99: `\begin{lemma}[Independent finite extrema]`
- TeX line 100: `Let $X_i$ be nonempty finite sets with extrema $x_i^-$ and $x_i^+$.  If the`
- TeX line 115: `are positive interval enclosures for their declared finite aggregation rules.`
- TeX line 140: `The identity does not select either map as canonical.  It instead predicts that`
- TeX line 143: `finite data.`
- TeX line 168: `thresholds by a wide margin, so their reversal is not a decimal-boundary`
- TeX line 223: `The finite obstruction is therefore two-layered.  First, TPC-309 already`
- TeX line 233: `The exact part of this paper is the selector enumeration, finite extrema rule,`
- TeX line 235: `is a numerical reproduction of padded parent intervals, not a directed-rounding`
- TeX line 237: `explicit.  We obtain no arithmetic $L^2$ estimate, no fixed-power credit, no`
- TeX line 238: `uniform asymptotic budget, no causal identification, no full Gate B passage,`
- TeX line 243: `On the locked finite TPC-309 atlas, the declared pooled, equal-case arithmetic,`

## Conversion limitations

- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:pooled` → `main.tex#L82` (existing project target or original TeX label line).
- Link relocation: `#eq:geom` → `main.tex#L88` (existing project target or original TeX label line).
- Link relocation: `#eq:pooled` → `main.tex#L82` (existing project target or original TeX label line).
- Link relocation: `#eq:geom` → `main.tex#L88` (existing project target or original TeX label line).
- Link relocation: `#tab:full` → `main.tex#L174` (existing project target or original TeX label line).
- Link relocation: `#eq:weighted` → `main.tex#L131` (existing project target or original TeX label line).
