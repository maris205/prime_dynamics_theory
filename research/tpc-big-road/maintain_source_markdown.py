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

from source_markdown_includes import expand_source_inputs, require_static_input_context, source_line_units

ROOT = Path(__file__).resolve().parents[2]
FORMAT = ("markdown+tex_math_dollars+raw_tex+pipe_tables-raw_attribute"
          "-header_attributes-fenced_divs-bracketed_spans-simple_tables"
          "-multiline_tables-grid_tables-smart")
VERSION = "source-markdown-audit-v2"
GLYPH_MAPPING_SHA256 = "395e568c1f4db5e89013e6aa4aac22a668b543256a20b4349436070356870851"


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


def select_paper(number, paper_name=None):
    """Resolve an existing directory; duplicate numbers require an exact name."""
    if type(number) is not int or number <= 0:
        raise ValueError("paper number must be a positive integer")
    found = [p for p in (ROOT / "papers").glob(f"tpc-{number}-*") if p.is_dir()]
    if paper_name is not None:
        if not isinstance(paper_name, str) or not re.fullmatch(
                rf"tpc-{number}-[A-Za-z0-9][A-Za-z0-9_-]*", paper_name):
            raise ValueError("paper directory must be an exact basename matching its number")
        found = [p for p in found if p.name == paper_name]
    if len(found) != 1:
        raise ValueError(f"paper {number}: expected one existing directory; use an exact --paper-dir")
    paper = found[0]
    if paper.resolve() != paper.absolute():
        raise ValueError("symlinked or rebound paper directory")
    return paper


def manuscript_source(paper, source_commit="HEAD"):
    """Choose one versioned main.tex layout, never an untracked fallback."""
    candidates = [paper / "paper/main.tex", paper / "main.tex"]
    saved = [path for path in candidates if subprocess.run(
        ["git", "cat-file", "-e", f"{source_commit}:{path.relative_to(ROOT)}"],
        cwd=ROOT, capture_output=True).returncode == 0]
    if len(saved) != 1:
        raise ValueError("expected exactly one versioned main.tex layout")
    selected = saved[0]
    if any(path != selected and (path.exists() or path.is_symlink()) for path in candidates):
        raise ValueError("competing local main.tex layout needs explicit handling")
    if not selected.is_file() or selected.resolve() != selected.absolute():
        raise ValueError("versioned main.tex missing, symlinked or rebound")
    return selected


def preserved_pdf(paper, source_commit="HEAD", *, source_path=None):
    """Choose a versioned original, never an ignored local build or new alias."""
    if source_path is not None and source_path not in (paper / 'main.tex', paper / 'paper/main.tex'):
        raise ValueError("PDF source layout must be an exact main.tex candidate")
    source_dir = source_path.parent if source_path is not None else paper / "paper"
    names = (paper.name + ".pdf", "main.pdf", "paper.pdf") if source_dir == paper else ("main.pdf", "paper.pdf")
    for name in names:
        candidate = source_dir / name
        saved = subprocess.run(["git", "cat-file", "-e",
                                f"{source_commit}:{candidate.relative_to(ROOT)}"],
                               cwd=ROOT, capture_output=True)
        if saved.returncode == 0:
            if not candidate.is_file() or candidate.resolve() != candidate.absolute():
                raise ValueError(f"versioned PDF missing, symlinked or rebound: {candidate}")
            return candidate
    raise ValueError(f"no preserved manuscript PDF in selected source layout: {paper}")


def split_document_tail(tex):
    """Keep material after an unambiguous document terminator as literal source."""
    endings = list(re.finditer(r"(?m)^[ \t]*\\end\{document\}[ \t]*\r?$", tex))
    if len(endings) > 1:
        raise ValueError("multiple document terminators need manual source handling")
    if not endings or not tex[endings[0].end():].strip():
        return tex, ""
    end = endings[0].end()
    return tex[:end], tex[end:]


