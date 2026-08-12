# RH-397 remote-source and provenance audit

## Recursive Git closure

RH-397 directly freezes the RH-396 release commit
`cd57086fa90939d56656c3f952a08ffad9aabefe`.  The recursive Git closure has
172 unique paths in three groups:

| Group | Count | Digest |
|---|---:|---|
| `rh396_immutable_closure` | 160 | `c331c37d3447ac1f54063287f5c79034b117e5c9516f3727d5eac5a148d9bd12` |
| `rh396_standard8` | 8 | `dbe2380bc2a6a060c69ca852625d9c2a7f20d82797108ed17fd1c0d231fa541a` |
| `rh396_prior_external_locks` | 4 | `57d0e03fff2be3fb1466834fefdc5fdc001e87686eb1e5898918d820163a57ea` |

Every row binds the exact RH-396 commit, relative path, and blob SHA-256.  The
ordered all-Git digest is
`b3f5688380762a4e3c27d512311f4c0d22173c434cc40459fc77bb3eb87fb5c4`.

## Ordered remote logical locks

The four inherited remote keys remain, in order:

1. Johnston--Yang arXiv 2204.01980v2;
2. Maynard, Annals of Mathematics 2015;
3. Tao, logarithmically averaged Chowla;
4. Tao--Teräväinen arXiv 1708.02610v2.

Their canonical object digests are respectively `d53b9321...`, `bd4aad4b...`,
`d2ca5eb4...`, and `a1448fb5...`; their exact pretty lock blobs are the four
JSON files shipped in `results/`.  The redistribution vector is
`false,false,true,false`.  Every PDF is nonvendored; the Johnston--Yang source
archive is also nonvendored.  Network verification defaults to disabled and
the release performs no request.

Four remote locks appended to 172 Git objects give 176 logical inputs with
digest
`e9588b58f75e02e31ba5ffb279aea267074ec72f717afa84670f320d6c1030e0`.
All six sealed external payload hashes have zero hits among publication
members and throughout the RH-397 tree.

## Mathematical roles

RH-394 is the sole analytic fixed-three-shift terminal-law input, inherited
through RH-396.  RH-396 is the direct collision-aware finite predecessor.
RH-392, RH-395, and RH-375 are transitive comparison precedents.  The four
remote records remain inherited provenance only; RH-397 makes no strengthened
claim from them.

Remote-source verdict: exact, offline, nonvendored, rights-closed, and free of
new analytic dependencies.
