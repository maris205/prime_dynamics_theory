# TPC-355 paper plan

## Question

Can a response-independent, position-aware diagonal normalization explain the
all-plus floor movement seen when TPC-353 is transferred to the TPC-354
higher-origin panel?

## Frozen protocol

Use the inherited finite V59 source and literal deleted-diagonal,
two-endpoint-divisibility-masked shell operator.  Compare the locked TPC-353
low-origin panel, the locked TPC-354 higher-origin panel, and a fresh
origins-only panel `(29001,33001,37001)`.  Counts, shell anchors, exponents,
height, source cutoff, and the four sign laws remain unchanged.  The new
normalization is declared before evaluating responses:

```text
B_p(u,t) = unsigned literal prime-p component
G_u      = sum_(p in S_Q) sum_(t in I) B_p(u,t)^2
A#       = D_G^(-1/2) A D_G^(-1/2),  D_G=diag(G_u).
```

The geometry diagonal uses neither `Lambda`, `b`, `beta`, a sign law, nor an
observed output.

## Claim-bearing components

1. Prove positivity/well-definedness of the finite diagonal congruence.
2. Prove that finite polarization and the Cauchy envelope apply to both `A`
   and `A#`.
3. Replay raw and normalized coefficients on all `648` law-level rows.
4. Quantify the locked-parent all-plus minimum-floor change and test it on the
   fresh panel.
5. Use an independent reverse-shell implementation and mutation stress.
6. Keep source-uniform arithmetic `L2`, an asymptotic operator bound, fixed
   power credit, Route-B reassembly, and the twin-prime endpoint open.

## Decision rule

If the normalized higher-origin floor drop is smaller than the raw drop, record
that as a finite partial repair only.  If mean transfer or another law moves
in the opposite direction, record the obstruction and pass the position-aware
question to an adversarial holdout.  No response-fitted normalization is
allowed.
