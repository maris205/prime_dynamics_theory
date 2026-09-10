"""Read-only original-byte line-anchor checks; no fixture files are created."""
from pathlib import Path
import unittest
from unittest.mock import patch

import check_source_markdown_batch as checker


class SourceLineLinks(unittest.TestCase):
    def check_fixture(self, blob, line):
        document = checker.m.ROOT / 'DOES_NOT_EXIST_LINK_FIXTURE/document.md'
        with patch.object(Path, 'read_text', return_value=f'[source](body.tex#L{line})\n'), \
             patch.object(Path, 'read_bytes', return_value=blob), \
             patch.object(Path, 'exists', return_value=True), \
             patch.object(Path, 'is_file', return_value=True):
            return checker.check_links(document)

    def test_raw_lf_counts(self):
        for blob, expected in [(b'', 0), (b'\n', 1), (b'one', 1), (b'one\n', 1),
                               (b'one\r\ntwo\n', 2), (b'one\rtwo\rthree\n', 1)]:
            with self.subTest(blob=blob):
                self.assertEqual(checker.source_line_count(blob), expected)

    def test_cr_only_extra_anchor_is_rejected(self):
        count, issues = self.check_fixture(b'one\rtwo\rthree\n', 3)
        self.assertEqual(count, 1)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['problem'], 'invalid source-line anchor')

    def test_original_line_still_valid_with_cr_fragments(self):
        self.assertEqual(self.check_fixture(b'one\rtwo\rthree\n', 1), (1, []))

    def test_unterminated_last_line_is_counted(self):
        self.assertEqual(self.check_fixture(b'one\ntwo', 2), (1, []))

    def test_empty_file_has_no_line_one(self):
        count, issues = self.check_fixture(b'', 1)
        self.assertEqual(count, 1)
        self.assertEqual(len(issues), 1)


if __name__ == '__main__':
    unittest.main()