def prepare_font_mapping_input(tex, paper_dir):
    """Exclude only a hash-audited PDF glyph map, never an unexpanded body input.

    The allowlisted TeX Live file has six comments and 5505 literal
    pdfglyphtounicode assignments. No TeX is executed. Unknown or shadowed
    versions, body inputs, and other external dependencies fail closed.
    """
    external = r"\\(?:input|include|addbibresource)\b"
    if not re.search(external, tex):
        return tex, []
    require_static_input_context(tex)
    starts = list(re.finditer(r"(?m)^[ \t]*\\begin\{document\}[ \t]*$", tex))
    allowed = list(re.finditer(r"(?m)^[ \t]*\\input\{glyphtounicode\}[ \t]*$", tex))
    if len(starts) != 1 or len(allowed) != 1 or allowed[0].start() >= starts[0].start():
        raise ValueError("external TeX dependency needs explicit handling")
    match = allowed[0]
    prepared = tex[:match.start()] + " " * len(match[0]) + tex[match.end():]
    if re.search(external, prepared) or r"\pdfglyphtounicode" in tex:
        raise ValueError("external TeX dependency needs explicit handling")
    located = run(["kpsewhich", "glyphtounicode.tex"], cwd=paper_dir)[0].strip()
    if not located or "\n" in located:
        raise ValueError("glyph mapping input cannot be resolved uniquely")
    path = Path(located)
    if not path.is_absolute():
        path = paper_dir / path
    blob = path.read_bytes()
    if digest(blob) != GLYPH_MAPPING_SHA256:
        raise ValueError("glyph mapping input differs from audited SHA-256")
    return prepared, [{"command": match[0].strip(),
                       "line": tex.count("\n", 0, match.start()) + 1,
                       "name": "glyphtounicode.tex", "sha256": digest(blob)}]


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


def separate_math_from_digits(value):
    r"""Keep dollar-math closing delimiters parseable before numeric prose.

    Pandoc writes adjacent TeX inlines such as 64\\(\\to\\)128 as
    64$\\to$128, but its Markdown reader rejects a closing dollar followed
    immediately by a digit. Insert only a whitespace AST node; do not alter
    the formula, numeric text, table cells, or source TeX.
    """
    count = 0
    if isinstance(value, dict):
        for child in value.values():
            count += separate_math_from_digits(child)
    elif isinstance(value, list):
        for child in value:
            count += separate_math_from_digits(child)
        for i in range(len(value) - 2, -1, -1):
            left, right = value[i:i + 2]
            if (isinstance(left, dict) and left.get("t") == "Math"
                    and left["c"][0]["t"] == "InlineMath"
                    and isinstance(right, dict) and right.get("t") == "Str"
                    and re.match(r"[0-9]", right["c"])):
                value.insert(i + 1, {"t": "Space"})
                count += 1
    return count


def text_signature(ast, blocks):
    plain = write_ast(ast, blocks, "plain")
    plain = re.sub(r"(?m)^[ \t]*[-+|: ][-+|: ]{2,}[ \t]*$", "", plain)
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", plain))


