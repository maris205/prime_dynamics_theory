# TPC-244 source lock

Baseline:

```text
HEAD = ba1aa9ddb12f42ae390a6d709f40225b2562c009
TPC_HANDOFF_SHA256 = 46704f3f8b61a469799deb6a568451ff8e1298677b57cd4359851dce9d6d74f0
```

Frozen source hashes:

```text
TPC214_BRIDGE = 8779910e87c77df2b2c1efbd7caac9b03560b71089280b72c9d1e30a34874f69
TPC214_PROOF = eec983abf4d69fbb14d965872b11513d822df97f682f602c2e0ab35f1eac7c84
TPC228_DERIVATION = 453d7eb8fb39f6af8c24e6e592d7ee5c732cd0e3e9adabeb6b0223c7f6ecdf0f
TPC228_PROOF = 1b6f91f100b89222dc08a070623e6162539b8e88b17b807b2d4ccfb6338da61d
TPC236_SOURCE = 039d9e6e8684eed34ede58b9491c3ddfc57e2097bd36cb930348d4cebc226272
TPC237_SOURCE = 35b338da0a5c8e84c4189022f717e029f45dc1f644291f9748487b8e2bf81d9a
TPC237_PROOF = 9464a698148f57c7b0ed57ad1f45760585d68b6b8d56969de2347833b6aee425
TPC242_PROOF = b195b1247b415499476c90c9e9e5cc7f20eff526b439790075152ceac7ce31ba
TPC243_PROOF = e7b17bd6babb1a00f690697ab4163053cfe33ddb61419bd73f8bf77d86e44faf
```

Source-backed facts:

- primitive reduced frequencies have canonical exactly-once coefficient
  coordinates;
- one literal outer `C_h` is retained in every frozen packet;
- TPC-214 complete-period clustering produces `|C_h|^2`;
- TPC-243 transports a supplied coefficient covariance to the hard window.

First physical blocker:

`NO_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_COEFFICIENT_ATTACHMENT`.
