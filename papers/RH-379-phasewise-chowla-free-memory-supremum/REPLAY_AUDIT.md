# RH-379 upstream replay audit

The upstream replay was intentionally read-only.  No MVP2 or volume builder
was run, because RH-379's write scope excludes every other paper directory.
Python bytecode and pytest cache writes were disabled.

## MVP2 and four-volume replay

From `papers/RH-MVP2-corpus-frontier-synthesis`:

```text
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  -m pytest -q -p no:cacheprovider
```

Result: `7 passed`.

Those tests read the consecutive RH-1--RH-361 inventory and independently
invoke the outer four-volume verifier with `write_output=False`.  A separate
read-only call to the same verifier returned:

```text
status                  rh_four_volume_archive_verified
volume_count            4
numbered_source_count    361
archive_member_count     73
dependency_hash_count    1548
result_hash_count        8
failure_count            0
manifest_sha256          24dcf3c6e74c5252e7e278d9141a656c6b97bb30fad6578da8c193cc1063a897
```

The replay checks the four fixed source ranges `1--160`, `161--241`,
`242--281`, and `282--361`; individual archive membership and hashes;
dependency and result hashes; semantic-PDF byte identity; and each volume's
Gate/forbidden-claim firewall.

## MVP2 boundary snapshot

The read-only summary reports 361 numbered papers, 1,356 source-file hashes,
Gates A--E all false, and every forbidden operator/trace/zero/RH claim false.
Its route coordinate remains
`actual_same_clock_unnormalized_head_transport_open`; RH-379 does not modify
or promote that route.

## RH-379 use of the replay

RH-379's result ledger locks the MVP2 summary and the stored four-volume
verification record, whose SHA-256 is
`b27f120f77c4bbf3afd3a4486fd800a8de93a2db52236c835809aa488d113751`.
The outer replay is provenance evidence only.  None of its finite counts is
used to infer RH-379's mathematical theorem.

**Replay verdict: PASS, with zero upstream writes.**