def remap_links(blocks, paper, tex="", source_locations=None, *, source_path=None):
    changes = []
    label_hits = list(re.finditer(r"\\label\{([^}]+)\}", tex))
    labels = {m[1]: tex.count("\n", 0, m.start()) + 1
              for m in label_hits}

    def source_target(label):
        source_line = labels[label]
        if source_locations is None:
            original = source_path or paper / "paper/main.tex"
            return os.path.relpath(original, paper / "paper") + "#L" + str(source_line)
        origin, origin_line = source_locations[source_line - 1]
        return os.path.relpath(origin, paper / "paper") + "#L" + str(origin_line)

    for node in list(nodes(blocks, "Link")) + list(nodes(blocks, "Image")):
        target = node["c"][-1][0]
        if target.startswith("#") and target[1:] in labels:
            replacement = source_target(target[1:])
            node["c"][-1][0] = replacement
            changes.append((target, replacement))
            continue
        attributes = dict(node["c"][0][2])
        if (node["t"] == "Link" and target.startswith("#") and "," in target
                and attributes.get("reference-type") == "ref"
                and attributes.get("reference") == target[1:]):
            # Pandoc represents a multi-target cref as one nonexistent anchor.
            # Split only its exact unresolved-label form, retaining visible text
            # and order. Never pick one target, guess numbering, or split a real
            # comma-containing label (handled above).
            reference = target[1:]
            keys = reference.split(",")
            canonical_attributes = ["", [], [["reference-type", "ref"],
                                             ["reference", reference]]]
            if (set(node) != {"t", "c"}
                    or type(node["c"]) is not list or len(node["c"]) != 3
                    or type(node["c"][-1]) is not list or len(node["c"][-1]) != 2
                    or not re.fullmatch(r"[^,\s]+(?:,[^,\s]+)+", reference)
                    or node["c"][0] != canonical_attributes
                    or node["c"][1] != [{"t": "Str", "c": "[" + reference + "]"}]
                    or node["c"][-1][1]):
                raise ValueError("unsupported multi-label source reference shape")
            if any(sum(hit[1] == key for hit in label_hits) != 1 for key in keys):
                raise ValueError("multi-label source reference has missing or duplicate source label")
            replacements = [source_target(key) for key in keys]
            inlines = [{"t": "Str", "c": "["}]
            for i, (key, replacement) in enumerate(zip(keys, replacements)):
                if i:
                    inlines.append({"t": "Str", "c": ","})
                inlines.append({"t": "Link", "c": [["", [], []],
                                [{"t": "Str", "c": key}], [replacement, ""]]})
                changes.append(("#" + key, replacement))
            inlines.append({"t": "Str", "c": "]"})
            node.clear()
            node.update({"t": "Span", "c": [["", [], []], inlines]})
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


