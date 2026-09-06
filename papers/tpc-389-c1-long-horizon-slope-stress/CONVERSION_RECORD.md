# TPC-389 conversion record

## Conversion identity

- **Repository source commit:** `a8e14036a6516d08a787b6e0af53141e3dc26b13`
- **TeX:** [`paper/main.tex`](paper/main.tex), SHA-256 `06fa793730e8cb345de96745ac8f0f51bfd726f1db13eae61cde4410164ddaeb`
- **PDF:** [`paper/main.pdf`](paper/main.pdf), SHA-256 `c3cac6b1c120279ec26715e88dd95b5864ddd0d8eae87d8f205ebf8b006b8abe`
- **Converted Markdown:** [`paper/main.md`](paper/main.md)
- **Conversion tool:** `pandoc -f latex -t gfm --wrap=none` plus a metadata/abstract preface
- **Link normalization:** the source's project-directory link is remapped to `../` from `paper/main.md`; its target package is unchanged.
- **Conversion status:** `FULL_TEX_TO_MARKDOWN_MECHANICAL`
- **Semantic review status:** `SCOPED_REVIEW_AGAINST_README_AND_PROOF_PACKAGE`
- **References:** no bibliography/reference section is present in the source TeX; the inventory therefore remains conservative.

## Source location map

| Source section | TeX line | PDF page (inferred from section text) | Match score |
|---|---:|---:|---:|
| `Question and claim boundary` | 30 | 1 | 4 |
| `Finite proxy` | 53 | 1 | 2 |
| `Forecast interface` | 70 | 1 | 2 |
| `Certification and results` | 95 | 2 | 3 |
| `Conclusion and next clue` | 133 | 2 | 4 |
| `Reproduction` | 153 | 2 | 1 |

The abstract begins before the first section in the front matter. PDF page numbers refer to the preserved compiled `main.pdf`; TeX line numbers refer to the exact source hash above.

## Formula and theorem-prerequisite audit

- Source has `8` displayed-equation environment markers before conversion; the Markdown retains the corresponding TeX math as Pandoc inline/display math.
- The converted claim was checked against the paper README and `PROOF_PACKAGE.md`; no stronger theorem, asymptotic conclusion, physical identification, arithmetic advance, fixed-power credit, Route-B closure, or twin-prime conclusion was added.
- Proof package present: `PASS`.
- README scope boundary present: `PASS`.
- Source proof/claim symbols represented: `PASS` (displayed inequalities, sums, roots, and named quantities are retained in the Markdown math).
- Finite-only boundary preserved: `PASS` (source and proof package both state the finite synthetic scope).

### Declared prerequisites

- **Domain/premises:** use the finite synthetic assumptions stated in the source manuscript and its proof package; do not silently generalize them.
- **Exact/computational evidence:** certificate, independent checker, and stress commands remain linked by the package README; this conversion does not reclassify computation as an arithmetic proof.
- **Scope gate:** the source’s finite-only and open-gate language is preserved verbatim in substance.

## Audit note

This record audits provenance and theorem-boundary preservation. It is not an independent proof certificate; the TeX manuscript, proof package, code, certificate, and Bridge-B checks remain the authoritative release chain.
