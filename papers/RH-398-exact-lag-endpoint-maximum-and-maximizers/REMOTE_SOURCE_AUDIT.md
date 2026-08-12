# RH-398 remote-source and provenance audit

## Recursive Git closure

RH-398 directly freezes the RH-397 release commit
`dd63a109dcfa72365c749e0b183820d2611af733`.  The recursive Git closure has
184 unique paths in three groups:

| Group | Count | Digest |
|---|---:|---|
| `rh397_immutable_closure` | 172 | `fd2d749a09316b9c412780e61882e5f1ac050af609cd0a96c0d1aea79ac4c82d` |
| `rh397_standard8` | 8 | `eb7355565e8429765cb967192c00e261998147abb68fb0307517695621bdfd62` |
| `rh397_prior_external_locks` | 4 | `e044509ee377c35cea8642b67a75ca5dc4ba861f455228bde7341418791bce20` |

Every row binds the exact RH-397 commit, relative path, and blob SHA-256.  The
ordered all-Git digest is
`e7341caa25f0787a2e48a4d9c156e0d785b6c2a5516172bdfb25c2ac45377ea8`.

## Ordered remote logical locks

The four inherited remote keys remain, in order:

1. Johnston--Yang arXiv 2204.01980v2;
2. Maynard, Annals of Mathematics 2015;
3. Tao, logarithmically averaged Chowla;
4. Tao--Teräväinen arXiv 1708.02610v2.

Their canonical object digests are respectively
`d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786`,
`bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e`,
`d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84`,
and
`a1448fb540b6f8fcf17cace1ff7d7218a6126cb3265699bbd43c444fcc558058`.
Their exact pretty lock blobs are the four JSON files shipped in `results/`.
The redistribution vector is `false,false,true,false`.  Every remote PDF is
nonvendored; the Johnston--Yang source archive is also nonvendored.  Network
verification defaults to disabled and the release performs no request.

Four remote locks appended to 184 Git objects give 188 logical inputs with
digest
`4cc752fb7baae977bb15a9420101c5ed37727b1f3f7eecf72afce9dec3c73b13`.
The canonical source-closure object is 64,997 bytes with SHA-256
`5cb3a2f4339ba0b2f11654092496bf7caf255d0d0e7ccf23524355d9f3fa97d7`.
All six sealed external payload hashes have zero hits in the publication
members and throughout the RH-398 tree.

## Mathematical roles

RH-396, commit `cd57086fa90939d56656c3f952a08ffad9aabefe`, is the sole
load-bearing theorem and analytic endpoint input: definitions (18)--(21),
Theorem 1.3 equation (22), and Corollary 1.4 equation (23), PDF page 3.
RH-397 is the direct release and provenance predecessor only and is not an
analytic input.  RH-394, RH-392, RH-395, and RH-375 remain transitive
provenance or comparison objects.  The four remote records are inherited
closure only; RH-398 makes no strengthened claim from them.

Remote-source verdict: exact, offline, nonvendored, rights-closed, and free of
new analytic dependencies.
