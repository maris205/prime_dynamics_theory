# TPC-236 proof package

## Lemma 1: internal row injectivity

Assume `4Q<H`, `h<=Q`, and `Q<q<=2Q`.  The map

```text
m -> m q^(-1) mod h
```

is injective on `0<|m|<=floor(hq/H)`.

### Proof

If two multipliers have the same residue, then `h|(m-m')`.  But

```text
|m-m'| <= 2 floor(hq/H) <= 4hQ/H < h.
```

Therefore `m=m'`. ∎

## Theorem 2: exact gcd-fiber multiplicity envelope

Let `R_h(a)` be the number of prime rows containing residue `a`, let
`g=gcd(a,h)`, and put `M_h=floor(2hQ/H)`.  Then

\[
R_h(a)\le
2\lfloor M_h/g\rfloor\lceil Qg/h\rceil
\le 4Q^2/H+4hQ/(gH)
\le 8Q^2/H.
\]

### Proof

Since every shell prime exceeds `h`, it is invertible modulo `h`.  From
`m q^(-1)=a (mod h)` one obtains `m=aq (mod h)`, hence `(m,h)=(a,h)=g`.  There are at
most `2 floor(M_h/g)` signed multiples of `g` in the global multiplier range.  For the
zero residue, `g=h` and `M_h<h`, so no nonzero atom exists.  Otherwise, for a fixed
such `m`, division by `g` gives one class modulo `h/g` because `a/g` is a unit there.
The shell interval has length `Q`, so it contains at most `ceil(Q/(h/g))`
integers in this class.  This proves the exact first bound.

Now use `M_h<=2hQ/H` and `ceil(Qg/h)<=Qg/h+1`:

\[
R_h(a)\le4Q^2/H+4hQ/(gH)\le8Q^2/H,
\]

where the last step uses `h<=Q<=gQ`. ∎

At V59, `h<=U` sharpens the uniform loss to

\[
4Q^2/H+4UQ/H=4x^{1/96}+4x^{23/2400}=(4+o(1))x^{1/96}.
\]

## Corollary 3: source-valid fixed-fiber Bessel bound

Let `v_(h,q)` be arbitrary Hilbert-valued rows supported on the physical residue sets.
Then

\[
\|\sum_q c_qv_{h,q}\|^2
\le (8Q^2/H)\sum_q|c_q|^2\|v_{h,q}\|^2.
\]

### Proof

At each residue at most `8Q^2/H` rows contribute.  Apply Cauchy--Schwarz at that
coordinate and sum. ∎

Consequently

\[
\sum_h |C_h|^2\|\sum_qc_{h,q}v_{h,q}\|^2
\le(8Q^2/H)\sum_{h,q}|C_h|^2|c_{h,q}|^2\|v_{h,q}\|^2.
\]

No row-dependent normalization occurs.  Composing the common packet output with one
linear map `T` multiplies the right side by `||T||^2` and leaves four-phase
polarization legal.

## Proposition 4: physical multiplicity two is false

Take `(Q,H,h)=(101,8830,80)`.  The integer inequalities
`8830^32<=101^63<8831^32` and `99^400<=101^399<100^400` make this an exact
V59-shaped floor fixture with `h<=U=99`.  For `q=113,127,193`, the cutoff is one and
the supports are all exactly `{17,63}`.  Hence bucket multiplicity is three.  Uniform rows have
individual squared norm two, summed squared norm eighteen, and Bessel ratio three. ∎

## Boundary

The direct sum is pre-reassembly.  Rational frequencies from different `h` are not
declared orthogonal.  No cancellation in `C_h`, arithmetic `L2`, strict `1/400`, or
full Gate B is proved.
