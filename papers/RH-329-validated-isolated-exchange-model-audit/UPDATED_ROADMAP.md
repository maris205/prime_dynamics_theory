# Roadmap after RH-329

RH-329 supplies the first fully frozen operator-coherent input to the RH-328
matching certificate.  That input fails:

```text
e_k/A_k -> -(1-C_* C_M) < 0,
e_k/H_k -> -infinity,
required contrast radius -> 1,
frozen contrast = 4/5.
```

The failure remains useful because it separates two statements that a
best-case interval screen cannot distinguish.  The required power is
eventually inside `[0,1]`, so some contrast magnitude is algebraically
reachable at every sufficiently large order.  The contrast furnished by the
pre-frozen model nevertheless misses by order `A_k`, exponentially larger
than `H_k`.  A physical proof must therefore derive the contrast rather than
optimize it after seeing the demand.

For this model the RH-328 tolerance scales are exactly

```text
H_k/A_k     = (k/a_k) (beta R)^(-2k),
H_k/(k A_k) = a_k^(-1) (beta R)^(-2k).
```

The power mismatch tends to `-(1-C_*C_M)` and the radius gap tends to
`1/5`; neither can meet its corresponding exponentially vanishing
tolerance.

This no-go belongs only to the graded isolated family defined in RH-329.  It
does not show that the actual noisy trace fails, and it does not construct a
single operator whose moments realize all model orders.

RH-330 should formulate the full-trace transfer criterion.  It must keep the
signed boundary, shell, parity, alias, observation, and far-remainder terms
on the same moving clock.  A valid criterion must explicitly require:

1. an identification map from actual localized trace blocks to the frozen
   shell fields, or quantified replacement errors for every field;
2. all prefix/suffix Duhamel weights for both critical channels;
3. a signed remainder estimate at `o(H_k)`, not separate same-order absolute
   majorants;
4. stability of the joint cancellation under the replacement; and
5. a firewall distinguishing an isolated-model verdict from an actual
   full-trace theorem.

The RH-329 failure is one test case for that criterion, not a transfer
theorem.  Gates A--E remain false/open.
