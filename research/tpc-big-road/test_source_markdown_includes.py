"""No-write source-tree, provenance and trust-boundary regressions."""
from pathlib import Path
import io
import unittest
from unittest.mock import patch

import maintain_source_markdown as m
import source_markdown_includes as inc


class StaticInputExpansion(unittest.TestCase):
    base = (m.ROOT / "DOES_NOT_EXIST_INPUT_FIXTURE").resolve()

    def fixture(self, texts, **kwargs):
        def read(path):
            relative = str(path.relative_to(self.base))
            if relative not in texts:
                raise FileNotFoundError(relative)
            return texts[relative]
        return inc.expand_source_inputs(self.base / "main.tex", read_text=read, **kwargs)

    def test_exact_order_original_locations_and_edges(self):
        text, locations, files, edges = self.fixture({
            "main.tex": "first\n\\input{sections/body}\nlast\n",
            "sections/body.tex": "\\section{Body}\n$x$\n"})
        self.assertEqual(text, "first\n\\section{Body}\n$x$\nlast\n")
        self.assertEqual([(str(p.relative_to(self.base)), n) for p, n in locations],
                         [("main.tex", 1), ("sections/body.tex", 1),
                          ("sections/body.tex", 2), ("main.tex", 3)])
        self.assertEqual(len(files), 2)
        self.assertEqual(edges[0]["line"], 2)
        self.assertEqual(edges[0]["command"], r"\input{sections/body}")

    def test_nested_paths_resolve_from_main_working_directory(self):
        text, locations, files, edges = self.fixture({
            "main.tex": "\\input{sections/body}\n",
            "sections/body.tex": "body\n\\input{tables/value.tex}\n",
            "tables/value.tex": "value\n"})
        self.assertEqual(text, "body\nvalue\n")
        self.assertEqual(len(files), 3)
        self.assertEqual(len(edges), 2)
        self.assertEqual(locations[-1], (self.base / "tables/value.tex", 1))

    def test_compact_root_inputs_keep_order_and_original_parent_line(self):
        text, locations, _, edges = self.fixture({
            'main.tex': '\\input{first}\\input{second}\nlast\n',
            'first.tex': 'one\n', 'second.tex': 'two\n'})
        self.assertEqual(text, 'one\ntwo\nlast\n')
        self.assertEqual([edge['line'] for edge in edges], [1, 1])
        self.assertEqual([edge['command'] for edge in edges],
                         [r'\input{first}', r'\input{second}'])
        self.assertEqual(locations, [(self.base / 'first.tex', 1),
                                    (self.base / 'second.tex', 1), (self.base / 'main.tex', 2)])

    def test_exact_compact_abstract_preserves_wrapper_and_child_locations(self):
        text, locations, _, edges = self.fixture({
            'main.tex': '\\begin{document}\\maketitle\\begin{abstract}\\input{abstract}\\end{abstract}\n',
            'abstract.tex': 'two\nlines\n'})
        self.assertEqual(text, '\\begin{document}\\maketitle\\begin{abstract}\ntwo\nlines\n\\end{abstract}\n')
        self.assertEqual(locations, [(self.base / 'main.tex', 1),
                                    (self.base / 'abstract.tex', 1),
                                    (self.base / 'abstract.tex', 2), (self.base / 'main.tex', 1)])
        self.assertEqual(edges[0]['line'], 1)

    def test_compact_forms_are_root_only_and_not_general_inline_support(self):
        for line in (r'prefix\input{a}\input{b}', r'\input{a}suffix',
                     r'$\input{a}$', r'\foo{\input{a}}',
                     r'\input{a}\label{x}\input{b}',
                     r'\input{a}\input{b}%comment',
                     r'\input{glyphtounicode}\input{a}'):
            with self.subTest(line=line), self.assertRaisesRegex(ValueError, 'standalone'):
                self.fixture({'main.tex': line + '\n', 'a.tex': 'a\n', 'b.tex': 'b\n'})
        with self.assertRaisesRegex(ValueError, 'standalone'):
            self.fixture({'main.tex': '\\input{child}\n',
                          'child.tex': '\\input{a}\\input{b}\n', 'a.tex': 'a\n', 'b.tex': 'b\n'})

    def test_compact_abstract_without_document_prefix_keeps_source_locations(self):
        text, locations, _, edges = self.fixture({
            'main.tex': '\\begin{document}\\maketitle\n'
                        '  \\begin{abstract} \\input{abstract} \\end{abstract}\nlast\n',
            'abstract.tex': 'first\nsecond'})
        self.assertEqual(text, '\\begin{document}\\maketitle\n'
                              '\\begin{abstract}\nfirst\nsecond\n\\end{abstract}\nlast\n')
        self.assertEqual(locations, [(self.base / 'main.tex', 1), (self.base / 'main.tex', 2),
                                    (self.base / 'abstract.tex', 1), (self.base / 'abstract.tex', 2),
                                    (self.base / 'main.tex', 2), (self.base / 'main.tex', 3)])
        self.assertEqual(edges[0]['line'], 2)
        self.assertEqual(edges[0]['command'], r'\input{abstract}')

    def test_compact_abstract_near_misses_and_child_wrapper_still_fail_closed(self):
        wrapper = r'\begin{abstract}\input{a}\end{abstract}'
        for raw in ('prefix' + wrapper, wrapper + 'suffix', wrapper + '%comment',
                    r'\begin{document}' + wrapper, r'\maketitle' + wrapper,
                    r'\begin{abstract}\input{a}\input{b}\end{abstract}',
                    r'\begin{abstract}\label{x}\input{a}\end{abstract}',
                    r'\begin{abstract}\input{glyphtounicode}\end{abstract}',
                    r'\begin{abstract}\input{a}\end{quote}'):
            with self.subTest(raw=raw), self.assertRaisesRegex(ValueError, 'standalone'):
                self.fixture({'main.tex': raw + '\n', 'a.tex': 'a\n', 'b.tex': 'b\n'})
        with self.assertRaisesRegex(ValueError, 'standalone'):
            self.fixture({'main.tex': '\\input{child}\n', 'child.tex': wrapper + '\n', 'a.tex': 'a\n'})

    def test_compact_abstract_keeps_conditionals_paths_and_repetition_guards(self):
        for raw in ('\\iffalse\n\\begin{abstract}\\input{a}\\end{abstract}\n',
                    '\\begin{abstract}\\input{../a}\\end{abstract}\n',
                    '\\input{a}\n\\begin{abstract}\\input{a}\\end{abstract}\n'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.fixture({'main.tex': raw, 'a.tex': 'a\n'})

    def test_compact_forms_still_reject_conditionals_repeats_and_paths(self):
        for raw in ('\\iffalse\n\\input{a}\\input{b}\n',
                    '\\input{a}\\input{a}\n', '\\input{a}\\input{../b}\n'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.fixture({'main.tex': raw, 'a.tex': 'a\n', 'b.tex': 'b\n'})

    def test_compact_units_do_not_modify_supported_standalone_lines(self):
        line = '  \\input{body} % retained comment\n'
        self.assertEqual(inc.source_line_units(line, is_main=True), [line])

    def test_empty_and_missing_final_newline_keep_line_map(self):
        for child, expected in [("", "\nlast\n"), ("value", "value\nlast\n")]:
            with self.subTest(child=child):
                text, locations, _, _ = self.fixture({
                    "main.tex": "\\input{body}\nlast\n", "body.tex": child})
                self.assertEqual(text, expected)
                self.assertEqual(len(locations), len(text.splitlines()))

    def test_noncanonical_or_nontex_path_fails_closed(self):
        for name in ("../outside", "/tmp/outside", "./body", "data.json"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.fixture({"main.tex": "\\input{" + name + "}\n"})

    def test_symlink_escape_fails_before_read(self):
        original = Path.resolve
        def resolve(path, *args, **kwargs):
            return self.base.parent / "outside.tex" if path.name == "evil.tex" else original(path, *args, **kwargs)
        with patch.object(Path, "resolve", resolve), self.assertRaisesRegex(ValueError, "escapes"):
            self.fixture({"main.tex": "\\input{evil}\n"})

    def test_in_tree_rebinding_and_nontex_targets_fail_before_read(self):
        original = Path.resolve
        for target in ('other.tex', 'references.bib'):
            def resolve(path, *args, **kwargs):
                return self.base / target if path.name == 'body.tex' else original(path, *args, **kwargs)
            with self.subTest(target=target), patch.object(Path, 'resolve', resolve):
                with self.assertRaisesRegex(ValueError, 'symlinked or rebound'):
                    self.fixture({'main.tex': '\\input{body}\n', target: 'wrong source\n'})

    def test_rebound_parent_component_fails_closed(self):
        original = Path.resolve
        def resolve(path, *args, **kwargs):
            if path.parent.name == 'sections':
                return self.base / 'other' / path.name
            return original(path, *args, **kwargs)
        with patch.object(Path, 'resolve', resolve), self.assertRaisesRegex(ValueError, 'symlinked or rebound'):
            self.fixture({'main.tex': '\\input{sections/body}\n', 'other/body.tex': 'wrong\n'})

    def test_non_lf_input_cannot_corrupt_original_label_location(self):
        for separator in ('\r', '\r\n', '\v', '\f', '\x85', '\u2028', '\u2029'):
            with self.subTest(separator=repr(separator)), self.assertRaisesRegex(ValueError, 'non-LF'):
                self.fixture({'main.tex': '\\input{body}\n\\label{eq:x}\n',
                              'body.tex': 'one' + separator + 'two' + separator})

    def test_explicit_cr_normalization_keeps_lf_source_line_and_parent_label(self):
        text, locations, _, _ = self.fixture({
            'main.tex': '\\input{body}\n\\label{eq:x}\n',
            'body.tex': 'one\rtwo\r'}, normalize_cr=True)
        self.assertEqual(text, 'one\ntwo\n\\label{eq:x}\n')
        self.assertEqual(locations, [(self.base / 'body.tex', 1), (self.base / 'body.tex', 1),
                                    (self.base / 'main.tex', 2)])
        node = {'t': 'Link', 'c': [['', [], []], [{'t': 'Str', 'c': '1'}], ['#eq:x', '']]}
        m.remap_links([node], self.base.parent, text, locations)
        self.assertEqual(node['c'][-1][0].split('/')[-1], 'main.tex#L2')

    def test_crlf_and_bare_cr_preserve_original_lf_counts(self):
        self.assertEqual(list(inc.reader_lines('one\r\ntwo\rthree\nfour', normalize_cr=True)),
                         [(1, 'one\n'), (2, 'two\n'), (2, 'three\n'), (3, 'four')])
        for separator in ('\v', '\f', '\x85', '\u2028'):
            with self.assertRaisesRegex(ValueError, 'non-LF'):
                list(inc.reader_lines('one' + separator + 'two', normalize_cr=True))

    def default_reader_fixture(self, blobs, **kwargs):
        def memory_open(path, mode='r', *args, **kw):
            stream = io.BytesIO(blobs[path.name])
            return stream if 'b' in mode else io.TextIOWrapper(stream, encoding='utf-8', newline=kw.get('newline'))
        with patch.object(Path, 'open', memory_open):
            return inc.expand_source_inputs(self.base / 'main.tex', **kwargs)

    def test_default_reader_does_not_hide_cr_before_validation(self):
        with self.assertRaisesRegex(ValueError, 'non-LF'):
            self.default_reader_fixture({'main.tex': b'\\input{body}\n', 'body.tex': b'one\rtwo\n'})

    def test_default_reader_explicit_normalization_preserves_original_lf_lines(self):
        text, locations, _, _ = self.default_reader_fixture({
            'main.tex': b'\\input{body}\n\\label{parent}\n',
            'body.tex': b'one\rtwo\r\\label{child}\n'}, normalize_cr=True)
        self.assertEqual([n for _, n in locations], [1, 1, 1, 2])
        self.assertEqual(locations[-1][0], self.base / 'main.tex')
        self.assertEqual(text, 'one\ntwo\n\\label{child}\n\\label{parent}\n')

    def test_default_reader_preserves_ordinary_lf_source(self):
        text, locations, _, _ = self.default_reader_fixture({
            'main.tex': b'\\input{body}\nlast\n', 'body.tex': b'one\ntwo\n'})
        self.assertEqual(text, 'one\ntwo\nlast\n')
        self.assertEqual([n for _, n in locations], [1, 2, 2])

    def test_missing_source_fails_closed(self):
        with self.assertRaises(FileNotFoundError):
            self.fixture({"main.tex": "\\input{missing}\n"})

    def test_inline_dynamic_and_include_commands_are_rejected(self):
        for line in (r"before \input{body}", r"\input{\name}", r"\input body",
                     r"\include{body}", r"\addbibresource{refs.bib}"):
            with self.subTest(line=line), self.assertRaisesRegex(ValueError, "standalone"):
                self.fixture({"main.tex": line + "\n"})

    def test_conditionals_and_verbatim_are_not_expanded_blindly(self):
        for prefix in (r"\iffalse", r"\ifdefined\foo", r"\catcode", r"\csname",
                       r"\endinput", r"\begin{verbatim}", r"\begin{lstlisting}",
                       r"\IfFileExists{missing}{", r"\InputIfFileExists{body}",
                       r"\begin{comment}", r"\unless", r"\loop"):
            with self.subTest(prefix=prefix), self.assertRaisesRegex(ValueError, "conditional/dynamic/verbatim"):
                self.fixture({"main.tex": prefix + "\n\\input{body}\n", "body.tex": "body\n"})

    def test_glyph_only_conditional_is_rejected_before_resolution(self):
        for wrapper in (r'\iffalse', r'\IfFileExists{missing}{', r'\begin{comment}'):
            tex = wrapper + '\n\\input{glyphtounicode}\n\\begin{document}\nbody\n'
            with self.subTest(wrapper=wrapper), patch.object(m, 'run') as run:
                with self.assertRaisesRegex(ValueError, 'conditional/dynamic/verbatim'):
                    m.prepare_font_mapping_input(tex, self.base)
                run.assert_not_called()

    def test_mathematical_iff_is_not_a_tex_conditional(self):
        text, _, _, _ = self.fixture({"main.tex": "$a\\iff b$\n"})
        self.assertEqual(text, "$a\\iff b$\n")

    def test_repeated_cyclic_and_deep_inputs_fail_closed(self):
        examples = [
            {"main.tex": "\\input{body}\n\\input{body}\n", "body.tex": "body\n"},
            {"main.tex": "\\input{body}\n", "body.tex": "\\input{main}\n"},
        ]
        for example in examples:
            with self.assertRaisesRegex(ValueError, "repeated or cyclic"):
                self.fixture(example)
        with self.assertRaisesRegex(ValueError, "depth"):
            self.fixture({"main.tex": "\\input{body}\n", "body.tex": "body\n"}, max_depth=0)

    def test_glyph_mapping_is_never_loaded_as_a_child(self):
        raw = "\\input{glyphtounicode}\n\\input{body}\n"
        text, _, files, _ = self.fixture({"main.tex": raw, "body.tex": "body\n"})
        self.assertEqual(text, "\\input{glyphtounicode}\nbody\n")
        self.assertEqual(len(files), 2)
        with self.assertRaisesRegex(ValueError, "main preamble"):
            self.fixture({"main.tex": "\\input{body}\n", "body.tex": "\\input{glyphtounicode}\n"})


class InputConversionIntegration(unittest.TestCase):
    def test_compact_manuscript_keeps_separator_disclosure_and_originals(self):
        paper, md, record, report = m.convert(230, source_commit='ab23455ba941e5a14ded27d49de0e874aee811ac')
        self.assertEqual(report['status'], 'FULL_TEX_TO_MARKDOWN_MECHANICAL')
        self.assertIn('Restricted compact/standalone literal', record)
        self.assertIn('Original CR/CRLF separator ledger', record)
        self.assertIn('| 0 | 2 |', record)
        self.assertIn('Source-format notice', md)
        self.assertIn('original LF-delimited', record)
        source = paper / 'paper/sections/2_mass_ceiling.tex'
        self.assertEqual(source.read_bytes().count(b'\r'), 2)

    def test_conditional_manuscript_cannot_receive_full_status(self):
        paper = next((m.ROOT / 'papers').glob('tpc-245-*'))
        main = paper / 'paper/main.tex'
        original_bytes = Path.read_bytes
        original_run = m.subprocess.run
        command = b'\\input{sections/3_classification}'
        replacement = b'\\IfFileExists{definitely-missing}{\n' + command + b'\n}{fallback}'
        mutated = original_bytes(main).replace(command, replacement)
        self.assertNotEqual(mutated, original_bytes(main))
        def read_bytes(path):
            return mutated if path == main else original_bytes(path)
        def run(args, *positional, **kwargs):
            result = original_run(args, *positional, **kwargs)
            if args[:2] == ['git', 'show'] and args[2].endswith(':' + str(main.relative_to(m.ROOT))):
                result.stdout = mutated
            return result
        with patch.object(Path, 'read_bytes', read_bytes), patch.object(m.subprocess, 'run', run):
            with self.assertRaisesRegex(ValueError, 'conditional/dynamic/verbatim'):
                m.convert(245, source_commit='ab23455ba941e5a14ded27d49de0e874aee811ac')

    def test_in_tree_rebound_manuscript_cannot_receive_full_status(self):
        original = Path.resolve
        paper = next((m.ROOT / 'papers').glob('tpc-245-*'))
        def resolve(path, *args, **kwargs):
            return paper / 'paper/references.bib' if path.name == '3_classification.tex' else original(path, *args, **kwargs)
        with patch.object(Path, 'resolve', resolve), self.assertRaisesRegex(ValueError, 'symlinked or rebound'):
            m.convert(245, source_commit='ab23455ba941e5a14ded27d49de0e874aee811ac')

    def test_child_equation_links_keep_original_file_and_line(self):
        paper = m.ROOT / "DOES_NOT_EXIST_INPUT_FIXTURE"
        child = paper / "paper/sections/body.tex"
        node = {"t": "Link", "c": [["", [], []], [{"t": "Str", "c": "1"}], ["#eq:x", ""]]}
        m.remap_links([node], paper, "heading\n\\label{eq:x}\n",
                      [(paper / "paper/main.tex", 1), (child, 7)])
        self.assertEqual(node["c"][-1][0], "sections/body.tex#L7")

    def test_multifile_body_and_provenance_are_not_just_main_skeleton(self):
        _, md, record, report = m.convert(245, source_commit="ab23455ba941e5a14ded27d49de0e874aee811ac")
        self.assertEqual(report["status"], "FULL_TEX_TO_MARKDOWN_MECHANICAL")
        self.assertEqual(report["math_nodes"], 95)
        self.assertIn("Static TeX dependency provenance", record)
        self.assertIn("paper/sections/3_classification.tex#L", record)
        self.assertIn("dependency ledger", md)
        self.assertNotIn(r"\input{sections/0_abstract}", md)

    def test_changed_included_source_is_not_accepted(self):
        read_bytes = Path.read_bytes
        def tampered(path):
            blob = read_bytes(path)
            return blob + b"\nchanged\n" if path.name == "3_classification.tex" else blob
        with patch.object(Path, "read_bytes", tampered), self.assertRaisesRegex(ValueError, "source differs"):
            m.convert(245, source_commit="ab23455ba941e5a14ded27d49de0e874aee811ac")


if __name__ == "__main__":
    unittest.main()
