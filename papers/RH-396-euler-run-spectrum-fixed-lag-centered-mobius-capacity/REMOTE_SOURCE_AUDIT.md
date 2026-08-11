# RH-396 remote-source and redistribution audit

## Ordered remote lock objects

| Source key | RH-396 role | Redistributable in release | Vendored |
|---|---|---:|---:|
| `johnston-yang-arxiv-2204.01980v2` | inherited closure-only through RH-394 | no grant | no PDF or source archive |
| `maynard-annals-2015-small-gaps` | inherited closure-only through RH-394 | no grant | no PDF |
| `tao-cambridge-2016-logarithmic-chowla` | inherited two-point provenance through RH-394 | CC BY 4.0 | no PDF by policy |
| `tao-teravainen-arxiv-1708.02610v2` | inherited odd-parity provenance through RH-394 | no grant | no PDF |

Ordered canonical lock digests:

```text
d53b93212b7c5b5b6b3f7e890099c48ce8e35f2bff9bdd49f9c330a9b5039786
bd4aad4b7042218e5733bb07db2a513770710628a8ac52d5bcc9881fcb0b5d2e
d2ca5eb4c860090981411a587a58da191df0afba8d65158bc0a44a6db4009e84
a1448fb540b6f8fcf17cace1ff7d7218a6126cb3265699bbd43c444fcc558058
```

Exact local pretty-lock SHA-256 values:

```text
d6ba2d91aef2e851a24c9f17393602042a3da75142185557f245c1f0c701c058
9a2e1ea8604f767c3538c2d6ad432a9d2ee2ffde50b2b362b4d457c6ac68cdba
825b3455be5eac151b7478f537fa6c503ae8eb02004cd8da821ca802d4ebdd8f
52ade551d8bef9aa35e850d03cefede1239cb9611b9211fdcda522f02fb501ec
```

The ordered redistribution vector is `false,false,true,false`.
`redistributable=true` for the Tao lock records a rights fact; publication
policy still keeps every external PDF nonvendored.

## Offline replay

`experiments/verify_offline_sources.py` contains no network implementation or
network option.  It checks strict pretty bytes, canonical objects, source
identity, rights, `pdf_vendored=false`, and disabled-by-default network
metadata.  Every CLI invocation returns `NETWORK_DISABLED`,
`network_opt_in=false`, and exact integer `requests_made=0`.  Normal and
optimized tests use runtime `require` checks rather than removable asserts.

## Git and logical closure

| Group | Count | Digest |
|---|---:|---|
| `rh395_immutable_closure` | 148 | `a0ff7451b704aedc6eb839494dc65a9711b1dd7694ec4991c8169e77abafdcae` |
| `rh395_standard8` | 8 | `631dcac47b47865202f13552894a48c7b174575ac893d692bfed575f83120a3e` |
| `rh395_prior_external_locks` | 4 | `b1822df0e748c9ebb18c08198840975a378e3e068c08105fd68dbc55be74f79f` |

The all-Git digest is
`472bf5ce5e352dce0d3a44ad10b22345b98e0e8b9a0cd745be9ecd93dedf0a86`.
Adding the four remote objects gives 164 logical inputs and digest
`72040ab3d7a5d98ce308b91d0748d52a8d4886cf245f5079f14c69ee659cc287`.

## Payload exclusion

The six forbidden payload identities are:

```text
565993a6def48b237a68a92acba604f2c42f99165e0e71e390f8e21a313b74b2
572d5739936ad3f5e867a142eccb0193b001dd2ee9b27b1d7183124071ec7edd
2a79d56dbd6da46d46c6ddd8852d9fa763c716110ebf08b7b029e52346f92602
3c24d010f00d1212418351b6f6baed9c94251a3ce958c36f56ebbc450ade9349
a5563f3a85b9c8cfd37be6f1df6bdae8377ce1762e4cb6a8b7856329ef7b30a2
232bdb1ad6e46789bfc124a589d6c3afda803eaf3ba2f93278fc31be3aa276ad
```

The archive requires `(payload_count,member_hits,tree_hits)=(6,0,0)`.  The
only publication PDFs are the frozen manuscript and its byte-identical
semantic copy.
