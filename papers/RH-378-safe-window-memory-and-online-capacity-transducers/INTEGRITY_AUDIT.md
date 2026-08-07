# RH-378 integrity audit

## Source and claim lock

- The repository copies of RH-366, RH-371, RH-372, RH-374, RH-375, RH-376,
  RH-377, and the four-volume MVP2 archive are the sole frozen sources.
- Davenport and Mirsky metadata are copied from the repository bibliography.
- Every arithmetic endpoint uses `m<=N-2`; early lag values use zero padding.
- The `rho-kappa2/2` comparison is explicitly conditional on `D2=o(N)`.

## Seven failure-mode review

1. **Finite-to-asymptotic upgrade:** absent.  All rows are labeled exact
   reproduction; no fit or convergence inference is used.
2. **Average upgrade:** absent.  The RH-376 logarithmic input is used only for
   rigidity of a hypothetical ordinary limit, never as ordinary Chowla.
3. **Endpoint drift:** absent.  `Q2,U2,V2,D2` share `m<=N-2`; `Q1,M` include
   the zero-padded first two lag sites exactly.
4. **Universal-safety shortcut:** absent.  The general theorem tests compatible
   length-`ell+2` blocks; both lag witnesses receive 243-row graph-lift tests.
5. **Model-class inflation:** absent.  State and window minimality statements
   name their exact deterministic models; the deterministic online obstruction excludes
   offline endpoint policies.
6. **Arithmetic-minimality inflation:** absent.  Formal basis dimension and
   rank five are not called minimal Möbius-correlation dimensions.
7. **Spectral/RH inflation:** absent.  Gates A--E are false/open; no operator,
   trace, zero identification, Hilbert--Pólya construction, or RH proof is
   asserted.

## Adversarial checks

- A nine-bit parity window is embedded into 17 integer sites before checking
  the two distance-two outputs; it is not treated as nine consecutive sites.
- Both branches of the four-step online adversary are replayed in the artifact,
  in addition to the exact deterministic causal-policy tree count `H4=0`.
- The six-term witness ledgers are checked at every prefix through `2^20`, not
  only at the three published rows.
- The nine-run counterexample is synthetic.  Möbius agreement follows from
  the exact modulo-9 and modulo-4 run obstruction.

No integrity blocker remains at manuscript-freeze time.
