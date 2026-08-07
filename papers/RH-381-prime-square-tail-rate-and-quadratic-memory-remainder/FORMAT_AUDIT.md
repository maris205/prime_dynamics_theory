# RH-381 format audit

Status: **PASS**

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` completed
  successfully and converged after bibliography and cross-reference passes.
- Final `main.log` has 655 lines. A case-sensitive scan for TeX errors,
  warnings, overfull/underfull boxes, undefined references, multiply-defined
  labels, fatal errors, and emergency stops returned zero matches.
- The PDF is A4, unencrypted, unrotated, PDF 1.5, and has 7 pages.
- `pdffonts` reports 22 font rows; every row is embedded, subset, and has a
  Unicode map.
- Ghostscript null-device replay returned zero.
- `pdftotext` extraction returned zero and produced 14,429 bytes of text;
  no unresolved `??` marker was present.
- The semantic PDF is byte-identical to `main.pdf`, with SHA-256
  `0ddb244cb80d95d04c077303f6ed924f8751ef4efde8137a97cfc1830e8767ca`.
- The final auxiliary file has 34 labels, 27 manuscript cross-references,
  and 4 bibliography citations; all resolve.
- All seven rendered pages were inspected at 140 dpi. No clipping,
  collision, blank page, broken rule, malformed equation, or overflow was
  found.
- PDF metadata contains the intended title, author, subject, keywords, and
  August 7, 2026 date.

The final visual result is a compact seven-page mathematical short paper.
