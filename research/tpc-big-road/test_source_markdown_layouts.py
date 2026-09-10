"""Read-only regressions for explicit directory identity and source layouts."""
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import maintain_source_markdown as m
import check_source_markdown_batch as batch


class SourceLayoutTests(unittest.TestCase):
    paper = m.ROOT / 'papers/tpc-200-four-form-determinant-resonance-refinement'
    critical = 'tpc-207-critical-moving-hole-bdh-defect'
    missing = 'tpc-207-moving-hole-bdh-translation-compiler'

    def virtual_files(self, versioned, local, rebound=None, symlinks=()):
        stack = ExitStack()
        entries = {str(path.relative_to(m.ROOT)) for path in versioned}
        def git(args, **kwargs):
            self.assertEqual(args[:3], ['git', 'cat-file', '-e'])
            return SimpleNamespace(returncode=0 if args[3].split(':', 1)[1] in entries else 1)
        stack.enter_context(patch.object(m.subprocess, 'run', side_effect=git))
        stack.enter_context(patch.object(Path, 'is_file', lambda path: path in local))
        stack.enter_context(patch.object(Path, 'exists', lambda path: path in local))
        stack.enter_context(patch.object(Path, 'is_symlink', lambda path: path in symlinks))
        stack.enter_context(patch.object(Path, 'resolve', lambda path: (rebound or {}).get(path, path.absolute())))
        return stack

    def test_exact_existing_root_directory(self):
        self.assertEqual(m.select_paper(200), self.paper)
        self.assertEqual(m.select_paper(200, self.paper.name), self.paper)

    def test_duplicate_number_requires_explicit_directory(self):
        with self.assertRaisesRegex(ValueError, 'expected one existing directory'):
            m.select_paper(207)
        self.assertEqual(m.select_paper(207, self.critical).name, self.critical)
        self.assertEqual(m.select_paper(207, self.missing).name, self.missing)

    def test_exact_missing_source_does_not_fall_back_to_sibling(self):
        paper = m.select_paper(207, self.missing)
        with self.assertRaisesRegex(ValueError, 'exactly one versioned main.tex'):
            m.manuscript_source(paper)

    def test_invalid_directory_identity_rejected(self):
        for value in ['', '../' + self.critical, '/tmp/' + self.critical,
                      self.critical + '/main.tex', self.critical + '*',
                      'tpc-0207-critical-moving-hole-bdh-defect',
                      'tpc-208-zero-hole-additive-edge-frame', self.critical + '\n', True]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                m.select_paper(207, value)

    def test_invalid_number_type_rejected(self):
        for value in [0, -1, True, 200.0, '200']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                m.select_paper(value)

    def test_rebound_paper_directory_rejected(self):
        with patch.object(Path, 'resolve', lambda path: self.paper.parent / 'replacement'):
            with self.assertRaisesRegex(ValueError, 'rebound paper'):
                m.select_paper(200)

    def test_exact_layouts_selected(self):
        root, nested = self.paper / 'main.tex', self.paper / 'paper/main.tex'
        for selected in [root, nested]:
            with self.subTest(selected=selected), self.virtual_files([selected], [selected]):
                self.assertEqual(m.manuscript_source(self.paper), selected)

    def test_two_versioned_layouts_rejected(self):
        roots = [self.paper / 'main.tex', self.paper / 'paper/main.tex']
        with self.virtual_files(roots, roots), self.assertRaisesRegex(ValueError, 'exactly one'):
            m.manuscript_source(self.paper)

    def test_unversioned_main_is_not_a_source(self):
        root = self.paper / 'main.tex'
        with self.virtual_files([], [root]), self.assertRaisesRegex(ValueError, 'exactly one'):
            m.manuscript_source(self.paper)

    def test_untracked_competing_layout_rejected(self):
        root, nested = self.paper / 'main.tex', self.paper / 'paper/main.tex'
        for selected, other in [(root, nested), (nested, root)]:
            with self.subTest(selected=selected), self.virtual_files([selected], [selected, other]):
                with self.assertRaisesRegex(ValueError, 'competing local'):
                    m.manuscript_source(self.paper)

    def test_dangling_competing_layout_rejected(self):
        root, nested = self.paper / 'main.tex', self.paper / 'paper/main.tex'
        with self.virtual_files([root], [root], symlinks=[nested]):
            with self.assertRaisesRegex(ValueError, 'competing local'):
                m.manuscript_source(self.paper)

    def test_missing_or_rebound_versioned_source_rejected(self):
        root = self.paper / 'main.tex'
        for local, rebound in [([], {}), ([root], {root: self.paper / 'replacement.tex'})]:
            with self.subTest(local=local), self.virtual_files([root], local, rebound):
                with self.assertRaisesRegex(ValueError, 'missing, symlinked or rebound'):
                    m.manuscript_source(self.paper)

    def test_root_pdf_priority_uses_exact_basename(self):
        names = [self.paper / (self.paper.name + '.pdf'), self.paper / 'main.pdf', self.paper / 'paper.pdf']
        for i in range(3):
            with self.subTest(first=i), self.virtual_files(names[i:], names):
                self.assertEqual(m.preserved_pdf(self.paper, source_path=self.paper / 'main.tex'), names[i])

    def test_ignored_root_pdf_does_not_override_versioned(self):
        primary, fallback = self.paper / (self.paper.name + '.pdf'), self.paper / 'main.pdf'
        with self.virtual_files([fallback], [primary, fallback]):
            self.assertEqual(m.preserved_pdf(self.paper, source_path=self.paper / 'main.tex'), fallback)

    def test_no_cross_layout_or_figure_pdf_fallback(self):
        candidates = [self.paper / 'paper/main.pdf', self.paper / 'figure.pdf']
        with self.virtual_files(candidates, candidates), self.assertRaisesRegex(ValueError, 'no preserved'):
            m.preserved_pdf(self.paper, source_path=self.paper / 'main.tex')

    def test_missing_or_rebound_pdf_fails_without_fallback(self):
        primary, fallback = self.paper / (self.paper.name + '.pdf'), self.paper / 'main.pdf'
        for local, rebound in [([fallback], {}), ([primary, fallback], {primary: fallback})]:
            with self.subTest(local=local), self.virtual_files([primary, fallback], local, rebound):
                with self.assertRaisesRegex(ValueError, 'missing, symlinked or rebound'):
                    m.preserved_pdf(self.paper, source_path=self.paper / 'main.tex')

    def test_unsupported_pdf_source_layout_rejected(self):
        for source in [self.paper / 'other.tex', self.paper.parent / 'main.tex']:
            with self.subTest(source=source), self.assertRaisesRegex(ValueError, 'exact main.tex candidate'):
                m.preserved_pdf(self.paper, source_path=source)

    def test_root_label_points_back_to_original(self):
        blocks = [{'t': 'Link', 'c': [['', [], []], [], ['#target', '']]}]
        m.remap_links(blocks, self.paper, '\\label{target}\n', source_path=self.paper / 'main.tex')
        self.assertEqual(blocks[0]['c'][-1][0], '../main.tex#L1')

    def test_batch_exact_override(self):
        self.assertEqual(batch.paper_overrides([self.critical], 200, 209), {207: self.critical})
        self.assertEqual(batch.paper_overrides([], 200, 209), {})

    def test_batch_malformed_duplicate_or_out_of_range_override_rejected(self):
        for names in [[self.critical, self.critical], [self.critical, self.missing],
                      ['../' + self.critical], [self.paper.name],
                      ['tpc-207-nonexistent'], ['tpc-0207-critical-moving-hole-bdh-defect']]:
            with self.subTest(names=names), self.assertRaises(ValueError):
                batch.paper_overrides(names, 207, 209)

    def test_actual_root_source_links_and_roundtrip(self):
        paper, md, record, report = m.convert(200, source_commit='ab23455ba941e5a14ded27d49de0e874aee811ac')
        self.assertEqual(paper, self.paper)
        self.assertTrue(report['text_roundtrip'])
        self.assertEqual(report['status'], 'FULL_TEX_TO_MARKDOWN_MECHANICAL')
        self.assertIn('[main.tex](../main.tex)', md)
        self.assertIn('[references.bib](../references.bib)', md)
        self.assertIn('](' + '../' + paper.name + '.pdf)', md)
        self.assertIn('- TeX: [main.tex](main.tex)', record)
        self.assertIn('paper/main.md with links back', record)

    def test_actual_duplicate_source_is_only_explicit_critical(self):
        paper, _, record, report = m.convert(207, paper_name=self.critical,
                                            source_commit='ab23455ba941e5a14ded27d49de0e874aee811ac')
        self.assertEqual(paper.name, self.critical)
        self.assertEqual(report['math_nodes'], 170)
        self.assertIn('- TeX: [paper/main.tex](paper/main.tex)', record)
        with self.assertRaisesRegex(ValueError, 'exactly one versioned'):
            m.convert(207, paper_name=self.missing)


if __name__ == '__main__':
    unittest.main()
