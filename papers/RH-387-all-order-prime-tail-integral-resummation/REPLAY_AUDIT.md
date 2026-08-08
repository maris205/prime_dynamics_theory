# RH-387 replay audit

## Offline replay

With dependencies from requirements.txt installed, run:

    make result
    make schema
    make test
    make remote
    make pdf
    make archive

The default remote command performs zero network requests. The separate
live-source audit requires the explicit make remote-network command.

## Frozen core snapshot

The final checkpoint has:

    42 oracle rows = 12 + 7 + 7 + 14 + 2
    24/24 genuine mathematical mutations rejected
    586/586 scalar-leaf attacks rejected
    68 immutable Git blobs + 1 remote logical lock
    certificate: 10785 bytes
    certificate SHA-256:
    3c89e51662bbc2f1c7712f4205ff8cde88e9eb80636e2779d06154e914459b4b

The result has 50,144 bytes and SHA-256
d71c69de7e5d05c5ac558a17d2a6089815334d19b43a74ecfde219affcc1e16c.
The schema has 224,419 bytes and SHA-256
c90e39f473234e5e0e103dba171cc9cdfdaff9be9b88fbb9ea75059ee9429d6e.

The final collected suite has 47 tests. Fresh archive replay reports 33
publication files, 68 immutable Git inputs, one remote logical lock, and
failure count zero. Stored result, schema, manifest, and archive report
are byte-equal to fresh deterministic rebuilds. Optimized -OO core,
result, and archive builders reproduce the same objects.

## Environment note

The builders are standard-library programs except for official schema
validation in the test suite. Local QA uses the workspace pytest
environment with the host jsonschema package path, exactly as recorded by
the invocation log. This split is not hard-coded into the Makefile. A
clean environment installs both packages from requirements.txt and may
select its interpreter via PYTHON=....
