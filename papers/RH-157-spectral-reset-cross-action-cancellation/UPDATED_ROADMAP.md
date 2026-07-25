# Roadmap after RH-157

The native reset route remains valid internally, but an exact full-memory
spectral reset is too invariant for the older projected-cross architecture:
its recent cross is only the negative tail coupling.

1. **RH-158: lagged reset cross bridge.** Replace the contemporaneous packet
   `P_t` by the coherent previous reset `P_{t-1}` (or a controlled hybrid).
   This breaks exact invariance while retaining RH-152 overlap control.
2. **Fallback native route.** If lagged packets also lose four-mode support,
   develop arithmetic meaning for the RH-156 native functional directly
   rather than forcing equivalence with RH-130.
3. **RH-159 review.** Compare recursive, contemporaneous-reset, lagged-reset,
   and native-only routes with every obstruction explicit.

The 54 positive tail-coupling diagnostics do not close a complete chain or
an all-level directional theorem.
