# PrimeGaps186 reference review

Reviewed against the public repository at
<https://github.com/openai/PrimeGaps186>, shallow-cloned at commit
`61340d0b74163003b32756bb16e91d9209a5e330` (2026-09-02). The temporary source
clone was not copied into this research repository; the URL and commit are the
reproducible source locator. This note is a reference review, not a TPC proof.

## Source inventory and evidence status

| Source | What was checked | Status |
|---|---|---|
| `README.md` | Result, three inputs, normalization, certificate command, build and comparator claims | Read and summarized |
| `PrimeGaps186.lean` | Header, explicit axioms, terminal declarations and dependency shape; file has 210,637 lines, 3 explicit `axiom` declarations, and 0 `sorry` tokens | Structural/source audit; full theorem semantics still require the pinned Lean toolchain |
| `Challenge.lean` | Challenge definitions, the three input axioms, and intentional target `sorry` placeholders | Read; challenge is specification, not imported proof source |
| `formalization.yaml` | Project metadata, theorem-to-source alignment, permitted axioms, and self-assessed review status | Read |
| `comparator/main.json` and `comparator/README.md` | Exact target names, permitted axiom allowlist, Nanoda switch, and invocation | Read |
| `prime_gap_186_certificate.py` | Embedded parameter policy, signed-convolution regression, fresh-output behavior, no-`-O` policy, and `passed` receipt path; 2,736 lines | Static entrypoint audit and Python syntax check |
| `short_gaps_numerics.pdf` | Present in the source repository; retained as an external original locator | Not copied or independently re-rendered here |

The source README's phrase “the numerical certificate is unchanged from its
earlier passing run” is repository history, not a new local certificate run.
The local environment has NumPy 2.4.4 but no `flint`, `lake`, Lean, or
Comparator executable, so the full numerical and Lean/Comparator runs were not
claimed here.

## What the project establishes, at its declared level

The target is

```text
liminf (p_(n+1) - p_n) <= 186.
```

The Lean file exposes three explicit non-logical inputs:

1. the normalized rank-three hyper-Kloosterman bound;
2. the rank-two Kloosterman correlation bound;
3. the physical integral and cap bounds supplied by the numerical companion.

The terminal declarations assemble these inputs into conditional `DHL[40,2]`,
infinitely many two-prime translates of the explicit admissible 40-tuple, and
the gap-186 liminf statement. The logic-related Comparator allowlist also
contains `propext`, `Quot.sound`, and `Classical.choice`; these are not the
three analytic/numerical inputs. The source metadata reports `sorry_count: 0`
for the three solution declarations, while `Challenge.lean` intentionally has
three theorem placeholders (the token audit observed four occurrences because
the explanatory comment also names the placeholders).

The Python certificate embeds the trial tables and parameters, performs a
startup regression for the known signed-FFT convolution defect, writes a fresh
JSON receipt only to a new path, and requires the final margin to exceed
`1/50000`. Its README explicitly warns that a passing receipt does not
discharge any Lean axiom. The Comparator configuration similarly checks the
solution against the challenge under an exact permitted-axiom list; it is a
conditional proof audit, not a proof of the axiom bodies.

## Practices reusable in this repository

- Declare every external mathematical or numerical input as a named assumption
  at the interface, rather than hiding it in a proof or certificate.
- Keep a source crosswalk: theorem/declaration, exact source location, object,
  normalization, and claim level.
- Keep a fresh numerical certificate separate from its source inputs, use a
  new output path, and make the pass condition machine-readable.
- Add an independent comparator or kernel/checker with an explicit allowlist;
  report exactly what it verifies and what it does not.
- Preserve the distinction between conditional formal proofs, numerical
  evidence, computational checks, and unconditional theorems.
- Pin repository/tool versions and record hashes so a later session can
  reproduce or invalidate the evidence deliberately.

These practices fit the TPC certificate/provenance cascade and its L0/L1/L2
claim firewall. They do not replace TPC's source-object, fixed-`h0`, named-atom,
normalization, exactly-once cover, or physical-loss requirements.

## What does not transfer to TPC

The PrimeGaps186 result is about a bounded gap of at most 186 and is not a
twin-prime theorem. Its conditional Lean theorem cannot be relabeled as an
unconditional TPC arithmetic result. Its finite-field axioms and physical
integral table have no demonstrated identity with the TPC packet, source
coefficient, fixed-`h0`, phase, or normalization. A numerical certificate cannot
pay TPC's strict `1/400` endpoint or create L2 evidence without the required
physical identification theorem. The current TPC `STOP_SCOPED` cells therefore
remain unchanged.

## Reproduction record

```text
source_commit = 61340d0b74163003b32756bb16e91d9209a5e330
PrimeGaps186.lean: explicit_axioms=3, sorry_tokens=0
Challenge.lean: intentional_target_placeholders=3
prime_gap_186_certificate.py: py_compile=PASS
local flint=UNAVAILABLE
local Lean/lake=UNAVAILABLE
local Comparator=UNAVAILABLE
```

The source-side commands, which require its pinned environment, are:

```sh
python3 -B prime_gap_186_certificate.py --workers 4 --output prime_gap_186_fresh.json
lake exe cache get
lake build PrimeGaps186
lake exe comparator comparator/main.json
```

The certificate must run with `PYTHONOPTIMIZE` unset and without `-O`/`-OO`, as
the source README specifies. A future local run must record its actual package,
toolchain, output hash, and receipt rather than inheriting the README's
historical pass claim.
