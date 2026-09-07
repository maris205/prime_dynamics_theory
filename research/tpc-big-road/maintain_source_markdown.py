#!/usr/bin/env python3
"""Read-only source conversion planner/checker; emits apply_patch input on request.

Never changes TeX/PDF, executes experiments, infers proof validity, or creates paper
directories. A caller applies emitted patches only to the named generated files.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FORMAT = ("markdown+tex_math_dollars+raw_tex+pipe_tables-raw_attribute"
          "-header_attributes-fenced_divs-bracketed_spans-simple_tables"
          "-multiline_tables-grid_tables-smart")
VERSION = "source-markdown-audit-v2"


def run(args, *, data=None, cwd=ROOT):
    result = subprocess.run(args, input=data, text=True, cwd=cwd,
                            capture_output=True, check=True)
    return result.stdout, result.stderr


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()


def normalize_eof(value):
    # Only whitespace is stripped. In particular, never use [ \\t], which also
    # matches literal backslash/t and was the cause of historical word damage.
    return "\n".join(line.rstrip(" \t") for line in value.splitlines()).rstrip("\n") + "\n"


def nodes(value, kind):
    if isinstance(value, dict):
        if value.get("t") == kind:
            yield value
        for child in value.values():
            yield from nodes(child, kind)
    elif isinstance(value, list):
        for child in value:
            yield from nodes(child, kind)


def blocks_for_meta(value):
    if not value:
        return []
    if value["t"] == "MetaBlocks":
        return value["c"]
    if value["t"] == "MetaInlines":
        return [{"t": "Para", "c": value["c"]}]
    if value["t"] == "MetaList":
        return [block for item in value["c"] for block in blocks_for_meta(item)]
    return []


def write_ast(ast, blocks, fmt=FORMAT):
    obj = {"pandoc-api-version": ast["pandoc-api-version"], "meta": {}, "blocks": blocks}
    return run(["pandoc", "-f", "json", "-t", fmt, "--wrap=none", "--atx-headers"],
               data=json.dumps(obj, ensure_ascii=False))[0]


def balanced_group(text, opening):
    if text[opening] != "{":
        raise ValueError("not a group")
    depth = 0
    for i in range(opening, len(text)):
        if text[i] in "{}" and (i == 0 or text[i - 1] != "\\"):
            depth += 1 if text[i] == "{" else -1
            if depth == 0:
                return text[opening + 1:i], i + 1
    raise ValueError("unbalanced TeX group")


def headings(tex):
    for m in re.finditer(r"\\((?:sub)*section)(\*)?\s*\{", tex):
        title, end = balanced_group(tex, m.end() - 1)
        plain = run(["pandoc", "-f", "latex", "-t", "plain", "--wrap=none"], data=title)[0].strip()
        yield {"tex": title, "plain": plain, "line": tex.count("\n", 0, m.start()) + 1,
               "kind": m[1], "starred": bool(m[2]), "end": end}


def display_blocks(tex):
    pattern = (r"(?<!\\)\\\[(.*?)\\\]|\\begin\{(equation\*?|align\*?|alignat\*?|"
               r"gather\*?|multline\*?|eqnarray\*?|displaymath)\}(.*?)\\end\{\2\}")
    for index, match in enumerate(re.finditer(pattern, tex, re.S), 1):
        yield {"id": index, "start": tex.count("\n", 0, match.start()) + 1,
               "end": tex.count("\n", 0, match.end()) + 1,
               "environment": match[2] or "\\[...\\]", "sha256": digest(match[0]),
               "source": match[0]}


def canonical_words(text):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFKC", text).casefold())


def pdf_page_map(sections, pages):
    for sec in sections:
        needle = canonical_words(sec["plain"])
        hits = []
        for page_number, page in enumerate(pages, 1):
            lines = page.splitlines()
            for i in range(len(lines)):
                # Match a heading at a line boundary, optionally numbered; no
                # guessed half-document page numbers or fabricated match scores.
                candidate = " ".join(lines[i:i + 3]).strip()
                candidate = re.sub(r"^\d+(?:\.\d+)*\s+", "", candidate)
                if needle and canonical_words(candidate).startswith(needle):
                    hits.append(page_number)
                    break
        hits = sorted(set(hits))
        sec["pdf_pages"] = hits
        sec["map_status"] = "HEADING_TEXT_MATCH" if len(hits) == 1 else "UNMAPPED_OR_AMBIGUOUS"


def math_signature(blocks):
    return [(node["c"][0]["t"], re.sub(r"\s+", "", node["c"][1]))
            for node in nodes(blocks, "Math")]


def text_signature(ast, blocks):
    plain = write_ast(ast, blocks, "plain")
    plain = re.sub(r"(?m)^[ \t]*[-+|: ][-+|: ]{2,}[ \t]*$", "", plain)
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", plain))


def remap_links(blocks, paper, tex=""):
    changes = []
    labels = {m[1]: tex.count("\n", 0, m.start()) + 1
              for m in re.finditer(r"\\label\{([^}]+)\}", tex)}
    for node in list(nodes(blocks, "Link")) + list(nodes(blocks, "Image")):
        target = node["c"][-1][0]
        if target.startswith("#") and target[1:] in labels:
            replacement = "main.tex#L" + str(labels[target[1:]])
            node["c"][-1][0] = replacement
            changes.append((target, replacement))
            continue
        if not target or target.startswith(("#", "/")) or re.match(r"[a-z]+:", target):
            continue
        path_part, sep, anchor = target.partition("#")
        if not (paper / "paper" / path_part).exists() and (paper / path_part).exists():
            replacement = "../" + path_part + sep + anchor
            node["c"][-1][0] = replacement
            changes.append((target, replacement))
        elif not (paper / "paper" / path_part).exists() and (ROOT / path_part).exists():
            replacement = os.path.relpath(ROOT / path_part, paper / "paper") + sep + anchor
            node["c"][-1][0] = replacement
            changes.append((target, replacement))
    return changes


def preserve_raw_tex(blocks):
    """Unknown/citation commands are explicit source code, never dropped prose."""
    retained = []
    for node in list(nodes(blocks, "Cite")):
        raw_items = list(nodes(node, "RawInline"))
        raw = raw_items[0]["c"][1] if raw_items else "\\cite{" + ",".join(item["citationId"] for item in node["c"][0]) + "}"
        retained.append(raw)
        node.clear()
        node.update({"t": "Code", "c": [["", [], []], raw]})
    for kind in ("RawInline", "RawBlock"):
        for node in list(nodes(blocks, kind)):
            if node["c"][0] not in ("latex", "tex"):
                continue
            raw = node["c"][1]
            retained.append(raw)
            node.clear()
            node.update({"t": "Code" if kind == "RawInline" else "CodeBlock",
                         "c": [["", ["latex"] if kind == "RawBlock" else [], []], raw]})
    return retained


def preserve_environments(tex):
    """Retain semantic environment names which the LaTeX reader can flatten."""
    names = r"theorem|proposition|lemma|corollary|definition|remark|assumption|claim|proof"
    catalog = []
    for match in re.finditer(r"\\begin\{(" + names + r")\*?\}(?:\[([^\]]+)\])?", tex):
        catalog.append({"name": match[1], "line": tex.count("\n", 0, match.start()) + 1,
                        "optional_title": match[2] or ""})
    def opening(match):
        title = match[1].capitalize()
        if match[2]:
            title += ": " + match[2]
        return r"\begin{quote}\textbf{" + title + r"}\quad "
    converted = re.sub(r"\\begin\{(" + names + r")\*?\}(?:\[([^\]]+)\])?", opening, tex)
    converted = re.sub(r"\\end\{(?:" + names + r")\*?\}", lambda _: r"\end{quote}", converted)
    return converted, catalog


def metadata(ast, tex):
    meta = ast["meta"]
    title_blocks = blocks_for_meta(meta.get("title"))
    author_blocks = blocks_for_meta(meta.get("author"))
    date_blocks = blocks_for_meta(meta.get("date"))
    if not title_blocks:
        center = re.search(r"\\begin\{center\}(.*?)\\end\{center\}", tex, re.S)
        if not center:
            raise ValueError("title unavailable: no TeX title metadata or centered title block")
        raw = center[1].strip()
        title, _ = balanced_group(raw, 0)
        title = re.sub(r"\\(?:Large|large|bf|bfseries)\b", "", title).strip()
        title_ast = json.loads(run(["pandoc", "-f", "latex", "-t", "json"], data=title)[0])
        title_blocks = title_ast["blocks"]
        # Keep the complete original centered author/date block in the body;
        # never fill missing metadata with guessed dates or a standard affiliation.
    title = write_ast(ast, title_blocks).strip().replace("\n", " ")
    author = write_ast(ast, author_blocks, "plain").strip() if author_blocks else "See preserved source title block"
    date = write_ast(ast, date_blocks, "plain").strip() if date_blocks else "See preserved source title block"
    return title, author, date


def patch_for(path, new):
    new = normalize_eof(new)
    if path.exists():
        old = path.read_text()
        if old == new:
            return ""
        return (f"*** Update File: {path}\n@@\n" +
                "\n".join("-" + line for line in old.splitlines()) + "\n" +
                "\n".join("+" + line for line in new.splitlines()) + "\n")
    return f"*** Add File: {path}\n" + "\n".join("+" + line for line in new.splitlines()) + "\n"


def convert(number, *, source_commit=None, scope_audit=None):
    found = list((ROOT / "papers").glob(f"tpc-{number}-*"))
    if len(found) != 1:
        raise ValueError(f"paper {number}: expected one existing directory")
    paper = found[0]
    if scope_audit is None and (paper / "CONVERSION_RECORD.md").is_file():
        saved = re.search(r"Supplemental prerequisite audit: \[[^]]+\]\(([^)]+)\)",
                          (paper / "CONVERSION_RECORD.md").read_text())
        if saved:
            scope_audit = (paper / saved[1]).resolve()
    if scope_audit:
        scope_audit = (ROOT / scope_audit).resolve()
        if not scope_audit.is_relative_to(ROOT) or not scope_audit.is_file():
            raise ValueError("supplemental scope audit must be an existing repository file")
    scope_line = ("\n- Supplemental prerequisite audit: [bounded source review](" +
                  os.path.relpath(scope_audit, paper) + ").") if scope_audit else ""
    tex_path = paper / "paper/main.tex"
    pdf_path = paper / "paper/main.pdf"
    tex = tex_path.read_text()
    if re.search(r"\\(?:input|include|addbibresource)\b", tex):
        raise ValueError(f"{number}: external TeX dependency needs explicit handling")
    bib_files = []
    bib_command = re.search(r"\\bibliography\{([^}]+)\}", tex)
    if bib_command:
        for name in bib_command[1].split(","):
            path = (tex_path.parent / name.strip()).with_suffix(".bib").resolve()
            if not path.is_relative_to(paper) or not path.is_file():
                raise ValueError(f"{number}: missing/out-of-scope bibliography {name}")
            bib_files.append(path)
    if source_commit is None:
        existing = paper / "CONVERSION_RECORD.md"
        prior = re.search(r"Repository source commit: `([0-9a-f]{40})`", existing.read_text()) if existing.is_file() else None
        source_commit = prior[1] if prior else run(["git", "rev-parse", "HEAD"])[0].strip()
    for locked in [tex_path, pdf_path] + bib_files:
        original = subprocess.run(["git", "show", f"{source_commit}:{locked.relative_to(ROOT)}"],
                                  cwd=ROOT, capture_output=True, check=True).stdout
        if digest(original) != digest(locked.read_bytes()):
            raise ValueError(f"source differs from declared commit: {locked}")
    has_bibliography = r"\begin{thebibliography}" in tex
    input_tex, environment_catalog = preserve_environments(tex)
    input_tex = input_tex.replace(r"\begin{thebibliography}",
                            r"\section*{References}" + "\n" + r"\begin{thebibliography}")
    raw_ast, warnings = run(["pandoc", "-f", "latex", "-t", "json"],
                           data=input_tex, cwd=tex_path.parent)
    ast = json.loads(raw_ast)
    title, author, date = metadata(ast, tex)
    abstract = blocks_for_meta(ast["meta"].get("abstract"))
    if not abstract:
        raise ValueError(f"{number}: abstract metadata missing; manual extraction required")
    body = copy.deepcopy(ast["blocks"])
    if bib_files:
        body.append({"t": "Header", "c": [1, ["references", [], []], [{"t": "Str", "c": "References (preserved BibTeX)"}]]})
        for bib in bib_files:
            body.append({"t": "Para", "c": [{"t": "Str", "c": "Bibliography source: " + str(bib.relative_to(paper))}]})
            body.append({"t": "CodeBlock", "c": [["", ["bibtex"], []], bib.read_text().strip()]})
    link_changes = remap_links(abstract + body, paper, tex)
    all_blocks = abstract + body
    raw_retained = preserve_raw_tex(all_blocks)
    abstract_md = write_ast(ast, abstract)
    body_md = write_ast(ast, body)
    # Preserve hard line breaks without trailing-space lint errors. Backslash
    # is a Markdown hard break, not a text-normalization character class.
    abstract_md = re.sub(r" {2,}\n", "\\\n", abstract_md)
    body_md = re.sub(r" {2,}\n", "\\\n", body_md)
    roundtrip = json.loads(run(["pandoc", "-f", FORMAT, "-t", "json"], data=abstract_md + "\n" + body_md)[0])
    expected_math = math_signature(all_blocks)
    recovered_math = math_signature(roundtrip["blocks"])
    math_ok = expected_math == recovered_math
    text_ok = text_signature(ast, all_blocks) == text_signature(ast, roundtrip["blocks"])
    if not math_ok:
        raise ValueError(f"{number}: math roundtrip mismatch ({len(expected_math)} vs {len(recovered_math)})")
    sections = list(headings(tex))
    if has_bibliography:
        start = tex.index(r"\begin{thebibliography}")
        sections.append({"tex": "References (thebibliography)", "plain": "References",
                         "line": tex.count("\n", 0, start) + 1, "kind": "bibliography", "starred": True})
    if bib_command:
        sections.append({"tex": "References (external bibliography)", "plain": "References",
                         "line": tex.count("\n", 0, bib_command.start()) + 1, "kind": "bibliography", "starred": True})
    pdf_text, pdf_warnings = run(["pdftotext", "-layout", str(pdf_path), "-"])
    pages = pdf_text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    pdf_page_map(sections, pages)
    displays = list(display_blocks(tex))
    proofs = paper / "PROOF_PACKAGE.md"
    readme = paper / "README.md"
    tex_hash = digest(tex_path.read_bytes())
    pdf_hash = digest(pdf_path.read_bytes())
    limitations = []
    if warnings.strip():
        limitations.append("Pandoc reader warnings: " + warnings.strip())
    if not text_ok:
        limitations.append("Plain-text roundtrip differs in formatting/structure; inspect the preserved source. Math roundtrip is separately checked.")
    if raw_retained:
        limitations.append(f"{len(raw_retained)} unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.")
    if not proofs.exists():
        limitations.append("No PROOF_PACKAGE.md is present; no proof-package review is claimed.")
    if bib_files:
        limitations.append("External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.")
    if environment_catalog:
        limitations.append("Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.")
    full = text_ok and not warnings.strip()
    status = "FULL_TEX_TO_MARKDOWN_MECHANICAL" if full else "PARTIAL_CONVERSION_REVIEW_REQUIRED"
    header = f"""# {title}

