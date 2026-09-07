# TPC-274 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `6be994e34a06fda0de2ed0bcaa42ff3db716ffef`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `7d5052b1429fbd34439ac243cfca5336bf7b3ec398e9d33a124aea7bf1564b95`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `3253b4bd9658d0f7c72e7d160f4d39fd2ae6768285da6a719aa8e5ec29d6cd92`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `d18591b363db07eb3785c9fb83898acd7a05f5a6cd30f881ed07e6c90dd54c93`.
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
| `Question and claim ceiling` | 43 | 1 | `HEADING_TEXT_MATCH` |
| `The locked finite operator` | 63 | 1 | `HEADING_TEXT_MATCH` |
| `The projected Frobenius theorem` | 91 | 2 | `HEADING_TEXT_MATCH` |
| `Exact finite audit` | 124 | 2 | `HEADING_TEXT_MATCH` |
| `Route evaluation and limits` | 179 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 197 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 206 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `63` before writing and `63` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `24d10284e78349c11116cb7544de44825078c5ed7a05cf5061584b0eac3fc9c5`.
- Source theorem/proof environment starts: theorem at TeX line 93, proof at TeX line 104, theorem at TeX line 154, proof at TeX line 161.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 48–50 | `fe3daacbc5786c1daa57f5078ae414f89c865d042b35d3eee29854b8eb1401e6` |
| D02 | \[...\] | 56–59 | `ce364b3c5ca9f53353b6eb9722bc4ac31b6fd02ab619532710433f69ccc63907` |
| D03 | \[...\] | 68–72 | `9fca1365b55602d11ee71ab01e6fcc90b4d9fb22e68341efff14a4198b81d4ec` |
| D04 | \[...\] | 78–81 | `8c97c46e512f41706b63213e103859b3a88aedcedc076b94c977edf59ab121c8` |
| D05 | \[...\] | 85–88 | `a8e017ce5e891a1785844fab0d8a178accb8b238091595de640cb578a097983c` |
| D06 | \[...\] | 95–97 | `72726aa8197d74d1019206398893e30cf2655a80a69eca74f71d6b92e5e77e2a` |
| D07 | \[...\] | 99–101 | `1b57f99a45d24dd11dee8a610996d6acc23f7765d32b0568f6d42dd3b3e8f937` |
| D08 | \[...\] | 106–109 | `c2fe1f554f29667655033c8304819cd76f78ac291a1bd9f9e2890fac89e977b3` |
| D09 | \[...\] | 117–119 | `14f2b0811220deb5a334b12238bf14bcd4edd26250e4fb1c7dd402eeb4c18e7d` |
| D10 | \[...\] | 186–192 | `f39fbdd50c4d3f4e339ee14a76002e08e43102663f86c38e380a0b461c79997e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 29: `TPC-273 showed that a finite correlation margin can move across quantitative`
- TeX line 34: `\(\Gperp=\|\Aperp\beta\|_2^2\).  We prove the exact finite inequality`
- TeX line 39: `of a norm-only output proof; it is not an upper bound on the actual margin,`
- TeX line 52: `TPC-273 then demonstrated finite cutoff sensitivity.  The present paper asks`
- TeX line 57: `\texttt{PROVED\_EXACT\_FINITE} \quad+\quad`
- TeX line 58: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE},`
- TeX line 63: `\section{The locked finite operator}`
- TeX line 94: `For every finite real or complex matrix \(B\) and vector \(v\),`
- TeX line 112: `does not use an independence or probabilistic assumption; its cost is that it`
- TeX line 116: `For positive finite lanes define the conservative proxy`
- TeX line 124: `\section{Exact finite audit}`
- TeX line 150: `\caption{Selected outward finite bounds.  The complete certificate has 12`
- TeX line 154: `\begin{theorem}[registered finite gap]`
- TeX line 172: `The gap is not a claim about a limiting sequence.  It is a finite diagnostic`
- TeX line 181: `The exact inequality is a reusable structural lemma, and the finite gap is a`
- TeX line 184: `registered interface.  It does not refute a signed estimate using the actual`
- TeX line 185: `coefficient phases.  In particular, the following gates remain open:`
- TeX line 188: `\texttt{SOURCE\_LEVEL\_OUTPUT\_BOUND}=\texttt{OPEN\_ASYMPTOTIC}\\`
- TeX line 189: `\texttt{SIGNED\_FOUR\_PACKET\_REASSEMBLY}=\texttt{OPEN}\\`
- TeX line 193: `The finite rows also contain one positive phase, which is retained rather than`
- TeX line 204: `is a finite, reproducible obstruction to the norm-only shortcut.`
- TeX line 211: `L. Wang, ''Finite Cutoff-Sensitivity Obstruction for a V59 Residual,'' TPC-268`
- TeX line 214: `L. Wang, ''A Finite Margin-Stability Matrix for the Literal V59 Residual,''`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
