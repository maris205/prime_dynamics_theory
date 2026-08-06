# RH-370 theorem ledger

| Item | Status | Exact scope |
|---|---|---|
| PCF map, interval, and fold | PROVED UPSTREAM / LOCKED | `f(x)=1-u x^2`, `J=[-(u-1),1]`, `q=|x|`, `T=|1-u y^2|`. |
| Mirror-compatible finite partitions | DEFINED | Cells over `[0,u-1]` occur in mirror pairs; the terminal band is unpaired. |
| Observable intertwiner | PROVED | Pullback by `q` intertwines the full and folded exact Ulam matrices. |
| Density aggregation intertwiner | PROVED | Pushforward mass map satisfies `A P_full^T=P_fold^T A`. |
| Mirror kernel | PROVED | `P_full^T ker(A)=0`; the kernel dimension is the number of paired cells. |
| Nonzero finite spectrum | PROVED | `chi_full(z)=z^m chi_fold(z)`, including algebraic/Jordan multiplicities at nonzero eigenvalues; zero structure is left unclassified. |
| Folded `L^1` weak bridge | PROVED | `E_h P_T E_h g -> P_T g` for fixed `g in L^1`; exterior resolvents converge on `|z|>1`. |
| Deterministic spike formula | PROVED | `P_T 1=(2 sqrt(u))^(-1)(1-y)^(-1/2)` on the terminal band. |
| BV projection barrier | PROVED | Terminal cell-average jump is `(2-sqrt(2))/sqrt(u h)`, so the BV norm diverges. |
| Common strong `-1` Riesz bridge | STOP_SCOPED | The natural BV/tower entry lacks a uniform deterministic projector bound. |
| Arbitrary RH-367 partitions | OPEN | Non-mirror aligned and phase-shifted grids are not covered. |
| Noisy continuum law | OPEN / NOT CLAIMED | Positive-noise schedules from RH-52/RH-55 cannot be specialized to zero noise. |
| Gates A--E | FALSE / OPEN | No canonical determinant, scattering completion, self-adjoint generator, von-Mangoldt trace, or zeta divisor equality. |

The finite audit is an exact algebra check.  It is not evidence for an
all-order spectral limit or a universal noise exponent.
