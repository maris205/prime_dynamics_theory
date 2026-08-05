# RH-MVP2 source crosswalk

The machine-readable canonical path and SHA-256 map is
`results/corpus_inventory.json`.  This human crosswalk records the synthesis
sections and the primary review anchors.  It is navigational: source papers
retain their own theorem status.

| Synthesis phase | Numbered sources | Primary anchors | Boundary carried forward |
|---|---|---|---|
| Foundation and Stage-A architecture | RH-1--RH-160 | RH-71, 81, 91, 100, 119, 129, 139, 149, 159; RH-MVP1 | Fixed-noise and finite foundation; Gate A and all later Gates remain open. |
| Physical clouds and trace envelopes | RH-161--RH-241 | RH-161, 171, 181, 191, 201, 211, 221, 231, 241 | Local/finite Riesz, cloud, transport and `det_2` structure; moving all-order noisy envelope and coefficient bridge open. |
| Deterministic anchors and counterloops | RH-242--RH-281 | RH-251, 261, 271, 281 | Deterministic all-order anchor/envelope/radius and counterloop; no actual noisy-head identification. |
| Noisy heads, annuli and endpoints | RH-282--RH-321 | RH-291, 301, 311, 321 | Finite actual heads, slow diagonals, analytic criteria and synthetic endpoint laws; physical common-clock aggregate open. |
| First alias and signed completion | RH-322--RH-361 | RH-331, 341, 351, 361 | Exact typed formulas and scoped information-class negatives; actual same-clock `D_(4k)(R)`, `q/E_off` bridge absent. |

## Review topology

The 29 review anchors are:

```text
71 81 91 100 119 129 139 149 159 171 181 191 201 211 221
231 241 251 261 271 281 291 301 311 321 331 341 351 361
```

Their declared ranges cover 349/361 numbered IDs.  The twelve IDs not in a
review anchor's direct range are `RH-101`--`RH-109`, `RH-150`, `RH-160`, and
`RH-161`.  RH-MVP1 covers RH-1--RH-160; RH-161 is retained explicitly as the
independent packet-to-Riesz assembly.

## Legacy aliases

Four numerical labels have a second empty directory.  The inventory selects
the non-empty path and records both names:

- RH-302: `RH-302-annular-tail-moving-head-reduction` is canonical;
- RH-303: `RH-303-annular-fixed-order-head-transport-necessity` is canonical;
- RH-304: `RH-304-minimal-clock-complement-mass-demand` is canonical;
- RH-306: `RH-306-sharp-annular-coefficient-envelope-saturation` is canonical.

The empty aliases are preserved and never staged or deleted.
