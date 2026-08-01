# Roadmap after RH-345

RH-345 closes only the scalar parity mechanism at the critical order.

After RH-344, parity does not face one alias-sized positive packet but two:

    S_k=A_(k,2k)+F_k^orb,
    S_k/A_(k,2k)->2.

The actual leading phase law therefore has the unique symbolic scalar balance

    C_* C_M lambda^eta=2.

Off this phase, parity alone cannot close the critical coefficient if the
actual orbit-free rest and head defect are target-negligible.  At the balance
phase, the available `o(1)` law is exponentially too weak, and exact scalar
parity sequences with the same square-root asymptotic can have zero or
divergent target-normalized critical residuals.

This does not decide the actual critical coefficient because no theorem makes

    Y_k=T_k^rest-d_(sigma,k,2k)

target-negligible or otherwise estimates it.  Actual critical signed
compensation therefore remains `NOT_TESTABLE`/open.

The default physical route now moves to RH-346, the lower-sideband combined
complement decomposition at order `2k-2`.  It must:

- freeze the same RH-334 cells and the same physical `sigma,k` clock;
- use `m=k-1` only as the lower-orbit period parameter, not as a new noise
  clock;
- extract all `2m` folded marked points of the period-`2m` boundary orbit;
- retain the phase-dependent location of its last critical marked point;
- identify the exact raw-rest, parity, alias/radial-sideband, and head signs;
- compare every omitted point with `H_m=mR^(-2m)` before calling it
  negligible.

Only after that exact physical decomposition may RH-347 test a lower-sideband
compensation mechanism.  Critical closure, lower-sideband closure,
`E_off,(4k)`, head transport, the full direct prefix, RH-288, and Gates A--E
all remain open.
