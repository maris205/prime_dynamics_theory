# TPC-273 computational protocol

1. Freeze the committed TPC-268 engine and parent payload digest.
2. Evaluate the 32 registered `(N,H,Q,z,s)` cases with exact rational beta,
   masks, shell, projection, and outward interval arithmetic supplied by the
   parent engine.
3. Transfer `rho^2` to `m^2` exactly and cube it for `m^6`.
4. Apply only the separated tests `m^2<1/64` and `m^2>1/16`; retain a
   middle band for all other rows.
5. Recompute the grid with an independent checker, mutate threshold and phase
   metadata in a hostile stress audit, and compare normal/optimized stdout.

The grid is finite and declared.  It is a stability obstruction for that
interface, not an asymptotic sample or a source-level theorem.