def convert(number, *, source_commit=None, scope_audit=None, paper_name=None):
    paper = select_paper(number, paper_name)
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
    if source_commit is None:
        existing = paper / "CONVERSION_RECORD.md"
        prior = re.search(r"Repository source commit: `([0-9a-f]{40})`", existing.read_text()) if existing.is_file() else None
        source_commit = prior[1] if prior else run(["git", "rev-parse", "HEAD"])[0].strip()
    tex_path = manuscript_source(paper, source_commit)
    original_tex = tex_path.read_text()
    reading_dir = paper / "paper"
    tex_link = os.path.relpath(tex_path, reading_dir)
    tex_record_link = str(tex_path.relative_to(paper))
    has_source_inputs = bool(re.search(r"\\(?:input|include|addbibresource)\b",
                                      original_tex.replace(r"\input{glyphtounicode}", "")))
    source_locations, source_files, source_edges = None, [tex_path], []
    source_blobs = {}
    if has_source_inputs:
        def read_locked_source(path):
            blob = path.read_bytes()
            saved = subprocess.run(["git", "show", f"{source_commit}:{path.relative_to(ROOT)}"],
                                   cwd=ROOT, capture_output=True, check=True).stdout
            if blob != saved:
                raise ValueError(f"source differs from declared commit: {path}")
            source_blobs[path] = blob
            return blob.decode("utf-8")

        tex, source_locations, source_files, source_edges = expand_source_inputs(
            tex_path, read_text=read_locked_source, normalize_cr=True)
    else:
        tex = original_tex
    prepared_tex, font_inputs = prepare_font_mapping_input(tex, tex_path.parent)
    if source_locations is not None:
        for entry in font_inputs:
            origin, origin_line = source_locations[entry["line"] - 1]
            entry["line"] = origin_line
            entry["source"] = str(origin.relative_to(paper))
    bib_files = []
    bib_command = re.search(r"\\bibliography\{([^}]+)\}", tex)
    if bib_command:
        for name in bib_command[1].split(","):
            path = (tex_path.parent / name.strip()).with_suffix(".bib").resolve()
            if not path.is_relative_to(paper) or not path.is_file():
                raise ValueError(f"{number}: missing/out-of-scope bibliography {name}")
            bib_files.append(path)
    pdf_path = preserved_pdf(paper, source_commit, source_path=tex_path)
    for locked in source_files + [pdf_path] + bib_files:
        original = source_blobs.get(locked)
        if original is None:
            original = subprocess.run(["git", "show", f"{source_commit}:{locked.relative_to(ROOT)}"],
                                      cwd=ROOT, capture_output=True, check=True).stdout
        if digest(original) != digest(locked.read_bytes()):
            raise ValueError(f"source differs from declared commit: {locked}")
    document_tex, trailing_source = split_document_tail(tex)
    if source_edges and trailing_source:
        raise ValueError("post-document content in a multi-file source needs explicit handling")
    has_bibliography = r"\begin{thebibliography}" in document_tex
    prepared_document, _ = split_document_tail(prepared_tex)
    input_tex, environment_catalog = preserve_environments(prepared_document)
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
    tail_scope = ""
    if trailing_source:
        tail_line = document_tex.count("\n") + 2
        tail_scope = (f"\n- Post-document material begins at TeX line {tail_line}; "
                      f"suffix SHA-256 `{digest(trailing_source)}`. Retained as literal code, "
                      "not interpreted as manuscript prose or counted as document math nodes.")
        body.extend([
            {"t": "Header", "c": [1, ["post-document-source", [], []],
                                      [{"t": "Str", "c": "Post-document source (uninterpreted)"}]]},
            {"t": "Para", "c": [{"t": "Str", "c":
                f"The following source follows the document terminator at original TeX line {tail_line - 1}. "
                "It is preserved literally, not silently removed or interpreted as part of the compiled manuscript."}]},
            {"t": "CodeBlock", "c": [["", ["latex"], []], trailing_source.strip("\r\n")]},
        ])
    if bib_files:
        body.append({"t": "Header", "c": [1, ["references", [], []], [{"t": "Str", "c": "References (preserved BibTeX)"}]]})
        for bib in bib_files:
            body.append({"t": "Para", "c": [{"t": "Str", "c": "Bibliography source: " + str(bib.relative_to(paper))}]})
            body.append({"t": "CodeBlock", "c": [["", ["bibtex"], []], bib.read_text().strip()]})
    if font_inputs:
        body.append({"t": "Header", "c": [1, ["non-content-font-mapping-input", [], []],
                     [{"t": "Str", "c": "Non-content font-mapping input (preserved command)"}]]})
        for entry in font_inputs:
            body.append({"t": "Para", "c": [{"t": "Str", "c":
                f"Original {entry.get('source', 'TeX')} line {entry['line']}: {entry['name']}, SHA-256 {entry['sha256']}. "
                "This audited PDF glyph-to-Unicode map is not manuscript content. "
                "Its command is retained without executing TeX or expanding the mapping table."}]})
            body.append({"t": "CodeBlock", "c": [["", ["latex"], []], entry["command"]]})
    link_changes = remap_links(abstract + body, paper, tex, source_locations, source_path=tex_path)
    all_blocks = abstract + body
    raw_retained = preserve_raw_tex(all_blocks)
    math_spacing = separate_math_from_digits(all_blocks)
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
    sections = list(headings(document_tex))
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
    displays = list(display_blocks(document_tex))
    proofs = paper / "PROOF_PACKAGE.md"
    readme = paper / "README.md"
    tex_hash = digest(tex_path.read_bytes())
    pdf_hash = digest(pdf_path.read_bytes())
    limitations = []
    if tex_path.parent == paper:
        limitations.append("The preserved manuscript is root main.tex; this reading layer remains at "
                            "paper/main.md with links back to root sources and the versioned original PDF. "
                            "No source file is copied, moved, or treated as a new paper.")
    cr_sources = [(path, blob.count(b'\r\n'), blob.count(b'\r') - blob.count(b'\r\n'))
                  for path, blob in source_blobs.items() if b'\r' in blob]
    compact_source = has_source_inputs and any(
        len(source_line_units(line, is_main=True)) > 1
        for line in original_tex.splitlines(keepends=True))
    if source_edges:
        input_kind = "Restricted compact/standalone literal" if compact_source else "Standalone literal"
        limitations.append(input_kind + " TeX inputs were expanded in memory from the manuscript directory; "
                            "all dependencies were checked against the source commit. Original-file/line links "
                            "and an ordered dependency ledger are retained. This is not a TeX execution or a "
                            "general conditional/dynamic-include interpreter.")
    if cr_sources:
        limitations.append("CR/CRLF separators were normalized only in the in-memory reader input; "
                            "all original file-byte hashes are unchanged. Source links count original LF-delimited "
                            "lines, so multiple reader lines from a bare CR share one original line. "
                            "Expanded-display hashes describe this normalized reader input, not literal source bytes. "
                            "No missing TeX command or suspected source typo is reconstructed.")
    if font_inputs:
        limitations.append("The preamble-only glyphtounicode input was resolved with kpsewhich and checked "
                            "against the audited SHA-256; its non-content mapping table was not expanded. "
                            "The original command, source line, and dependency hash are retained in the reading layer.")
    if math_spacing:
        limitations.append(f"{math_spacing} whitespace separator(s) inserted after inline math before numeric prose "
                            "to preserve dollar-delimiter parsing; formulas and original TeX are unchanged.")
    if trailing_source:
        limitations.append("Post-document source is retained in an explicit uninterpreted code block; "
                            "its meaning and PDF inclusion are not inferred. See the formula-scope entry for provenance.")
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

