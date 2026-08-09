# RH-390 replay audit

## Offline replay

With dependencies from `requirements.txt` installed, run:

    make result
    make schema
    make test
    make remote
    make pdf
    make archive

The default remote target invokes both frozen verifiers without network
access and makes zero requests.  Live checks require an explicit
`remote-network-*` target.

## Frozen artifact snapshot

The final checkpoint has:

    72 rows = 12 + 7 + 15 + 12 + 10 + 10 + 6
    24/24 genuine semantic mutations rejected
    87 immutable Git blobs + 2 remote logical locks = 89 logical inputs
    certificate bytes: 17571
    certificate SHA-256:
    e2116abd4aeb910c24ee470a520623f29f1f454bb9b5293840875da091682b3b

The result has 68,696 bytes and SHA-256
`f91eba3665de25e5572fd71de39f917da40859fb941c9b7df42e84fc02840405`.
The schema has 265,230 bytes and SHA-256
`d6d0daeb126bc90373f06fcc6314a3de1cb6cfda204629945ef77c7078406039`.

## Final archive replay

The collected suite has 52 tests.  Fresh archive replay reports:

    publication members: 34
    release-stage files including manifest/report: 36
    immutable external Git inputs: 87
    remote logical inputs: 2
    logical input total: 89
    external payload hashes excluded: 4/4
    offline remote requests: 0+0
    archive failure count: 0

Stored result, schema, manifest, and archive report agree with fresh
deterministic builds under normal and optimized `python -OO`.  The outer
verifier checks exact membership, hashes, the RH-388 source commit, remote
order, logical digest, offline request counts, semantic PDF identity, and
recursive payload exclusion.

## Environment note

The builders use the standard library.  Official schema validation needs
`jsonschema`; the suite needs `pytest`.  Neither host path is hard-coded in
the Makefile.  A clean environment installs `requirements.txt` and may
choose its interpreter with `PYTHON=...`.
