# RH-389 remote-source audit

## Ordered remote logical locks

The release contains three compact lock records but vendors no remote
payload:

| source | RH-389 role | canonical SHA-256 |
|---|---|---|
| Johnston--Yang, arXiv:2204.01980v2 | inherited closure only | `d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786` |
| Maynard, Annals 181(1) (2015) | inherited closure only | `bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e` |
| Tao, Forum Math. Pi 4 (2016), e8 | upstream Liouville provenance for TPC-137 | `d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84` |

The objects are ordered by fixed source key.  With 95 Git blobs, their
logical digest is
`99a9e6d4372a081b028c28acba7de539850b4092b64063d9553ca261809e3e74`.

## Inherited locks

The Johnston--Yang lock fixes a 278,380-byte, 22-page arXiv v2 PDF with
SHA-256
`565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2`,
a 21,523-byte source tar with SHA-256
`572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd`,
and its 57,970-byte top-level `main.tex` with SHA-256
`2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602`.

The Maynard lock fixes a 528,115-byte, 31-page Annals publisher PDF with
SHA-256
`3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349`.
Neither source is a theorem input to RH-389; both are retained only because
the immutable source closure is linear.

## Tao lock

The local lock fixes:

    source key: tao-cambridge-2016-logarithmic-chowla
    DOI: 10.1017/fmp.2016.6
    locator: Theorem 2, equation (3), printed/PDF page 3
    affine domain: fixed natural a1,a2 and integer b1,b2,
                   a1*b2-a2*b1 != 0
    averaging domain: 1<=omega(x)<=x, omega(x)->infinity
    MIME: application/pdf
    bytes: 534086
    pages: 36
    SHA-256:
      a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2

The printed phrase `as n tends to infinity` immediately after equation
(3) is locked as a typographical `x`/`n` slip, resolved from the theorem
variable, abstract, and context without strengthening the statement.
The pretty lock is 3,285 bytes with SHA-256
`825b3455be5eac151b7478f537fa6c503ae8eb02004cd8da821ca802d4ebdd8f`.
Its compact canonical object is 2,952 bytes, has no trailing newline, and
has the canonical SHA recorded above.

## License and nonvendor boundary

The Cambridge VOR is Copyright The Author 2016 and licensed CC BY 4.0;
reuse is permitted with attribution.  Project policy nevertheless sets
`pdf_vendored=false`, so the PDF is not included.  The inherited
Johnston--Yang and Maynard objects retain their conservative
`redistributable_in_release=false` settings.  Lock metadata and verifier
code are included; payload files are not.

## Network policy and replay

`make remote` invokes the inherited Johnston--Yang and Maynard verifiers
and the local Tao verifier with network disabled.  Each reports
`NETWORK_DISABLED`, `network_opt_in=false`, and `requests_made=0`.

The explicit live targets gate allowlisted final URLs, status, PDF MIME,
bytes, pages, and SHA-256.  The Johnston--Yang path additionally gates the
source tar, safe member set, and source `main.tex`.  Redirect, transport,
type, duplicate/nonfinite JSON, length, hash, and page attacks fail closed.
Retrieved bytes remain in memory or a temporary PDF-info directory and are
never persisted in this tree.

Independent opt-in replay on August 9, 2026 returned PASS for Tao.  The
inherited verifiers had already returned PASS on their frozen payloads.
Recursive member and tree scans find zero matches for all five payload
hashes.
