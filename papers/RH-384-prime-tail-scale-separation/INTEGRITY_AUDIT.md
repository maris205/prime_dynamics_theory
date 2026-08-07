# RH-384 Integrity Audit

## Claim-to-evidence audit

- The prime-tail theorem cites the classical mathematical PNT source, Montgomery–Vaughan, directly.
- RH-2 is identified only as repository provenance for the PNT-bearing source blob.
- RH-368/RH-371 are not used as prime-counting sources.
- RH-382 is cited for the exact two-scale gap expansion; RH-383 for the intrinsic tail coordinates and successor convention.
- Finite rows are described as reproduction and mutation checks, never as proof of an asymptotic theorem.
- The displayed interval is explicitly for `Y_infinity-2*m_infinity`; positivity of `C` follows only after division by `pi^2>0`.

## Citation audit

Every bibliography entry is cited in the manuscript. The Montgomery–Vaughan book DOI is `10.1017/CBO9780511618314`; Chapter 6 is identified with chapter DOI `10.1017/CBO9780511618314.008`. Repository-paper references are marked as frozen releases, not as independently published external literature.

## Numerical integrity

- No binary float enters the certificate.
- `FloatOperation` is trapped.
- Finite Euler products use independent downward/upward contexts.
- `theta_N` is an exact Fraction.
- `(m-1)*theta_N` is rounded upward before the lower tail-factor complement is rounded downward.
- Linear intervals are sign-aware.
- Ambient Decimal state is isolated, including `Emin`, `Emax`, Underflow, and Clamped traps.
- Canonical JSON forbids NaN and Infinity constants even though mutation labels may contain those words.

## Source and archive integrity

The result locks exactly 51 immutable release blobs. Mutable `AGENTS.md` and `RH_HANDOFF.md` are excluded. The source contract freezes membership, path safety, release commits, per-file SHA-256, group digests, and the aggregate digest. The publication manifest freezes 29 local members plus the same 51 external inputs and requires the semantic PDF to be byte-identical to `main.pdf`.

## Boundary integrity

The endpoint mutations are not misrepresented as asymptotic counterexamples. Bare PNT surrogates are explicitly forbidden at the exact subtraction surface. No effective rate, threshold, growing clock, active `c11`, adaptive capacity, operator, trace formula, zero identification, or RH claim appears. Gates A–E remain false.

## Required disclosures

- Data/code availability: present.
- Author contributions: present.
- Funding: no external funding.
- Competing interests: none declared.
- Ethics: not applicable; no humans, animals, personal data, or clinical materials.
- AI assistance: disclosed for auditing, code checking, adversarial tests, and typesetting; author responsibility retained.

No integrity blocker remains.
