# RH-394 format audit

## Source and build

- Exact title: *Odd-Parity Terminal-Log Möbius Compiler and the Complete
  Three-Shift Table Law*.
- LaTeX and BibTeX complete without warnings, undefined references or
  citations, overfull boxes, underfull boxes, or fatal errors.
- Four bibliography keys are cited and all four resolve.
- The manuscript uses eight A4 pages with one-inch margins.
- The archive hard-gates the frozen source, bibliography, PDF, and log hashes.

## PDF

- `main.pdf` is 364,403 bytes, eight A4 pages, and unencrypted.
- Ghostscript null-device validation succeeds.
- `pdftotext` extracts the title, theorem statements, equations, source
  boundary, limitations, declarations, and references without error markers.
- All 23 reported font rows are embedded, subset, and Unicode-mapped.
- The semantic PDF is byte-identical to `main.pdf`.

## JSON and text

- Result, schema, manifest, and report use sorted, two-space-indented UTF-8
  JSON with one terminal line feed and no NaN or Infinity values.
- Strict loaders reject duplicate keys; recursive comparators retain exact
  Boolean, integer, and sequence types.
- Publication text members are UTF-8 with exactly one terminal line feed;
  the generated LaTeX log is excluded from the hand-edited EOF gate.
- Whole-tree gates reject unlisted regular files, symlinks, special paths,
  caches, bytecode, filename sentinels, literal sealing sentinels, editor
  temporaries, carriage returns, and EOF defects.

Verdict: format gate passes.
