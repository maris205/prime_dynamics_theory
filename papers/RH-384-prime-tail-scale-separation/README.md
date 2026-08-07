# RH-384: Prime-Tail Scale Separation

This package proves the fixed-r prime-square tail law

\[
P_r(y)\sim \frac{1}{(2r-1)p_y^{2r-1}\log p_y}
\]

for the strict tail `p > p_y`, compiles the scale of every fixed partition, and combines that dictionary with the immutable RH-382 expansion

\[
B_\infty-G(q_y)=A T_y+B T_y^2+C S_y+O(T_y^3).
\]

The resulting hierarchy is

\[
T_y^3=o(S_y),\qquad S_y=o(T_y^2),\qquad
\frac{S_y}{T_y^3(\log p_y)^2}\to\frac13.
\]

It yields five normalized gap limits. The exact subtraction surface is part of the theorem: L2 subtracts `A*T_y`, and L3–L5 subtract `A*T_y+B*T_y^2`. Bare-PNT surrogates are not licensed at those smaller scales.

A precision-80 directed certificate proves

\[
1.5463476716710499204\le Y_\infty-2m_\infty
\le1.5484488989771761113,
\]

so `C=(Y_infinity-2*m_infinity)/pi^2` is positive. The twice-subtracted residual is therefore eventually positive and its quotient by `T_y^3` tends to positive infinity, without an effective threshold.

## Reproduction

From this directory:

```bash
make result
make schema
make test
make pdf
make archive
```

The default Python is `/root/math/.venv/bin/python`. The certificate itself uses only the Python standard library. The test suite requires `pytest>=7` and `jsonschema>=4.18`, declared in both `requirements.txt` and the `test` optional dependency group.

The expected release summary is:

- 8 fixed-r rows;
- 66 fixed-partition rows through degree 8;
- 48 exact successor-interface rows;
- 5 intrinsic scale rows;
- 5 normalized gap rows;
- 10 precision-80 interval rows;
- 20 rejected mutations;
- 51 immutable external source blobs;
- 20 fail-closed tests, including official Draft 2020-12 metaschema validation.

The canonical certificate has 48,689 bytes and SHA-256 `01c91e57a01de9841f282327ab2f6e1a9368e136393ddab7a2cfe6b019a519c8`. The 51-source aggregate digest is `90434e0468ecc062cb522da096a267748725b5dca8e59c642bb7711f45a3e0e4`.

## Package map

- `main.tex`, `references.bib`: manuscript and bibliography.
- `main.pdf`, `prime-tail-scale-separation.pdf`: byte-identical publication PDFs.
- `src/prime_tail_scales/core.py`: exact algebra, directed intervals, and mutation oracle.
- `experiments/build_result.py`: immutable 51-source lock and result builder.
- `experiments/build_schema.py`: recursively closed Draft 2020-12 schema.
- `experiments/build_archive.py`, `verify_archive.py`: publication/external-input manifest and verifier.
- `results/result.json`, `result.schema.json`: frozen result and exact schema.
- `tests/`: exact, hostile-context, source, schema, optimized-mode, and archive mutation tests.
- `THEOREM_LEDGER.md`, `TABLE_TRACE.md`: claim and artifact traceability.
- `REVIEW_AUDIT.md`, `INTEGRITY_AUDIT.md`, `FORMAT_AUDIT.md`, `REPLAY_AUDIT.md`, `VISUAL_QA.md`: ARS review records.

## Boundary

Route A is `GO`; Route B is `STOP_SCOPED`. The theorem is fixed-r and fixed-partition only, fixes each clock before the prefix limit, and stays in the universally distance-two-safe phasewise class with `c11=0`. Inclusive/current-prime endpoint mutations are exact-interface errors but do not change the leading PNT equivalent. There is no growing-clock theorem, active-correlation cancellation, adaptive-capacity limit, operator, prime-power trace formula, Riemann-zero identification, or proof of RH. Gates A–E remain false.
