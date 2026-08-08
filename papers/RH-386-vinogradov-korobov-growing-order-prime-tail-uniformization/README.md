# RH-386: Vinogradov--Korobov Growing-Order Prime-Tail Uniformization

This package proves an explicit, growing-order version of the strict
prime-square tail asymptotic. For `x=p_y`, `L=log x`,

```text
V = L^(3/5) (log L)^(-1/5),
epsilon_x = 0.027 L^1.801 exp(-0.1853 V),
P_r(y) = sum_{p>x} (p^2-1)^(-r).
```

With `J_r`, `I_2r`, and `K_r` the exact Stieltjes, power, and leading
kernels, respectively, the quantitative one-factor ledger is

```text
|log(P_r/J_r)| <= 14 r epsilon_x,
0 <= log(J_r/I_2r) <= r/(x^2-1),
|log(I_2r/K_r)| <= 1/((2r-1)L).
```

The source line requires `L>=512` and `7 r epsilon_x<=1/2`. For a
partition `lambda=1^k1 2^k2 ...`, put

```text
d  = sum r k_r,
H  = sum k_r/(2r-1),
H2 = sum k_r/(2r-1)^2.
```

Then

```text
|log(P_lambda/M_lambda) + H/L|
  <= 14 d epsilon_x + d/(x^2-1) + 2 H2/L^2.
```

Thus `d epsilon_x+d/x^2 -> 0` controls the source and power kernels, and
the leading equivalent holds exactly when `H/L -> 0`. The convenient
sufficient conditions are `log d=o(V)` and `H=o(L)`. The all-ones family
`lambda=1^floor(cL)` has leading ratio `exp(-c)`, so the `H/L` condition
cannot be dropped.

## Reproduction

From this directory, with Python 3.10 or newer and the dependencies in
`requirements.txt` installed:

```bash
make result
make schema
make test
make pdf
make archive
```

`PYTHON` is overridable; the Makefile does not depend on a host-specific
environment. The core compiler itself uses only the standard library.
Tests additionally require `pytest>=7` and `jsonschema>=4.18`.

Remote verification is deliberately opt-in:

```bash
make remote          # verifies only the local lock; makes zero requests
make remote-network  # downloads the two exact versioned arXiv objects
```

The network verifier retains downloads only in memory or a temporary
directory. It never writes the Johnston--Yang PDF or source tar into this
package.

## Exact artifact

The certificate contains exactly 96 structured rows:

- 16 source, endpoint, hazard, and kernel rows;
- 8 fixed-order fixtures;
- 66 partitions of degrees at most 8;
- 6 envelope and sharpness rows.

All 24 theorem-interface mutations and 7 auxiliary metadata/strict-JSON
attacks are rejected. The field-level verifier checks 1,522 scalar leaves
without calling the canonical certificate builder. The canonical
certificate is 29,717 bytes with SHA-256
`64761d3a85afdee4682982ad545d20a66d2ed69926764bcc9580e0dc8c5f8710`.

The proof-minimal immutable closure has 59 Git release blobs in groups
`51/8`, plus one logical external source lock. The Git aggregate digest is
`6247477a1744ccfe676ebd1c20b4d659c597ce0749f3d3a9a0b1c8aa2c87069d`.

## Package map

- `main.tex`, `references.bib`: manuscript and bibliography.
- `src/vk_prime_tail/core.py`: exact certificate compiler and independent
  field verifier.
- `experiments/build_result.py`, `build_schema.py`: fresh result and closed
  official Draft 2020-12 schema builders.
- `experiments/verify_remote_source.py`: offline-by-default, opt-in network
  source verifier.
- `experiments/build_archive.py`, `verify_archive.py`: publication manifest
  and fail-closed replay.
- `results/external_source_lock.json`: non-redistributed remote source lock.
- `THEOREM_LEDGER.md`, `TABLE_TRACE.md`, `UPDATED_ROADMAP.md`: mathematical
  and artifact traceability.
- `INTEGRITY_AUDIT.md`, `REVIEW_AUDIT.md`, `FORMAT_AUDIT.md`,
  `REPLAY_AUDIT.md`, `VISUAL_QA.md`, `REMOTE_SOURCE_AUDIT.md`: ARS audit
  records.

## Boundary

The finite artifact is `reproduction_not_analytic_proof`. The theorem uses
Johnston--Yang Theorem 1.4 equation (1.8); the Corollary 1.2/Table 1
fallback is locked only as source context and is not promoted to an RH-386
result. In the surrounding program, clocks remain fixed and finite and
the phasewise class retains `c11=0`. There is no growing-clock theorem,
active-`c11` cancellation, effective threshold, operator or trace formula,
zero identification, or implication for the Riemann hypothesis. Gates
A--E are false.
