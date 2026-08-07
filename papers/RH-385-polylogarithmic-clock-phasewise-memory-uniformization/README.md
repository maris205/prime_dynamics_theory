# RH-385: Polylogarithmic-Clock Uniformization

For every fixed real `B>0`, this package proves uniform convergence over the
RH-379 universally distance-two-safe, phasewise `c11(r)=0` lag-two families:

```text
sup_{1<=q<=floor((log N)^B)} sup_{f in F_q} |S_N(q,f)-L_q(f)| -> 0.
```

Here `mu_0(m)=mu(m)` for `m>=1` and is zero for `m<=0`,

```text
S_N(q,f)=N^-1 sum_{n<=N} mu(n) f_{n mod q}(mu_0(n-2),mu(n)),
L_q(f)=sum_{r mod q} [c02(r) delta_{q,r}+c22(r) theta_{q,r}].
```

For `P>=2`, `M_P=(prod_{p<=P}p)^2`, `Q=lcm(q,M_P)`, and
`tau_P=sum_{p>P}p^-2`, the proof retains the conservative ledger

```text
4*sqrt(Q)*D_*(N)/N + 13*tau_P + 6*Q/N + 4/N.
```

Taking `P=floor(sqrt(log log N))` and one fixed Davenport exponent `A>B/2`
closes the bound. Consequently the restricted finite optimizers converge
uniformly to the fixed-clock optimizers, their maximum tends to `B_infinity`,
and the nonempty square-clock diagonal gives a positive witness.

## Reproduction

From this directory:

```bash
make result
make schema
make test
make pdf
make archive
```

The default interpreter is `/root/math/.venv/bin/python`. The certificate
generator uses only the Python standard library. Tests require `pytest>=7`
and `jsonschema>=4.18`.

The exact finite surface contains:

- 512 truth tables and 4,608 interpolation evaluations;
- 192 phasewise-zero `c11` tables;
- 24 coefficient vectors, each with multiplicity 8;
- coefficient-vector maxima `l1=3` and squared `l2=5`;
- cutoff periods `4,36,900,44100` and coprime/noncoprime LCM fixtures;
- normalized-DFT channel costs `1,1,2`, including the legal `c21=-2` case;
- four exact square-mask means, a tail/padding ledger, and three diagnostic
  small-clock max-plus rows;
- 24 genuine certificate mutations, all rejected by the semantic verifier.

The canonical certificate has 472,145 bytes and SHA-256
`3100168ed679a02c2d97496a2457ff512c2327764ca884b248ad312a6af8eea8`.
The immutable source lock has 67 unique release blobs in groups `51/8/8`;
its aggregate digest is
`14a401e81d5d1868a8b3148478ca26f8975d0bde08b0a0117d4808571a2c5d79`.

## Package map

- `main.tex`, `references.bib`: manuscript and frozen-source bibliography.
- `main.pdf`, `polylogarithmic-clock-phasewise-memory-uniformization.pdf`:
  byte-identical publication PDFs.
- `src/polylog_clock/core.py`: exact enumeration, cutoff, DFT, DP, verifier,
  and mutation logic.
- `experiments/build_result.py`: result builder and 67-blob release lock.
- `experiments/build_schema.py`: recursively closed official Draft 2020-12
  schema.
- `experiments/build_archive.py`, `verify_archive.py`: individual publication
  manifest and verifier.
- `results/`: result, schema, manifest, and archive-verification records.
- `tests/`: independent exact, strict-type, source, schema, optimized-mode,
  and archive tests.
- `THEOREM_LEDGER.md`, `TABLE_TRACE.md`, `UPDATED_ROADMAP.md`: mathematical
  and artifact traceability.
- `INTEGRITY_AUDIT.md`, `REVIEW_AUDIT.md`, `FORMAT_AUDIT.md`,
  `REPLAY_AUDIT.md`, `VISUAL_QA.md`: ARS audit records.

## Boundary

Route A is `GO`; Route B is `STOP_SCOPED`. `B` is fixed, `Q` is only a
valid common period, and the finite artifact is
`reproduction_not_analytic_proof`. Nothing here proves an unrestricted or
polynomial clock theorem, a varying-`B` theorem, active-`c11` cancellation,
an effective threshold, an adaptive `K_N/N` limit, a projectively compatible
selector, an operator/trace/zero statement, or RH. Gates A--E remain false.
