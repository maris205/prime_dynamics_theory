# RH-390 remote-source audit

## Ordered remote logical locks

The release contains two compact lock records but vendors no remote
payload:

| source | RH-390 role | canonical SHA-256 |
|---|---|---|
| Johnston--Yang, arXiv:2204.01980v2 | prime-counting envelope via RH-386 | `d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786` |
| Maynard, Annals 181(1) (2015) | fixed-rank bounded-gap necessity | `bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e` |

The objects are ordered by fixed source key.  With 87 Git blobs, their
logical digest is
`2255b26dd68adf09f447e251eb5d38c8b1d31fbaa1c26befd8c04165097ed922`.
The local pretty copies are byte-identical to the released RH-388 lock
blobs.

## Johnston--Yang lock

The lock fixes Theorem 1.4, equation (1.8), printed page 2 and a
278,380-byte, 22-page arXiv v2 PDF with SHA-256
`565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2`.
It also fixes a 21,523-byte source tar with SHA-256
`572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd`
and its 57,970-byte top-level `main.tex` with SHA-256
`2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602`.
The locked corollary fallback and known out-of-scope typos are not used.

The arXiv nonexclusive distribution license grants distribution to arXiv,
not a general third-party redistribution right.  The version of record is
Copyright 2023 Elsevier.  The release therefore records
`redistributable_in_release=false` and `source_tar_vendored=false`.

## Maynard lock

The lock fixes Theorem 1.3, printed page 385/PDF page 3, DOI
`10.4007/annals.2015.181.1.7`, and a 528,115-byte, 31-page official Annals
PDF with SHA-256
`3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349`.
Its theorem role is only the unconditional bound
`liminf(p_(n+1)-p_n)<=600` for consecutive primes.

The publisher version is Copyright 2015 Department of Mathematics,
Princeton University and is not established as CC BY.  The current 2022
copyright agreement is recorded only as present policy; its applicability
to the 2015 article is not inferred.  The release conservatively records
`redistributable_in_release=false` and `pdf_vendored=false`.

## Network policy and replay

`make remote` invokes the frozen RH-387 Johnston--Yang verifier and RH-388
Maynard verifier with network disabled.  Both report
`NETWORK_DISABLED`, `network_opt_in=false`, and `requests_made=0`.

Network retrieval requires an explicit `remote-network-*` target.  The
fixed verifiers gate allowlisted final URLs, status, PDF MIME, bytes,
pages, and SHA-256.  The Johnston--Yang path additionally gates the source
tar, safe member set, and source `main.tex`.  Retrieved bytes are not
persisted in this tree.

The archive scans every publication member and the complete RH-390 tree.
It finds zero matches for all four external payload hashes.