> Mechanical reading layer generated from the preserved TeX. Original TeX/PDF and hand-edited package materials remain authoritative. This conversion does not certify a proof or upgrade any finite, conditional, synthetic, or open claim.

- Source TeX: [main.tex](main.tex)
- Preserved PDF: [main.pdf](main.pdf)
{chr(10).join('- Bibliography source: [' + b.name + '](' + b.name + ')' for b in bib_files)}
- Conversion and audit scope: [CONVERSION_RECORD.md](../CONVERSION_RECORD.md)
- Author metadata: {'; '.join(author.splitlines())}
- Source date: {date}
- Source repository commit: `{source_commit}`
- Converter: `{VERSION}`

## Abstract

{abstract_md.strip()}

<!-- SOURCE_BODY_BEGIN -->

{body_md.strip()}

<!-- SOURCE_BODY_END -->
"""
    output = normalize_eof(header)
    table = "\n".join(f"| `{s['tex']}` | {s['line']} | {', '.join(map(str, s['pdf_pages'])) or 'UNMAPPED'} | `{s['map_status']}` |" for s in sections)
    formulas = "\n".join(f"| D{d['id']:02} | {d['environment']} | {d['start']}–{d['end']} | `{d['sha256']}` |" for d in displays) or "| — | No explicit display environment | — | — |"
    package_links = [f"[{p.relative_to(paper)}]({p.relative_to(paper)})" for p in
                     [readme, proofs, paper / "DERIVATION_PACKAGE.md", paper / "notes/claim_firewall.md", paper / "notes/route_evaluation.md", paper / "experiments/protocol.md"] if p.is_file()]
    boundaries = []
    for line_no, line in enumerate(tex.splitlines(), 1):
        if re.search(r"finite|synthetic|assum|uniform|does not|not an? |no arithmetic|OPEN|h_?0", line, re.I):
            boundaries.append(f"- TeX line {line_no}: `{line.strip().replace('`', chr(39))}`")
    boundary_text = "\n".join(boundaries[:32]) or "No boundary keywords found; semantic audit required."
    record = f"""# TPC-{number} conversion record

