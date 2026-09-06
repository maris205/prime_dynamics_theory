# TPC-358 source-to-Markdown conversion

## Conversion identity

- **Repository source commit:** `642a0314e9c2a8dd7eb8a83d0bbd3e22d903b18e`
- **TeX:** [`paper/main.tex`](paper/main.tex), SHA-256 `e29acc87ca87c17cd9a76b5d96792297b8d6d100c3e993b817c03d1c891c6530`
- **PDF:** [`paper/main.pdf`](paper/main.pdf), SHA-256 `8a931e6cabfe29f27d8db5f8dc47aef62fd28dd63500265ec5913b13265fcb1f`
- **Converted Markdown:** [`paper/main.md`](paper/main.md)
- **Conversion tool:** `pandoc -f latex -t gfm --wrap=none` plus a metadata/abstract preface
- **Conversion status:** `FULL_TEX_TO_MARKDOWN_MECHANICAL`
- **Semantic review status:** `SCOPED_REVIEW_AGAINST_README_AND_PROOF_PACKAGE`
- **References:** no bibliography/reference section is present in the source TeX; the inventory therefore remains conservative.

## Source location map

| Source section | TeX line | PDF page (inferred from section text) | Match score |
|---|---:|---:|---:|
| `Question and scope` | 39 | 1 | 3 |
| `Model and frozen holdout` | 53 | 1 | 3 |
| `Finite inequalities and transfer criterion` | 89 | 1 | 3 |
| `Results` | 113 | 2 | 3 |
| `Controls and claim firewall` | 166 | 2 | 3 |
| `Conclusion` | 183 | 2 | 3 |

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
