"""Read-only regression tests for archival conversion; no source/build writes."""
import json
import unittest

import maintain_source_markdown as m


class ConversionHelpers(unittest.TestCase):
    def test_numeric_math_boundary_is_whitespace_only_and_idempotent(self):
        blocks = [{"t": "Para", "c": [{"t": "Str", "c": "64"},
                  {"t": "Math", "c": [{"t": "InlineMath"}, r"\to"]},
                  {"t": "Str", "c": "128"}]}]
        before = m.math_signature(blocks)
        self.assertEqual(m.separate_math_from_digits(blocks), 1)
        self.assertEqual(blocks[0]["c"][2], {"t": "Space"})
        self.assertEqual(m.math_signature(blocks), before)
        self.assertEqual(m.separate_math_from_digits(blocks), 0)

    def test_safe_math_boundaries_unchanged(self):
        for kind, following in [("InlineMath", "x"), ("DisplayMath", "128")]:
            blocks = [{"t": "Math", "c": [{"t": kind}, "a"]},
                      {"t": "Str", "c": following}]
            before = json.dumps(blocks)
            self.assertEqual(m.separate_math_from_digits(blocks), 0)
            self.assertEqual(json.dumps(blocks), before)

    def test_numeric_math_boundary_roundtrip_in_quote_table(self):
        tex = (r"\begin{quote}\begin{tabular}{cc}"
               r"pair & value\\64\(\to\)128 & \(x\)\\"
               r"96\(\to\)192 & \(y\)\end{tabular}\end{quote}")
        ast = json.loads(m.run(["pandoc", "-f", "latex", "-t", "json"], data=tex)[0])
        before_math = m.math_signature(ast["blocks"])
        before_text = m.text_signature(ast, ast["blocks"])
        self.assertEqual(m.separate_math_from_digits(ast["blocks"]), 2)
        md = m.write_ast(ast, ast["blocks"])
        reread = json.loads(m.run(["pandoc", "-f", m.FORMAT, "-t", "json"], data=md)[0])
        self.assertEqual(m.math_signature(reread["blocks"]), before_math)
        self.assertEqual(m.text_signature(ast, reread["blocks"]), before_text)

    def test_document_tail_is_not_deleted_or_parsed(self):
        tex = "body\n" + r"\end{document}" + "\n`broken_token`\n"
        document, tail = m.split_document_tail(tex)
        self.assertEqual(document + tail, tex)
        self.assertEqual(tail, "\n`broken_token`\n")

    def test_empty_document_tail_is_byte_unchanged(self):
        tex = "body\n" + r"\end{document}" + "\n\n"
        self.assertEqual(m.split_document_tail(tex), (tex, ""))

    def test_ambiguous_document_terminators_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "multiple document terminators"):
            m.split_document_tail((r"\end{document}" + "\n") * 2)

    def test_terminal_letters_are_not_whitespace(self):
        self.assertEqual(m.normalize_eof("text  \nhighest\t\nt\n\n"), "text\nhighest\nt\n")

    def test_original_main_pdf_has_priority(self):
        paper = m.ROOT / 'papers/tpc-308-adversarial-exclusive-completion-envelope'
        self.assertTrue((paper / 'paper/paper.pdf').is_file())
        self.assertEqual(m.preserved_pdf(paper), paper / 'paper/main.pdf')

    def test_no_known_original_pdf_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "no preserved"):
            m.preserved_pdf(m.ROOT / 'DOES_NOT_EXIST_TEST_ONLY')

    def test_balanced_nested_title(self):
        raw = r"{A $L^{2}$ title}ignored"
        self.assertEqual(m.balanced_group(raw, 0)[0], "A $L^{2}$ title")

    def test_display_counts_not_line_breaks(self):
        raw = r"Title\\[5pt] \[x=1\] \begin{align}a&=b\\c&=d\end{align}"
        self.assertEqual(len(list(m.display_blocks(raw))), 2)
        self.assertEqual(list(m.display_blocks(raw))[0]['source'], r"\[x=1\]")

    def test_missing_pdf_heading_is_unmapped(self):
        sec = [{"plain": "An absent heading"}]
        m.pdf_page_map(sec, ["1 Another heading\ncontent", "2 Final heading"])
        self.assertEqual(sec[0]["pdf_pages"], [])
        self.assertEqual(sec[0]["map_status"], "UNMAPPED_OR_AMBIGUOUS")

    def test_multiline_pdf_heading_matches_actual_page(self):
        sec = [{"plain": "A long actual heading"}]
        m.pdf_page_map(sec, ["1 Other text", "2 A long actual\n heading\nbody"])
        self.assertEqual(sec[0]["pdf_pages"], [2])

    def test_patch_has_one_terminal_newline(self):
        patch = m.patch_for(m.ROOT / "DOES_NOT_EXIST_TEST_ONLY.md", "text\n\n")
        self.assertTrue(patch.endswith("+text\n"))

    def test_equation_links_point_to_preserved_source(self):
        link = {"t": "Link", "c": [["", [], []], [{"t": "Str", "c": "1"}], ["#eq:x", ""]]}
        changes = m.remap_links([link], m.ROOT, "line one\n" + r"\label{eq:x}")
        self.assertEqual(link["c"][-1][0], "main.tex#L2")
        self.assertEqual(len(changes), 1)

    def test_repository_relative_link_relocated(self):
        paper = m.ROOT / 'papers/tpc-387-c1-count-ladder-renormalization'
        link = {"t": "Link", "c": [["", [], []], [{"t": "Str", "c": "source"}], [str(paper.relative_to(m.ROOT)) + '/', ""]]}
        m.remap_links([link], paper)
        self.assertEqual(link['c'][-1][0], '..')


