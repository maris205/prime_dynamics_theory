# RH-389 replay audit

## Offline replay

With dependencies from `requirements.txt` installed, run:

    make result
    make schema
    make test
    make remote
    make pdf
    make archive

The default remote target invokes all three frozen verifiers without
network access and makes zero requests.  Live checks require an explicit
`remote-network-*` target.

## Frozen artifact snapshot

The final checkpoint has:

    602 rows = 512 + 8 + 64 + 8 + 6 + 4
    24/24 genuine semantic mutations rejected
    95 immutable Git blobs + 3 remote logical locks = 98 logical inputs
    certificate bytes: 208648
    certificate SHA-256:
    b31187db4ea284152b0c1cb895439e29cfa80a4e564c87814ee182f87be0a020

The result has 489,106 bytes and SHA-256
`3c551568aab4e0965b2b0236d9f684e1f953dc36ecbc575e6e007c5f15bfd310`.
The schema has 3,133,596 bytes and SHA-256
`763d25bae19d35b36578619bd50aa79cc8121a73c543f8b051e54200e16445ec`.

## Final archive replay

The collected suite has 61 tests.  Fresh archive replay reports:

    publication members: 37
    release-stage files including manifest/report: 39
    immutable external Git inputs: 95
    remote logical inputs: 3
    logical input total: 98
    external payload hashes excluded: 5/5
    offline remote requests: 0+0+0
    archive failure count: 0

Stored result, schema, manifest, and archive report agree with fresh
deterministic builds under normal and optimized `python -OO`.  The outer
verifier checks exact membership, hashes, two source commits, remote order,
logical digest, offline request counts, semantic PDF identity, and recursive
payload exclusion.

## Environment note

The builders use the standard library.  Official schema validation needs
`jsonschema`; the suite needs `pytest`.  Neither host path is hard-coded in
the Makefile.  A clean environment installs `requirements.txt` and may
choose its interpreter with `PYTHON=...`.
