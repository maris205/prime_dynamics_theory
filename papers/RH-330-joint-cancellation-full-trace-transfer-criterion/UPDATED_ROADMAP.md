# Roadmap after RH-330

RH-330 supplies the exact transfer architecture required by the first-alias
route:

```text
E_prefix = E_off + |e_actual|/(2H_k),
e_actual = e_model + Theta,
Theta = Delta_B + Delta_S + Delta_R + Delta_P - Delta_A.
```

The route coordinate is now

```text
first_alias_transfer_criterion_exact_actual_replacement_open
```

The criterion separates three independent obligations:

1. the off-alias weighted background must vanish on a clock containing the
   first alias but no second alias;
2. the observable critical replacement defect must have the required signed
   behavior at scale `H_k`; and
3. the remaining head/counterloop budget required by determinant gluing must
   close separately.

For a model that already closes, obligation 2 is `Theta=o(H_k)`.  For the
failed RH-329 model, actual closure instead requires the tuned repair

```text
Theta = -e_model + o(H_k).
```

Since `e_model` is order `A_k >> H_k`, this is an `A_k`-sized signed
correction with `H_k`-scale precision.  The synthetic repair in RH-330 proves
that the isolated failure alone says nothing decisive about the actual
operator.  Conversely, a proved `Theta=o(A_k)` would preserve the RH-329
negative divergence.  Neither actual estimate exists.

RH-331 should be the ten-layer first-alias frontier review.  It should:

1. audit RH-322--RH-330 as one typed chain;
2. record separately the local Gaussian, composition, parity/alias, shell,
   isolated-model, and transfer layers;
3. keep the observable-shell gauge firewall explicit;
4. verify that actual identification, two-channel Duhamel, signed far
   remainder, and off-alias background remain open;
5. build and verify the individual and batch publication archives; and
6. update `RH_HANDOFF.md` without promoting any conditional criterion.

Passing the conditional transfer theorem does not activate determinant
gluing and does not change Gates A--E.
