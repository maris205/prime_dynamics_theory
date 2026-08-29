# TPC-304 derivation package

Let `S` and `T` be adjacent finite prime shells and let `a:S->{-1,+1}` and
`b:T->{-1,+1}` be their source-first weighted labels.  On the nonempty overlap
`O=S cap T`, define

```text
rho(a,b) = max_{epsilon in {-1,+1}} |O|^{-1} sum_{p in O} a(p) epsilon b(p)
d(a,b)   = min_{epsilon in {-1,+1}} |O|^{-1} #{p in O:a(p) != epsilon b(p)}.
```

Because `a(p)b(p)` is binary,

```text
rho(a,b) = |sum_O a(p)b(p)|/|O|,
d(a,b) = (1-rho(a,b))/2.
```

Independent global sign choices for either label multiply the inner product by
`+1` or `-1`, so both quantities are gauge invariant.  The producer records
the optimizing sign, restricted labels, exact mismatch primes, and rational
fractions.  TPC-304 then groups the six exponent/pair rows by the three Q
transitions and attaches the independently replayed TPC-303 descent census.

The crosswalk is descriptive: a low overlap correlation identifies a candidate
label-switching location.  It does not evaluate a counterfactual budget with a
transported label, so it cannot separate label switching from physical
operator change causally.
