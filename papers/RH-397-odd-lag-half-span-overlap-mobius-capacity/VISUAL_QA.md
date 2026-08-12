# RH-397 visual QA

Frozen PDF: 387,054 bytes, SHA-256
`be06c3bcd37acb7f2144cd390423ae207f9b412ffd833a8156a317c59dd44ea6`.
It contains nine A4 pages.  Every page was rasterized and inspected at page
scale after the final token and citation-locator repair.

| Page | Content checked | Verdict |
|---:|---|---|
| 1 | title, abstract, principal formula, keywords, opening definitions | clean |
| 2 | phase densities, collision-aware products, Theorem 1.1 | clean |
| 3 | Theorem 1.2, terminal bridge, exact-support masses | clean |
| 4 | three-shift firewall, projection, exact cells, reflection | clean |
| 5 | flag obstruction, relation census, rectangle table, MUVW start | clean |
| 6 | translation identity, phase sums, edge filling, rising-set proof | clean |
| 7 | odd-lag clock theorem, all CRT branches, certificate introduction | clean |
| 8 | control table, frozen identities, source roles, firewalls, declarations | clean |
| 9 | interests/funding/ethics and two bibliography entries | clean |

No page has clipped mathematics, overlapping text, a margin escape, broken
glyph, unintended blank region, malformed table, or unreadable identifier.
The repaired `\qquad` spacing and `\max_J` operator render correctly; no raw
command token remains in the text layer.

Mechanical checks agree with the visual review: A4 media/crop geometry, zero
rotation, Ghostscript exit zero, clean text extraction, and 25/25 font rows
embedded, subset, and Unicode-mapped.  The semantic PDF is byte-identical to
`main.pdf`.

Visual verdict: 9/9 pages pass.
