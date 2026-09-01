# TPC-331 proof and scope package

## Proposition 1: control-orbit Pythagorean identity

Let `A` be any real symmetric matrix, let `w_1,...,w_m` be finite vectors,
let `v_bar=m^{-1}sum_j w_j`, and let `z_j=w_j-v_bar`.  Then

```text
m^{-1} sum_j w_j^T A w_j
 = v_bar^T A v_bar + m^{-1} sum_j z_j^T A z_j.
```

### Proof

Expand `w_j=v_bar+z_j`:

```text
w_j^T A w_j = v_bar^T A v_bar
              + 2 v_bar^T A z_j + z_j^T A z_j.
```

Summing over `j` removes the middle term because
`sum_j z_j=sum_j w_j-m v_bar=0`.  This is finite bilinearity.

## Proposition 2: application to signed Gram forms

For `A_E=C_e^T C_e`, `A_D=diag(sum_u C_e(u,t)^2)`, and `A_O=A_E-A_D`,
the proposition gives the three identities

```text
mean E(w_j) = E(v_bar) + mean E(z_j)
mean D(w_j) = D(v_bar) + mean D(z_j)
mean O(w_j) = O(v_bar) + mean O(z_j).
```

This is a proved exact finite theorem for every finite source vector.  It is
not an assertion that any component is positive.

## Proposition 3: finite certified component census

Under the hash-locked TPC-330 panel and five controls, the TPC-331 certificate
contains 128 law-level decompositions.  The all-plus average and centered
components have positive off-diagonal classification in all 32 rows; the
coherent component has 31 positive and 1 negative.  The alternating law has
`23/9` negative/positive rows in each component; mod-4 and half-split have
`32/0` in each component.

### Evidence level

This proposition is `NUMERICALLY_CERTIFIED_FINITE`, not a symbolic or growing
arithmetic theorem.  The producer and independent checker rebuild the source,
shell matrices, five placements, mean vectors, centered vectors, all three
quadratic triples, guarded ratios, and exact anchor.  The stress checker
rejects representative schema, control, digest, census, and firewall
mutations.  Normal and optimized runs must agree.

## Corollary: finite localization of the positive response

For the all-plus law on this panel, the positive control-average and centered
position terms are not an artifact of one affine control: they survive the
five-control averaging.  The coherent mean term is positive on 31 rows and
negative on one.  This localizes the finite positive signal to a robust
centered component, but does not show that the component is small, canonical,
or uniformly controlled as the source grows.

## Exact anchor

The rational 16-point anchor stores four triples: identity, control average,
coherent mean, and centered position.  Every triple satisfies its Gram split
exactly, and the average triple equals the coherent plus centered triples in
all three coordinates.  Reduced-fraction SHA-256 digests are checked by both
implementations.

## Missing theorem and route boundary

The certificate does not bound the centered response uniformly over origins,
scales, or the true arithmetic residual.  In particular:

```text
GROWING_SOURCE_NATIVE_L2 = OPEN
UNIFORM_POSITION_RESPONSE_BOUND = OPEN
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The Session-named Route-A/Route-B evaluator files are absent, so the local
Bridge-B checker is a fail-closed fallback and no official route pass is
claimed.
