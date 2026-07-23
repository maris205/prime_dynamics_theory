# TPC-68: Signed Native Operator Certificates

Working title:

> *Signed Native Operator Certificates at a Fixed Shift: Pairing Defects,
> Star Norms, Operator Walks, and the Shorted Reassembly Boundary*

## Scope

This paper studies only the literal missing-native map inherited from
TPC-61. It keeps:

- one fixed nonzero physical shift `h0`;
- the complete actual missing-high carrier;
- every missing-active physical row;
- complete native output labels, including side, block, opposite-row,
  gamma, and orbit labels;
- raw counting-measure atomic normalization.

Only the residual label is erased. The paper does not extend the
two-affine entry formula to the entire prime packet or to unproved
represented/missing cross terms.

## Main exact results

- `K = I + H` for the normalized literal missing-native Gram, with `H`
  Hermitian and zero diagonal.
- The residual/native split is explicit:
  `K_res = I + Xi_=s` and
  `K_nat = I + Xi_=s + Xi_neqs`; an erasure-only estimate is not treated
  as a bound for the full native Gram.
- After a unitary row gauge, every off-diagonal entry is the exact
  fixed-`h0` two-affine sum with signs
  `mu(m*j+h0) mu(n*j+h0)`.
- On same-residual collisions that sign freezes to `mu(d_m) mu(d_n)`;
  pure `H_res` closed walks therefore have target-sign product one.
  The new signed walk door lies in `H_erase` edges or literal complex
  phases.
- Sign-reversing partial matchings and Abel summation give literal
  complex-weight pair certificates.
- Exact star bounds:
  `s_* <= ||H|| <= sqrt(Delta) s_*`.
- Pair-majorant/Perron certificate:
  `||H|| <= rho(P)`, including reducible `P`.
- Even power-row and trace certificates retain complete decorated-walk
  cancellation.
- An exact certificate lattice bounds both extremal eigenvalues of the
  missing-native Gram.
- For full represented-plus-missing reassembly, the exact shorted Gram is
  `G_sh = G_dir - C_N`; the nuisance penalty `C_N` must be controlled
  separately.

## Claim status

- **L0 proved:** all finite-dimensional matrix, pairing, star, Perron,
  walk, moment, and shorting statements.
- **L1 recorded:** exact crosswalk to the complete literal fixed-`h0`
  missing carrier.
- **L2 open:** uniform pair defects, star savings, growing walk estimates,
  missing-mass savings, represented lower comparison, and nuisance
  shorting control.

No parity, prime-pair, or twin-prime conclusion is claimed.

## Build

From this directory:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The draft intentionally cites TPC-60, TPC-61, TPC-62, and TPC-67 as the
immediate dependency chain.
