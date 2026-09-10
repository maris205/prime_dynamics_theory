# TPC-211 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `9113b0a1f6ad815b4305de2610126ecefa80088bdb4b0065853a6561f49831cd`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `b612a0c82854c6516f14567fa573586a78ccc551f91cb4c1fae0d34103992851`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `b98905efcfddc837f7d3b899506d3be01fef02cfb9bc69bb99a03ebcadecb6a7`; 8 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `a1ec8fecf1443a5927f2b45a46d3aa397341520172e322038286c7527d0240e9`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC210_214.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim ceiling` | 68 | 1 | `HEADING_TEXT_MATCH` |
| `The literal product-coupled profile family` | 107 | 2 | `HEADING_TEXT_MATCH` |
| `Full divisor rank from Fourier support` | 196 | 3 | `HEADING_TEXT_MATCH` |
| `The logarithmic M\"obius packet derivative` | 278 | 4 | `HEADING_TEXT_MATCH` |
| `Why the complete packet does not finish the physical gate` | 365 | 5 | `HEADING_TEXT_MATCH` |
| `A shared-endpoint Gram obstruction` | 438 | 6 | `HEADING_TEXT_MATCH` |
| `Exact certificate and adversarial checks` | 489 | 7 | `HEADING_TEXT_MATCH` |
| `Route decision` | 521 | 7 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 545 | 8 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `131` before writing and `131` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `36`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `4081e283232057c1e4cae965d9b4c333c2913df15936265fffaff5ad9a7f2fbc`.
- Source theorem/proof environment starts: proposition at TeX line 165, proof at TeX line 182, theorem at TeX line 225, proof at TeX line 237, remark at TeX line 271, lemma at TeX line 293, proof at TeX line 305, theorem at TeX line 311, proof at TeX line 335, proposition at TeX line 424, proof at TeX line 431, theorem at TeX line 447, proof at TeX line 469.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 100–102 | `b56eb87516dfba60a419e32d91a020e575d49183a36b0c78b5aa078265c734a0` |
| D02 | \[...\] | 110–114 | `902b560bd2f045eaae52520268073dbc86722040dd8b13a498f5ee4600867315` |
| D03 | \[...\] | 117–120 | `c997f57d9f6abd04896f84e3ba6c0f455c2be3ed4cbdd26be9e700cc25671a11` |
| D04 | \[...\] | 122–129 | `5aae51381405fe3919cb6b69c7f402d2e423733a6d62eac3e00a3dca2be22cd1` |
| D05 | \[...\] | 133–138 | `1129c09a97d6a48bf776698894ef2b4ff3a0dae95ff83260bce60b91682fe58b` |
| D06 | \[...\] | 142–147 | `2a10fb47271cafe0eaef9d5200d75781d6ef64c6ba85162d2928006a0ebfda00` |
| D07 | \[...\] | 154–161 | `527522432698305ae43ea99edb310e4040fa5d9eb18b513ecd86e245c14da0a4` |
| D08 | \[...\] | 168–172 | `dd3ce699cc3322ef3f9e3bc983f24e3daa04ba92dc12bc70ea4daf6738ba24f7` |
| D09 | \[...\] | 174–179 | `5c1a3cc08c7890474e7b3adec8e638a51598d71f46e7ad23b0bc6af2c456fd53` |
| D10 | \[...\] | 185–187 | `31211fef79c7660b4eaa467aff0976c28fadad6f33f70b7f63f1451628ecd9c7` |
| D11 | \[...\] | 199–203 | `8eedbb05d7c504748d343331342147ae7345a5ee7b778d457e37b0b8502820d9` |
| D12 | \[...\] | 205–208 | `97bcb617024796850c12b664bad991c772e66eeb93d9b3cff9fa7765cc7089f2` |
| D13 | \[...\] | 210–214 | `4309909eb1def0ef10fed69665ed2fefdd924c3c9ae73b6edc911fdf190bb7ad` |
| D14 | \[...\] | 221–223 | `7e5baa5610048b2a1cb1335a12dcf66eac0bd36c9bd8901081e9ab78b6ce428f` |
| D15 | \[...\] | 228–232 | `26f09ca93e57773ba82c81372e269d6f79b66616b55ad2b4a2f826a9a33c1ef8` |
| D16 | \[...\] | 243–248 | `bdb18828c1862a192344a46394afe90f1f9fcd6db7cda9fff12a3e3713a67a47` |
| D17 | \[...\] | 250–256 | `48b8aa6df364ac8a49f0f8b62913c482d8bbe2550bda51990df5c6d23ad75014` |
| D18 | \[...\] | 261–266 | `bb98c2c3301598bf5504c16b611b00ba7247ae22b68fca19f4f5d806018462b6` |
| D19 | \[...\] | 282–285 | `5b034e363d424891f229774765ddec351144dc5b21dd4dfc73d6a064255d008f` |
| D20 | \[...\] | 296–301 | `1b31d57ae973cdd96efa31cfcc1a76f71b3430ae348a2a4018a87450a07e0dff` |
| D21 | \[...\] | 314–319 | `b4b907cc9857cacb336da450d6772cefb4a702375e47306667b38f05ea1a20af` |
| D22 | \[...\] | 321–326 | `dae281279de9a38af797fafaba3d406b7d766654ea0194ae7eddc455abf84fc4` |
| D23 | \[...\] | 328–332 | `aaed0c6a80e08e3ad686b293a7971ef42472f12c75aaca04ec63da8486622227` |
| D24 | \[...\] | 344–347 | `986b6396515e85b0867c91ae0f8e10ff332de99b8d1de684a93b1619e6e878bb` |
| D25 | \[...\] | 350–354 | `728f05d2cb8cf5f122abda3fb8e3d743f119ceb420d7df147c859d303f16ae72` |
| D26 | \[...\] | 357–361 | `7c76104805fa7f63b32a02849995c418f06d0e1f2724ce5229a4d3fb566cbe03` |
| D27 | \[...\] | 368–373 | `da01692cff86b765b439092e36f696c14242d63cb2bd17e33bafa5d303b74344` |
| D28 | \[...\] | 375–381 | `cab4c6d543700fd8c4f70b3cc9148eee806e71e4ff8e5d9b98197f7d1ca365a7` |
| D29 | \[...\] | 386–389 | `52c9a76b4df065b56b8c02a0948482ec4b91f72d821e0a6670fa00674c286dd8` |
| D30 | \[...\] | 394–399 | `201beb1b44a506e363d34620b082e443c9bb7a4aa0c81f51049c2501c52f0692` |
| D31 | \[...\] | 403–406 | `f3baf4dae0408083a74b474dbd9ddc53e6ddfa63846c100e1cd6e9e47d09dbba` |
| D32 | \[...\] | 411–417 | `42e7ec95d46c3325367706696e689a1daa2b9172d8ee5210ad022c98c5c653ef` |
| D33 | \[...\] | 441–444 | `7058e7498bbd156ea2a1cca089bb00e8dd1ff8c749396486c348e608ba26793f` |
| D34 | \[...\] | 451–455 | `bc30347b9cd13f0fadf16b1193681b492b3b95d2fd00e35f6070e65e2c6c8812` |
| D35 | \[...\] | 457–460 | `dd7ccc400ab99d40f122b527da7ffddc66f555a6a3cb6d83081095033184ff5d` |
| D36 | \[...\] | 462–466 | `8adaa3400e1ed1b240b9231055c728f5d6363eda7eba1df9216614de4a447b9c` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 12: `pdfsubject={TPC-211 finite physical profile coupling and Gram obstruction}`
- TeX line 45: `M\"obius-aligned cross-divisor Gram obstruction, while explicitly leaving open`
- TeX line 48: `and studies that interface exactly at finite modulus.  For active primes`
- TeX line 59: `unpaid.  Finally, positive-definite Gram duality constructs a single finite`
- TeX line 62: `based only on product rank or common endpoint data, not an arithmetic`
- TeX line 73: `finite Schwartz construction realizes exact M\"obius alignment and defeats any`
- TeX line 75: `does not use the literal relation between the shifted-prime tensor and the`
- TeX line 83: `This note gives the finite structural answer.  There are two parts.`
- TeX line 115: `The cutoff condition is the finite version of the V46 regime in which the`
- TeX line 149: `function one.  Thus all profiles in (2.5) live in the same finite Hilbert`
- TeX line 192: `stronger than declaring one arbitrary profile per divisor, but it does not yet`
- TeX line 280: `The full-rank theorem does not make the product structure useless.  The`
- TeX line 295: `For every finite prime set $\mathcal P$,`
- TeX line 363: `exact algebraic compression, not an estimate.`
- TeX line 365: `\section{Why the complete packet does not finish the physical gate}`
- TeX line 408: `boundary is therefore a real term, not a cosmetic change of notation.`
- TeX line 424: `\begin{proposition}[complete-packet cancellation is not a transition bound]`
- TeX line 427: `not imply a bound for (5.1) unless one additionally proves a uniform estimate`
- TeX line 445: `By Theorem~\ref{thm:fullrank}, $G$ is positive definite.`
- TeX line 447: `\begin{theorem}[finite shared-endpoint interpolation]`
- TeX line 470: `Positive definiteness of $G$ gives a unique coefficient vector $\alpha$ with`
- TeX line 478: `defects, and only the common finite endpoint is chosen by Gram duality.  It is`
- TeX line 479: `still not an arithmetic counterexample.  The endpoint in Theorem~\ref{thm:shared}`
- TeX line 481: `and does not include the $d$-dependent emitter (5.2).  The correct conclusion`
- TeX line 485: `finite rank, and a common endpoint.  It must control the truncated boundary`
- TeX line 501: `\caption{TPC-211 finite structural certificate.}`
- TeX line 518: `script all pass.  These finite results certify the algebraic statements and`
- TeX line 529: `still support finite M\"obius-aligned correlations under a shared endpoint`
- TeX line 532: `The next open theorem is narrower than the original TPC-210 question.  It is`
- TeX line 536: `arithmetic $L^2$, strict $1/400$ margin, and twin-prime endpoint remain open.`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#lem:derivative` → `main.tex#L294` (existing project target or original TeX label line).
- Link relocation: `#thm:packet` → `main.tex#L312` (existing project target or original TeX label line).
- Link relocation: `#thm:fullrank` → `main.tex#L226` (existing project target or original TeX label line).
- Link relocation: `#thm:shared` → `main.tex#L448` (existing project target or original TeX label line).
- Link relocation: `#thm:fullrank` → `main.tex#L226` (existing project target or original TeX label line).
- Link relocation: `#thm:shared` → `main.tex#L448` (existing project target or original TeX label line).
