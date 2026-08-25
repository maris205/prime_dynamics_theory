# TPC-245 source lock

Baseline:

```text
HEAD = edc6f6ee80249a6c29f96acdc2a47e088f533474
TPC_HANDOFF_SHA256 = cdeb66efabdbe32814c8f1a69d04dbba0b06d7b010b4835519d1c7fcc76a33df
```

Frozen source hashes:

```text
TPC219_PROOF = c4954445bfb83bd4bbdb7674b3401c2327a6e4cd69d6d6ed9264f29a8f7e6f60
TPC219_DERIVATION = b1c3795762f780625edab11fbe8543799eb121a33deb203b269fd6c338b6daca
TPC243_PROOF = e7b17bd6babb1a00f690697ab4163053cfe33ddb61419bd73f8bf77d86e44faf
TPC244_PROOF = f24de94c94db9dadf15727fb72cfd1b8c1ae596585ed99a0615ff13534109b49
TPC244_BRIDGE = 28d14c10c1e59a5d87c10508e974d776a641edb0075be4d569e256a0e6015439
```

Source-backed facts:

- TPC-244 names the local covariance as the next structural object.
- TPC-243 transports only already-supplied coefficient lanes.
- TPC-219's longitudinal object is the constant-prime-label subspace of `V^P`.
- No frozen source defines a canonical one-dimensional `u_h` inside a TPC-244 block.

First physical blocker:

`NO_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_COEFFICIENT_ATTACHMENT`.

Additional TPC-245 blocker:

`NO_SOURCE_BACKED_CANONICAL_ONE_DIMENSIONAL_U_H_IN_H_H`.
