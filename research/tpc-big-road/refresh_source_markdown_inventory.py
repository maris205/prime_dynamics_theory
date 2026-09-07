#!/usr/bin/env python3
"""Read-only inventory refresher; print an apply_patch plan or check current files."""
import argparse
from collections import Counter
import difflib
import re

from maintain_source_markdown import ROOT, digest, normalize_eof

BASE = ROOT / "research/tpc-big-road"
INDEX = BASE / "PAPER_MATERIALS_INDEX.md"
LINKS = BASE / "PAPER_MATERIALS_LINKS.md"
BATCH = BASE / "TPC_CONVERSION_BATCH_2026-09-07.md"


def compact_patch(path, value):
    old = path.read_text()
    if old == value:
        return ""
    diff = list(difflib.unified_diff(old.splitlines(), value.splitlines(), lineterm=""))[2:]
    return f"*** Update File: {path}\n" + "\n".join("@@" if line.startswith("@@") else line for line in diff) + "\n"


def link(path, label=None):
    relative = "../../" + str(path.relative_to(ROOT))
    return f"[{label or path.name}]({relative})" if path.exists() else "—"


def inventory():
    pattern = (r"^\| (RH|TPC) \| `([^`]+)` \| (\d+) \| (\d+) \| (\d+)"
               r" \| `([^`]+)` \| (.*?) \|$")
    old_rows = list(re.finditer(pattern, INDEX.read_text(), re.M))
    if len(old_rows) != 823:
        raise ValueError("inventory baseline changed; inspect before extending scope")
    rows, full = [], []
    for match in old_rows:
        program, name, _, _, _, prior_status, prior_md = match.groups()
        paper = ROOT / "papers" / name
        counts = Counter(p.suffix.lower() for p in paper.rglob("*") if p.is_file())
        record_path = paper / "CONVERSION_RECORD.md"
        reading = paper / "paper/main.md"
        status = prior_status
        representative = prior_md
        if record_path.is_file() and reading.is_file():
            record = record_path.read_text()
            if "Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`" in record:
                expected = re.search(r"Reading layer: .*?SHA-256 `([0-9a-f]{64})`", record)
                if not expected or digest(reading.read_bytes()) != expected[1]:
                    raise ValueError(f"reading layer hash mismatch: {name}")
                status, representative = "full-source-md", "`paper/main.md`"
                full.append(paper)
        if status == "full-source-md" and paper not in full:
            raise ValueError(f"unverified historical full conversion: {name}")
        rows.append((program, name, counts['.pdf'], counts['.tex'], counts['.md'], status, representative))
    return rows, sorted(full, key=lambda p: int(p.name.split('-')[1]), reverse=True)


