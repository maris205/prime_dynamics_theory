# Source lock

Verified directly on 2026-08-25 against repository baseline
`7b95d43a3dc6526851b1567071f36d48548295bd`.

Hashes below use SHA-256 after normalizing CRLF and bare CR to LF.

| Source | Locator | Normalized LF SHA-256 | Locked use |
|---|---|---|---|
| TPC-217 | `papers/tpc-217-finite-window-rational-large-sieve/PROOF_PACKAGE.md:21-42,138-168` | `591928fe33c658345f7b558266dcd021b7dbd5bea2dcd1f7fcd898a0b1d3b927` | V59 interval and exponents; primitive spacing; existing standard upper large-sieve scale |
| TPC-238 | `papers/tpc-238-finite-window-lower-frame-obstruction/PROOF_PACKAGE.md:3-29,141-234` | `9cc39a7209c0f343a71415d345e4bb892d436d7e6d2f961db45ee7163f3acba6` | Triangular-minorant lower baseline and circular packing precedent |
| TPC-242 | `papers/tpc-242-phase-fourier-collision-separation/PROOF_PACKAGE.md:3-60,163-194` | `b195b1247b415499476c90c9e9e5cc7f20eff526b439790075152ceac7ce31ba` | Conjugate-linear-first convention and selected mode `F_1=<Y,X>` |

## Direct verification

The producer and independent checker resolve the repository root from their
own file locations, normalize line endings, recompute all three hashes, and
fail closed on any mismatch. No source text is copied into the certificate as
a substitute for identity verification.

## Type boundaries

- TPC-217 already owns the standard upper large-sieve scale. TPC-243 claims no
  novelty for that upper result.
- TPC-238 supplies a lower estimate through a triangular minorant. It does not
  contain the direct rectangular near-isometry or the signed bilinear
  corollary proved here.
- TPC-242 identifies an abstract phase-Fourier mode. It does not identify the
  literal physical V59 top-prime coefficient vectors required by TPC-243.

## Task lock

```text
task_id = TPC243-WRITE-20260825-A
baseline_head = 7b95d43a3dc6526851b1567071f36d48548295bd
baseline_handoff_sha256 = a43fb5d8d4d98aba88aa5a817144bfb08759a233fbda414c0cc434f17b1129d7
prewrite_status_sha256 = 25ceaa072759ccb1a761ef705516c235e32b3a8e3fa997c7be4050af197bfd08
```
