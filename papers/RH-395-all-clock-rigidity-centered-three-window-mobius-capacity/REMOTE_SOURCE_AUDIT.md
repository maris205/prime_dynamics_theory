# RH-395 remote-source and redistribution audit

## Ordered remote lock objects

| Source key | RH-395 role | Redistributable in release | Vendored |
|---|---|---:|---:|
| `johnston-yang-arxiv-2204.01980v2` | inherited closure-only through RH-394 | no grant | no PDF or source archive |
| `maynard-annals-2015-small-gaps` | inherited closure-only through RH-394 | no grant | no PDF |
| `tao-cambridge-2016-logarithmic-chowla` | inherited two-point provenance through RH-394 | CC BY 4.0 | no PDF by policy |
| `tao-teravainen-arxiv-1708.02610v2` | inherited odd-parity analytic provenance through RH-394 | no grant | no PDF |

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

The ordered release-redistribution vector is
`false,false,true,false`.  `redistributable=true` for the Tao lock records a
rights fact; publication policy still keeps every external PDF nonvendored.

## Offline replay

`experiments/verify_offline_sources.py` contains no network implementation or
network option.  It validates strict pretty bytes, canonical objects, source
identity, rights, `pdf_vendored=false`, and default-disabled network metadata.
Every CLI invocation returns `NETWORK_DISABLED`, `network_opt_in=false`, and
exact integer `requests_made=0`.  The behavior is tested under ordinary Python
and `python -OO -B`, with runtime `require` checks rather than removable
assertions.

## Git and logical closure

The Git closure contains 148 release objects:

| Group | Count | Digest |
|---|---:|---|
| `rh394_immutable_closure` | 128 | `0a44007f1e5888ed9b1cc6eae380b25fec38e17fe7e4329594625538d36c579b` |
| `rh394_standard8` | 8 | `cab0bfbc807eb5ed2e8c85435a3348fb48d823327a77c740dc281c195fed9e47` |
| `rh394_prior_external_locks` | 4 | `e9d259e020d0bef964630388a58487efcdc0a48ee895a6c335f35d0269f6d7e2` |
| `rh375_direct_all_clock_release8` | 8 | `14ef15bf6df11e32a05925e5a103c8e2d16ed26abb62620153f9387d84c840ce` |

The all-Git digest is
`9b5e0c04bb3189ddcb802ccb65d5f6b3cc8aa081000acd9fa781fd9f81e50ec9`.
Adding the four ordered remote objects gives 152 logical inputs and digest
`5c4b81ea2f7bdd661fe4374d1174ef3a1909a8327d5982aa01510e4201340bd3`.

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