## Provenance and status

- Converter: `{VERSION}`; Pandoc `{run(['pandoc', '--version'])[0].splitlines()[0]}`.
- Repository source commit: `{source_commit}`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `{tex_hash}`.
{chr(10).join('- Bibliography: [' + str(b.relative_to(paper)) + '](' + str(b.relative_to(paper)) + '), SHA-256 `' + digest(b.read_bytes()) + '`.' for b in bib_files)}
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `{pdf_hash}`; {len(pages)} extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `{digest(output)}`.
- Conversion status: `{status}`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.{scope_line}
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: {', '.join(package_links)}.
- Separate proof package: `{'PRESENT (availability only)' if proofs.exists() else 'ABSENT'}`.
- Bibliography/reference section detected: `{'YES' if has_bibliography or bib_files else 'NO'}`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
{table}

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `{len(expected_math)}` before writing and `{len(recovered_math)}` after Markdown parsing; normalized TeX expressions and inline/display kinds: `{'PASS' if math_ok else 'FAIL'}`.
- Whitespace-normalized plain-text roundtrip: `{'PASS' if text_ok else 'DIFF_REVIEW_REQUIRED'}`.
- Explicit source display blocks: `{len(displays)}`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `{digest(json.dumps(expected_math, ensure_ascii=False))}`.
- Source theorem/proof environment starts: {', '.join(item['name'] + ' at TeX line ' + str(item['line']) for item in environment_catalog) or 'none'}.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
{formulas}

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