def outputs():
    rows, full = inventory()
    counts = Counter(row[5] for row in rows)
    counts.setdefault("reliable-full-md", 0)
    programs = Counter(row[0] for row in rows)
    summary = ", ".join(f"`{key}={counts[key]}`" for key in
                        ("full-source-md", "reliable-full-md", "partial-or-notes", "source-inaccessible"))
    index = f"""# TPC/RH paper-materials inventory

Updated: 2026-09-07. Scope: {len(rows)} paper-directory entries in the preserved inventory ({programs['TPC']} TPC, {programs['RH']} RH). This is an archive inventory, not a mathematical result.

## Reading-status rule

`full-source-md` means a complete mechanical reading layer of the available manuscript with a per-paper provenance record and passing conversion checks; it is not an independent verification of the source mathematics. `reliable-full-md` requires explicit full-content and semantic review evidence; an abstract, bibliography, README, or proof-package filename alone does not establish it. A source without references is preserved as such, not completed with invented references. `partial-or-notes` means Markdown exists with TeX/PDF but no verified full conversion is recorded. `notes-only` has Markdown without TeX/PDF; `not-converted` has TeX/PDF without Markdown; `source-inaccessible` has no local Markdown/TeX/PDF manuscript, though its directory may contain other artifacts.

Summary: {summary}. The archive is not fully converted or independently reviewed. The full-source rows link to mechanical conversions, including source issues explicitly preserved in the [repair audit](TPC_MAINTENANCE_REPAIR_2026-09-07.md). Original TeX/PDF and hand-edited materials remain authoritative. File counts are actual current files under each inventoried directory, including preserved build artifacts, not fixed package-size assumptions or mathematical correctness checks.

| Program | Paper directory | PDF | TeX | MD | Status | Representative Markdown |
|---|---|---:|---:|---:|---|---|
"""
    index += "\n".join(f"| {program} | `{name}` | {pdf} | {tex} | {md} | `{status}` | {representative} |"
                       for program, name, pdf, tex, md, status, representative in rows) + "\n"
    status_by_name = {row[1]: row[5] for row in rows}
    links = LINKS.read_text().splitlines()
    for i, line in enumerate(links):
        match = re.match(r"^\| (RH|TPC) \| \[([^]]+)\]", line)
        if not match:
            continue
        name = match[2]
        cells = line.split(" | ")
        cells[2] = f"`{status_by_name[name]}`"
        if status_by_name[name] == "full-source-md":
            cells[3] = link(ROOT / "papers" / name / "paper/main.md", "MD")
        links[i] = " | ".join(cells)
    links[2] = ("Updated 2026-09-07. Each row links the preserved directory and representative artifacts. "
                "Verified mechanical conversion rows point to paper/main.md. The "
                "[batch record](TPC_CONVERSION_BATCH_2026-09-07.md) links provenance, page maps, summary, "
                "and available proof/application materials; absence is explicit. For status and counts see "
                "[PAPER_MATERIALS_INDEX.md](PAPER_MATERIALS_INDEX.md). These links do not imply independent "
                "semantic review. Source originals and hand-edited files are preserved.")
    numbers = [int(p.name.split('-')[1]) for p in full]
    supplemental = set()
    for paper in full:
        match = re.search(r"Supplemental prerequisite audit: \[[^]]+\]\(([^)]+)\)",
                          (paper / 'CONVERSION_RECORD.md').read_text())
        if match:
            supplemental.add((paper / match[1]).resolve())
    audit_links = "\n".join('- ' + link(p, p.stem) for p in sorted(supplemental)) or 'No additional scope notes recorded.'
    batch = f"""# TPC source-Markdown conversion coverage: {max(numbers)}–{min(numbers)}

Updated 2026-09-07. {len(full)} preserved manuscripts have source-complete mechanical
Markdown. The repair covered the prior 64 conversions (TPC355–418) plus
TPC350–354; subsequent existing-source batches are included in the links
below. This record supersedes older inconsistent
counts and generic review claims; it creates no paper or route edge.

## Method and explicit limits

The read-only [converter](maintain_source_markdown.py) uses the installed
Pandoc LaTeX reader and math-enabled Markdown writer. Full abstract/body
formula sequences and normalized plain text are compared after Markdown
parsing. Each conversion record locks the source commit and TeX/PDF hashes,
catalogues raw displayed equations, and maps source section lines to actual
extracted PDF heading matches. Missing or multiple page hits remain explicit.
No PDF is recompiled or claimed to be proven synchronized with its TeX.

Every detected source bibliography is retained, including the complete
external BibTeX files when present. Per-paper records identify and hash-lock
these dependencies; sources without references are not supplied with invented
entries. Theorem/proof names and boundaries remain; printed numbering
and unresolved citation formatting are not reconstructed. A separate proof
package is absent in TPC359–363, so only existing notes are linked below.

The [repair and bounded manual audit](TPC_MAINTENANCE_REPAIR_2026-09-07.md)
documents the original text-trimming defect, corrected mapping evidence,
per-paper TPC350–354 prerequisite checks, the unresolved TPC352 manuscript/
producer operator mismatch, TPC353–354 notation issues, and the TPC402
ambiguous page match. Automated preservation is not theorem validation.
Numerical certificates and the production cascade were not rerun.

## Supplemental per-batch prerequisite audits

{audit_links}

## Per-paper reading and evidence links

The abstract is included in every full-source Markdown; the README remains
the original short summary. Available package files are listed, not certified.

| Paper | Full source Markdown | Provenance / maps / formula checks | Original summary | Available proof / application materials | TeX | PDF |
|---|---|---|---|---|---|---|
"""
    package_paths = ["PROOF_PACKAGE.md", "DERIVATION_PACKAGE.md", "notes/claim_firewall.md",
                     "notes/route_evaluation.md", "experiments/protocol.md"]
    for paper in full:
        number = int(paper.name.split('-')[1])
        package = ", ".join(link(paper / rel, rel) for rel in package_paths if (paper / rel).is_file()) or "—"
        batch += (f"| TPC-{number} | {link(paper / 'paper/main.md')} | {link(paper / 'CONVERSION_RECORD.md')} | "
                  f"{link(paper / 'README.md')} | {package} | {link(paper / 'paper/main.tex')} | {link(paper / 'paper/main.pdf')} |\n")
    batch += f"""
## Coverage and next work

Across {len(rows)} entries: {summary}.
The {counts['partial-or-notes']} partial/notes entries remain the accessible conversion pool;
the source-inaccessible entry is specifically the moving-hole translation-
compiler directory for TPC207, not the separate critical-moving-hole paper.
Continue from the inventory, preserving original sources and hand edits and
recording unsupported conversions rather than guessing. This is not a claim
that all three archive-maintenance tasks are finished.

## Scientific stop remains unchanged

`TPC418_ROUND2_CLUE = NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES`.
Arithmetic advance remains `NO`, fixed-power credit remains `0`, and the
full gate remains `OPEN`. No TPC419 or new theorem is created.
"""
    return {INDEX: normalize_eof(index), LINKS: normalize_eof("\n".join(links)), BATCH: normalize_eof(batch)}, counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--patch", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    files, counts = outputs()
    if args.patch:
        print("*** Begin Patch\n" + "".join(compact_patch(path, value) for path, value in files.items()) + "*** End Patch")
    elif args.check:
        for path, value in files.items():
            if path.read_text() != value:
                raise ValueError(f"inventory output differs: {path}")
        print(dict(counts))
    else:
        print(dict(counts))


if __name__ == "__main__":
    main()
