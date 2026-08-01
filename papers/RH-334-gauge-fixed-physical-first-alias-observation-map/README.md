# RH-334: Gauge-Fixed Physical First-Alias Observation Map

RH-334 repairs the data-type mismatch in the localized deterministic slots of
RH-327.  The noisy operator used there is the folded backward-observable
operator on `[0,1]`, while the physical flat trace sums every signed fixed
point of `f` on `[-1,1]`.  A positive-coordinate test `x in J` therefore does
not partition the physical fixed points.

Let `T=abs(f)` and, for measurable `J` in `[0,1]`, define

```text
P_n^abs(J)
  = sum_(f^n(x)=x, abs(x) in J) 1/abs(1-(f^n)'(x))
  = sum_(T^n(y)=y, y in J)       1/abs(1-(T^n)'(y)).
```

The absolute-value map is a multiplier-preserving bijection from
`Fix(f^n)` to `Fix(T^n)` for every `n>=1`.  For the conditioned signed and
folded Gaussian operators, respectively `K_signed` and `K_fold`, RH-334 also
proves for every `n>=2`

```text
Tr(M_(abs(x) in J) K_signed^n) = Tr(M_J K_fold^n).
```

Both operators act on backward observables, so `M_J` marks the cyclic source
or basepoint.  The restriction `n>=2` is the repository-backed trace-class
boundary; no localized `n=1` operator trace is asserted.

The old RH-327 definition already fails at `n=2`.  Besides the fixed point
`r`, the physical two-cycle is

```text
x_minus = (1-sqrt(4*u_c-3))/(2*u_c) < 0,
x_plus  = (1+sqrt(4*u_c-3))/(2*u_c) > 0.
```

Positive-`x` binning omits `x_minus` and therefore misses exactly

```text
w_c = 1/(1+4*(u_c-1)) = 1/(4*u_c-3)
    = 0.314984831592965... .
```

For the frozen reproduction choice `k=2`, `sigma=1/4`, and `A=1/4`, put
`b=u_c^(-1/2)`.  The boundary-owned windows are

```text
J_minus = [b-1/8,b),
J_plus  = [b,b+1/8],
F       = [0,1] \ (J_minus union J_plus).
```

Their corrected deterministic slots are `(0,w_c,w_r+w_c)`, whereas the old
positive-`x` slots were `(0,w_c,w_r)`.  Once these windows are frozen before
evaluation, define `B,S,R` from the Hardy-scaled localized defects
`L_(sigma,n)(J)-P_n^abs(J)`.  Then the raw packet is exactly `B+S+R`.
The slot memberships and the fixed-point-free gauge interval are certified
analytically from the rational bracket `3/2<u_c<25/16`; the printed decimals
are not used for those conclusions.

At the first alias `n=2k`, the coefficient

```text
q_FT = c^H_(sigma,n) - s_(k,n) - a_n^num
```

has `coefficient_type=hardy_full_trace_constituent` and satisfies the exact
five-slot identity

```text
q_FT = e = B + S + R + P - A.
```

It is not automatically the modulus-complement coefficient.  If
`d=h_(sigma,n)-s_(k,n)`, then the correctly typed relation is

```text
tau_(sigma,n)-a_n^num = q_FT-d.
```

The paper does not localize Perron/parity projectors or Floquet sectors.

There is a second, distinct exact result.  Reassigning a positive-measure set
`E` containing no folded period-`n` point between two unfrozen cells changes
two localized defects by opposite nonzero amounts because the noisy cyclic
kernel is strictly positive.  Thus the slots depend on the frozen window
partition even though their total does not.  This is different from the
RH-330 exchange/observation gauge, which redistributes two model terms inside
one already frozen observable shell.

The artifact uses exact rational fixtures and 110-decimal working precision.
A 32-point Gauss--Legendre symmetric Nyström calculation checks finite
signed/folded lobe distributivity; it is a reproduction check only, not a
continuum or interval certificate.  No slot sign or asymptotic, `o(H_k)` far
bound, probability-to-trace identification, physical exchange parameter,
actual/model replacement, Duhamel closure, off-alias/head closure,
determinant gluing, Gate A--E promotion, Hilbert--Polya construction,
Riemann-zero identification, or RH conclusion is obtained.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_result.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf gauge-fixed-physical-first-alias-observation-map.pdf
```
