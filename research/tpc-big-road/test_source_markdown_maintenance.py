"""Read-only regression tests for archival conversion; no source/build writes."""
import json
import unittest

import maintain_source_markdown as m


class ConversionHelpers(unittest.TestCase):
    def test_terminal_letters_are_not_whitespace(self):
        self.assertEqual(m.normalize_eof("text  \nhighest\t\nt\n\n"), "text\nhighest\nt\n")

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
