# TPC-347 paper plan

## Research question

Can the literal deleted-diagonal prime-shell matrix be placed on a genuine
`ell^2` interface without erasing its endpoint divisibility masks?  What is
the exact relation between the translation-invariant residue kernel and the
physical finite matrix?

## Exact object

For a shell `S_Q`, sign law `e`, height `H=66`, and exponent `s`, define

```text
k_p(d) = 1_(d != 0) p H^(2s)/(H^2+d^2)^s
         (1_(p divides d)-1/(p-1)),
K_e = sum_p e_p K_p.
```

On `I`, let `P_p` multiply by `1_(p does not divide n)`, and let `R_I,E_I`
be restriction/extension.  The physical matrix is
`A_I=sum_p e_p R_I P_p K_p P_p E_I`.

## Claim-bearing outputs

1. Prove the mask factorisation and the exact defect identity.
2. Prove the Fourier multiplier norm formula for `K_e`, its compression
   inequality, and a Young tail envelope.
3. Rebuild the physical and ideal matrices on a disjoint two-origin,
   three-count panel and compare their spectral norms.
4. Verify ideal translation invariance, the finite triangle envelope, and an
   exact rational six-point anchor independently.
5. State the narrowest consequence: masks are not discardable on this finite
   panel, while the arithmetic `L2` gate remains open.

## Deliberate non-claims

The unmasked Fourier interface is not an estimate for the masked operator by
itself.  The finite defect table is not a growing theorem, does not identify
the canonical sign law, pays no fixed power, and says nothing about the
twin-prime conjecture.

## Decision rule

If the defect ratio has a robust lower witness, the next paper should isolate
its position-sensitive mechanism.  If it is uniformly small, the next paper
should test a source-native projection against the unmasked symbol.  Either
branch must retain the masks and use a fresh finite certificate.
