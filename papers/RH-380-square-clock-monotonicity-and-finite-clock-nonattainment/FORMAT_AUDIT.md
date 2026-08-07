# RH-380 format audit

Status: **PASS**

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` completed
  successfully and converged.
- Final `main.log` has 656 lines. A case-sensitive scan for `Warning`,
  `Error`, `Overfull`, `Underfull`, `undefined`, multiply-defined labels,
  and unresolved citations returned zero matches.
- The PDF is A4, unencrypted, unrotated, PDF 1.5, and has 8 pages.
- `pdffonts` reports 24 embedded/subset font rows; every row is embedded and
  has a Unicode map.
- Ghostscript null-device replay returned zero.
- `pdftotext` extraction returned zero and produced 18,749 bytes of text.
- The semantic PDF is byte-identical to `main.pdf`:
  `813206ae797072ca258e27e6afaf5d077f7f0203db72dcd224754cc49ab5fbcc`.
- All eight rendered pages were inspected at 120 dpi. No clipping,
  collision, blank page, broken rule, malformed equation, or table overflow
  was found.
- PDF metadata has the intended title, author, subject, keywords, and
  August 7, 2026 date.

The final visual result is a compact eight-page theoretical short paper.
