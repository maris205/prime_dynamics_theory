"""Restricted, read-only TeX input expansion with original-file line provenance.

This is not a TeX interpreter. Standalone literal input commands and two
restricted root-source compact forms are supported. Conditional, dynamic,
verbatim and out-of-tree cases fail closed.
The caller must verify every returned dependency against its source commit.
"""
from pathlib import Path, PurePosixPath
import re


INPUT_LINE = re.compile(r"^[ \t]*\\input\{([A-Za-z0-9_./-]+)\}[ \t]*(?:%[^\n]*)?(?:\n)?$")
INPUT_TOKEN = r"\\input\{[A-Za-z0-9_./-]+\}"
COMPACT_INPUTS = re.compile(r"(?:[ \t]*" + INPUT_TOKEN + r"[ \t]*){2,}")
COMPACT_ABSTRACT = re.compile(
    r"[ \t]*((?:\\begin\{document\}[ \t]*\\maketitle[ \t]*)?\\begin\{abstract\})"
    r"[ \t]*(" + INPUT_TOKEN + r")[ \t]*(\\end\{abstract\})[ \t]*")
EXTERNAL = re.compile(r"\\(?:input|include|addbibresource)\b")
AMBIGUOUS = re.compile(
    r"\\(?:[iI]f(?!f\b)[A-Za-z]*|InputIfFileExists|else|fi|unless|newif|loop|repeat|"
    r"endinput|catcode|csname|endcsname|expandafter|scantokens)\b"
    r"|\\begin\{(?:verbatim\*?|Verbatim\*?|lstlisting|minted|comment)\}")


def require_static_input_context(raw):
    """Refuse unsupported control flow before any input is removed or expanded."""
    if AMBIGUOUS.search(raw):
        raise ValueError("conditional/dynamic/verbatim TeX needs explicit handling")


def unbound_source_path(path, base=None):
    """Do not let resolution replace a declared source path by another file."""
    lexical = Path(path).absolute()
    resolved = lexical.resolve()
    if base is not None and not resolved.is_relative_to(base):
        raise ValueError("TeX input path escapes the manuscript directory")
    if resolved != lexical:
        raise ValueError("symlinked or rebound TeX source path needs explicit handling")
    return lexical


def source_line_units(line, *, is_main):
    """Split only two root-source command-only forms; keep the caller's line.

    The exact abstract wrapper may optionally carry begin-document/maketitle.
    No prose, formula, label, comment, arbitrary wrapper or glyph-map input
    is allowed beside a compact input. Inserted newlines separate commands
    and child files, never split or reconstruct source text tokens.
    """
    if not is_main or INPUT_LINE.fullmatch(line):
        return [line]
    compact = line.removesuffix("\n")
    if r"\input{glyphtounicode}" in compact:
        return [line]
    if COMPACT_INPUTS.fullmatch(compact):
        return [token[0] + "\n" for token in re.finditer(INPUT_TOKEN, compact)]
    abstract = COMPACT_ABSTRACT.fullmatch(compact)
    if abstract:
        return [part + "\n" for part in abstract.groups()]
    return [line]


def reader_lines(raw, *, normalize_cr=False):
    """Yield (original LF-delimited line, reader line), preserving source bytes.

    Optional CR handling changes only the in-memory reader input. A bare CR
    splits reader lines but both pieces still point to the same original
    LF-delimited line. CRLF is one source/reader line ending.
    """
    if re.search(r"[\v\f\x1c-\x1e\x85\u2028\u2029]", raw) or ('\r' in raw and not normalize_cr):
        raise ValueError("non-LF TeX input line endings need explicit handling")
    parts = raw.split('\n')
    for line_no, part in enumerate(parts, 1):
        ending = '\n' if line_no < len(parts) else ''
        if not part and not ending:
            continue
        if ending and part.endswith('\r'):
            part = part[:-1]
        normalized = part.replace('\r', '\n') + ending
        for line in normalized.splitlines(keepends=True):
            yield line_no, line


def expand_source_inputs(main_path, *, read_text=None, max_depth=16, normalize_cr=False):
    """Return expanded text, one source (path,line) per line, files and edges.

    Literal input paths are resolved from the main manuscript directory, as
    for a TeX invocation with that working directory. No parent traversal,
    absolute paths, symlinked paths/components, cycles, or repeated dependencies are
    accepted. The audited system glyph-map command is left to the caller's
    separate, preamble-only hash check, and is forbidden in child inputs.
    CR normalization is opt-in and requires a separate provenance disclosure.
    A custom read_text callback must decode original bytes without normalizing
    separators; otherwise original-source provenance cannot be established.
    """
    main_path = unbound_source_path(main_path)
    base = main_path.parent
    read_text = read_text or (lambda path: path.read_bytes().decode('utf-8'))
    files, edges, seen = [], [], set()

    def expand(path, depth):
        if depth > max_depth:
            raise ValueError("TeX input depth exceeds the declared bound")
        if path in seen:
            raise ValueError("repeated or cyclic TeX input needs explicit handling")
        seen.add(path)
        raw = read_text(path)
        files.append(path)
        require_static_input_context(raw)
        chunks, locations = [], []
        source_lines = [(line_no, unit)
                        for line_no, line in reader_lines(raw, normalize_cr=normalize_cr)
                        for unit in source_line_units(line, is_main=path == main_path)]
        for line_no, line in source_lines:
            if not EXTERNAL.search(line):
                chunks.append(line)
                locations.append((path, line_no))
                continue
            match = INPUT_LINE.fullmatch(line)
            if not match:
                raise ValueError("only standalone literal TeX input commands are supported")
            name = match[1]
            if name == "glyphtounicode":
                if path != main_path:
                    raise ValueError("system glyph mapping is only allowed in the main preamble")
                chunks.append(line)
                locations.append((path, line_no))
                continue
            relative = PurePosixPath(name)
            if relative.is_absolute() or ".." in relative.parts or name.startswith("."):
                raise ValueError("out-of-tree or noncanonical TeX input path")
            if relative.suffix not in ("", ".tex"):
                raise ValueError("only TeX source dependencies are supported")
            child = unbound_source_path(base / str(relative.with_suffix(".tex")), base)
            if EXTERNAL.search(line[match.end():]):
                raise ValueError("multiple external commands on one line")
            edges.append({"parent": path, "line": line_no,
                          "command": line.rstrip("\r\n"), "child": child})
            child_text, child_locations = expand(child, depth + 1)
            # A file boundary is whitespace to the reader. Keep empty inputs
            # as one blank, parent-mapped line rather than inventing a child line.
            chunks.append(child_text if child_text.endswith("\n") else child_text + "\n")
            locations.extend(child_locations or [(path, line_no)])
        text = "".join(chunks)
        if len(text.splitlines()) != len(locations):
            raise ValueError("expanded-source line map is not one-to-one")
        return text, locations

    text, locations = expand(main_path, 0)
    return text, locations, files, edges
