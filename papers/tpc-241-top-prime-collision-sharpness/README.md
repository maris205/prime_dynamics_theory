# TPC-241: Top-Prime Collision Sharpness

Author: Liang Wang, Huazhong University of Science and Technology, Wuhan 430074,
P.R. China; `liang.wang@hust.edu.cn`.

Status: `PROVED_SOURCE_LOCKED_FIXED_PROFILE_UNSIGNED_TOP_PRIME_COLLISION_SHARPNESS`

TPC-241 closes the unsigned fixed-power audit opened by TPC-237--240.  Keep

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
```

and fix, independently of `x`, a real profile `psi` in `C_c^infinity(R)` with
`0<=psi<=1`, support in `[-1,1]`, and integral one.  For top primes
`U/2<p<=U`, collapse all shell-prime rows at each primitive residue:

```text
B_p^psi(a)=sum_(Q<q<=2Q)B_(p,q)^psi(a),
E_top^psi=sum_(U/2<p<=U)|C_p|^2
            sum_((a,p)=1)|B_p^psi(a)|^2,
C_p=-log(p)/p.
```

The normalized profile first moment is uniform on the top shell, and Cauchy on
the `p-1` primitive residues supplies the missing collision factor.  Weighted
PNT then proves

```text
liminf_(x->infinity) [(log x)/x^(1/48)]E_top^psi
 >=10773log(2)/1600.
```

Applying the TPC-238 lower frame to the complete primitive-frequency vector
before restricting its nonnegative coefficient norm to top primes gives

```text
liminf_(x->infinity) [(log x)/x^(1/48)]
 [N^(-1)sum_(n in I_x)|K_psi(n)|^2]
 >=10773log(2)/3200.
```

Thus, for every fixed admissible `psi`, every fixed `delta>0`, and every real
`A`, no eventual upper bound
`O_(psi,delta,A)(x^(1/48-delta)(log x)^A)` is possible.  The exact unsigned
common-profile exponent `1/48` is sharp up to logarithms.

This is a structural obstruction, not an arithmetic Gate-B theorem.  The
argument takes an absolute square after q-collapse and therefore does not use
the literal `C_h` signs or four-packet polarization.  Arithmetic `L2`, the
signed four-packet Gate-B scalar, and strict `1/400` remain open.

## Reproduction

From this project directory:

```bash
python -B code/tpc241_collision_sharpness_certificate.py --check
python -O -B code/tpc241_collision_sharpness_certificate.py --check
python -B experiments/tpc241_independent_checker.py --check
python -O -B experiments/tpc241_independent_checker.py --check
python -B experiments/tpc241_collision_stress.py --check
python -O -B experiments/tpc241_collision_stress.py --check
```

The programs use exact `Fraction` arithmetic, strict runtime guards, canonical
JSON, and independent recomputation.  Their finite rational profiles are
`NUMERICAL_FINITE_ILLUSTRATION_ONLY`; they are not theorem evidence.

The compiled manuscript is `paper/paper.pdf`.

## Route extraction

- Strongest positive result: explicit source-locked coefficient and
  finite-window `x^(1/48)/log x` liminfs.
- Strongest obstruction: the exact unsigned common-profile channel attains the
  full fixed-power `1/48` scale up to logarithms.
- Open theorem: determine whether literal four-packet polarization or signed
  `C_h` cancels this top-prime collision mode before absolute squaring.
- Reusable structure: fixed-profile first-moment Riemann summation,
  primitive-residue Cauchy, weighted PNT, and the full-vector finite-window
  lower frame.
- `ROUND2_CLUE`:
  `FORCE_THE_NEXT_ARGUMENT_TO_RETAIN_FOUR_PACKET_POLARIZATION_OR_C_H_SIGNS_BEFORE_SQUARING_BECAUSE_THE_UNSIGNED_TOP_PRIME_COLLISION_CHANNEL_IS_FIXED_POWER_SHARP`.
