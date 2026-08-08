# RH-388 replay audit

## Offline replay

With dependencies from `requirements.txt` installed, run:

    make result
    make schema
    make test
    make remote
    make pdf
    make archive

The default remote target invokes both frozen verifiers without network
access and performs zero requests.  Live source replay is an explicit
opt-in via `make remote-network-jy`, `make remote-network-maynard`, or
`make remote-network`.

## Frozen artifact snapshot

The final checkpoint has:

    56 oracle rows = 12 + 7 + 12 + 7 + 10 + 8
    24/24 genuine semantic mutations rejected
    77 immutable Git blobs + 2 remote logical locks = 79 logical inputs
    certificate bytes: 14531
    certificate SHA-256:
    373d870847bb0bf134aa1eba30c5e4d2c3a01dba470af9c75ebacadd81976371

The result has 60,053 bytes and SHA-256
`b80e29174e6616bc7f4c2de999069ba9d745d80d7c46f88ae8046bf2b5b41665`.
The schema has 242,806 bytes and SHA-256
`283182d019009b282f4e653efe1dbbc4ab48510046e65ddd77ca4e9db968cbb5`.

## Final archive replay

The collected suite has 58 tests.  Fresh archive replay reports:

    publication members: 36
    immutable external Git inputs: 77
    remote logical inputs: 2
    logical input total: 79
    archive failure count: 0

Stored result, schema, manifest, and archive report agree with fresh
deterministic rebuilds.  Optimized `-OO` core, result, source, and archive
builders reproduce the same objects.  The outer verifier checks exact
membership, hashes, source commit, remote ordering, logical digest,
semantic PDF identity, and recursive external-payload exclusion.

## Environment note

The builders use the standard library.  Official schema validation in
the test suite additionally uses `jsonschema`.  Local QA uses the
workspace pytest interpreter with the host `jsonschema` package path;
that host path is not hard-coded in the Makefile.  A clean environment
installs both packages from `requirements.txt` and may select its
interpreter with `PYTHON=...`.
