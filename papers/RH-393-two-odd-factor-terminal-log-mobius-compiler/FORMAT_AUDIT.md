# RH-393 format audit

## Source and build

- Exact PDF title: *Two-Odd-Factor Terminal-Log Möbius Compiler and the
  Multi-Shift Squarefree Landscape*.
- LaTeX and BibTeX complete without warnings, undefined citations, overfull
  boxes, or underfull boxes.
- Five bibliography keys are cited and all five resolve.
- The manuscript uses A4 paper with one-inch margins.
- The frozen source, bibliography, PDF, and log hashes are hard-gated by the
  archive builder.

## PDF

- `main.pdf` has six A4 pages and is unencrypted.
- Ghostscript null-device validation succeeds.
- `pdftotext` extracts the title, theorem statements, formulas, source
  boundary, and declarations without replacement or error markers.
- All 20 reported font rows are embedded, subset, and Unicode-mapped.
- The semantic PDF is byte-identical to `main.pdf`.

## JSON and text

- Result, schema, manifest, and report use sorted two-space-indented UTF-8 JSON
  with one terminal line feed and no NaN/Infinity values.
- Strict loaders reject duplicate keys.
- Publication text members are UTF-8 and have exactly one terminal line feed,
  with the generated LaTeX log excluded from the hand-edited EOF gate.
- No cache, symlink, filename sentinel, literal sealing sentinel,
  editor-temporary, or special publication member is permitted.

Verdict: format gate passes.
