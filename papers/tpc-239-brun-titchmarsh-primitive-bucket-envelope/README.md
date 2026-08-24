# TPC-239: Brun--Titchmarsh Primitive-Bucket Envelope

Author: Liang Wang, Huazhong University of Science and Technology, Wuhan 430074,
P.R. China; `liang.wang@hust.edu.cn`.

Status: `PROVED_SOURCE_BACKED_PRIME_DENSITY_L1`

TPC-239 inserts a source-backed prime-density estimate into the exact TPC-237
common-source composition. Under the frozen physical hypotheses

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400), 4Q<H, U<Q,
```

put

```text
M_h=floor(2hQ/H),
M_h^x={m:0<|m|<=M_h, gcd(m,h)=1}.
```

For `2<=h<=U` and a primitive residue `a mod h`, dropping only the
`q`-dependent physical cutoff gives

```text
R_h(a)
 <= sum_(m in M_h^x)
      [pi(2Q;h,a^(-1)m)-pi(Q;h,a^(-1)m)]
 <= 16 (Q^2/H) (h/phi(h))/log(2Q/h).
```

Every displayed progression is reduced because both `a` and `m` are units
modulo `h`. The constant is exactly the product of
`pi(2Q;h,b)<=4Q/[phi(h)log(2Q/h)]` and
`#M_h^x<=2M_h<=4hQ/H`. For `h=1`, every row is empty since `2Q<H`.
Internal row injectivity prevents a hidden duplicate inside one physical
`q`-row. The AP sum is nevertheless retained as a pair census, may overcount
across multiplier rows, and ignores the physical cutoff.

At V59,

```text
Q/U=x^(1/1200),
max_(h<=U,(a,h)=1) R_h(a)
 << x^(1/96) loglog(x)/log(x).
```

Substitution before the reduced-frequency large sieve proves

```text
N^(-1) sum_(n in I_x) sum_(j=1)^J |K_j(n)|^2
 << J M^2 x^(1/48) (log x)^4 loglog x,
```

where `M=max_j ||psi_j||_infty` and
`N=#((x/2,x] intersect Z)`. The leading unnormalized fixed-power exponent
remains `49/48+o(1)`. Relative to TPC-237, the improvement is exactly the
genuine logarithmic factor `log x/loglog x`; it is not a fixed-power saving.

## Claim firewall

```text
TPC239_STATUS = PROVED_SOURCE_BACKED_PRIME_DENSITY_L1
TPC239_ROUTE_ADVANCE = YES_LOGARITHMIC_ONLY
TPC239_ARITHMETIC_INPUT = BRUN_TITCHMARSH
TPC239_ARITHMETIC_ADVANCE = NO
C_H_SIGNED_CANCELLATION = NONE
SIGNED_FOUR_PACKET_PROJECTION = NOT_PROVED
L2 = NONE
FIXED_ATOM_CREDIT = 0
STRICT_1_OVER_400 = UNPAID_GLOBAL
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
SHARPNESS = NOT_CLAIMED
```

The paper does not claim signed cancellation, an actual signed four-packet
projection, arithmetic `L2`, fixed-atom credit, strict `1/400`, Gate B, a
twin-prime theorem, or sharpness.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc239_bt_bucket_certificate.py --check
python -O -B code/tpc239_bt_bucket_certificate.py --check
python -B experiments/tpc239_independent_checker.py --check
python -O -B experiments/tpc239_independent_checker.py --check
python -B experiments/tpc239_bucket_stress.py --check
python -O -B experiments/tpc239_bucket_stress.py --check
```

The finite fixture `(Q,H,h)=(101,8830,82)` enumerates all shell primes,
physical rows, primitive buckets, and compiled AP rows. It illustrates
`actual R_h(a) <= AP census <= factor-16 real RHS`; it is not evidence for the
general analytic theorem.

## Research extraction

```text
STRONGEST_POSITIVE_RESULT = finite-window common-source packet trace with x^(1/48)(log x)^4 loglog x
STRONGEST_OBSTRUCTION = prime density saves only logarithm and leaves fixed-power 1/48
OPEN_THEOREM = weighted or signed within-bucket cancellation beyond coefficient-blind prime counting
REUSABLE_STRUCTURE = primitive residue -> reduced prime AP compiler
ROUND2_CLUE = test exact top-band C_h before seeking further uniform bucket savings
```

## Layout

The analytic derivation and proof are in `DERIVATION_PACKAGE.md` and
`PROOF_PACKAGE.md`. The paper sources and final PDF are under `paper/`; the
producer, independent checker, stress checker, deterministic JSON certificate,
and audit notes occupy their correspondingly named directories.
