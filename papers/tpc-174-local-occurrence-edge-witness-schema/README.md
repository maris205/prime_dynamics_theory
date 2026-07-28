# TPC-174: Local occurrence-edge witness schema

TPC-174 defines and verifies the minimal typed certificate for a source-locked
production local occurrence-edge family.

Each accepted production edge must contain:

- the five-field archived cut address `(ell,k,native_d,jL,jK)`;
- a distinct actual-occurrence ID and canonical edge ID;
- an exact nonzero rational edge weight;
- edgewise fixed `h0=2` and physical-normalization lineage; and
- a TPC-173 **qualifying** claim with matching path, hash, theorem locator,
  formula locator, and exactly matching nonempty derivation AST.

For every covered cut address the local edge weights must sum exactly to one.
Archive address and actual occurrence identity remain distinct.
The root witness, every edge, and every source bundle use closed field sets:
undeclared fields and any positive claim-boundary promotion are rejected.

Actual active support and canonical/minimal representation are deliberately
not claimed: they remain independent H1 roots.

The committed positive fixture is:

```text
SYNTHETIC_L0_ONLY
one covered cut
two typed local edges with weights 1/3 and 2/3
```

It proves schema/verifier nonvacuity only. TPC-173 has
`qualifying_count=0`, so the production status remains `NOT_TESTABLE`.

Reproduce:

```powershell
python experiments/tpc174_witness_contract.py
python experiments/tpc174_witness_contract.py --check
python experiments/tpc174_witness_contract.py `
  --witness samples/tpc174_synthetic_local_edge_witness.json
```

An external production candidate is checked with:

```powershell
python experiments/tpc174_witness_contract.py `
  --witness path/to/witness.json --production
```

Generated outputs:

- `samples/tpc174_synthetic_local_edge_witness.json`
- `experiments/tpc174_witness_contract.json`
- `experiments/tpc174_witness_contract_audit.json`

No production local edge, actual active support, canonical/minimal actual
representation, named fixed phase, positive fixed-X L2, strict `1/400`,
prime-pair lower bound, or twin-prime theorem is proved.
