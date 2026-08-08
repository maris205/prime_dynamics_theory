# RH-386 replay audit

## Offline replay

With dependencies from `requirements.txt` installed, run:

```bash
make result
make schema
make test
make remote
make pdf
make archive
```

The default remote command performs zero network requests. To reproduce the
separate live-source audit explicitly, run `make remote-network`.

## Frozen core snapshot

The current core/result/schema checkpoint has:

```text
96 oracle rows = 16 + 8 + 66 + 6
24/24 theorem mutations rejected
7/7 auxiliary attacks rejected
1522/1522 scalar-leaf attacks rejected
59 Git source blobs + 1 remote logical lock
certificate: 29717 bytes
SHA-256: 64761d3a85afdee4682982ad545d20a66d2ed69926764bcc9580e0dc8c5f8710
```

The result is 85,958 bytes with SHA-256
`b59fc7921ef89d556fbc81a409ada9304fafc92424b0f4a79f97aa4d57f25ff4`.
The schema is 450,807 bytes with SHA-256
`a5f679c5ceccbb485dc526512994e0c2fa66dd94c69c8aed479599bdfb386330`.

The final suite has 77 passing tests and zero failures. Fresh archive replay
reports 33 publication files, 59 immutable Git inputs, one remote logical
lock, and failure count zero. The stored result, schema, manifest, and
archive report are byte-equal to their fresh deterministic rebuilds.

## Environment note

The builders are standard-library programs except for official schema
validation in the test suite. During local QA, `pytest` came from the
workspace virtual environment while `jsonschema` was supplied by the host
Python package path. This split is recorded honestly and is not embedded in
the Makefile. A normal clean environment should install both dependencies
from `requirements.txt` and may select its interpreter via `PYTHON=...`.
