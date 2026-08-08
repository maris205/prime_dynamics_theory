# RH-386 remote-source audit

## Locked objects

The external source lock records, but does not redistribute:

| object | fixed URL | bytes | SHA-256 |
|---|---|---:|---|
| arXiv v2 PDF | `https://arxiv.org/pdf/2204.01980v2` | 278380 | `565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2` |
| arXiv v2 source tar | `https://arxiv.org/src/2204.01980v2` | 21523 | `572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd` |
| source `main.tex` | member of locked tar | 57970 | `2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602` |

The PDF has MIME type `application/pdf` and 22 pages. The direct source
URL returns HTTP 200 and avoids a redirect-dependent contract.

## Network policy

`experiments/verify_remote_source.py` is offline by default. A default run
returns `NETWORK_DISABLED`, makes zero requests, and verifies only that the
local JSON lock equals the sealed core object. Network access requires the
explicit `--network` flag.

The opt-in verifier rejects transport failure, non-200 status, any final
URL outside the exact allowlist, wrong PDF MIME, byte counts, hashes,
wrong PDF page count, unsafe tar paths, missing or duplicate top-level
`main.tex`, and wrong source-member hash. It retains no downloaded source
in the publication tree.

## Independent replay

An explicit opt-in replay on August 8, 2026 returned PASS for both requests:

```text
PDF:  status 200, final URL exact, application/pdf,
      278380 bytes, 22 pages, SHA-256 exact.
tar:  status 200, final URL exact, 21523 bytes, SHA-256 exact.
main: 57970 bytes, SHA-256 exact.
```

The deterministic unit suite covers the offline default and all listed
failure modes without requiring network access. Archive tests separately
assert that the lock and verifier are included while the external PDF and
source tar hashes are absent.
