# Roadmap after RH-159

The finite reset maze now has two typed survivors and a two-gate common open
frontier.

1. **RH-160: conditional all-level reset theorem.** State separate native and
   directional hypotheses.  The native branch needs eventual packet-gap,
   overlap, selected-eigenvalue/tail, and spread bounds.  The directional
   branch additionally needs an eventual bounded-lag fourth-cross lower and
   lag-path conditioning.
2. **Prove sufficiency and omission witnesses.** Compose each hypothesis set
   to its correctly typed seed and show why omitting each major input defeats
   this proof architecture.  Keep the downstream assembly as an explicit
   interface if it is assumed rather than proved.
3. **Falsifiable experiments.** Report the exact scale diagnostics that would
   reject each eventual hypothesis: closing packet gap, overlap collapse,
   tail/eigenvalue threshold contact, spread blow-up, growing required lag,
   fourth-cross loss, or assembly-radius overflow.

Only after an all-level hypothesis is independently proved should the route be
propagated farther.  Finite 120/120 counts are not asymptotic laws.