{boundary_text}

## Conversion limitations

{chr(10).join('- ' + x for x in limitations) or '- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.'}

{chr(10).join('- Link relocation: `' + a + '` → `' + b + '` (existing project target or original TeX label line).' for a,b in link_changes)}
"""
    return paper, output, normalize_eof(record), {"paper": number, "status": status, "math_nodes": len(expected_math), "text_roundtrip": text_ok,
        "displays": len(displays), "pages": len(pages), "unmapped": sum(s["map_status"] != "HEADING_TEXT_MATCH" for s in sections),
        "limitations": limitations, "tex_sha256": tex_hash, "pdf_sha256": pdf_hash}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", type=int, required=True)
    parser.add_argument("--source-commit")
    parser.add_argument("--scope-audit", help="existing repository-relative supplemental review note")
    parser.add_argument("--patch", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    paper, markdown, record, report = convert(args.paper, source_commit=args.source_commit, scope_audit=args.scope_audit)
    if args.patch:
        for path in [paper / "paper/main.md", paper / "CONVERSION_RECORD.md"]:
            if path.exists():
                # Existing untracked files may be the user's unpublished work.
                run(["git", "ls-files", "--error-unmatch", "--", str(path)])
                run(["git", "diff", "--exit-code", "HEAD", "--", str(path)])
        existing_md = paper / "paper/main.md"
        if existing_md.exists() and not re.search(r"mechanical.*(?:conversion|reading layer)|Mechanical reading layer", existing_md.read_text()):
            raise ValueError("refusing to replace an unrecognized hand-edited Markdown file")
        edits = patch_for(paper / "paper/main.md", markdown) + patch_for(paper / "CONVERSION_RECORD.md", record)
        print("*** Begin Patch\n" + edits + "*** End Patch")
    elif args.check:
        for path, expected in [(paper / "paper/main.md", markdown), (paper / "CONVERSION_RECORD.md", record)]:
            if not path.is_file() or path.read_text() != expected:
                raise ValueError(f"generated artifact mismatch: {path}")
        print(json.dumps(report))
    else:
        print(json.dumps(report))


if __name__ == "__main__":
    main()
