# RH-398 visual QA

Frozen PDF: 358,870 bytes, SHA-256
`b5ac3c2f5489815dc4c98c64c88bb64d818c4ca3789dc789027332e968cfe96f`.
It contains 11 A4 pages.  Every page was rasterized at 150 dpi and inspected
at page scale after the final quartet was declared unique and quiescent.

| Page | Content checked | Verdict |
|---:|---|---|
| 1 | title, abstract, principal maximum, keywords, fixed-interface opening | clean |
| 2 | fixed interface, distance and run objects, RH-396 endpoint locator | clean |
| 3 | main theorems, second difference, cutoff, and alternating telescope | clean |
| 4 | telescope proof, CRT phase spaces, local levels, and path optimizer | clean |
| 5 | deletion normalization, exact `Lambda_T(L)` formula, all four parity branches | clean |
| 6 | local contribution, collision-level order, finite transfer, and cofinal passage | clean |
| 7 | maximum proof, strict-witness table, auxiliary primes, and invisibility | clean |
| 8 | complement sequence, normalized `K_1/(p^2-1)` bound, and gap setup | clean |
| 9 | quantitative-gap completion, joint endpoint, certificate table, source closure | clean |
| 10 | source roles, result/schema identities, limits, and declarations | clean |
| 11 | both bibliography entries and terminal whitespace | clean |

No page has clipped mathematics, overlapping text, a margin escape, broken
glyph, unintended blank-page anomaly, malformed table, or unreadable
identifier.  The sparse final bibliography page is intentional and legible.

Mechanical checks agree with the visual review: A4 media/crop geometry, zero
rotation, Ghostscript exit zero, clean text extraction, and 22/22 font rows
embedded, subset, and Unicode-mapped.  The semantic PDF is byte-identical to
`main.pdf`.

Visual verdict: 11/11 pages pass.
