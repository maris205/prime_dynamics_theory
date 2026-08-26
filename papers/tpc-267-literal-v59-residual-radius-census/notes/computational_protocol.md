# Computational protocol

1. Run with `PYTHONDONTWRITEBYTECODE=1` and Python 3.12 or later.
2. `--write` deterministically regenerates `results/tpc267_certificate.json`.
   It is a release-generation command, not part of a read-only check.
3. `--check` recomputes the twelve rows and compares the canonical JSON byte
   representation.  It uses no external data files.
4. The independent checker uses a separate floating-point implementation and
   does not import the producer.  It replays all twelve rows and rejects seven
   schema/claim mutations.
5. The prime cutoff is (P=50000); the omitted Euler tail is retained as an
   outward interval.  The logarithm guard is (10^{-25}), and interval
   endpoints are rounded outward to a (10^{-30}) grid.
6. The kernel is (K_{H,s}(h)=(1+(h/H)^2)^{-s}), (s=1,2).  These are
   explicit normalized nonnegative Fourier-profile choices; their use here is
   a finite modeling choice, not identification with an unspecified smooth
   source profile.

Expected read-only markers:

```text
TPC267_CERTIFICATE=PASS
TPC267_INDEPENDENT_CHECK=PASS
TPC267_KERNEL_STRESS=PASS
```
