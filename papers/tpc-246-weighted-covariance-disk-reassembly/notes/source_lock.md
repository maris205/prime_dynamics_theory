# TPC-246 source lock

Baseline:

```text
HEAD = df998dccb04f28f37f6a4abf74d36e8d03bf2b71
TPC_HANDOFF_SHA256 = 2d80bc675cbfa48c17b0db08a65177b3a7007e03862288f5b5ca151d2d0d39fd
```

Frozen source hashes:

```text
TPC243_PROOF = e7b17bd6babb1a00f690697ab4163053cfe33ddb61419bd73f8bf77d86e44faf
TPC244_PROOF = f24de94c94db9dadf15727fb72cfd1b8c1ae596585ed99a0615ff13534109b49
TPC245_PROOF = fca7b77605202974e5b87178a1540625058e54feaab27babd3a1267084745413
TPC244_BRIDGE = 28d14c10c1e59a5d87c10508e974d776a641edb0075be4d569e256a0e6015439
TPC245_BRIDGE = 9fb4cb67b7c157666b0ad148f223e44c9f3c0e1b900df93373cea1bcbcef9129
```

Source-backed facts:

- TPC-243 supplies a coefficient-to-hard-window bilinear error bound.
- TPC-244 supplies common-multiplier weights `|M_h|^2` in an abstract direct sum.
- TPC-245 supplies exact local disks only in transverse dimension at least two,
  with lower-dimensional circle/singleton branches recorded separately.

Open source interfaces:

- literal V59 phasewise primitive two-lane coefficient attachment;
- source-native canonical block directions;
- independent source realization of the Cartesian product of local disks;
- payable local moments, transverse energies, and coefficient norms.