class ConversionIntegration(unittest.TestCase):
    def test_numeric_table_arrows_preserved(self):
        _, md, record, report = m.convert(270, source_commit="6be994e34a06fda0de2ed0bcaa42ff3db716ffef")
        self.assertEqual(report["math_nodes"], 67)
        self.assertTrue(report["text_roundtrip"])
        self.assertEqual(report["status"], "FULL_TEX_TO_MARKDOWN_MECHANICAL")
        self.assertIn(r"64$\to$ 128", md)
        self.assertIn("4 whitespace separator(s)", record)

    def test_post_document_source_retained_with_scope(self):
        paper, md, record, report = m.convert(294, source_commit="7bba57e68d04514ee33ab2192a507a1f4edfebab")
        _, tail = m.split_document_tail((paper / 'paper/main.tex').read_text())
        self.assertIn(tail.strip("\r\n"), md)
        self.assertIn("Post-document source (uninterpreted)", md)
        self.assertIn("begins at TeX line 252", record)
        self.assertIn(m.digest(tail), record)
        self.assertTrue(report['text_roundtrip'])
        self.assertEqual(report['status'], 'FULL_TEX_TO_MARKDOWN_MECHANICAL')

    def test_original_paper_pdf_fallback_keeps_provenance(self):
        paper, md, record, report = m.convert(305, source_commit="ed725e6537012bd17a32d061d9d8e6dd3b253613")
        self.assertEqual(m.preserved_pdf(paper), paper / 'paper/paper.pdf')
        self.assertIn("Preserved PDF: [paper.pdf](paper.pdf)", md)
        self.assertIn("Preserved PDF: [paper/paper.pdf](paper/paper.pdf)", record)
        self.assertEqual(report['pdf_sha256'], m.digest((paper / 'paper/paper.pdf').read_bytes()))
        self.assertTrue(report['text_roundtrip'])

    def test_supplemental_scope_persists(self):
        _, md, record, report = m.convert(349, source_commit="1de1964aa411aa631587da690524beadf1127d3c")
        self.assertIn("Supplemental prerequisite audit:", record)
        self.assertIn("TPC_CONVERSION_SCOPE_TPC345_349.md", record)
        self.assertTrue(report['text_roundtrip'])

    def test_source_bibliography_retained(self):
        _, md, record, report = m.convert(350, source_commit="388a605cbc0ce49256310c2efc1f2df77edafadd")
        self.assertTrue(report["text_roundtrip"])
        self.assertIn("# References", md)
        self.assertIn("John B. Conway", md)
        self.assertIn("**Theorem", md)
        self.assertIn("**Proof**", md)
        self.assertIn("Bibliography/reference section detected: `YES`", record)

    def test_external_bib_preserved_with_hash(self):
        _, md, record, report = m.convert(356, source_commit="388a605cbc0ce49256310c2efc1f2df77edafadd")
        self.assertTrue(report["text_roundtrip"])
        self.assertIn("@misc{v59,", md)
        self.assertIn("paper/references.bib", record)

    def test_missing_proof_package_never_passes(self):
        _, md, record, report = m.convert(360, source_commit="388a605cbc0ce49256310c2efc1f2df77edafadd")
        self.assertIn("Separate proof package: `ABSENT`", record)
        self.assertIn("NOT_INDEPENDENTLY_REPROVED", record)

    def test_current_endpoint_preserves_math(self):
        _, md, record, report = m.convert(418, source_commit="388a605cbc0ce49256310c2efc1f2df77edafadd")
        self.assertEqual(report["math_nodes"], 48)
        self.assertTrue(report["text_roundtrip"])
        self.assertIn("sigma", md)


if __name__ == "__main__":
    unittest.main()
