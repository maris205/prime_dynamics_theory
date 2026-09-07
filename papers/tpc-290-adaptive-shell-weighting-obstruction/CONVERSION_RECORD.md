# TPC-290 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `7bba57e68d04514ee33ab2192a507a1f4edfebab`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `f0ac2d2c1313af2d0586c62d00c628265d544e1785f4b8ee903b9425bc6db5e6`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `cda6e57289c395681c2ef88bb3f4b4daaa14d995628968519967a29346ec0fb1`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `bb6f65d2f5b63902a17223f52fdc3e76c5cb7bbe11d79faea5960c61cd30947a`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `d8897366e6fc7722568f0e5681a11e15c504f53bc81e02aa566f10dc50b34dfc`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC290_294.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Route position and question` | 50 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen physical model` | 66 | 1 | `HEADING_TEXT_MATCH` |
| `Weighted Gram lemmas` | 87 | 2 | `HEADING_TEXT_MATCH` |
| `Finite protocol` | 150 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 171 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and claim firewall` | 208 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 232 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 249 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `58` before writing and `58` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `5bb33c3f42740ae908f47921fb4514fa7849ff2c754031e17c4b85cf0edcabaa`.
- Source theorem/proof environment starts: lemma at TeX line 89, proof at TeX line 98, proposition at TeX line 103, proof at TeX line 108, proposition at TeX line 113, proof at TeX line 123, lemma at TeX line 133, proof at TeX line 142.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 32–35 | `aeb3092b628825e81484fa047a2c68e4100d240cdd948e349511693c688a9bf3` |
| D02 | \[...\] | 70–74 | `a641d953a37284c10446dcf660c55e3b027e135132e489b2ff3d09a4ad996782` |
| D03 | \[...\] | 76–79 | `4095466d15d602b959c36ab9e866d11b5d7d2aad9c5c9653aec2c62a2ae72993` |
| D04 | \[...\] | 81–83 | `d715e6f846a0503f16e9deb95eb89b804c53b0f93910f1fff82126e8cc12cc72` |
| D05 | equation | 91–95 | `904658b740e4abb1398f6a54444c50ff3127b2b0d84a2abfe5c0ae396e387890` |
| D06 | equation | 116–120 | `3d93968a9404835602ec296e1d28c905578f31b2ac9369f0c9849a10eb96722d` |
| D07 | \[...\] | 126–129 | `724fd1627002431039eb14464eb009f83e456498cebd9f1570f76f0287c3d2ee` |
| D08 | equation | 135–138 | `aa111256457655e184469f84015d865cb2be6017fed67038b5c9593f517a14ec` |
| D09 | \[...\] | 156–158 | `17427613cc8a57e600bbe2ba70b6bd712fd6b8c14d251a991d85bc2d660e98bc` |
| D10 | \[...\] | 200–202 | `34a7a4eb52a1e21dc898c7d4ea7a2540e1301650257ec374981660bf8821dc6c` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 27: `TPC-289 found a finite late-shell block whose physical prime-component`
- TeX line 40: `TPC-289 18-row grid tests uniform, inverse-diagonal, and linear-taper`
- TeX line 45: `coherence wall; the only finite nonnegative escape is sparse concentration on`
- TeX line 46: `a sign-flip pair.  This is a structural obstruction, not an asymptotic`
- TeX line 53: `scalar cancellation to the physical output Gram and showed finite full-rank`
- TeX line 63: `and a finite certificate.  We do not alter the source, kernel, deletion rule,`
- TeX line 84: `The finite computations have $d_q>0$.  The unweighted physical ratio from`
- TeX line 146: `For uniform weights, $\kappa(w)=|S|$, so \eqref{eq:effective} recovers the`
- TeX line 150: `\section{Finite protocol}`
- TeX line 159: `respectively called uniform, inverse-diagonal, and linear taper.  Scaling a`
- TeX line 160: `weight vector does not change $R(w)$.  In addition, the certificate evaluates`
- TeX line 161: `the equal-pair ratio \eqref{eq:pair} for every pair and the uniform ratio after`
- TeX line 164: `The positive-block thresholds are the inherited finite values`
- TeX line 212: `finite scan refines this statement rather than universalizing it.  An early`
- TeX line 221: `\item the three policies are not an optimization over all weighting rules;`
- TeX line 222: `\item the sparse witnesses are not a full-shell $L^2$ saving;`
- TeX line 223: `\item no arithmetic $L^2$ estimate, fixed-power credit, Gate-B conclusion, or`
- TeX line 242: `FINITE: 54/54 full-support policies amplified; 18/18 drop-one amplified`
- TeX line 243: `FINITE: 3 sparse equal-pair subunit witnesses in one sign-flip row`
- TeX line 244: `OPEN: growing diffuse weighted theorem and arithmetic L2`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:weighted` → `main.tex#L94` (existing project target or original TeX label line).
- Link relocation: `#eq:weighted` → `main.tex#L94` (existing project target or original TeX label line).
- Link relocation: `#eq:weighted` → `main.tex#L94` (existing project target or original TeX label line).
- Link relocation: `#eq:effective` → `main.tex#L119` (existing project target or original TeX label line).
- Link relocation: `#eq:pair` → `main.tex#L137` (existing project target or original TeX label line).
- Link relocation: `#eq:effective` → `main.tex#L119` (existing project target or original TeX label line).
