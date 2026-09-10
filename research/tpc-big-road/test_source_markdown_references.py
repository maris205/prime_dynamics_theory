"""Read-only tests for ordered, source-locked multi-target reference links."""
import copy
import json
import unittest

import maintain_source_markdown as m


class MultiSourceReferences(unittest.TestCase):
    paper = m.ROOT / 'papers/tpc-181-metric-fixed-atom-selector-gate'
    tex = '\\label{a}\nline two\n\\label{b}\n\\label{c}\n'

    def reference(self, labels='a,b,c'):
        return {'t': 'Link', 'c': [['', [], [['reference-type', 'ref'],
                 ['reference', labels]]], [{'t': 'Str', 'c': '[' + labels + ']'}],
                 ['#' + labels, '']]}

    def targets(self, node):
        return [link['c'][-1][0] for link in m.nodes(node, 'Link')]

    def test_root_targets_keep_order_and_visible_text(self):
        node = self.reference('c,a,b')
        changes = m.remap_links([node], self.paper, self.tex,
                                source_path=self.paper / 'main.tex')
        self.assertEqual(self.targets(node), ['../main.tex#L4', '../main.tex#L1', '../main.tex#L3'])
        self.assertEqual(''.join(n['c'] for n in m.nodes(node, 'Str')), '[c,a,b]')
        self.assertEqual(changes, [('#c', '../main.tex#L4'), ('#a', '../main.tex#L1'),
                                   ('#b', '../main.tex#L3')])

    def test_nested_source_default(self):
        node = self.reference()
        m.remap_links([node], self.paper, self.tex)
        self.assertEqual(self.targets(node), ['main.tex#L1', 'main.tex#L3', 'main.tex#L4'])

    def test_included_labels_use_original_child_lines(self):
        node = self.reference('c,a,b')
        child = self.paper / 'sections/claims.tex'
        locations = [(child, 20), (child, 21), (self.paper / 'main.tex', 8), (child, 25)]
        m.remap_links([node], self.paper, self.tex, locations)
        self.assertEqual(self.targets(node), ['../sections/claims.tex#L25',
                                             '../sections/claims.tex#L20', '../main.tex#L8'])

    def test_missing_label_fails_before_rewriting_group(self):
        node = self.reference('a,missing,c')
        original = copy.deepcopy(node)
        with self.assertRaisesRegex(ValueError, 'missing or duplicate'):
            m.remap_links([node], self.paper, self.tex)
        self.assertEqual(node, original)

    def test_duplicate_source_label_fails_before_rewriting_group(self):
        node = self.reference()
        original = copy.deepcopy(node)
        with self.assertRaisesRegex(ValueError, 'missing or duplicate'):
            m.remap_links([node], self.paper, self.tex + '\\label{a}\n')
        self.assertEqual(node, original)

    def test_repeated_reference_is_not_deduplicated(self):
        node = self.reference('b,a,b')
        m.remap_links([node], self.paper, self.tex)
        self.assertEqual(self.targets(node), ['main.tex#L3', 'main.tex#L1', 'main.tex#L3'])
        self.assertEqual(''.join(n['c'] for n in m.nodes(node, 'Str')), '[b,a,b]')

    def test_empty_or_whitespace_component_fails(self):
        for labels in ['a,,b', ',a', 'a,', 'a, b', 'a,\nb']:
            with self.subTest(labels=labels), self.assertRaisesRegex(ValueError, 'shape'):
                m.remap_links([self.reference(labels)], self.paper, self.tex)

    def test_noncanonical_visible_text_or_metadata_fails(self):
        variants = []
        for index, value in [(0, ['id', [], [['reference-type', 'ref'], ['reference', 'a,b,c']]]),
                             (1, [{'t': 'Str', 'c': 'Theorems 1–3'}]),
                             (2, ['#a,b,c', 'custom title'])]:
            node = self.reference()
            node['c'][index] = value
            variants.append(node)
        for node in variants:
            original = copy.deepcopy(node)
            with self.subTest(node=node), self.assertRaisesRegex(ValueError, 'shape'):
                m.remap_links([node], self.paper, self.tex)
            self.assertEqual(node, original)

    def test_untyped_link_and_image_are_not_split(self):
        nodes = [self.reference() for _ in range(3)]
        nodes[0]['c'][0][2] = []
        nodes[1]['c'][0][2][1][1] = 'different-reference'
        nodes[2]['t'] = 'Image'
        for node in nodes:
            original = copy.deepcopy(node)
            self.assertEqual(m.remap_links([node], self.paper, self.tex), [])
            self.assertEqual(node, original)

    def test_extra_payload_is_rejected_without_content_loss(self):
        variants = [self.reference() for _ in range(3)]
        extra_math = {'t': 'Math', 'c': [{'t': 'InlineMath'}, 'x^2']}
        variants[0]['c'].insert(2, copy.deepcopy(extra_math))
        variants[1]['c'][-1].append(copy.deepcopy(extra_math))
        variants[2]['extra'] = copy.deepcopy(extra_math)
        for node in variants:
            original = copy.deepcopy(node)
            before_math = m.math_signature(node)
            with self.subTest(node=node), self.assertRaisesRegex(ValueError, 'shape'):
                m.remap_links([node], self.paper, self.tex)
            self.assertEqual(node, original)
            self.assertEqual(m.math_signature(node), before_math)

    def test_exact_comma_containing_label_has_priority(self):
        node = self.reference()
        m.remap_links([node], self.paper, self.tex + '\\label{a,b,c}\n')
        self.assertEqual(node['t'], 'Link')
        self.assertEqual(self.targets(node), ['main.tex#L5'])

    def test_single_label_behavior_is_unchanged(self):
        node = self.reference('b')
        expected = copy.deepcopy(node)
        expected['c'][-1][0] = '../main.tex#L3'
        self.assertEqual(m.remap_links([node], self.paper, self.tex,
                                      source_path=self.paper / 'main.tex'), [('#b', '../main.tex#L3')])
        self.assertEqual(node, expected)

    def test_remapping_is_idempotent(self):
        node = self.reference()
        m.remap_links([node], self.paper, self.tex, source_path=self.paper / 'main.tex')
        original = copy.deepcopy(node)
        self.assertEqual(m.remap_links([node], self.paper, self.tex,
                                      source_path=self.paper / 'main.tex'), [])
        self.assertEqual(node, original)

    def test_pandoc_roundtrip_preserves_text_and_math(self):
        tex = self.tex + r' $x^2$ See \cref{c,a,b}; end.'
        ast = json.loads(m.run(['pandoc', '-f', 'latex', '-t', 'json'], data=tex)[0])
        before_text = m.text_signature(ast, ast['blocks'])
        before_math = m.math_signature(ast['blocks'])
        m.remap_links(ast['blocks'], self.paper, tex, source_path=self.paper / 'main.tex')
        self.assertEqual(m.text_signature(ast, ast['blocks']), before_text)
        md = m.write_ast(ast, ast['blocks'])
        reread = json.loads(m.run(['pandoc', '-f', m.FORMAT, '-t', 'json'], data=md)[0])
        self.assertEqual(m.text_signature(ast, reread['blocks']), before_text)
        self.assertEqual(m.math_signature(reread['blocks']), before_math)
        self.assertEqual(len(list(m.nodes(reread['blocks'], 'Link'))), 3)

    def test_real_tpc181_all_three_labels_and_roundtrips(self):
        _, md, record, report = m.convert(181, source_commit='ab23455ba941e5a14ded27d49de0e874aee811ac')
        self.assertEqual(report['math_nodes'], 61)
        self.assertTrue(report['text_roundtrip'])
        self.assertEqual(report['status'], 'FULL_TEX_TO_MARKDOWN_MECHANICAL')
        self.assertNotIn('](#prop:singleton,thm:stop,prop:frontier)', md)
        for label, line in [('prop:singleton', 208), ('thm:stop', 246), ('prop:frontier', 331)]:
            self.assertIn('[' + label + '](../main.tex#L' + str(line) + ')', md)
            self.assertIn('`#' + label + '` → `../main.tex#L' + str(line) + '`', record)


if __name__ == '__main__':
    unittest.main()
