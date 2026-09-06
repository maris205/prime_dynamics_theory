# TPC-355 source-to-Markdown conversion

## Conversion identity

- **Repository source commit:** `642a0314e9c2a8dd7eb8a83d0bbd3e22d903b18e`
- **TeX:** [`paper/main.tex`](paper/main.tex), SHA-256 `f220b9b21b044fb1ca15e16d98c4ca4b39d0898a1379f6179db6bbf7735bdb5c`
- **PDF:** [`paper/main.pdf`](paper/main.pdf), SHA-256 `0978499b12e6247e05c69e58bd59fe78ffcc337a44c466d060095683f8c851d6`
- **Converted Markdown:** [`paper/main.md`](paper/main.md)
- **Conversion tool:** `pandoc -f latex -t gfm --wrap=none` plus a metadata/abstract preface
- **Conversion status:** `FULL_TEX_TO_MARKDOWN_MECHANICAL`
- **Semantic review status:** `SCOPED_REVIEW_AGAINST_README_AND_PROOF_PACKAGE`
- **References:** no bibliography/reference section is present in the source TeX; the inventory therefore remains conservative.

## Source location map

| Source section | TeX line | PDF page (inferred from section text) | Match score |
|---|---:|---:|---:|
| `Question and scope` | 39 | 1 | 3 |
| `Finite operator and normalization` | 55 | 1 | 3 |
| `Exact finite identities` | 86 | 1 | 3 |
| `Frozen protocol and audit` | 109 | 2 | 3 |
| `Results` | 147 | 2 | 3 |
| `Interpretation and route status` | 214 | 2 | 3 |
| `Reproducibility` | 240 | 2 | 3 |

The abstract begins before the first section in the front matter. PDF page numbers refer to the preserved compiled `main.pdf`; TeX line numbers refer to the exact source hash above.

## Formula and theorem-prerequisite audit

- Source has `3` displayed-equation markers before conversion; the Markdown retains the corresponding TeX math as Pandoc inline/display math.
- The converted claim was checked against the paper README and available proof/application materials; no stronger theorem, asymptotic conclusion, physical identification, arithmetic advance, fixed-power credit, Route-B closure, or twin-prime conclusion was added.
- Proof package present: `PASS`.
- README scope boundary present: `PASS`.
- Source proof/claim symbols represented: `PASS` (displayed formulas, inequalities, sums, masks, and named quantities are retained in the Markdown math).
- Finite-only boundary preserved: `PASS` (source and available package materials state the finite synthetic scope).

### Declared prerequisites

- **Domain/premises:** use the finite synthetic assumptions stated in the source manuscript and available package materials; do not silently generalize them.
- **Exact/computational evidence:** certificate, independent checker, and stress commands remain linked where present; this conversion does not reclassify computation as an arithmetic proof.
- **Scope gate:** the finite operator, predeclared panel, computed profile, and audit language remain finite-scope objects; no scale/origin uniformity, arithmetic estimate, fixed-power credit, Route-B closure, or twin-prime conclusion is inferred.

## Audit note

This record audits provenance and theorem-boundary preservation. It is not an independent proof certificate; the TeX manuscript, proof package or available notes, code, certificate, and Bridge-B checks remain the authoritative release chain.
