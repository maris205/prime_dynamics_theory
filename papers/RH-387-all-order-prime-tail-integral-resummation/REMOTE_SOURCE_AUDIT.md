# RH-387 remote-source audit

## Locked objects

The inherited external source lock records, but does not redistribute:

| object | fixed URL | bytes | SHA-256 |
|---|---|---:|---|
| arXiv v2 PDF | https://arxiv.org/pdf/2204.01980v2 | 278380 | 565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2 |
| arXiv v2 source tar | https://arxiv.org/src/2204.01980v2 | 21523 | 572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd |
| source main.tex | member of locked tar | 57970 | 2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602 |

The PDF has MIME application/pdf and 22 pages. The direct source URL
returns HTTP 200 and avoids a redirect-dependent contract. The canonical
lock object has SHA-256
d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786
and is byte-for-byte inherited from the frozen RH-386 release blob.

## License and scope

The arXiv nonexclusive-distribution license grants permission to arXiv,
not a general third-party republication right. The version of record is
Copyright 2023 Elsevier Inc., all rights reserved. Accordingly,
redistributable_in_release, pdf_vendored, and source_tar_vendored are all
false.

The lock records two out-of-scope text issues: the Section 5.2
Corollary 1.5 reference intended to point to Corollary 1.2/equation (1.5),
and the arXiv-v2 equation (1.9) pi(x)-x text corrected to pi(x)-li(x) in
the version of record. Neither is used by RH-387. The only external
analytic input is Theorem 1.4 equation (1.8), printed page 2.

## Network policy

experiments/verify_remote_source.py is offline by default. A default run
returns NETWORK_DISABLED, makes zero requests, and verifies the local JSON
lock against the exact upstream release object. Network access requires
the explicit --network flag.

The opt-in verifier rejects transport failure, non-200 status, final URLs
outside the exact allowlist, wrong PDF MIME, byte counts, hashes, wrong
PDF page count, unsafe tar paths, missing or duplicate top-level main.tex,
and wrong source-member hash. It retains no downloaded source in the
publication tree.

## Independent replay

An explicit opt-in replay on August 8, 2026 returned PASS:

    PDF: status 200, exact final URL, application/pdf,
         278380 bytes, 22 pages, SHA-256 exact.
    tar: status 200, exact final URL, 21523 bytes, SHA-256 exact.
    main: 57970 bytes, SHA-256 exact.

The deterministic 13-test remote suite covers the offline default,
successful in-memory replay, and all listed failure modes without network
access. Archive tests assert that the lock and verifier are included while
all three external payload hashes are absent.
