# TPC-173: Production source-claim inventory

TPC-173 freezes a contiguous theorem corpus:

```text
every main.tex from TPC-133 through TPC-172, exactly 40 files
```

Production archives and route outputs are locked separately as data/status
substrate. Their hashes prove integrity only.

Every theorem file receives exactly one corpus disposition:

```text
MAPPED_DISQUALIFIED
REVIEWED_NO_CANDIDATE
NOT_MAPPED_YET
QUALIFYING
```

The current exact partition is:

```text
MAPPED_DISQUALIFIED   30 files
REVIEWED_NO_CANDIDATE 10 files
NOT_MAPPED_YET         0 files
QUALIFYING             0 files
```

The mapped near-claims include the TPC-153 shadow identities, TPC-154 formal
obstructions, the TPC-155 verifier theorem, the TPC-164 archive key, the
TPC-165 formal gluing theorem, and the TPC-149/TPC-167--170 actual-core
arithmetic theorems. None concludes a source-locked local **actual
occurrence** edge above the five-field production cut address with exact edge
weight, fixed `h0=2`, and physical-normalization lineage.

Therefore:

```text
qualifying_count = 0
max_defensible_family_status = EMPTY_IN_FROZEN_DECLARED_CORPUS
```

This is a scoped L1 source-census obstruction. It is not a theorem that local
occurrence edges do not exist in mathematics.

Reproduce:

```powershell
python experiments/tpc173_source_claim_inventory.py
python experiments/tpc173_source_claim_inventory.py --check
```

Generated outputs:

- `experiments/tpc173_source_claim_inventory.json`
- `experiments/tpc173_source_claim_inventory_audit.json`

No actual active-support certificate, canonical/minimal actual
representation, named fixed phase, program-positive L2 result, strict
`1/400`, prime-pair lower bound, or twin-prime theorem is proved.
