# TPC-326 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `b13909fddbffed372f43022d2cfaa2d7bdb1110e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `53e296ee7d02afb3ad3a1a93ea42da0feef5c51a4e9e364817513d6244033c95`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `26151898fe19ac90e4d68a83b2386cc44c50bff495e31d2580f42b1192c7c3cb`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `e8e8d50aae846c809c9d8737812cdb8f63669662b7d9708521c0abf4325e6f7e`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `ec20075c56ef43b0320cf5a34f4e5d237caffeb005785202005d1f306b8e4942`.
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
| `Question and claim boundary` | 33 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen operator and cross-origin test` | 73 | 2 | `HEADING_TEXT_MATCH` |
| `Certified results` | 98 | 2 | `HEADING_TEXT_MATCH` |
| `What the replication establishes` | 150 | 2 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 171 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 188 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `38` before writing and `38` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `0e27b9deaf5fee19d30942921e71206f65628d3032ff9b089691513b9f3221d8`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 38–41 | `45f1ec37d57b799fdc26c0682163c0dd54fa77fe35cb65422343d12f0151909b` |
| D02 | equation | 44–49 | `4e18a0b31bfb3ab9d9aee6a1e2ad47878fc7b1f30517393797c8f8055508b466` |
| D03 | \[...\] | 51–55 | `ec93802632bcc58f2bcb02703e4ae7f4a148f96cb01ea39439b9919f5e74210a` |
| D04 | \[...\] | 61–65 | `b27e9ebbddad4f9dffd2c352d4dc1a4eb588a9542a32fc47b64a3729b4bc4a7a` |
| D05 | \[...\] | 83–86 | `157807ab7d8a1853123f8656c51eae24ddb6c5057e3e5dd878a8e2eb7c096a47` |
| D06 | \[...\] | 162–166 | `0f3817368d1c39b7a0255552db612da21117897b1f3fed01865100a537d390d4` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 9: `\title{Cross-Origin Replication of a Finite Source--Scale Prime--Shell Spectral Ladder}`
- TeX line 17: `Finite source--scale experiments can be misleading if their profile is tied`
- TeX line 26: `with the parent within predeclared finite thresholds.  Independent reverse`
- TeX line 28: `normal/optimized replay all pass.  This is a finite cross-origin replication`
- TeX line 29: `certificate only: it supplies no uniform-in-source theorem, arithmetic`
- TeX line 66: `The release claim is deliberately finite:`
- TeX line 68: `\textbf{NUMERICALLY CERTIFIED FINITE:} the new origin reproduces the`
- TeX line 75: `Every displayed Gram matrix is a finite Gram matrix, hence positive`
- TeX line 76: `semidefinite.  Its trace-normalized decreasing spectrum is therefore a`
- TeX line 77: `probability vector whenever the trace is positive.  This exact finite typing`
- TeX line 79: `\cite{horn2013matrix} for the underlying finite-dimensional spectral facts.`
- TeX line 94: `signed/direct trace ratios.  We compare these finite diagnostics with the`
- TeX line 106: `\caption{All-plus finite ladder at the second origin.}`
- TeX line 152: `The strongest conclusion is a finite adversarial one: the TPC--325 readout`
- TeX line 155: `control evidence for the finite operator experiment.  They do not establish`
- TeX line 157: `a growing-scale limit, and the threshold comparison does not quantify an`
- TeX line 165: `\texttt{FULL\_GATE\_B = OPEN}.`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.

- Link relocation: `#tab:ladder` → `main.tex#L107` (existing project target or original TeX label line).
