# RH-391 replay audit

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

    60 rows = 10 + 12 + 12 + 12 + 8 + 6
    24/24 genuine semantic mutations rejected
    97 immutable Git objects + 2 remote logical locks = 99 logical inputs
    certificate bytes: 10062
    certificate SHA-256:
    cc2874435e62205a3e969e841d80d37243d95826855bd242f0eff3478dccf367

The result has 61,539 bytes and SHA-256
`023aa55c4a4e3795994eed866cc9d1412aef90bc0df9b27831f3718c069c1046`.
The schema has 230,301 bytes and SHA-256
`f5fd98019eefdf600432ca59c6546a6c6d5c7c832a4f8da0603512d20ee40f54`.

The frozen manuscript checkpoint is:

    main.tex: 21049 bytes
    SHA-256: 27d58b4745fe0ce8e61ed788d67f76f47ac72774e5e808d952bb51cc9cb83061
    references.bib: 1532 bytes
    SHA-256: 63cd8b8859b46fc10b9364557f64220c63f62b1f308bdcecd7ab52cf37abdd5a
    main.pdf: 341924 bytes, 8 A4 pages
    SHA-256: 90275847d4e07c9c6fb8a7fdf8ea291abf1b044bb74c70cd59740c2baef0d9d1
    main.log: 25675 bytes
    SHA-256: 4df66e0d74de6b8b5950b26d93a4ceb372ee5bfa9a436ebfda6128fbafe8b16d

## Final archive replay

The collected suite has 84 tests.  Fresh archive replay reports:

    publication members: 34
    release-stage files including manifest/report: 36
    immutable external Git inputs: 97
    remote logical inputs: 2
    logical input total: 99
    external payload hashes: 4
    publication payload hash hits: 0
    full-tree payload hash hits: 0
    offline remote requests: 0+0
    archive failure count: 0

Stored result, schema, manifest, and archive report agree with fresh
deterministic builds under normal and optimized `python -OO`.  The outer
verifier checks exact membership and hashes, the RH-390 release commit,
97-source identity and ordered digest, remote order, logical digest,
offline request counts, rights/nonvendoring, semantic PDF identity,
frozen Stage 1/manuscript hashes, and recursive payload exclusion.

## Environment note

The builders use the standard library.  Official schema validation needs
`jsonschema`; the suite needs `pytest`.  No host path is hard-coded in the
Makefile.  A clean environment installs `requirements.txt` and may choose
its interpreter with `PYTHON=...`.
