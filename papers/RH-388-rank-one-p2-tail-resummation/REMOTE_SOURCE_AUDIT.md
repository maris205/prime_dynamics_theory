# RH-388 remote-source audit

## Ordered remote logical locks

The release contains two lock records but redistributes no external
payload:

| source | frozen role | canonical SHA-256 |
|---|---|---|
| Johnston--Yang, arXiv:2204.01980v2 | explicit theta envelope | `d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786` |
| Maynard, Annals 181(1) (2015) | bounded consecutive gaps | `bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e` |

The objects are ordered by fixed source key.  Together with 77 Git blobs
they give logical digest
`bffce602d6e3b568eb96662820f08aa457ff5d0de4065f3c9eeac53d8d8dfa39`.

## Johnston--Yang lock

The inherited exact lock records:

| object | bytes | SHA-256 |
|---|---:|---|
| versioned arXiv v2 PDF | 278380 | `565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2` |
| versioned arXiv v2 source tar | 21523 | `572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd` |
| top-level source `main.tex` | 57970 | `2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602` |

The PDF is application/pdf with 22 pages.  The proof uses only Theorem
1.4, equation (1.8), printed page 2.  The two known out-of-scope source
typos and the Corollary 1.2 fallback are not RH-388 inputs.

## Maynard lock

The separate Maynard lock fixes:

    source key: maynard-annals-2015-small-gaps
    official article page:
      https://annals.math.princeton.edu/2015/181-1/p07
    DOI: 10.4007/annals.2015.181.1.7
    fixed requested/final PDF URL:
      https://annals.math.princeton.edu/wp-content/uploads/
      annals-v181-n1-p07-p.pdf
    HTTP status: 200
    MIME: application/pdf
    bytes: 528115
    pages: 31
    SHA-256:
      3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349
    locator: Theorem 1.3, printed page 385, PDF page 3 (one-based)
    statement used: liminf of consecutive prime gaps is at most 600

The pretty lock file is 2,467 bytes with SHA-256
`9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba`.
Its compact sorted canonical object has no trailing newline and is 2,171
bytes with the canonical SHA above.

## License boundary

The Johnston--Yang arXiv nonexclusive-distribution license grants
distribution to arXiv, not a general third-party republication right;
the version of record is Copyright 2023 Elsevier Inc.  The Maynard
version of record is Copyright 2015 Department of Mathematics, Princeton
University.  Official current Annals policy and the 2022 copyright form
do not establish the article-specific agreement applicable in 2015.
Both locks therefore conservatively record no release redistribution;
all PDF/source vendoring flags are false.

## Network policy and replay

`make remote` calls the inherited Johnston--Yang verifier and the local
Maynard verifier in their default offline modes; both make zero network
requests.  The explicit live targets fetch into memory only.

The Johnston--Yang opt-in path gates exact URLs, HTTP status, PDF MIME,
bytes, page count, PDF/source-tar hashes, safe tar membership, and source
`main.tex` hash.  The Maynard opt-in path gates exact requested/final
URL, status, PDF MIME, bytes, pages, and PDF SHA.  Rebinding, redirect,
transport, type, duplicate/nonfinite JSON, length, hash, and page attacks
fail closed.  No retrieved payload is persisted.

Independent opt-in replays on August 8, 2026 returned PASS for both
sources.  Recursive publication-tree and archive scans find zero matches
for all four external payload hashes.
