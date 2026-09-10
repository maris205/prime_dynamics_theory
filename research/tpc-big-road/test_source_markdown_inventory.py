"""Focused read-only tests for inventory/backlog separation and patch planning."""
import unittest
from unittest.mock import MagicMock, patch

import refresh_source_markdown_inventory as inventory


class InventoryTests(unittest.TestCase):
    def sample(self):
        return [
            ('TPC', 'tpc-1-full', 1, 1, 3, 'full-source-md', '`paper/main.md`'),
            ('TPC', 'tpc-2-pending', 1, 1, 1, 'partial-or-notes', '`README.md`'),
            ('TPC', 'tpc-3-missing', 0, 0, 0, 'source-inaccessible', '—'),
            ('RH', 'RH-1-pending', 1, 1, 1, 'partial-or-notes', '`README.md`'),
        ]

    def render(self, rows):
        with patch.object(inventory, 'link', side_effect=lambda path, label=None: label or path.name):
            return inventory.remaining_work(rows)

    def test_all_directories_listed_once(self):
        text = self.render(self.sample())
        for row in self.sample():
            self.assertEqual(text.count('| ' + row[1] + ' |'), 1)
        self.assertIn('all 4 preserved', text)

    def test_mechanical_is_not_reliable(self):
        text = self.render(self.sample())
        self.assertIn('| TPC | 3 | 1 | 0 | 1 | 1 |', text)
        self.assertIn('| RH | 1 | 0 | 0 | 1 | 0 |', text)
        self.assertIn('All 4 directories still lack', text)
        self.assertIn('independent full-content/semantic review and PDF/source reconciliation remain', text)

    def test_inaccessible_not_counted_as_reviewed(self):
        text = self.render(self.sample())
        self.assertIn('inaccessible originals are included', text)
        self.assertIn('Locate the missing original manuscript', text)

    def test_explicit_reliable_status_is_not_pending(self):
        rows = self.sample()
        rows[0] = (*rows[0][:5], 'reliable-full-md', rows[0][6])
        text = self.render(rows)
        self.assertIn('| TPC | 3 | 0 | 1 | 1 | 1 |', text)
        self.assertIn('All 3 directories still lack', text)

    def test_missing_file_emits_add_without_read(self):
        path = MagicMock()
        path.__str__.return_value = '/archive/remaining.md'
        path.exists.return_value = False
        self.assertEqual(inventory.compact_patch(path, '# Title\n\nBody\n'),
                         '*** Add File: /archive/remaining.md\n+# Title\n+\n+Body\n')
        path.read_text.assert_not_called()

    def test_unchanged_file_has_no_patch(self):
        path = MagicMock()
        path.exists.return_value = True
        path.read_text.return_value = 'unchanged\n'
        self.assertEqual(inventory.compact_patch(path, 'unchanged\n'), '')

    def test_stop_and_manuscript_selection_remain_explicit(self):
        text = self.render(self.sample())
        self.assertIn('NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES', text)
        self.assertIn('fixed-power credit `0`', text)
        self.assertIn('figure PDF or an ignored local build', text)


if __name__ == '__main__':
    unittest.main()
