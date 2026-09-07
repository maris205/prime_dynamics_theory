# TPC-322 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `88c46824c79e9c202a698cf4db36fcaf98260537`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `f7b8fd0add2c2b5dd20ca9990212a51c9ed5e7cf58aedc49a8a3313a4dc427e1`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `46c7cb5f8990fbf366fa484c5f02ab3e98b03300b294c108c37d5ab46852b03c`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `09d9bda32b011542eb27e7e314ab5c6b3c18cf0183f3317604126c1ce9af5c10`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC320_324.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 44 | 1 | `HEADING_TEXT_MATCH` |
| `Literal blocks and the direct-sum output` | 61 | 1 | `HEADING_TEXT_MATCH` |
| `Signed diagonal projection` | 87 | 2 | `HEADING_TEXT_MATCH` |
| `Cross-block Gram and exact algebra` | 129 | 2 | `HEADING_TEXT_MATCH` |
| `Finite protocol` | 147 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 168 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and route status` | 213 | 3 | `HEADING_TEXT_MATCH` |
| `Statements` | 234 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 253 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `72` before writing and `72` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `12`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a73a14cacdbfe0710760ab6d676ae7e126029aed832ea8f03d248ca6ca3df851`.
- Source theorem/proof environment starts: proposition at TeX line 102, proof at TeX line 111.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 65–70 | `758eeb25e0ff8faaba36534207574635df0769e6bab03f7078c5e8e2572f7a6c` |
| D02 | equation | 73–77 | `6244784040a79c62cedc4248da2011a1ec35574398459155c0e7c5d72d771f25` |
| D03 | equation | 79–82 | `001591b89bb9abab4fc081143d81e92e8000c872c27954f055b776842371c129` |
| D04 | equation | 90–94 | `6f50f3d31960b59557ecd490423ca9838b95c0f2a9f835269c4f4c7f22fe2ff3` |
| D05 | equation | 97–100 | `2f60485730af1657793696362ab1232bb29a93df3200f45b288d1b40f228106c` |
| D06 | equation | 104–109 | `85abc5e6fe23b4c609ba982416deae84bef30ee651c7beed5638a0274e2ce4b8` |
| D07 | equation | 120–124 | `5157013e961f33ffc1e902b66d4a8443650c98ba4a28a81e1def6a96f38b289c` |
| D08 | equation | 132–135 | `6b46bb02669f358770f287cb9d58c4871002fbed3ef53531bbc8321d1bdbaa32` |
| D09 | equation | 138–142 | `48d6d019eecd62e6f9e7c1dfd4767b4de8264c91fdc31f5ab57495db9f675ca5` |
| D10 | \[...\] | 150–152 | `b87ec71983081215a6b679cac4fbf88eb91eb0cf80450bd8f6a4df796789260f` |
| D11 | \[...\] | 193–195 | `7c1777604d16245c595c9f57b864ee719b97347760705beab6d6efb002275023` |
| D12 | \[...\] | 197–199 | `e55824c31b4afab5f000f5d52ad6664ece6f94710b551dff43ebdf4a38c2cfae` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 26: `The preceding finite audits used a positive-semidefinite direct-sum Gram`
- TeX line 29: `therefore does not specify how cross-prime signs are to be reassembled.  We`
- TeX line 30: `introduce a finite operator-level interface: a sign-labelled isometric`
- TeX line 37: `contracts on 21 rows.  The finite ratios range from`
- TeX line 39: `precise signed interface and a finite sign-law obstruction; they do not`
- TeX line 56: `The answer below is finite and operator-level.  It is deliberately agnostic`
- TeX line 58: `separation matters: a sign pattern that contracts one finite operator is not`
- TeX line 103: `For every finite block family and every sign vector $e$,`
- TeX line 136: `It is positive semidefinite, and $D=\tr(H^{\rm blk})$.  Expanding`
- TeX line 147: `\section{Finite protocol}`
- TeX line 163: `order and uses 'einsum' for each block inner product; it does not import the`
- TeX line 170: `Table~\ref{tab:atlas} reports the finite sign-law census.  ''Below'' and`
- TeX line 177: `\caption{Finite operator-level reassembly census on 24 rows.}`
- TeX line 192: `The exhaustive minimum ratio lies in the finite range`
- TeX line 204: `index-alternating choice mostly cancels them, with three finite reversals in`
- TeX line 215: `The positive result is a typed finite interface: the previously implicit`
- TeX line 220: `The obstruction is equally important.  A finite sign vector exists in both`
- TeX line 223: `law.  The result is not a contradiction: $\phi_e=\rho_e/m\leq1$ always, and`
- TeX line 227: `No arithmetic advance is claimed.  The signs were selected by finite`
- TeX line 236: `\paragraph{Data availability.} All finite inputs, source code, certificate,`
- TeX line 247: `\paragraph{Funding.} No external funding is claimed for this finite audit.`
- TeX line 256: `without hiding the cross-prime terms.  Its 24-row atlas establishes finite`
- TeX line 261: `from the present finite ratios.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:coherent` → `main.tex#L99` (existing project target or original TeX label line).
- Link relocation: `#tab:atlas` → `main.tex#L178` (existing project target or original TeX label line).
