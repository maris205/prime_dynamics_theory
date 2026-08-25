# TPC-244: Common-Multiplier Sign Localization

This project determines exactly where the outer sign or phase of a clustered
coefficient can survive in a two-lane covariance.  Let

```text
H = direct_sum_h H_h,
B = direct_sum_h C_h b_h,
W = direct_sum_h C_h w_h,
```

with the inner product conjugate-linear in the first slot.  Then

```text
<W,B> = sum_h |C_h|^2 <w_h,b_h>.
```

Consequently, a common unit phase `C_h -> eta_h C_h` applied to both lanes is
exactly invisible in the coefficient covariance and both coefficient norms.
For the literal real Möbius-log tail

```text
C_h = sum_(d in D_x, h|d) mu(d) log(d)/d,
```

this erases only the **aggregate outer sign**.  The internal Möbius signs still
change the magnitude `|C_h|` and therefore remain arithmetically relevant.

For nonorthogonal embeddings `J_h` and real signs `s_h`, the complete sign
dependence is a cut polynomial:

```text
Q(s) = D + sum_(h<k) s_h s_k S_hk,
Q(s)-Q(1) = -2 sum_(h<k, s_h!=s_k) S_hk.
```

The covariance is invariant under every sign pattern if and only if every
symmetrized cross-block coefficient `S_hk` vanishes.  The individual directed
cross terms need not vanish.

Under the TPC-243 hard-window synthesis theorem, if a literal common-multiplier
two-lane coefficient attachment is supplied, any two common sign patterns obey

```text
|Q_I(s)-Q_I(t)| <= 2 epsilon ||W||_2 ||B||_2,
```

where the norms are coefficient-space norms.  This physical specialization is
`CONDITIONAL_ON_LITERAL_V59_PHASEWISE_PRIMITIVE_TWO_LANE_ATTACHMENT`; the
required literal `beta,w` crosswalk is not present in the current source chain.

## Main progress

- proves exact common-phase invariance on orthogonal denominator blocks;
- gives the full nonorthogonal sign-cut expansion and an exact iff criterion;
- localizes all outer-sign sensitivity to cross-block leakage or lane
  asymmetry;
- transfers the localization through TPC-243 with the sharp triangle-bound
  factor `2 epsilon`;
- rules out outer `C_h` sign as a mechanism for same-bucket main covariance.

## Artifacts

- `PROOF_PACKAGE.md`: complete proof, edge cases, and invalidation conditions;
- `DERIVATION_PACKAGE.md`: source-to-invariant derivation;
- `results/tpc244_certificate.json`: canonical exact certificate;
- `code/tpc244_common_multiplier_certificate.py`: producer/checker;
- `experiments/tpc244_independent_checker.py`: independent strict checker;
- `experiments/tpc244_sign_localization_stress.py`: exhaustive finite stress;
- `paper/paper.pdf`: compiled manuscript.

## Reproduction

Run from this project directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc244_common_multiplier_certificate.py --write
PYTHONDONTWRITEBYTECODE=1 python -B code/tpc244_common_multiplier_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B -O code/tpc244_common_multiplier_certificate.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc244_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B -O experiments/tpc244_independent_checker.py --check
PYTHONDONTWRITEBYTECODE=1 python -B experiments/tpc244_sign_localization_stress.py --check
PYTHONDONTWRITEBYTECODE=1 python -B -O experiments/tpc244_sign_localization_stress.py --check
```

All fixture calculations use exact rational or Gaussian-rational arithmetic.
They are `NUMERICAL_FINITE_ILLUSTRATION_ONLY`; the theorem is symbolic.

## Maximum status

`PROVED_STRUCTURAL_L1_COMMON_MULTIPLIER_SIGN_LOCALIZATION`.

`ARITHMETIC_ADVANCE = NO`.  Literal V59 phasewise primitive two-lane
attachment, coefficient norm bounds, lane-asymmetric arithmetic covariance,
arithmetic `L2`, fixed-atom credit, strict `1/400`, full Gate B, and every
twin-prime conclusion remain open.
