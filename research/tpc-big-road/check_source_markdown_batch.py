#!/usr/bin/env python3
"""Read-only mechanical/source-lock/link checks for an existing conversion batch.

This checks archival conversion evidence, not scientific certificates or proofs.
It never compiles, writes sources, calls a producer, or accesses the network.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import re
from urllib.parse import unquote

import maintain_source_markdown as m
import refresh_source_markdown_inventory as inventory


COVERAGE_KEYS = ('full-source-md', 'reliable-full-md',
                 'partial-or-notes', 'source-inaccessible')


def current_coverage_issues(content, marker, expected):
    """Check the one explicitly current paragraph, not historical receipts."""
    starts = list(re.finditer(re.escape(marker), content))
    if len(starts) != 1:
        return [f'expected exactly one current-coverage marker: {marker}']
    paragraph = content[starts[0].end():].split('\n\n', 1)[0]
    status_starts = re.findall(r'`(' + '|'.join(COVERAGE_KEYS) + r')=', paragraph)
    if len(status_starts) != len(COVERAGE_KEYS) or set(status_starts) != set(COVERAGE_KEYS):
        return ['current-coverage paragraph must contain each status exactly once']
    entries = re.findall(r'`(' + '|'.join(COVERAGE_KEYS) + r')=(\d+)`', paragraph)
    if len(entries) != len(COVERAGE_KEYS) or {key for key, _ in entries} != set(COVERAGE_KEYS):
        return ['current-coverage paragraph must contain each status exactly once']
    observed = {key: int(value) for key, value in entries}
    required = {key: expected[key] for key in COVERAGE_KEYS}
    return [] if observed == required else [f'stale current coverage: {observed}; inventory: {required}']


def paper_overrides(names, first, last):
    """An explicit directory may disambiguate one number in this batch only."""
    selected = {}
    for name in names:
        match = re.fullmatch(r'tpc-([1-9][0-9]*)-[A-Za-z0-9][A-Za-z0-9_-]*', name)
        if not match:
            raise ValueError('invalid exact paper-directory basename')
        number = int(match[1])
        if number in selected or not first <= number <= last:
            raise ValueError('duplicate or out-of-range paper-directory override')
        m.select_paper(number, name)
        selected[number] = name
    return selected


def check_paper(number, paper_name=None):
    paper, md, record, report = m.convert(number, paper_name=paper_name)
    files = [paper / 'paper/main.md', paper / 'CONVERSION_RECORD.md']
    for path, expected in zip(files, [md, record]):
        if not path.is_file() or path.read_text() != expected:
            raise ValueError(f'generated output mismatch: {path}')
    scope = re.search(r'Supplemental prerequisite audit: \[[^]]+\]\(([^)]+)\)', record)
    if scope:
        files.append((paper / scope[1]).resolve())
    return report, files


def check_links(path):
    content = path.read_text()
    if path == m.ROOT / 'TPC_HANDOFF.md':
        # Only the maintenance entry was changed, not the historical science.
        content = re.split(r'\nTPC-\d+ current section:', content, maxsplit=1)[0]
    ast = json.loads(m.run(['pandoc', '-f', m.FORMAT, '-t', 'json'], data=content)[0])
    anchors = {node['c'][1][0] for node in m.nodes(ast, 'Header')}
    anchors.update(re.findall(r'(?:id|name)="([^"]+)"', content))
    count, issues = 0, []
    for node in list(m.nodes(ast, 'Link')) + list(m.nodes(ast, 'Image')):
        target = node['c'][-1][0]
        if re.match(r'[A-Za-z][A-Za-z0-9+.-]*:', target):
            continue
        count += 1
        name, _, fragment = unquote(target).partition('#')
        destination = (path.parent / name).resolve() if name else path
        problem = None
        if not destination.exists():
            problem = 'missing local path'
        elif fragment and re.fullmatch(r'L\d+', fragment):
            if not destination.is_file() or not 1 <= int(fragment[1:]) <= source_line_count(destination.read_bytes()):
                problem = 'invalid source-line anchor'
        elif fragment and destination == path and fragment not in anchors:
            problem = 'missing same-document anchor'
        if problem:
            issues.append({'file': str(path.relative_to(m.ROOT)), 'target': target, 'problem': problem})
    return count, issues


def source_line_count(blob):
    """Bounds for original LF-delimited source anchors, never reader lines."""
    return blob.count(b'\n') + int(bool(blob) and not blob.endswith(b'\n'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--first', required=True, type=int)
    parser.add_argument('--last', required=True, type=int)
    parser.add_argument('--paper-dir', action='append', default=[],
                        help='exact existing directory basename for a duplicated number; repeat for distinct numbers')
    args = parser.parse_args()
    if not 0 < args.first <= args.last:
        parser.error('require 0 < first <= last')
    selected = paper_overrides(args.paper_dir, args.first, args.last)
    with ThreadPoolExecutor(max_workers=4) as pool:
        checked = list(pool.map(lambda number: check_paper(number, selected.get(number)),
                                range(args.first, args.last + 1)))
    files = {path for _, paths in checked for path in paths}
    base = m.ROOT / 'research/tpc-big-road'
    files.update(base / name for name in ['PAPER_MATERIALS_INDEX.md', 'PAPER_MATERIALS_LINKS.md',
                                         'PAPER_MATERIALS_REMAINING.md',
                                         'TPC_CONVERSION_BATCH_2026-09-07.md', 'TPC_HISTORY_SUMMARY.md'])
    files.add(m.ROOT / 'TPC_HANDOFF.md')
    with ThreadPoolExecutor(max_workers=4) as pool:
        links = list(pool.map(check_links, sorted(files)))
    expected, coverage = inventory.outputs()
    for path, value in expected.items():
        if path.read_text() != value:
            raise ValueError(f'inventory mismatch: {path}')
    issues = [item for _, items in links for item in items]
    current_coverage = []
    for path, marker in [(m.ROOT / 'TPC_HANDOFF.md', 'Current coverage is'),
                         (base / 'TPC_HISTORY_SUMMARY.md', 'The archive inventory is now')]:
        content = path.read_text()
        if path.name == 'TPC_HANDOFF.md':
            content = re.split(r'\nTPC-\d+ current section:', content, maxsplit=1)[0]
        current_coverage.extend({'file': str(path.relative_to(m.ROOT)), 'problem': problem}
                                for problem in current_coverage_issues(content, marker, coverage))
    reports = [report for report, _ in checked]
    result = {'mechanical_only': True, 'papers': len(reports),
              'math_nodes': sum(row['math_nodes'] for row in reports),
              'source_locks_pass': len(reports),
              'text_roundtrip_pass': sum(row['text_roundtrip'] for row in reports),
              'unmapped_sections': [{'paper': row['paper'], 'count': row['unmapped']}
                                    for row in reports if row['unmapped']],
              'linked_documents_checked': len(files), 'local_links_checked': sum(n for n, _ in links),
              'link_issues': issues, 'coverage': dict(coverage),
              'current_coverage_issues': current_coverage,
              'cross_document_non_line_anchors': 'not independently checked'}
    print(json.dumps(result, indent=2))
    if issues or current_coverage:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
