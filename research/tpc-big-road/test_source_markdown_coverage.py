"""No-write checks for current-versus-historical archive coverage receipts."""
from contextlib import ExitStack, redirect_stdout
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import check_source_markdown_batch as batch


class CurrentCoverage(unittest.TestCase):
    marker = 'Current coverage is'
    expected = {'full-source-md': 199, 'reliable-full-md': 0,
                'partial-or-notes': 623, 'source-inaccessible': 1}

    def paragraph(self, **changes):
        values = self.expected | changes
        return self.marker + ' ' + ',\n'.join(f'`{key}={values[key]}`' for key in batch.COVERAGE_KEYS) + '.'

    def check(self, content):
        return batch.current_coverage_issues(content, self.marker, self.expected)

    def test_matching_wrapped_current_counts(self):
        self.assertEqual(self.check(self.paragraph()), [])

    def test_historical_counts_do_not_override_current_paragraph(self):
        content = '`full-source-md=189`, `partial-or-notes=633` in the prior batch.\n\n' + self.paragraph()
        self.assertEqual(self.check(content), [])

    def test_stale_current_counts_fail_even_when_other_paragraph_is_correct(self):
        stale = self.paragraph(**{'full-source-md': 189, 'partial-or-notes': 633})
        correct_elsewhere = self.paragraph().replace(self.marker, 'A separate record says')
        self.assertIn('stale current coverage', self.check(stale + '\n\n' + correct_elsewhere)[0])

    def test_missing_or_duplicate_marker_fails(self):
        for content in ('', self.paragraph() + '\n\n' + self.paragraph()):
            with self.subTest(content=content):
                self.assertIn('exactly one', self.check(content)[0])

    def test_missing_field_is_not_taken_from_later_paragraph(self):
        content = self.paragraph().replace(',\n`source-inaccessible=1`', '')
        self.assertIn('each status exactly once', self.check(content + '\n\n`source-inaccessible=1`')[0])

    def test_duplicate_status_cannot_replace_missing_status(self):
        content = self.paragraph().replace('`source-inaccessible=1`', '`reliable-full-md=0`')
        self.assertIn('each status exactly once', self.check(content)[0])

    def test_malformed_count_is_rejected(self):
        for value in ('-1', 'true', '1.0', 'NaN'):
            with self.subTest(value=value):
                content = self.paragraph().replace('`source-inaccessible=1`', f'`source-inaccessible={value}`')
                self.assertIn('each status exactly once', self.check(content)[0])

    def test_reliable_status_cannot_be_silently_promoted(self):
        self.assertIn('stale current coverage', self.check(self.paragraph(**{'reliable-full-md': 1}))[0])

    def test_history_marker_uses_same_protocol(self):
        marker = 'The archive inventory is now'
        self.assertEqual(batch.current_coverage_issues(
            self.paragraph().replace(self.marker, marker), marker, self.expected), [])

    def test_extra_malformed_duplicate_is_not_ignored(self):
        for marker in (self.marker, 'The archive inventory is now'):
            for value in ('-1', 'true', '1.0', 'NaN', ''):
                with self.subTest(marker=marker, value=value):
                    content = self.paragraph().replace(self.marker, marker) + f' `source-inaccessible={value}`'
                    issues = batch.current_coverage_issues(content, marker, self.expected)
                    self.assertIn('each status exactly once', issues[0])

    def run_mock_main(self, overrides=None):
        root = batch.m.ROOT
        documents = {root / 'TPC_HANDOFF.md': self.paragraph(),
                     root / 'research/tpc-big-road/TPC_HISTORY_SUMMARY.md':
                     self.paragraph().replace(self.marker, 'The archive inventory is now')}
        documents.update(overrides or {})
        def read_text(path, *args, **kwargs):
            return documents[path]
        report = {'paper': 210, 'math_nodes': 1, 'text_roundtrip': True, 'unmapped': 0}
        stream = io.StringIO()
        with ExitStack() as stack:
            stack.enter_context(patch('sys.argv', ['batch', '--first', '210', '--last', '210']))
            stack.enter_context(patch.object(batch, 'check_paper', return_value=(report, [])))
            stack.enter_context(patch.object(batch, 'check_links', return_value=(0, [])))
            stack.enter_context(patch.object(batch.inventory, 'outputs', return_value=({}, self.expected)))
            stack.enter_context(patch.object(Path, 'read_text', read_text))
            stack.enter_context(patch.object(batch.m, 'convert', side_effect=AssertionError('no source reads')))
            stack.enter_context(patch.object(batch.m, 'run', side_effect=AssertionError('no subprocess')))
            stack.enter_context(patch.object(batch.inventory, 'inventory', side_effect=AssertionError('no scan')))
            stack.enter_context(redirect_stdout(stream))
            try:
                batch.main()
                code = 0
            except SystemExit as exc:
                code = exc.code
        return code, json.loads(stream.getvalue())

    def test_integrated_main_accepts_current_counts_without_source_work(self):
        code, report = self.run_mock_main()
        self.assertEqual(code, 0)
        self.assertEqual(report['current_coverage_issues'], [])

    def test_integrated_main_rejects_extra_malformed_duplicates(self):
        root = batch.m.ROOT
        for path, marker in ((root / 'TPC_HANDOFF.md', self.marker),
                             (root / 'research/tpc-big-road/TPC_HISTORY_SUMMARY.md',
                              'The archive inventory is now')):
            for value in ('-1', 'true', '1.0', 'NaN', ''):
                with self.subTest(path=path, value=value):
                    content = self.paragraph().replace(self.marker, marker) + f' `source-inaccessible={value}`'
                    code, report = self.run_mock_main({path: content})
                    self.assertEqual(code, 1)
                    self.assertEqual(len(report['current_coverage_issues']), 1)


if __name__ == '__main__':
    unittest.main()