- Source TeX: [main.tex]({tex_link})
- Preserved PDF: [{pdf_path.name}]({os.path.relpath(pdf_path, reading_dir)})
{chr(10).join('- Bibliography source: [' + b.name + '](' + os.path.relpath(b, reading_dir) + ')' for b in bib_files)}
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
    dependency_record = ""
    location_explanation = "TeX line numbers refer to the hashed original above."
    environment_text = ', '.join(item['name'] + ' at TeX line ' + str(item['line']) for item in environment_catalog) or 'none'
    if source_edges:
        def location(line, relative_to=paper):
            path, number = source_locations[line - 1]
            relative = os.path.relpath(path, relative_to)
            return f"[{relative}:L{number}]({relative}#L{number})"

        table = "\n".join(f"| `{s['tex']}` | {location(s['line'])} | {', '.join(map(str, s['pdf_pages'])) or 'UNMAPPED'} | `{s['map_status']}` |" for s in sections)
        formulas = "\n".join(f"| D{d['id']:02} | {d['environment']} | {location(d['start'])} – {location(d['end'])} | `{d['sha256']}` |" for d in displays) or "| — | No explicit display environment | — | — |"
        boundary_text = "\n".join(
            f"- {location(line_no)}: `{line.strip().replace('`', chr(39))}`"
            for line_no, line in enumerate(tex.splitlines(), 1)
            if re.search(r"finite|synthetic|assum|uniform|does not|not an? |no arithmetic|OPEN|h_?0", line, re.I)
        )
        boundary_text = "\n".join(boundary_text.splitlines()[:32]) or "No boundary keywords found; semantic audit required."
        environment_text = ', '.join(item['name'] + ' at ' + location(item['line']) for item in environment_catalog) or 'none'
        location_explanation = ("Every source locator names the hashed original file and its original line; "
                                "no expanded line is presented as a main.tex line. Raw display hashes cover "
                                "the expanded block, which can span multiple linked source files.")
        dependency_rows = "\n".join(
            f"| [{p.relative_to(paper)}]({p.relative_to(paper)}) | `{digest(p.read_bytes())}` |"
            for p in source_files)
        edge_rows = "\n".join(
            f"| [{e['parent'].relative_to(paper)}:L{e['line']}]({e['parent'].relative_to(paper)}#L{e['line']}) | "
            f"`{e['command'].strip()}` | [{e['child'].relative_to(paper)}]({e['child'].relative_to(paper)}) |"
            for e in source_edges)
        dependency_record = ("\n## Static TeX dependency provenance\n\n"
            f"All {len(source_files)} manuscript-source files below match the declared source commit. "
            "Input order is preserved; no source file is rewritten or TeX executed.\n\n"
            "| Original source | SHA-256 |\n|---|---|\n" + dependency_rows + "\n\n"
            "| Parent input location | Preserved input command | Included source |\n|---|---|---|\n" + edge_rows + "\n")
        if cr_sources:
            dependency_record += ("\n### Original CR/CRLF separator ledger\n\n"
                "These counts refer to the hash-locked original bytes. Only reader whitespace is normalized; "
                "original-file links use LF-delimited source lines and no scientific source is repaired.\n\n"
                "| Original source | CRLF pairs | Bare CR bytes |\n|---|---:|---:|\n" +
                "\n".join(f"| [{path.relative_to(paper)}]({path.relative_to(paper)}) | {pairs} | {bare} |"
                          for path, pairs, bare in cr_sources) + "\n")
            location_explanation += (" This source contains CR separators: source lines count original LF "
                                     "delimiters, while expanded-block hashes use the explicitly normalized "
                                     "reader input. The separate file hashes preserve exact original bytes.")
        # Make the included-source ledger visible before the reading layer body.
        output = output.replace("- Converter: `" + VERSION + "`\n",
            "- Converter: `" + VERSION + "`\n- Included-source hashes, input order, and original-file line/page maps: "
            "[dependency ledger](../CONVERSION_RECORD.md#static-tex-dependency-provenance)\n", 1)
        if cr_sources:
            output = output.replace("\n## Abstract\n", "\n> Source-format notice: the originals contain CR "
                "separators. Only reader line endings are normalized; suspected TeX typos are not repaired. "
                "See the [separator ledger](../CONVERSION_RECORD.md#original-crcrlf-separator-ledger) "
                "and bounded source audit before interpreting affected formulas.\n\n## Abstract\n", 1)
    record = f"""# TPC-{number} conversion record

## Provenance and status

- Converter: `{VERSION}`; Pandoc `{run(['pandoc', '--version'])[0].splitlines()[0]}`.
- Repository source commit: `{source_commit}`.
- TeX: [{tex_record_link}]({tex_record_link}), SHA-256 `{tex_hash}`.
{chr(10).join('- Bibliography: [' + str(b.relative_to(paper)) + '](' + str(b.relative_to(paper)) + '), SHA-256 `' + digest(b.read_bytes()) + '`.' for b in bib_files)}
- Preserved PDF: [{pdf_path.relative_to(paper)}]({pdf_path.relative_to(paper)}), SHA-256 `{pdf_hash}`; {len(pages)} extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `{digest(output)}`.
- Conversion status: `{status}`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.{scope_line}
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: {', '.join(package_links)}.
- Separate proof package: `{'PRESENT (availability only)' if proofs.exists() else 'ABSENT'}`.
- Bibliography/reference section detected: `{'YES' if has_bibliography or bib_files else 'NO'}`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.{dependency_record}

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
{table}

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. {location_explanation}

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.{tail_scope}
- Pandoc math-node sequence: `{len(expected_math)}` before writing and `{len(recovered_math)}` after Markdown parsing; normalized TeX expressions and inline/display kinds: `{'PASS' if math_ok else 'FAIL'}`.
- Whitespace-normalized plain-text roundtrip: `{'PASS' if text_ok else 'DIFF_REVIEW_REQUIRED'}`.
- Explicit source display blocks: `{len(displays)}`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `{digest(json.dumps(expected_math, ensure_ascii=False))}`.
- Source theorem/proof environment starts: {environment_text}.

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
    parser.add_argument("--paper-dir", help="exact existing directory basename; required for duplicate numbers")
    parser.add_argument("--source-commit")
    parser.add_argument("--scope-audit", help="existing repository-relative supplemental review note")
    parser.add_argument("--patch", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    paper, markdown, record, report = convert(args.paper, source_commit=args.source_commit, scope_audit=args.scope_audit, paper_name=args.paper_dir)
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
