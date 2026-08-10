# RH-393 remote-source and redistribution audit

## Ordered remote objects

| Source key | RH-393 role | Redistributable | Vendored |
|---|---|---:|---:|
| `johnston-yang-arxiv-2204.01980v2` | inherited closure only | no established grant | no PDF or source archive |
| `maynard-annals-2015-small-gaps` | inherited closure only | no established grant | no PDF |
| `tao-cambridge-2016-logarithmic-chowla` | inherited through RH-392 for fixed nonparallel forms | CC BY 4.0 | no PDF by policy |

Ordered canonical lock digests:

```text
d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786
bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e
d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84
```

Exact local pretty-lock SHA-256 values:

```text
d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058
9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba
825b3455be5eac151b7478f537fa6c503ae8eb02004cd8da821ca802d4ebdd8f
```

## Offline replay

`experiments/verify_offline_sources.py` has no network implementation or
network option. It validates strict pretty bytes, canonical objects, source
identity, rights, `pdf_vendored=false`, and default-disabled network metadata.
Every invocation returns `NETWORK_DISABLED`, `network_opt_in=false`, and
integer `requests_made=0`.

## Payload exclusion

The five forbidden payload identities are:

```text
565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2
572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd
2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602
3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349
a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2
```

The archive requires `(payload_count, member_hits, tree_hits)=(5,0,0)`. The
only publication PDFs are the frozen manuscript and its byte-identical
semantic copy.
