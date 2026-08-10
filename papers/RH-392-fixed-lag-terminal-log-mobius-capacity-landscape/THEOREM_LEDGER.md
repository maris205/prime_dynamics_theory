# RH-392 theorem ledger

## Fixed quantifiers

- A terminal clock satisfies `1<=omega(X)<=X` and `omega(X)->infinity`.
- Periods, lags, shifts, affine coefficients, periodic masks, phase
  polynomials, and truth tables are fixed before `X->infinity`.
- Every terminal average is normalized by `log omega(X)` on
  `X/omega(X)<n<=X`.

## Terminal analytic ledger

1. Abel transfer sends `A(t)=alpha*t+o(t)` for bounded coefficients to the
   terminal logarithmic limit `alpha` for every admissible clock.
2. For fixed positive-leading affine forms `D,V` with arbitrary nonzero
   determinant and a fixed periodic mask, the full-Möbius terminal average
   vanishes.
3. The proof inserts `mu=lambda*1_sf`, uses one fixed cutoff `P` for both
   coordinates, combines congruences with
   `L=lcm(M,k^2,l^2)<=M(P#)^2`, and splits each compatible system into its
   finite disjoint residue classes. No assumption `(k,l)=1` is made.
4. After extracting contents `c_D,c_V`, the reduced determinant is exactly
   `L*Delta/(c_D*c_V)`, so Tao's fixed nonparallel theorem applies.
5. The determinant-free Boolean tail is `O_F(log omega/P+1)`. The order is
   fix `P`, take `X->infinity`, then `P->infinity`.

## Density ledger

For the distinct residue set `A_p={0,h mod p^2}`,
`nu_p=|A_p|` and `tau_(p,r)=#{a in A_p:a=r mod p}`. The exact formula is

```text
theta^(h)_(q,r)
 = q^-1 prod_(p not|q)(1-nu_p/p^2)
        prod_(p||q)(1-tau_(p,r)/p)
        prod_(p^2|q) 1_(r mod p^2 notin A_p).
```

Finite CRT is followed by a square-divisor union tail; no all-lag density
black box is imported. The cone and totals are

```text
0<=theta_r<=delta_r,
theta_r<=delta_(r-h),
sum_r delta_r=6/pi^2,
sum_r theta_r=kappa_h.
```

| `(h,q,r,p)` | `nu_p` | `tau_(p,r)` | local `p||q` factor |
|---|---:|---:|---:|
| `(2,2,0,2)` | 2 | 2 | 0 |
| `(6,3,0,3)` | 2 | 2 | 1/3 |
| `(4,2,0,2)` | 1 | 1 | 1/2 |
| `(9,3,0,3)` | 1 | 1 | 2/3 |

## Diagonalization ledger

- For a fixed finite set of distinct shifts and total degree at most two,
  constants and diagonal coordinate squares survive; linear and
  off-diagonal quadratic channels vanish.
- Separately, for one fixed lag and coordinatewise bidegree at most two,
  exactly `c00,c20,c02,c22` survive. The `c22` channel has total degree four
  and is not folded into the finite-shift theorem.
- For a truth table `f`, interpolate `z*f(x,z)` on the ternary square.
  Its `c00,c10,c20` coefficients vanish.

## Finite compiler and charge

- Positive-current projection maps 512 tables to eight actions with 64
  preimages each, preserves safety, and never lowers the signed score.
- Compatibility is `A_r=empty or +1 notin A_(r+h)`.
- Baseline `B_0={-1,0}` has `H_r=delta_r-theta_r/2`.
- A plus phase `r` charges the forced-empty predecessor `r-h` through

```text
H_(r-h)-theta_r/2
 =(delta_(r-h)-theta_(r-h))/2
 +(delta_(r-h)-theta_r)/2 >= 0.
```

- Translation has `gcd(q,h)` cycles of length `q/gcd(q,h)`. If `q|h`,
  self-loops force the plus set empty. The fixture `(q,h)=(6,4)` has two
  cycles of length three.
- Reflection preserves safety and negates the surviving channels. Tables 36
  and 72 witness the two signs of the absolute maximum.

## Capacity landscape

```text
G_log(q,h)=6/pi^2-kappa_h/2,
kappa_h=prod_(p^2|h)(1-p^-2) prod_(p^2 not|h)(1-2p^-2).
```

The value is independent of fixed `q` and maximal exactly for squarefree
`h`. Every finite `h` has `kappa_h<6/pi^2`, while
`h_y=(prod_(p<=y)p)^2` gives `kappa_(h_y)->6/pi^2`; hence `3/pi^2` is the
unattained infimum.

## Executable role and firewalls

The 640-row certificate verifies finite algebra only. Its false-mode
verifier calls no row or certificate builder, and all 24 semantic mutations
are rejected. It does not replace the affine-cancellation or CRT proof.
Fixed-data, post-limit, degree, source, and Gates A--E firewalls are exact
false Booleans in the result.
