# Roadmap after RH-181

## Current coordinate

```text
Reset-history candidate:
  source memory -> finite history polar packet       [proved]
  finite history -> transfer/determinant space       [open]
  physical D/K/H                                    [open]

Finite-cycle candidate:
  reduced double-cycle determinant + marks           [proved algebraically]
  physical length calibration and clock construction [open]
  cycle -> transfer/determinant space                 [open]
  physical D/K/H                                    [open]

Then for either viable route:
  Q cloud ledger -> U complement -> Z canonicity -> T directed limit
  -> macro Gate A
```

## Recommended RH-182 target

Construct a data-derived finite temporal clock from the physical history
cocycle, testing both candidate lengths `L=r-3` and `L=r-4` without fitting
transfer eigenvalues.  Measure:

1. endpoint-to-seed wrap residual;
2. primal and adjoint cyclic defects;
3. root-phase and radial error;
4. the rank-one orientation mark;
5. scale compatibility.

If both lengths fail, reject this finite-cycle physical branch.  If one
survives, validate its cycle-to-transfer map and feed outward budgets into
RH-180.

Gates B--E remain untouched.
